# Investigations

One write-up per failure family. Each uses the templates in [`../templates/`](../templates/), cites trace IDs, and classifies the case as a configuration issue, product limitation, or defect.

| Scenarios | Failure family | Write-up | Classification |
|---|---|---|---|
| 03 / 04 | RAG answer quality: stale article outranks the current one | [03-04-outdated-vpn-answer.md](03-04-outdated-vpn-answer.md) | Configuration issue + product limitation |
| 05 / 06 | RAG answer quality: tiny chunks give cut-off answers | [05-06-truncated-answers.md](05-06-truncated-answers.md) | Configuration issue |
| 07 | Integration auth: every call returns 401 | [07-integration-auth-failure.md](07-integration-auth-failure.md) | Configuration issue |
| 08 / 09 | Rate limiting and retries | [08-09-rate-limiting.md](08-09-rate-limiting.md) | 08 works as designed; 09 product limitation |
| 10 / 11 | Tool arguments: bare number sent instead of INC number | [10-11-ticket-not-found.md](10-11-ticket-not-found.md) | Configuration issue |
| 12 | API change: renamed fields break create and lookup | [12-api-schema-change.md](12-api-schema-change.md) | Defect |

**Bug reports** (cases classified as defects or product gaps)
- [BUG-001: tool layer breaks when the API renames fields](bug-reports/BUG-001-tool-layer-breaks-on-api-field-rename.md)
- [BUG-002: sustained 429 leaves the assistant with no fallback](bug-reports/BUG-002-sustained-429-no-fallback.md)

**Customer-facing KB articles** (cases classified as configuration issues)
- [KB-001: The assistant gave me outdated instructions](kb-articles/KB-001-assistant-gave-outdated-instructions.md)
- [KB-002: "The ServiceNow integration rejected our credentials"](kb-articles/KB-002-integration-credentials-rejected.md)

## About the trace IDs
The trace IDs quoted here come from the run committed in `logs/` and `reports/evidence.md`. Re-running a scenario clears `logs/` and creates new trace IDs, so the IDs in a fresh run will differ from the ones cited here. The full timeline for every request is in [`../../reports/evidence.md`](../../reports/evidence.md).
