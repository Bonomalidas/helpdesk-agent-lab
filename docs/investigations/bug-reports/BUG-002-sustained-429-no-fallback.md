# BUG: Retry policy - on sustained rate limiting the assistant gives up after ~2 s with no fallback

**Severity:** S3 (minor, product gap / enhancement)  **Customer impact:** During a long bulk import, every ticket lookup fails with a generic "try again shortly" message and no indication of when to retry.
**Environment:** default settings (`max_retries: 2`, `backoff_s: 0.3`, `max_retry_sleep_s: 1`), mock API fault mode `rate_limit` (every call returns 429 with `Retry-After: 1`). Related RCA: [08-09](../08-09-rate-limiting.md)

## Expected vs actual
- Expected: when throttling persists, the assistant degrades gracefully, for example by telling the user roughly when to retry, offering to log a ticket by another route, or backing off for longer so it does not add load.
- Actual: three attempts at +0 s, +1.01 s and +2.01 s, all 429, then `rate_limited` with a generic message. Every later request repeats the same pattern against the already throttled API.

## Steps to reproduce (minimal)
1. `python scenarios/run_scenarios.py 09_tickets`
2. `python tools/summarize_logs.py --trace <trace_id>`

## Evidence
Trace `tr-ecfbb7a3`:
```
tool_call  attempt 1  status 429   retry_scheduled retry_after_header: 1  delay_s: 1.0
tool_call  attempt 2  status 429   retry_scheduled retry_after_header: 1  delay_s: 1.0
tool_call  attempt 3  status 429
answer     outcome: rate_limited  attempts: 3  "ServiceNow is busy right now ... Please try again shortly. (ref tr-ecfbb7a3)"
```

## Suspected area (hypothesis)
The retry policy is a fixed attempt count with a capped sleep, with no memory across requests (no circuit breaker or queue), and the user message does not use the `Retry-After` value that the API sent.

## Workaround
Throttle or reschedule the bulk import, or give the assistant its own integration user and quota.
