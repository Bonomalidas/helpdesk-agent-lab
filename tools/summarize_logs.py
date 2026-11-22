"""Turn the raw JSONL logs into something you can investigate.

    python tools/summarize_logs.py                 # one-line-per-request table (also writes reports/run_summary.md)
    python tools/summarize_logs.py --trace tr-1234 # full cross-system timeline for one request
    python tools/summarize_logs.py --evidence      # timelines for every request -> reports/evidence.md
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS = ROOT / "logs"
SHORT_CHUNK_WORDS = 25


def load() -> dict:
    by_trace = defaultdict(list)
    for path in sorted(LOGS.glob("*.jsonl")):
        for line in path.read_text().splitlines():
            rec = json.loads(line)
            if rec.get("trace_id"):
                by_trace[rec["trace_id"]].append(rec)
    for events in by_trace.values():
        events.sort(key=lambda r: r["ts"])
    return by_trace


def summarize(events: list) -> dict:
    row = {"scenario": "", "query": "", "action": "", "outcome": "", "http": [], "flags": []}
    for e in events:
        ev = e["event"]
        if ev == "scenario_query":
            row["scenario"], row["query"] = e["scenario"], e["query"]
        elif ev == "plan":
            row["action"] = e["tool"] or "kb"
        elif ev == "answer":
            row["outcome"] = e["outcome"]
        elif ev == "tool_call":
            row["http"].append(str(e.get("status") or e.get("error")))
        elif ev == "retrieval":
            top = e["results"][0] if e["results"] else None
            if top:
                row["flags"].append(f"top={top['doc_id']}({top['score']})")
                if top["words"] < SHORT_CHUNK_WORDS:
                    row["flags"].append(f"short_chunk={top['words']}w")
            if e.get("conflicts"):
                row["flags"].append("conflicting_articles")
            if e.get("top_is_stale"):
                row["flags"].append("TOP_RESULT_OLDER_VERSION")
        elif ev == "retry_scheduled":
            row["flags"].append("retry")
        elif ev == "arg_normalized":
            row["flags"].append(f"arg_normalized({e['before']}->{e['after']})")
        elif ev == "schema_mismatch":
            row["flags"].append(f"schema_mismatch(missing={','.join(e['missing_fields'])})")
        elif ev == "conflict_resolved":
            row["flags"].append("conflict_resolved")
    return row


def timeline(events: list) -> str:
    t0 = events[0]["ts"]
    lines = []
    for e in events:
        extra = {k: v for k, v in e.items() if k not in ("ts", "component", "trace_id", "event") and v is not None}
        lines.append(f"+{e['ts'] - t0:5.2f}s  {e['component']:<9} {e['event']:<18} {json.dumps(extra, default=str)}")
    return "\n".join(lines)


def table(by_trace: dict) -> str:
    rows = [(tid, summarize(ev)) for tid, ev in by_trace.items() if any(e["event"] == "scenario_query" for e in ev)]
    rows.sort(key=lambda r: min(e["ts"] for e in by_trace[r[0]]))
    out = ["| scenario | trace | query | action | outcome | http | flags |", "|---|---|---|---|---|---|---|"]
    for tid, r in rows:
        out.append(f"| {r['scenario']} | {tid} | {r['query'][:42]} | {r['action']} | {r['outcome']} | "
                   f"{','.join(r['http']) or '-'} | {'; '.join(r['flags']) or '-'} |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trace")
    ap.add_argument("--evidence", action="store_true")
    args = ap.parse_args()
    by_trace = load()
    if not by_trace:
        sys.exit("No logs found. Run: python scenarios/run_scenarios.py")
    (ROOT / "reports").mkdir(exist_ok=True)
    if args.trace:
        print(timeline(by_trace[args.trace]))
    elif args.evidence:
        parts = ["# Evidence: cross-system timelines per request\n"]
        for tid, ev in sorted(by_trace.items(), key=lambda kv: kv[1][0]["ts"]):
            s = summarize(ev)
            if not s["scenario"]:
                continue
            parts.append(f"## {s['scenario']} / {tid}\n\nUser: {s['query']}\n\n```\n{timeline(ev)}\n```\n")
        (ROOT / "reports" / "evidence.md").write_text("\n".join(parts))
        print("wrote reports/evidence.md")
    else:
        text = table(by_trace)
        (ROOT / "reports" / "run_summary.md").write_text("# Run summary\n\n" + text + "\n")
        print(text)


if __name__ == "__main__":
    main()
