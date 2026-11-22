# The assistant gave me outdated instructions (for example, an old VPN client)

**Applies to:** HelpDesk Assistant, knowledge-base answers  **Last reviewed:** 2026-11-22

## Symptoms
- You ask a how-to question and the answer names software or a server that your company no longer uses (for example "Cisco AnyConnect" or `vpn-old.acme.example` instead of GlobalProtect).
- The answer starts with "According to '...' (updated 2022-03-14)" and the date is old.

## Cause
An older version of the help article is still in the assistant's library, and it matched the question better than the current article. The assistant does not know the old article has been replaced.

## Resolution
1. Find the old article. Check the `updated` date in the answer, then look for a second article on the same topic in the knowledge-base folders the assistant reads (`kb/` and `kb_extra/`).
2. Remove the old article from those folders, or move it out of the indexed folders.
3. Re-index the knowledge base.
4. As a safety net, turn on `prefer_latest_on_conflict: true` in the assistant settings, so that when two articles cover the same topic the newest one wins.

## How to confirm it worked
Ask the same question again. The answer should cite the current article and its recent `updated` date, and it should no longer mention the old software.

## When to contact support
Send the exact question, the full text of the answer, the article title and date it cited, and the time you asked.
