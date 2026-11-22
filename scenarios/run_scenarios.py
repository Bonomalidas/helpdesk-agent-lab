"""Failure Lab runner.

Starts the mock ServiceNow API, then runs each scenario: set a fault mode on the
API and/or override assistant settings, send a few user messages, and log
everything. Root causes are deliberately NOT recorded here: diagnose them from
the logs with tools/summarize_logs.py.

    python scenarios/run_scenarios.py              # run everything
    python scenarios/run_scenarios.py stale_kb     # run scenarios whose name contains "stale_kb"
"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ["LAB_LOG_DIR"] = str(ROOT / "logs")

import requests  # noqa: E402

from assistant.factory import build_assistant  # noqa: E402
from lab_logging import log, new_trace  # noqa: E402

API = "http://127.0.0.1:8099"

KB_QUERIES = [
    "How do I connect to the VPN from home?",
    "I forgot my password, how do I reset it?",
    "How do I request access to Salesforce?",
]
TOOL_QUERIES = [
    "Create a ticket: my laptop screen is flickering",
    "What's the status of INC0004521?",
    "Update INC0004521: user confirmed the issue persists after reboot",
]

SCENARIOS = [
    dict(name="01_baseline_kb", fault="none", overrides={}, queries=KB_QUERIES,
         description="Healthy system, knowledge-base questions"),
    dict(name="02_baseline_tools", fault="none", overrides={}, queries=TOOL_QUERIES,
         description="Healthy system, ticket actions"),
    dict(name="03_vpn_answer_wrong", fault="none", overrides={"kb_dirs": ["kb", "kb_extra"]},
         queries=[KB_QUERIES[0]],
         description="Customer reports the assistant gave outdated VPN instructions"),
    dict(name="04_vpn_answer_retest", fault="none",
         overrides={"kb_dirs": ["kb", "kb_extra"], "prefer_latest_on_conflict": True},
         queries=[KB_QUERIES[0]],
         description="Retest of 03 after a configuration change"),
    dict(name="05_answers_incomplete", fault="none",
         overrides={"chunk_size_words": 12, "chunk_overlap_words": 0}, queries=KB_QUERIES,
         description="Customer reports answers are cut off / useless after a re-index"),
    dict(name="06_answers_retest", fault="none", overrides={}, queries=KB_QUERIES,
         description="Retest of 05 after reverting the re-index settings"),
    dict(name="07_tickets_all_failing", fault="auth_expired", overrides={},
         queries=[TOOL_QUERIES[0], TOOL_QUERIES[1]],
         description="Customer reports every ticket action fails since this morning"),
    dict(name="08_tickets_intermittent", fault="rate_limit_first2", overrides={},
         queries=[TOOL_QUERIES[1]],
         description="Customer reports ticket lookups are flaky"),
    dict(name="09_tickets_busy_all_day", fault="rate_limit", overrides={},
         queries=[TOOL_QUERIES[1]],
         description="Customer reports ticket lookups never work during a bulk import"),
    dict(name="10_ticket_not_found", fault="none", overrides={"normalize_args": False},
         queries=["What's the status of ticket 4521?"],
         description="Customer says a ticket that exists is reported as not found"),
    dict(name="11_not_found_retest", fault="none", overrides={"normalize_args": True},
         queries=["What's the status of ticket 4521?"],
         description="Retest of 10 after a configuration change"),
    dict(name="12_after_api_upgrade", fault="schema_v2", overrides={},
         queries=[TOOL_QUERIES[0], TOOL_QUERIES[1]],
         description="Ticket actions broke right after ServiceNow upgraded the instance"),
]


def wait_for_api(timeout=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if requests.get(f"{API}/health", timeout=1).ok:
                return
        except requests.RequestException:
            time.sleep(0.2)
    raise RuntimeError("mock API did not start")


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    log_dir = ROOT / "logs"
    if log_dir.exists():
        shutil.rmtree(log_dir)
    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "mock_servicenow.app:app", "--port", "8099", "--log-level", "warning"],
        cwd=ROOT, env=os.environ.copy())
    try:
        wait_for_api()
        for sc in SCENARIOS:
            if only not in sc["name"]:
                continue
            requests.post(f"{API}/_admin/reset")
            requests.post(f"{API}/_admin/fault", json={"mode": sc["fault"]})
            bot = build_assistant(sc["overrides"])
            print(f"\n== {sc['name']}: {sc['description']}")
            for query in sc["queries"]:
                trace = new_trace()
                log("scenarios", "scenario_query", trace, scenario=sc["name"],
                    description=sc["description"], query=query)
                out = bot.handle(query, trace_id=trace)
                print(f"  [{trace}] {query}\n    -> ({out['outcome']}) {out['answer'][:140]}")
    finally:
        server.terminate()
        server.wait(timeout=5)


if __name__ == "__main__":
    main()
