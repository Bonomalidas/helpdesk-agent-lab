# The assistant says "the ServiceNow integration rejected our credentials"

**Applies to:** HelpDesk Assistant, ticket actions (create, look up, update)  **Last reviewed:** 2026-11-22

## Symptoms
- Every ticket request fails with: "I couldn't complete that: the ServiceNow integration rejected our credentials. (ref tr-xxxxxxxx)".
- Creating, looking up and updating tickets all fail, for every user, from some point in time.
- Knowledge-base questions still work.

## Cause
The login the assistant uses to talk to ServiceNow is no longer accepted, usually because it has expired, been replaced, or the integration account was disabled. No tickets are changed when this happens.

## Resolution
1. In ServiceNow, check that the integration user is active, and issue a new token or password for it.
2. Update the credential on the assistant: set the `SERVICENOW_TOKEN` environment variable (it takes priority over the token in the settings file).
3. Restart the assistant so that it picks up the new value.

## How to confirm it worked
Ask for the status of a ticket that you know exists. You should get its number, summary and status instead of the credentials message.

## When to contact support
Send the `ref` code from the message (for example `tr-9c11c567`), the time, and what you tried. The ref code lets support find the exact request in the logs.
