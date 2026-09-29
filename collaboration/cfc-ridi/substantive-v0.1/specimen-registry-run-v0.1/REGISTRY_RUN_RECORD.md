# CFC ↔ RIDI Specimen Registry Run v0.1

**Status:** CONSTRUCTED + CHECKED / POOL OUTPUT IS DRAFT / NOT FROZEN  
**Date:** 2026-09-29  
**Frozen eligibility checker SHA-256:** `96ca16e12e3f2fecb5a06998eb28476e250b2a0965f2b26713da298391958904`

## Source frame

The registry was constructed from all 800 primary registered Qwen3-8B / BM25 / k=10 reference-vs-random RAG pairs from the retained RIDI Nature v95.4 package.

No registration was filtered using model-output equality or difference, correctness, CFC output, RIDI output, desired asymmetry, or publication value.

Dataset frame:
- Natural Questions: 250
- HotpotQA: 250
- FEVER: 150
- SciFact: 150

Structural checks before registry construction:
- 800 unique query pairs;
- exactly one reference and one random arm per pair;
- complete relevance-grade vector identical between reference and random for all 800 pairs;
- no original authoritative independent-support-count rule found in the preregistration; the recorded status is `NO_AUTHORITATIVE_REQUIREMENT_SPECIFIED`, not `AUTHORITATIVE_1`.

## Original retained source artifacts

- `contexts_800.jsonl` — 25,266,491 bytes — SHA-256 `1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1`
- `registered_generations_primary_800.jsonl` — 564,276 bytes — SHA-256 `e7d1c8c06eece5482f632d628f933741ebbfc379ae01a99a293abdd9debf929c`
- `protocol/PREREGISTRATION_NATURE_RAG.md` — 17,508 bytes — SHA-256 `0f7babda273f68e2095343f2fb33f2dca3c8720f95ed87ca3a0f47d1b337b063`

## Derived pre-run artifacts

Derived source specimens intentionally exclude hidden gold/correctness and model outputs.

Derived offline endpoint records intentionally exclude correctness and pair-level comparison fields. Arm A/B endpoint bytes were hash-bound independently and were not compared during registry construction.

- `source_specimens_1600.jsonl` — SHA-256 `a612fd38f0a502fd082f1955e4c1679f3c2a6bc91a9df44ca12c120dbf56f1f1`
- `offline_endpoints_1600.jsonl` — SHA-256 `49441ff1e495f645cc0ae7d2117a4c9ff7c6be4ce622e9c83b9bc7bd78f5319e`
- `specimen_registry.tsv` — 800 registrations — SHA-256 `09824e8fa0837cc852b34c984b3ad7156a7433a57d672f4124356f4806e2fccf`

Input package:
- SHA-256 `2b96ee5319cb93bce9b752fb4c6c3353c0e0463d8cd11e79f0dd682423093b00`
- 435,772 bytes

## Frozen checker execution

The exact frozen checker bytes were verified before execution:
`96ca16e12e3f2fecb5a06998eb28476e250b2a0965f2b26713da298391958904`

Observed output:
```text
registration_count=800
accepted_count=800
rejected_count=0
```

All 800 audit rows have:
- `eligibility_status = ACCEPT`
- `reason_codes = NONE`

Generated artifacts:
- `eligibility_audit.tsv` — SHA-256 `23e027e7228c3a09d13b238619ca87389f304f3fb281c37b386cca6a6defe826`
- `eligible_pool_draft.tsv` — 800 rows — SHA-256 `ebb7e660199687650a5c03888839401cc6f88f5b3fe6a55a77649bb855a43ade`
- `checker_run.txt` — SHA-256 `8718c56a1a1afce095b74df409d67f0a346c0d0d6dbf1e8560f2ffaa69c67f2a`

## Boundary

The 800-row pool output is a DRAFT checker product, not a frozen pool.

Current state:
- specimen registry constructed: yes
- eligibility checker executed: yes
- pool frozen: no
- randomization material created: no
- shared specimen chosen: no
- substantive CFC execution: no
- substantive RIDI execution: no

No randomization or specimen scoring is permitted until the exact pool bytes are bilaterally reviewed and frozen in a later step.
