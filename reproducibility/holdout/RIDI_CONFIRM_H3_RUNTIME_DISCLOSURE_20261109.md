# RIDI-CONFIRM — Mistral runtime setting for dense retrieval

Dated 9 November 2026. Project bjuwe; registration 794p5. This project-file disclosure was prepared after the H3 results were known. It documents an implementation decision made locally before successful Mistral generation. The original registration remains unchanged.

Contrast D replaces whole-document BM25 with the pinned full-corpus Contriever. The frozen Mistral prompts included FEVER item 202303 with 10,794 input tokens. At 23:18 UTC on 8 November, the 8,192-token preflight failed on this item. At 23:23 UTC, the 16,384-token preflight passed all 1,500 Mistral inputs with the same token manifest. The higher runtime limit applied to every D prompt for this model. The 128-token output limit, model revision, prompt bytes, scorer and cohort were retained. No prompt was dropped or truncated to resolve the overflow. W and its re-execution controls retained their original settings. The runtime setting is therefore a possible difference in the Mistral D comparison. The benchmark-equal excess uses the registered score analysis. Both the timing and the deviation must accompany its interpretation.

SHA-256 receipts:

- Failed preflight: 5a7ed2c47f793a2d3cb15200999331a60ba7df8b9683af62d6d102d6b95a9068
- Passing preflight: a5d69c0a37508a0909113a10f0cbd414aabf58b068ebb9e5aa7a43cdc3b166fe
- Frozen Mistral token manifest in both preflights: 72579086e08e7e02133cc9bce0873ea08e6adb309d086dbf68102c4e8c20f1a1
- Local pre-generation note referenced in the passing preflight: d2ef1fe71c43604695e9184d1db12354dd42bf284feb32bef6a023fb710cccc4
- Signed Mistral D output: f35267d3db8c3cba9ee194ad3836711d5455c0af53835c537ef2ae4b14b2ed9a
- Frozen combined H1–H4 report: d3244baaa9d8c0b94edf54855eedf75c0cd91d44827c5273033cbb9302aec028
