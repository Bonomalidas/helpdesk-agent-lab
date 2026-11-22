"""Shared structured logging.

Every component (assistant, mock API, scenario runner) writes one JSON object per
line to <LAB_LOG_DIR>/<component>.jsonl. Every record carries a trace_id so a single
user request can be followed across the assistant and the (mock) ServiceNow API,
the same way you would follow a request across systems in Kibana or Grafana.
"""
import json
import os
import time
import uuid
from pathlib import Path


def log_dir() -> Path:
    return Path(os.environ.get("LAB_LOG_DIR", "logs"))


def new_trace() -> str:
    return "tr-" + uuid.uuid4().hex[:8]


def log(component: str, event: str, trace_id: str | None, **fields) -> None:
    d = log_dir()
    d.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": round(time.time(), 3),
        "component": component,
        "trace_id": trace_id,
        "event": event,
        **fields,
    }
    with open(d / f"{component}.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, default=str) + "\n")
