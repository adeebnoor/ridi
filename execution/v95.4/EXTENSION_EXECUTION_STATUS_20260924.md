# RIDI Nature extension execution status — 24 September 2026

Registration: OSF ms4w8 (DOI 10.17605/OSF.IO/MS4W8)
Filed protocol commit: 440f72f3d4879b9c5320e34f0fa6afaa731f5fb2
Code-freeze commit: fb29c4cdbaed7598412081b14a4b9183c0f78177

## P2 — execution floor

HF job: 6ab451d36b030d633f68c73d (completed)
Model: Qwen/Qwen3-8B @ b968826d9c46dd6066d109eabc6255188de91218
Archived single-prompt byte identity: 1600/1600.
Registered equal-dataset macro: identity-exchange change 17.267%; primary execution floor 1.033%; excess 16.233 percentage points.
The remote script stored the paired excess point estimate on the pooled scale and did not persist the fixed-batch query-level generation file. The registered-scale audit therefore enumerated all 48 within-dataset pairing structures consistent with the saved marginals using the frozen bootstrap settings (20,000; seed 20260923). Every admissible pairing supports H-P2; the minimum lower 95% bound is 13.433 percentage points.
Secondary stored pooled result: excess 15.875 points, 95% paired-bootstrap interval 13.25–18.50.
P2 generation-file SHA-256 reported by the remote job: d5bbeaceacec4a1366af199cc58cabac834bd7e432d3207e0b6e4fb4398e1ab8.
Audit script commit: f74a2e0b8f30f7bf6821c4d71a0115e756019be9.
Audit summary commit: 3611236ebb42b2dd396782131c18730b3ee4e601.

## P3 — replacement-draw variability

Same HF job (completed).
Five pooled correctness-change rates: 17.000%, 16.125%, 16.125%, 16.625%, 13.750%.
Any-draw change: 28.625%; majority-draw change: 14.500%; mean per-query change probability: 15.925%.
Reported generation-file SHA-256: f8d10c277f151387c34b555d86676ee0375973506abde815fa7ce96516e0737a.

## P5 — natural-prevalence qualification gate

HF job: 6ab457fd52d0dbd7f1d87fd3 (completed).
Frozen unused-query sample: 1,049 queries; 420 qualification and 629 estimation.
Twenty registered configurations produced 20,980 ranking rows.
Zero of 760 configuration-pair-by-dataset cells passed the registered joint nDCG@10 + Recall@10 equivalence criterion at margin 0.01 after Holm correction.
The confirmatory answer-generation stage was therefore not entered and H-P5 is unsupported.
Rankings SHA-256 reported by the remote job: 43050f9a720130658ca54b199c90a06c10a2ac3e7a5648390db85a56275531b6.
Pairs-result SHA-256: a643980275110e3585486eda51b66263622246ed046f8e45fe4b2ea5f44bf3eb.

## P1 — frontier/API transfer

No study output. The GitHub execution path verified the code freeze, exact registered contexts, scorer and prompt hashes, then stopped because OPENAI_API_KEY was unavailable in GitHub Actions. A subsequent HF non-study smoke path received a literal placeholder and failed authentication. No registered P1 query was sent through either failed path.

## P4 — semantic audit

No study output. The filed registration specified two judges from different model families but omitted exact model IDs. Before any P4 output, the post-registration/pre-outcome clarification was locked at commit 0ce7426d1b67cb5ee12bab848e3c2904a95d9ab5. Subsequent HF GPU and CPU job-creation attempts returned HTTP 402 Payment Required before execution. Human annotation has not begun and remains gated by the KAU institutional determination.

## Raw-artifact persistence limitation

The completed HF P2/P3 and P5 jobs were configured to emit compact evidence payloads and hashes to logs. Their ephemeral environments were not mounted to persistent storage, and full P2/P3 generation files and P5 ranking/pair files were not retained after job completion. The stored summaries and hashes support the reported displayed results, but a final archival rerun that persists the complete raw artifacts is required before the submission package is declared fully reproducible. No result or threshold will be changed during that rerun.
