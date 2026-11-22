# HelpDesk Agent + Failure Lab

A small enterprise helpdesk assistant (RAG + agent actions on a ServiceNow-style API) **and** a lab of
reproducible failures, each diagnosed from its logs. Built as a miniature of the kind of AI assistant a
support engineer has to troubleshoot: answers that are wrong, workflows that fail, integrations that break.

The point of the repo is the second half: [`docs/investigations/`](docs/investigations/) contains the root-cause
analyses, bug reports and customer-facing KB articles for each failure.

## Architecture

```
 user message
      |
      v
+--------------------+   plan: KB question or ticket action?
|  assistant/agent   |-------------------------------------+
+--------------------+                                     |
      |  KB question                                       | ticket action (YAML-defined tools)
      v                                                    v
+--------------------+                           +----------------------+   REST + retries
| retriever (TF-IDF) |  top-k chunks + scores    |  tool call           |------------------+
| kb/*.md articles   |  conflict / confidence    |  config/tools.yaml   |                  v
+--------------------+  checks                   +----------------------+      +----------------------+
      |                                                    |                    | mock_servicenow/app  |
      v                                                    v                    | (switchable faults)  |
   answer (cited)                              answer / error message           +----------------------+
      |                                                    |                                |
      +---------------- structured JSONL logs, one trace_id per request, shared -----------+
                                  logs/assistant.jsonl  logs/api.jsonl
                                                |
                                  tools/summarize_logs.py  ->  reports/
```

## Quick start

```bash
pip install -r requirements.txt
python scenarios/run_scenarios.py          # runs all 12 scenarios (starts the mock API itself, ~10 s)
python tools/summarize_logs.py             # one row per request -> reports/run_summary.md
python tools/summarize_logs.py --trace tr-xxxxxxxx   # full assistant + API timeline for one request
python tools/summarize_logs.py --evidence  # timelines for every request -> reports/evidence.md
```

**Web app:** `python -m uvicorn web.app:app --port 8099`, then open <http://127.0.0.1:8099>. Chat with the assistant, pick a
fault mode or load one of the failure scenarios, and see the log timeline (assistant and API events, one trace ID) for every
answer. It writes to `logs_web/`, so the committed lab logs in `logs/` are not touched.

**Live demo page:** the `docs/index.html` page is a static copy that replays recorded runs of the 9 scenarios, so it can be hosted free on GitHub Pages (repo **Settings > Pages > Deploy from a branch > main, /docs**). No Python needed to view it.

Terminal alternative: `python -m uvicorn mock_servicenow.app:app --port 8099` in one terminal, `python chat.py` in another.

## What is in the box

| Piece | File | Notes |
|---|---|---|
| Knowledge base | `kb/` (15 articles), `kb_extra/` (1 legacy article) | Front-matter has `topic` and `updated` |
| Retrieval | `assistant/retriever.py` | Word chunking, TF-IDF, top-k with scores |
| Agent | `assistant/agent.py` | Plan, tool validation, argument normalization, retry with `Retry-After`, response schema check |
| Tools as config | `config/tools.yaml` | Tool paths, required args, expected response fields |
| Settings | `config/settings.yaml` | Chunking, confidence threshold, retries, timeouts |
| Mock ServiceNow | `mock_servicenow/app.py` | Table-API-style incidents (create / get / update) with fault modes |
| Web UI | `web/app.py`, `web/index.html` | Chat page with fault/settings controls and a live log timeline |
| Static demo | `docs/index.html` | Same page, replaying recorded runs; hostable on GitHub Pages |
| Observability | `lab_logging.py`, `tools/summarize_logs.py` | One trace ID across assistant and API |

## The Failure Lab

Each scenario starts from a customer-style symptom. Root causes are **not** recorded in the code; the
runner only injects a fault or a misconfiguration. Scenarios `04`, `06`, `11` are retests after a change.

| Scenario | Reported symptom |
|---|---|
| `01_baseline_kb`, `02_baseline_tools` | Healthy reference runs |
| `03_vpn_answer_wrong` | The assistant gave outdated VPN instructions |
| `04_vpn_answer_retest` | Retest of 03 after a configuration change |
| `05_answers_incomplete` | Answers are cut off / useless after a re-index |
| `06_answers_retest` | Retest of 05 after reverting the re-index settings |
| `07_tickets_all_failing` | Every ticket action fails since this morning |
| `08_tickets_intermittent` | Ticket lookups are flaky |
| `09_tickets_busy_all_day` | Ticket lookups never work during a bulk import |
| `10_ticket_not_found` | A ticket that exists is reported as not found |
| `11_not_found_retest` | Retest of 10 after a configuration change |
| `12_after_api_upgrade` | Ticket actions broke right after the ServiceNow instance was upgraded |

For each: reproduce, find the evidence in the logs, decide **configuration issue vs. product limitation vs.
defect**, and write it up using the templates in [`docs/templates/`](docs/templates/).

## Findings at a glance

| Scenarios | Root cause (short) | Class | Write-up |
|---|---|---|---|
| 03 / 04 | Deprecated VPN article is indexed and outranks the current one; retrieval ignores `updated` | Config + product limitation | [RCA](docs/investigations/03-04-outdated-vpn-answer.md) |
| 05 / 06 | `chunk_size_words: 12` cuts answers mid-sentence; scores went up, so confidence checks never fired | Config | [RCA](docs/investigations/05-06-truncated-answers.md) |
| 07 | Every call returns 401: the integration credential is rejected | Config | [RCA](docs/investigations/07-integration-auth-failure.md) |
| 08 / 09 | 429s: retries absorb short throttling (08); sustained throttling outlasts the retry budget (09) | 08 as designed; 09 product limitation | [RCA](docs/investigations/08-09-rate-limiting.md) |
| 10 / 11 | `normalize_args: false` sends `4521` instead of `INC0004521`, giving a misleading 404 | Config | [RCA](docs/investigations/10-11-ticket-not-found.md) |
| 12 | API v2 renames fields; tool layer hard-codes v1 names (response check catches the lookup) | Defect | [RCA](docs/investigations/12-api-schema-change.md) |

Also in [`docs/investigations/`](docs/investigations/): 2 bug reports and 2 customer-facing KB articles.

## Honest limitations

- **AI assistance.** This project, including the failure scenarios and the first drafts of the write-ups, was built with Claude (Anthropic). The findings are based on the committed logs and the code, and can be reproduced with the commands above.
- **Running a single scenario clears `logs/`**, so trace IDs in a fresh run differ from the ones cited in the write-ups.
- **The default LLM provider is a rule-based stand-in** (`provider: offline`): a regex planner and extractive
  answers. It makes runs deterministic and key-free; it is not an LLM. `anthropic` and `openai` providers exist
  in `assistant/llm.py` but are untested in the scenario runs.
- **Retrieval is TF-IDF, not embeddings.** The failure modes shown (stale documents, bad chunking, low confidence)
  also occur with embedding retrieval, but scores are not comparable.
- **The ServiceNow API is a simplified mock**, not a real instance: lookups are by incident number and only a few
  fields exist. Pointing it at a real developer instance would need path/query changes.
- **No Kibana/Grafana.** Logs are JSONL so they can be shipped to Loki/ELK; `tools/summarize_logs.py` stands in.
