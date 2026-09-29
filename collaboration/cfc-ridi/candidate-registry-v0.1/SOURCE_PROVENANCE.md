# CFC ↔ RIDI Candidate Registry v0.1 — Source Provenance

Status: CONSTRUCTED UNDER FROZEN ELIGIBILITY GATE; NOT A FROZEN POOL.

Source frame: all 800 primary registered Qwen3-8B / BM25 / k=10 reference-vs-random RAG pairs. No candidate was filtered using model-output equality, correctness, CFC output, RIDI output, desired asymmetry, or publication value.

Original source artifacts (from retained RIDI Nature v95.4 package):
- contexts_800.jsonl: 25266491 bytes; SHA-256 `1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1`
- registered_generations_primary_800.jsonl: 564276 bytes; SHA-256 `e7d1c8c06eece5482f632d628f933741ebbfc379ae01a99a293abdd9debf929c`
- protocol/PREREGISTRATION_NATURE_RAG.md: 17508 bytes; SHA-256 `0f7babda273f68e2095343f2fb33f2dca3c8720f95ed87ca3a0f47d1b337b063`

Structural pre-selection checks:
- 800 unique query pairs.
- Dataset counts: NQ 250; HotpotQA 250; FEVER 150; SciFact 150.
- Every pair has exactly one reference and one random arm.
- All 800 pairs have identical complete relevance-grade vectors between reference and random.
- No original authoritative independent-support-count rule was found in the preregistration; registry status is `NO_AUTHORITATIVE_REQUIREMENT_SPECIFIED`, not `AUTHORITATIVE_1`.

Derived source specimens deliberately exclude hidden gold/correctness and model outputs. They retain query identity, question, task, passage identities/grades, prompt/scorer hashes and source-registration linkage. Passage text is resolvable from the retained registered context artifact; the compact specimen binds the exact evidence identities and audit-grade vector.

Derived offline endpoint records deliberately exclude `correct` and any pair-level comparison field. Each arm records raw output, canonical output, model/revision and source archive only. A/B endpoints were hash-bound independently and were not compared during registry construction.

`a1_preexisting_authority_available=TRUE` means no new post-selection authority assertion is needed to execute the frozen mapping; it does not assert that every CFC authority field is VERIFIED. Frozen M1/A1 may still map unavailable facts to NOT_SUPPLIED/UNRESOLVED.

`prior_public_exposure=TRUE` records that the query panel/case identities were publicly registered; it does not assert that every A/B outcome was publicly highlighted.
