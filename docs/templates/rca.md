# RCA: <short title>

**Scenario / trace:** `<scenario name>` / `<trace_id>`
**Reported symptom (customer words):**

## Reproduction
Steps and settings used. Command to re-run: `python scenarios/run_scenarios.py <name>`

## Evidence (paste the log lines that matter, not everything)
```
<timeline excerpt from: python tools/summarize_logs.py --trace <trace_id>>
```

## What happened (in order)
1.
2.
3.

## Root cause
One or two sentences. Name the exact component and setting/field.

## Classification
- [ ] Configuration issue (customer/admin can fix)
- [ ] Product limitation (works as designed, needs a workaround)
- [ ] Defect (needs an engineering fix; link bug report)
Why: 

## Fix / workaround and verification
What changed, and which retest run proved it (trace id).

## What I'd tell the customer (3 sentences, no jargon)

## Prevention / follow-up
Monitoring, alerting, or KB article that would catch or deflect this next time.
