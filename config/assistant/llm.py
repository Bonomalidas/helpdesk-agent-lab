"""LLM layer with pluggable providers.

provider "offline"   - deterministic rule-based planner + extractive answers. Needs
                       no API key. It is a stand-in for an LLM, NOT an LLM.
provider "anthropic" - calls the Anthropic Messages API (needs ANTHROPIC_API_KEY).
provider "openai"    - calls the OpenAI chat completions API (needs OPENAI_API_KEY).

The anthropic/openai providers are thin and have not been exercised in the
default scenario runs (which use the offline provider).
"""
import json
import os
import re

import requests

NUMBER_RE = re.compile(r"\b(INC\d{7}|\d{3,7})\b", re.I)
UPDATE_RE = re.compile(r"\b(update|add (a )?note|comment on)\b", re.I)
GET_RE = re.compile(r"\b(status|check|look ?up|details|progress)\b", re.I)
CREATE_RE = re.compile(r"\b(create|open|raise|log|file|submit)\b.*\b(ticket|incident)\b", re.I)


def after_colon(message: str) -> str:
    return message.split(":", 1)[1].strip() if ":" in message else message.strip()


def rule_based_plan(message: str) -> dict:
    number = NUMBER_RE.search(message)
    if UPDATE_RE.search(message) and number:
        return {"action": "tool", "tool": "update_incident",
                "args": {"number": number.group(1), "work_notes": after_colon(message)}}
    if GET_RE.search(message) and number:
        return {"action": "tool", "tool": "get_incident", "args": {"number": number.group(1)}}
    if CREATE_RE.search(message):
        return {"action": "tool", "tool": "create_incident",
                "args": {"short_description": after_colon(message)[:120]}}
    return {"action": "kb", "tool": None, "args": {}}


class OfflineLLM:
    name = "offline-rules"

    def plan(self, message: str, tools: dict) -> dict:
        return {**rule_based_plan(message), "planner": self.name}

    def answer(self, question: str, chunks: list[dict]) -> str:
        top = chunks[0]
        excerpt = " ".join(top["text"].split()[:70])
        return f"According to '{top['title']}' (updated {top['updated']}): {excerpt}"


class _HTTPLLM:
    name = "http"

    def _complete(self, system: str, user: str) -> str:  # pragma: no cover - network
        raise NotImplementedError

    def plan(self, message: str, tools: dict) -> dict:
        system = (
            "You route helpdesk requests. Reply with ONLY a JSON object: "
            '{"action": "kb" | "tool", "tool": <name or null>, "args": {...}}. '
            "Use a tool only when the user wants to create, look up or update a ticket. "
            "Tools: " + json.dumps({n: {"required": t["required_args"], "optional": t.get("optional_args", [])}
                                    for n, t in tools.items()})
        )
        try:
            data = json.loads(re.search(r"\{.*\}", self._complete(system, message), re.S).group(0))
            if data.get("action") not in ("kb", "tool"):
                raise ValueError("bad action")
            return {"action": data["action"], "tool": data.get("tool"), "args": data.get("args", {}),
                    "planner": self.name}
        except Exception as exc:  # fall back, but record that we did
            return {**rule_based_plan(message), "planner": f"{self.name}-fallback", "plan_error": str(exc)[:200]}

    def answer(self, question: str, chunks: list[dict]) -> str:
        context = "\n\n".join(f"[{c['title']} | updated {c['updated']}]\n{c['text']}" for c in chunks)
        system = ("Answer the employee's question using ONLY the knowledge-base excerpts. "
                  "Cite the article title. If the excerpts do not answer it, say so.")
        return self._complete(system, f"Question: {question}\n\nExcerpts:\n{context}")


class AnthropicLLM(_HTTPLLM):  # pragma: no cover - network
    def __init__(self, model: str):
        self.model = model
        self.name = f"anthropic:{model}"

    def _complete(self, system: str, user: str) -> str:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"},
            json={"model": self.model, "max_tokens": 600, "system": system,
                  "messages": [{"role": "user", "content": user}]},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]


class OpenAILLM(_HTTPLLM):  # pragma: no cover - network
    def __init__(self, model: str):
        self.model = model
        self.name = f"openai:{model}"

    def _complete(self, system: str, user: str) -> str:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
            json={"model": self.model,
                  "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


def get_llm(settings: dict):
    cfg = settings.get("llm", {})
    provider = cfg.get("provider", "offline")
    if provider == "anthropic":
        return AnthropicLLM(cfg["model"])
    if provider == "openai":
        return OpenAILLM(cfg["model"])
    return OfflineLLM()
