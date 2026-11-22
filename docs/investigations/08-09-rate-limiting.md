# RCA: Ticket lookups flaky (08) and never working during a bulk import (09)

**Scenario / trace:** `08_tickets_intermittent` / `tr-667d852a`; `09_tickets_busy_all_day` / `tr-ecfbb7a3`
**Reported symptoms (customer words):** 08: "Ticket lookups are flaky." 09: "Ticket lookups never work while the bulk import is running."

## Reproduction
08: fault `rate_limit_first2` (the first two calls get 429, then the API recovers). 09: fault `rate_limit` (every call gets 429). Query: status of INC0004521.
Re-run: `python scenarios/run_scenarios.py 08_tickets` and `09_tickets` (each regenerates `logs/`).

## Evidence
```
08  attempt 1  429   retry_scheduled retry_after_header: 1, delay_s: 1.0     (+0.00 s)
08  attempt 2  429   retry_scheduled retry_after_header: 1, delay_s: 1.0     (+1.01 s)
08  attempt 3  200   "INC0004521 - Outlook keeps asking for password. Status: In Progress."   (+2.01 s)

09  attempt 1  429   retry_scheduled ...                                      (+0.00 s)
09  attempt 2  429   retry_scheduled ...                                      (+1.01 s)
09  attempt 3  429   answer outcome: rate_limited, attempts: 3                (+2.01 s)
                     "ServiceNow is busy right now and I couldn't complete that. Please try again shortly. (ref tr-ecfbb7a3)"
```

## What happened (in order)
**08:** the API throttled two requests and then recovered. The assistant read the `Retry-After: 1` header, waited, retried twice, and succeeded on the third attempt. The user got the right answer about 2 seconds late.
**09:** the API throttled every request. The assistant used its whole retry budget (`max_retries: 2`, so 3 attempts, each wait capped at `max_retry_sleep_s: 1`), then gave up after about 2 seconds with a clear "busy" message.

## Root cause
Both are API rate limiting (HTTP 429), not assistant faults.
- 08: short-lived throttling. The retry logic is doing its job; what users experience as "flaky" is roughly 2 seconds of added latency.
- 09: sustained throttling that outlasts the retry budget. The likely driver is the bulk import consuming the same API quota as the assistant (a hypothesis: the logs show the 429s, not who is consuming the quota).

## Classification
- 08: [x] Works as designed (no change needed; transient throttling absorbed by retries)
- 09: [x] Product limitation (fixed retry budget, no fallback) **and** a customer-side configuration cause (the bulk import competes for quota). Product gap written up as [BUG-002](bug-reports/BUG-002-sustained-429-no-fallback.md).

Why not simply raise `max_retries` for 09? Longer waits would keep the chat hanging, and extra retries against an API that is already throttling add load and can make the problem worse.

## Fix / workaround and verification
- Throttle or schedule the bulk import outside working hours, or give the assistant its own integration user and quota.
- 08 needs no fix. Verification for 09 would be to run the baseline ticket scenario (`02`) while the import is throttled or paused. This lab has no retest scenario for 09, so that step was not run.

## What I'd tell the customer (3 sentences, no jargon)
ServiceNow is limiting how many requests it accepts, and the bulk import is using most of that allowance. Short slowdowns are handled automatically (about 2 seconds extra), but during a long import the assistant has to give up and ask you to retry. Running the import at quieter times, or giving the assistant its own allowance, will fix this.

## Prevention / follow-up
- Monitor 429 rates per integration user, not just failures.
- Record the `Retry-After` value in the user-facing message ("try again in about a minute").
- Consider a circuit breaker so the assistant stops hammering a throttled API (see BUG-002).
