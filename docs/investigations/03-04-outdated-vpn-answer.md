# RCA: Assistant answered with outdated VPN instructions

**Scenario / trace:** `03_vpn_answer_wrong` / `tr-fc4ba193` (retest: `04_vpn_answer_retest` / `tr-07244bed`)
**Reported symptom (customer words):** "The assistant told me to use Cisco AnyConnect to connect to the VPN from home."

## Reproduction
Settings used: `kb_dirs: [kb, kb_extra]`, everything else default. Query: "How do I connect to the VPN from home?"
Re-run: `python scenarios/run_scenarios.py 03_vpn` (note: this regenerates `logs/`, so trace IDs will change).

## Evidence
```
assistant retrieval  results: vpn-setup-legacy chunk 0  score 0.56   updated 2022-03-14
                              vpn-setup        chunk 1  score 0.229  updated 2026-03-02
                              vpn-setup        chunk 0  score 0.215  updated 2026-03-02
                     conflicts: {"vpn": {"vpn-setup-legacy": "2022-03-14", "vpn-setup": "2026-03-02"}}
                     top_is_stale: true
assistant answer     citations: ["vpn-setup-legacy"]
                     "According to 'Connect to the VPN from Home (Cisco AnyConnect)' (updated 2022-03-14): ... vpn-old.acme.example ..."
```

## What happened (in order)
1. The planner routed the message to the knowledge base (no ticket action).
2. The index contained two VPN articles because `kb_dirs` includes `kb_extra/`, which holds `vpn-setup-legacy.md` (AnyConnect, 2022).
3. The legacy article scored 0.56 against 0.229 for the current GlobalProtect article.
4. The assistant flagged the conflict (`top_is_stale: true`) but still answered from the top-scored chunk.

## Why the old article won
Retrieval ranks by text similarity only; it never looks at the `updated` date. The question shares more words with the legacy article, whose title ("Connect to the VPN from Home") is indexed with its text. Word counts including the title: "home" appears 5 times in the legacy article and 0 times in the current one, "vpn" 9 vs 5, "connect" 4 vs 2. The legacy article is also a single 76-word chunk, so none of its content is diluted by splitting.

## Root cause
A deprecated article (`kb_extra/vpn-setup-legacy.md`) is part of the indexed knowledge base, and the retriever has no concept of freshness or deprecation (`prefer_latest_on_conflict: false`).

## Classification
- [x] Configuration issue (the stale article should not be in the index; a setting exists to prefer newer articles)
- [x] Product limitation (retrieval ranks by similarity only, so any stale document can outrank a current one)
- [ ] Defect

Why: nothing is malfunctioning. The system did exactly what it was configured to do, and the configuration lets the old content in.

## Fix / workaround and verification
- Quick mitigation: set `prefer_latest_on_conflict: true`. Retest `04` shows `conflict_resolved: original_top=vpn-setup-legacy, preferred=vpn-setup, rule=newest_updated`, and the answer now cites `vpn-setup` (2026-03-02).
- Proper fix: remove or archive `vpn-setup-legacy.md` from the indexed folders so it cannot be retrieved at all.

**Residual issue found during the retest.** The retest answer starts mid-article ("...drops repeatedly, switch from Wi-Fi to a wired network...") and does not include the install and connect steps. The conflict rule picked chunk 1 of the current article (it ties with chunk 0 on `updated`, and `max()` returns the first), and the same chunk is the top hit in the healthy baseline (`01`, score 0.24). So the stale-source problem is fixed, but the answer is still not very helpful. That is a separate answer-quality problem (chunk selection), not covered by this fix.

## What I'd tell the customer (3 sentences, no jargon)
The assistant was reading an old VPN guide that was still in its library, and it ranked that guide above the new one. We have told it to prefer the newest guide, and we will remove the old guide so this cannot happen again. Please ask the question again, and it should now point you to the GlobalProtect instructions.

## Prevention / follow-up
- Remove deprecated articles from the index when a replacement is published (see [KB-001](kb-articles/KB-001-assistant-gave-outdated-instructions.md)).
- Alert on the `top_is_stale` / `TOP_RESULT_OLDER_VERSION` flag, which is already logged.
- Add a regression query ("connect to VPN from home") that must cite the current article after every re-index.
- Fix chunk selection so the answer uses the chunk that contains the steps.
