# RCA: Ticket actions broke right after the ServiceNow upgrade

**Scenario / trace:** `12_after_api_upgrade` / `tr-cc22bc61` (create), `tr-9f266766` (lookup)
**Reported symptom (customer words):** "Ticket actions broke right after ServiceNow upgraded the instance."

## Reproduction
Fault mode `schema_v2` (a simulated API v2: `short_description` becomes `summary`, `state` becomes `status`). Queries: create a ticket, look up INC0004521.
Re-run: `python scenarios/run_scenarios.py 12_after` (regenerates `logs/`).

## Evidence
```
create  tool_call   POST /api/now/table/incident   args_sent: {short_description: "my laptop screen is flickering"}   status 422
                    {"error":{"message":"Invalid request","detail":"Field 'summary' is required"}}
        answer      outcome: bad_request  "ServiceNow rejected the request I sent, so nothing was changed. (ref tr-cc22bc61)"

lookup  tool_call   GET /api/now/table/incident/INC0004521   status 200
        schema_mismatch  missing_fields: [short_description, state]
                         fields_present: [number, status, summary, urgency, work_notes]
        answer      outcome: schema_mismatch  "ServiceNow replied in a format I didn't expect, so I can't show the result reliably."
```

## What happened (in order)
- **Create:** the assistant still sent the old field name `short_description`. The API now requires `summary` and rejected the request with 422. Nothing was created.
- **Lookup:** the call succeeded (200), but the fields were renamed. The assistant's response check expected `short_description` and `state`, found `summary` and `status`, and refused to show the result.

## Root cause
The API contract changed (field renames) and the assistant still speaks the old one. The old field names are fixed in three places:
- `config/tools.yaml`: `required_args` and `expects` list `short_description` and `state`.
- The request body is built directly from the argument names, so the field name sent to the API is the same as the name the planner produces.
- `assistant/agent.py`: the success messages read `data['short_description']` and `data['state']` directly.

Editing `tools.yaml` alone cannot fix this: updating `expects` would let the response check pass and then the message formatting would fail on the missing key, and `create_incident` would still need the planner to produce `summary`.

## Classification
- [ ] Configuration issue
- [ ] Product limitation
- [x] Defect (needs an engineering fix; see [BUG-001](bug-reports/BUG-001-tool-layer-breaks-on-api-field-rename.md))

Why: the trigger is an upstream change, not a customer misconfiguration, and the assistant has no mapping layer between its internal field names and the API's, so it cannot be adapted by configuration.

What worked: the response schema check. Rather than show wrong or empty data, the assistant stopped and said so, which turned a silent failure into a diagnosable one.

## Fix / workaround and verification
- Workaround: if the instance still supports API v1, pin the integration to it.
- Fix: add a per-API-version field mapping so internal names (`short_description`, `state`) are translated to the API's names on the way out and back. Verify with scenario `12` plus the healthy baseline `02`. No retest was run, since the fix is not implemented in this lab.

## What I'd tell the customer (3 sentences, no jargon)
ServiceNow's upgrade renamed some fields, and the assistant is still using the old names. It did not create or change any tickets with wrong data; it stopped and reported the problem. We are updating how the assistant talks to ServiceNow, and in the meantime you may be able to keep the integration on the previous API version.

## Prevention / follow-up
- Read ServiceNow release notes before an instance upgrade and test the integration in a non-production instance first.
- Alert on a rise in 4xx responses and on `schema_mismatch` events straight after a change.
- Version the tool definitions so a new API version is a new configuration, not a code change.
- Caveat: the mock "v2" is invented for this lab. Real ServiceNow Table API field names are not renamed like this, but the failure pattern (an upstream contract change) is real.
