# BUG: Tool layer - all ticket actions fail when the ServiceNow API renames fields

**Severity:** S2 (major)  **Customer impact:** Users cannot create tickets, and ticket lookups are refused. Nothing is created or modified incorrectly.
**Environment:** default assistant settings (`provider: offline`, `normalize_args: true`), mock API fault mode `schema_v2` (simulated API v2). Related RCA: [12](../12-api-schema-change.md)

## Expected vs actual
- Expected: after an API change that only renames fields, the assistant keeps creating and reading tickets (or fails over to a documented compatibility setting).
- Actual: create returns 422 ("Field 'summary' is required") and lookup returns 200 but is rejected by the response check (`missing_fields: [short_description, state]`).

## Steps to reproduce (minimal)
1. `python scenarios/run_scenarios.py 12_after`
2. Read the two request timelines: `python tools/summarize_logs.py --trace <trace_id>` (IDs are printed by the run).

## Evidence
Traces from the committed run: `tr-cc22bc61` (create), `tr-9f266766` (lookup).
```
tool_call   POST /api/now/table/incident  args_sent: {short_description: "..."}  status 422
            body: {"error":{"message":"Invalid request","detail":"Field 'summary' is required"}}
tool_call   GET  /api/now/table/incident/INC0004521  status 200
schema_mismatch  missing_fields: [short_description, state]  fields_present: [number, status, summary, urgency, work_notes]
```

## Suspected area (hypothesis, not confirmed by a code change)
Field names are fixed in three places: `config/tools.yaml` (`required_args`, `expects`), request-body construction in `_call_tool` (body keys equal the planner's argument names), and the success messages in `_run_tool` (`data['short_description']`, `data['state']`). There is no mapping between internal field names and API field names.

## Workaround
Pin the integration to the previous API version if the instance supports it. Do not edit `expects` alone: the success-message code would then raise a KeyError.
