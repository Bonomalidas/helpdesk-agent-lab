# RCA: Answers cut off and useless after a re-index

**Scenario / trace:** `05_answers_incomplete` / `tr-0e2fa4dd`, `tr-98e784c7`, `tr-572f1eb1` (retest: `06_answers_retest` / `tr-2eb7eef8`, `tr-0f4ee70c`, `tr-e7fbd9d9`)
**Reported symptom (customer words):** "Since the knowledge base was re-indexed, the answers stop mid-sentence and don't tell me anything."

## Reproduction
Settings used: `chunk_size_words: 12`, `chunk_overlap_words: 0`. Queries: VPN, password reset, Salesforce access.
Re-run: `python scenarios/run_scenarios.py 05_answers` (regenerates `logs/`).

## Evidence
```
05  retrieval  chunk_size_words: 12   hits have words = 12, 4, 12
05  answer     "According to 'Connect to the Corporate VPN (GlobalProtect)' ...: To work remotely you must connect to the corporate VPN using the"
05  answer     "According to 'Reset Your Password' ...: Forgot password and verify your identity with an Okta Verify push or"
05  answer     "According to 'Request Salesforce Access' ...: Request Salesforce access in the Access Portal and choose the role you"
```
Top retrieval scores, broken index (05) vs. healthy index (01/06):

| Query | 05 (12-word chunks) | 06 (80-word chunks) |
|---|---|---|
| VPN from home | 0.374 | 0.24 |
| Reset password | 0.622 | 0.431 |
| Salesforce access | 0.773 | 0.561 |

## What happened (in order)
1. The index was rebuilt with 12-word chunks and no overlap, instead of 80 words with 20 overlap.
2. Every article was cut into 5-10 tiny fragments that end mid-sentence.
3. The assistant answers from the top-scoring chunk only, so each answer is a single 12-word fragment.
4. Confidence checks passed: scores went **up**, well above `min_confidence: 0.10`, so nothing declined or warned.

## Root cause
`chunk_size_words` (12) and `chunk_overlap_words` (0) in the assistant settings. Short chunks score higher against a short question because a few matching words make up a larger share of the chunk, but they carry no usable content.

## Classification
- [x] Configuration issue
- [ ] Product limitation
- [ ] Defect

Why: reverting the two settings fully restores the previous behavior (retest `06` reproduces the exact scores of baseline `01`: 0.24, 0.431, 0.561).

## Fix / workaround and verification
Set `chunk_size_words: 80`, `chunk_overlap_words: 20`, re-index. Retest `06` returns full-sentence answers and the same scores as the baseline.

## What I'd tell the customer (3 sentences, no jargon)
The re-index split the help articles into pieces that were far too small, so each answer was just a fragment. We have restored the original size and rebuilt the index. Please try your question again, and tell us if any answer still looks cut off.

## Prevention / follow-up
- Retrieval score is not a quality signal: a higher score here came with a worse answer. Do not use it alone to judge an index change.
- After any re-index, run a fixed set of test questions and compare answer length and the cited chunk size (the log summary already flags `short_chunk=12w`).
- Add a validation that rejects chunk sizes below a sensible minimum (for example 40 words).
