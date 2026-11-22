# RCA: Every ticket action fails with "credentials rejected"

**Scenario / trace:** `07_tickets_all_failing` / `tr-9c11c567` (create), `tr-cdfe7d71` (lookup)
**Reported symptom (customer words):** "Every ticket action fails since this morning."

## Reproduction
Fault mode `auth_expired`, default assistant settings. Queries: create a ticket, look up INC0004521.
Re-run: `python scenarios/run_scenarios.py 07_tickets` (regenerates `logs/`).

## Evidence
```
assistant plan        tool: create_incident, args: {short_description: "my laptop screen is flickering"}
api       http_request  POST /api/now/table/incident  status 401
assistant tool_call   attempt 1, status 401, body: {"error":{"message":"User Not Authenticated","detail":"Required to provide Auth information"}}
assistant answer      outcome: auth_failed, attempts: 1
                      "I couldn't complete that: the ServiceNow integration rejected our credentials. (ref tr-9c11c567)"
```
The lookup (`tr-cdfe7d71`) fails the same way.

## What happened (in order)
1. The planner correctly chose the tool and extracted valid arguments.
2. The request reached the API, which answered 401 "User Not Authenticated".
3. The assistant did not retry, which is correct: a 401 will not fix itself on a second attempt.
4. The user got a clear message with a reference ID.

## How I ruled other causes out
- Not an argument problem: the arguments are well-formed, and the healthy baseline (`02`) succeeds with the same kind of request (201 create, 200 lookup).
- Not specific to one tool or ticket: two different tools (POST create, GET lookup) fail identically.
- Not rate limiting or API errors: the status is 401, not 429 or 5xx.
- A failure of every call, starting at once, on all tools is the pattern of a credential-level problem.

## Root cause
The bearer token the assistant sends (`servicenow.token`, overridable by the `SERVICENOW_TOKEN` environment variable) is rejected by the ServiceNow API. In this lab the mock API is in `auth_expired` mode, which the API log also states. On a real instance the log would show only the 401, and the logs alone cannot distinguish between an expired token, a rotated secret, or a disabled integration user. The next step would be to check those on the ServiceNow side.

## Classification
- [x] Configuration issue (credential held by the customer or admin)
- [ ] Product limitation
- [ ] Defect

Why: the assistant behaved correctly. It sent its configured credential, did not retry a non-retryable error, and reported the failure clearly. The fix is to renew the credential.

## Fix / workaround and verification
Issue a new token for the integration user, update `SERVICENOW_TOKEN` (the environment variable takes priority over the settings file), restart the assistant. Verify by re-running the healthy ticket scenario (`02_baseline_tools`: 201, 200, 200). See [KB-002](kb-articles/KB-002-integration-credentials-rejected.md).

## What I'd tell the customer (3 sentences, no jargon)
The assistant's login to ServiceNow stopped being accepted, so every ticket action is being turned away at the door. This is a credentials renewal, not a fault in your tickets, and no tickets were changed. Once the new credential is in place, ticket actions will work again immediately.

## Prevention / follow-up
- Alert when 401s exceed a small threshold, so this is noticed before users report it.
- Track token expiry dates and renew ahead of time.
- Keep the user-facing ref ID in the message (it already is), because it takes support straight to the trace.
