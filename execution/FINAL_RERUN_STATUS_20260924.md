# RIDI Nature final rerun closure status — 24 September 2026

## Resolved

### EPSS v4→v5 / Extended Data Fig. 2
Verified from the submission source-data workbooks.

- Fixed 2026 universe: **338,575 CVE identifiers**.
- Top-1,000 v4→v5 replacements: **577**.
- Adjacent same-version changes: **0** and **1**.
- 0.1% frontier: **528 necessary**, **49 avoidable (8.5%)**.
- `Source_Data_ED_Fig2.xlsx` contains the v4→v5 source row with value 577.
- `Source_Data_EPSS_v4_to_v5_2026.xlsx` independently records 577 on the same 338,575-CVE universe.
- The submission manuscript Methods now explicitly states that Extended Data Fig. 2 uses the same fixed 13–16 June universe and the same verified turnover of 577. No alternative v4→v5 count is used.

## Deterministic raw reruns prepared

Execution branch: `execution-v95-4-20260924`.

### P2/P3
Script: `execution/rerun_p2_p3_raw.py`
Commit adding script: `0b0c938d4a9a05acc6f80fce2e39e8f0c009c1d6`

The job fails unless the regenerated raw files match:
- P2 generations SHA-256: `d5bbeaceacec4a1366af199cc58cabac834bd7e432d3207e0b6e4fb4398e1ab8`
- P3 generations SHA-256: `f8d10c277f151387c34b555d86676ee0375973506abde815fa7ce96516e0737a`

### P5
Script: `execution/rerun_p5_raw.py`
Commit adding script: `0761438ad391eea4205e40a4732101af2ddd49e0`

The job fails unless:
- rankings SHA-256 = `43050f9a720130658ca54b199c90a06c10a2ac3e7a5648390db85a56275531b6`
- pairs.json SHA-256 = `a643980275110e3585486eda51b66263622246ed046f8e45fe4b2ea5f44bf3eb`

The same job then runs the requested post-hoc `p5_margin_diagnostic` on the regenerated `pairs.json` and writes the full diagnostic JSON. It does not change the registered P5 decision.

### P4 machine audit
Script: `execution/run_p4_machine.py`
Commit adding script: `844f6d7a0a4299912cbcea33eb1280ddafbcca59`

Locked pre-outcome clarification: `0ce7426d1b67cb5ee12bab848e3c2904a95d9ab5`.
Judges:
- Mistral-7B-Instruct-v0.3 @ `c170c708c41dac9275d15a8fff4eca08d52bab71`
- OLMo-2-1124-7B-Instruct @ `470b1fba1ae01581f270116362ee4aa1b97f4c84`

P4 requires the exact persisted P2 raw generations before analysis.

### P1
Script: `execution/run_p1_openai.py`
Commit adding script: `c594d22cc8472aa4bbd3c80254bfcf81712aa86c`

Uses the registered API model `gpt-5.6-sol`, three repeats over the recovered 800-query panel, and the frozen scorer. Requires a valid `OPENAI_API_KEY` passed as a secret.

## Durable execution assets

The frozen execution bundle and v95.4 code-freeze bundle were copied to a 14-day firestorage share on 24 September 2026. The orchestration scripts verify the local archive SHA-256 before execution.

- frozen post-registration execution bundle SHA-256: `509af2d85d0c305bb729b055a78e5c43670b871969d70b5cd66c64ae63cc4081`
- v95.4 ready/code-freeze bundle SHA-256: `4316136c29e27e8617c6031d79d0dcc7863e5b4f9c7e5619e16d2e916640ed58`

## Current external blockers

1. Hugging Face Jobs currently returns **402 Payment Required**, including for a CPU-basic probe. Therefore no new GPU rerun can start until the account has a positive compute-credit balance.
2. P1 requires completion of the OpenAI API-key setup. No registered P1 query will be sent until a valid secret is available.

## Submission-document rule

Do **not** remove the manuscript/Supplementary raw-artifact archival limitation until deterministic P2/P3/P5 reruns have completed, raw files have been persisted, and the expected hashes above have been verified.

After that verification:
- remove the archival-limitation language;
- add the actual P5 margin-diagnostic values if scientifically useful;
- integrate P1/P4 only according to their preregistered/clarified decision rules;
- render and re-audit the final DOCX/SI before packaging.
