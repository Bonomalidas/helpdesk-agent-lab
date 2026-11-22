"""The helpdesk assistant: plan -> (retrieve + answer | call a tool) -> log everything.

Each handled message gets a trace_id. Every step logs a structured event so a bad
answer or failed action can be diagnosed afterwards from the logs alone.
"""
import os
import re
import time

import requests

from lab_logging import log, new_trace


def normalize_incident_number(value) -> str:
    v = str(value).strip().upper()
    return "INC" + v.zfill(7) if re.fullmatch(r"\d{1,7}", v) else v


NORMALIZERS = {"incident_number": normalize_incident_number}


class Assistant:
    def __init__(self, settings: dict, tools: dict, retriever, llm):
        self.settings = settings
        self.tools = tools
        self.retriever = retriever
        self.llm = llm

    # ------------------------------------------------------------------ entry
    def handle(self, message: str, trace_id: str | None = None) -> dict:
        trace_id = trace_id or new_trace()
        log("assistant", "request_received", trace_id, message=message, llm=self.llm.name)
        plan = self.llm.plan(message, self.tools)
        log("assistant", "plan", trace_id, action=plan["action"], tool=plan.get("tool"),
            args=plan.get("args"), planner=plan.get("planner"), plan_error=plan.get("plan_error"))
        if plan["action"] == "tool" and plan.get("tool") in self.tools:
            result = self._run_tool(trace_id, plan["tool"], plan.get("args", {}))
        else:
            result = self._answer_from_kb(trace_id, message)
        result["trace_id"] = trace_id
        return result

    # --------------------------------------------------------------- KB path
    def _answer_from_kb(self, trace_id: str, question: str) -> dict:
        s = self.settings
        hits = self.retriever.search(question, s["top_k"])
        conflicts = self._conflicts(hits)
        if conflicts and s.get("prefer_latest_on_conflict"):
            newest = max((h for h in hits if h["topic"] in conflicts), key=lambda h: h["updated"])
            log("assistant", "conflict_resolved", trace_id, original_top=hits[0]["doc_id"],
                preferred=newest["doc_id"], rule="newest_updated")
            hits = [newest] + [h for h in hits if h is not newest]
        # Is the article we are about to answer from an older version of a topic that
        # also has a newer article in the results?
        top_is_stale = any(
            hits[0]["doc_id"] in docs and hits[0]["updated"] < max(docs.values())
            for docs in conflicts.values()
        )
        log("assistant", "retrieval", trace_id,
            top_k=s["top_k"], chunk_size_words=s["chunk_size_words"],
            results=[{k: h[k] for k in ("doc_id", "chunk_idx", "score", "updated", "words")} for h in hits],
            conflicts=conflicts or None, top_is_stale=top_is_stale)

        if not hits or hits[0]["score"] < s["min_confidence"]:
            answer = ("I couldn't find a reliable answer in the knowledge base. "
                      "I can open a ticket for the Service Desk if you'd like.")
            outcome = "low_confidence"
            citations = []
        else:
            answer = self.llm.answer(question, hits)
            outcome = "answered"
            citations = [hits[0]["doc_id"]]
        log("assistant", "answer", trace_id, outcome=outcome, citations=citations, answer=answer)
        return {"outcome": outcome, "answer": answer}

    @staticmethod
    def _conflicts(hits: list[dict]) -> dict:
        """Topics where retrieved chunks come from more than one article version."""
        by_topic: dict = {}
        for h in hits:
            by_topic.setdefault(h["topic"], {})[h["doc_id"]] = h["updated"]
        return {t: docs for t, docs in by_topic.items() if t and len(docs) > 1}

    # ------------------------------------------------------------- tool path
    def _run_tool(self, trace_id: str, name: str, args: dict) -> dict:
        res = self._call_tool(trace_id, name, args)
        data = res.get("data") or {}
        outcome = res["outcome"]
        if outcome == "ok":
            if name == "create_incident":
                answer = f"I've created {data['number']}: {data['short_description']}."
            elif name == "get_incident":
                answer = f"{data['number']} - {data['short_description']}. Status: {data['state']}."
            else:
                answer = f"I've added your note to {data['number']}."
        else:
            answer = {
                "auth_failed": "I couldn't complete that: the ServiceNow integration rejected our credentials.",
                "not_found": "I couldn't find that ticket. Please double-check the number.",
                "rate_limited": "ServiceNow is busy right now and I couldn't complete that. Please try again shortly.",
                "bad_request": "ServiceNow rejected the request I sent, so nothing was changed.",
                "schema_mismatch": "ServiceNow replied in a format I didn't expect, so I can't show the result reliably.",
                "missing_args": "I need a bit more information to do that.",
            }.get(outcome, "Something went wrong talking to ServiceNow.")
            answer += f" (ref {trace_id})"
        log("assistant", "answer", trace_id, outcome=outcome, tool=name,
            http_status=res.get("http_status"), attempts=res.get("attempts"), answer=answer)
        return {"outcome": outcome, "answer": answer}

    def _call_tool(self, trace_id: str, name: str, args: dict) -> dict:
        tool, sn = self.tools[name], self.settings["servicenow"]
        missing = [a for a in tool["required_args"] if not args.get(a)]
        if missing:
            log("assistant", "tool_validation_failed", trace_id, tool=name, missing=missing)
            return {"outcome": "missing_args"}

        sent = dict(args)
        if self.settings.get("normalize_args", True):
            for arg, kind in tool.get("normalize", {}).items():
                if arg in sent:
                    before, sent[arg] = sent[arg], NORMALIZERS[kind](sent[arg])
                    if before != sent[arg]:
                        log("assistant", "arg_normalized", trace_id, arg=arg, before=before, after=sent[arg])

        placeholders = re.findall(r"{(\w+)}", tool["path"])
        path = tool["path"].format(**{p: sent[p] for p in placeholders})
        body = None if tool["method"] == "GET" else {k: v for k, v in sent.items() if k not in placeholders}
        url = sn["base_url"] + path
        token = os.environ.get("SERVICENOW_TOKEN", sn["token"])
        headers = {"Authorization": f"Bearer {token}", "X-Trace-Id": trace_id}
        attempts_allowed = sn["max_retries"] + 1

        resp = None
        for attempt in range(1, attempts_allowed + 1):
            t0 = time.time()
            try:
                resp = requests.request(tool["method"], url, headers=headers, json=body, timeout=sn["timeout_s"])
            except requests.RequestException as exc:
                log("assistant", "tool_call", trace_id, tool=name, attempt=attempt, method=tool["method"],
                    url=url, error=type(exc).__name__, latency_ms=round((time.time() - t0) * 1000))
                if attempt < attempts_allowed:
                    time.sleep(sn["backoff_s"])
                    continue
                return {"outcome": "network_error", "attempts": attempt}
            status = resp.status_code
            log("assistant", "tool_call", trace_id, tool=name, attempt=attempt, method=tool["method"], url=url,
                args_sent=sent, status=status, latency_ms=round((time.time() - t0) * 1000),
                body_excerpt=resp.text[:300] if status >= 400 else None)
            if status in (429, 500, 502, 503, 504) and attempt < attempts_allowed:
                retry_after = resp.headers.get("Retry-After")
                delay = min(float(retry_after) if retry_after else sn["backoff_s"] * 2 ** (attempt - 1),
                            sn["max_retry_sleep_s"])
                log("assistant", "retry_scheduled", trace_id, tool=name, reason=status,
                    retry_after_header=retry_after, delay_s=delay)
                time.sleep(delay)
                continue
            break

        status = resp.status_code
        base = {"http_status": status, "attempts": attempt}
        if 200 <= status < 300:
            data = resp.json().get("result", {})
            missing_fields = [f for f in tool["expects"] if f not in data]
            if missing_fields:
                log("assistant", "schema_mismatch", trace_id, tool=name, missing_fields=missing_fields,
                    fields_present=sorted(data.keys()))
                return {**base, "outcome": "schema_mismatch"}
            return {**base, "outcome": "ok", "data": data}
        outcome = {401: "auth_failed", 404: "not_found", 429: "rate_limited"}.get(
            status, "bad_request" if status in (400, 422) else "http_error")
        return {**base, "outcome": outcome}
