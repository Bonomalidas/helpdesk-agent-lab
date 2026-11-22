# RCA: A ticket that exists is reported as "not found"

**Scenario / trace:** `10_ticket_not_found` / `tr-58a27228` (retest: `11_not_found_retest` / `tr-2346f4b1`)
**Reported symptom (customer words):** "I asked about ticket 4521, which definitely exists, and the assistant said it couldn't find it."

## Reproduction
Settings used: `normalize_args: false`. Query: "What's the status of ticket 4521?"
Re-run: `python scenarios/run_scenarios.py 10_ticket` (regenerates `logs/`).

## Evidence
```
10  plan          tool: get_incident, args: {number: "4521"}
10  tool_call     GET /api/now/table/incident/4521   args_sent: {number: "4521"}   status 404
                  {"error":{"message":"No Record found","detail":"Record doesn't exist or ACL restricts the record retrieval"}}
10  answer        "I couldn't find that ticket. Please double-check the number. (ref tr-58a27228)"

11  arg_normalized  number: "4521" -> "INC0004521"
11  tool_call     GET /api/now/table/incident/INC0004521   status 200
11  answer        "INC0004521 - Outlook keeps asking for password. Status: In Progress."
```

## What happened (in order)
1. The user typed the bare number "4521". The planner extracted it as-is.
2. With normalization off, the assistant sent `4521` to the API. Tickets are stored as `INC0004521`, so the API returned 404.
3. The assistant told the user to double-check a number that was in fact correct.
4. With normalization on (retest), the number was converted to `INC0004521`, the API returned 200, and the answer was right.

## Root cause
`normalize_args: false` disables the `incident_number` normalizer defined for `get_incident` and `update_incident` in `config/tools.yaml`. The assistant therefore sent the raw number the user typed instead of the full incident number.

## Classification
- [x] Configuration issue
- [ ] Product limitation
- [ ] Defect

Why: the normalizer exists and works. The setting was switched off, and turning it back on fixes the case (retest `11`, trace `tr-2346f4b1`).

## Fix / workaround and verification
Set `normalize_args: true` (the default). Retest `11` shows the normalization step in the log and a 200 response.

## What I'd tell the customer (3 sentences, no jargon)
The ticket exists. The assistant looked it up under the short number you typed instead of its full ID, INC0004521, so ServiceNow said it didn't know it. We have re-enabled the step that fills in the full ID, so typing "4521" now works.

## Prevention / follow-up
- Two follow-ups that would make this class of problem less confusing, even with normalization off: validate the incident number format before calling the API, and make the "not found" message say which ID was looked up.
- Note that a 404 from ServiceNow can also mean "you may not see this record" (the API's own message says so), so "not found" is not proof that a ticket does not exist.
- Log `args_sent` on every tool call (already done), which is what made this diagnosable.
