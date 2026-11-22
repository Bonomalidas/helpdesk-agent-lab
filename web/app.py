"""Web UI for the HelpDesk Agent + Failure Lab.

Serves a chat page on top of the same FastAPI app that hosts the mock ServiceNow API, so
one process is enough:

    python -m uvicorn web.app:app --port 8099
    then open http://127.0.0.1:8099

The page lets you pick a fault mode for the mock API and a few assistant settings (the same
knobs the scenario runner turns), send a message, and see the answer plus the log timeline
for that request. Logs go to logs_web/ so the committed lab logs in logs/ stay untouched.
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.environ["LAB_LOG_DIR"] = str(ROOT / "logs_web")  # set before the log helpers are used

from fastapi import Request  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402

from assistant.factory import build_assistant  # noqa: E402
from mock_servicenow.app import STATE, app  # noqa: E402

FAULTS = ["none", "auth_expired", "rate_limit_first2", "rate_limit", "schema_v2"]
SHOWN_FIELDS = ("message", "action", "tool", "args", "results", "conflicts", "top_is_stale", "outcome",
                "citations", "attempt", "status", "args_sent", "delay_s", "retry_after_header",
                "missing_fields", "fields_present", "arg", "before", "after", "preferred",
                "original_top", "http_status", "attempts", "answer", "path", "detail", "chunk_size_words")


def build_overrides(opts: dict) -> dict:
    overrides: dict = {}
    if opts.get("include_legacy_kb"):
        overrides["kb_dirs"] = ["kb", "kb_extra"]
    if opts.get("prefer_latest_on_conflict"):
        overrides["prefer_latest_on_conflict"] = True
    if opts.get("normalize_args") is False:
        overrides["normalize_args"] = False
    size = opts.get("chunk_size_words")
    if isinstance(size, int) and 5 <= size <= 200:
        overrides["chunk_size_words"] = size
        overrides["chunk_overlap_words"] = 0 if size < 40 else 20
    return overrides


def read_timeline(trace_id: str) -> list[dict]:
    events = []
    log_dir = ROOT / "logs_web"
    for path in sorted(log_dir.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            if rec.get("trace_id") == trace_id:
                events.append(rec)
    events.sort(key=lambda r: r["ts"])
    t0 = events[0]["ts"] if events else 0
    return [{"t": round(e["ts"] - t0, 2), "component": e["component"], "event": e["event"],
             "data": {k: v for k, v in e.items() if k in SHOWN_FIELDS and v is not None}} for e in events]


@app.get("/")
def index():
    return FileResponse(ROOT / "web" / "index.html")


@app.post("/ui/chat")
async def ui_chat(request: Request):
    body = await request.json()
    message = str(body.get("message", "")).strip()[:500]
    if not message:
        return {"error": "Type a message first."}
    fault = body.get("fault", "none")
    STATE["fault"] = fault if fault in FAULTS else "none"
    STATE["rl_count"] = 0
    # The assistant calls this same server over HTTP, so run it off the event loop.
    from starlette.concurrency import run_in_threadpool
    bot = await run_in_threadpool(build_assistant, build_overrides(body.get("options", {})))
    result = await run_in_threadpool(bot.handle, message)
    return {"answer": result["answer"], "outcome": result["outcome"], "trace_id": result["trace_id"],
            "timeline": read_timeline(result["trace_id"])}
