# CFC ↔ RIDI selected neutral specimen bindings v0.1

**Case:** `RAG-nq-test1035`  
**Status:** SELECTED IDENTITY FROZEN / EXACT-LINE EXTRACTION PENDING / NO SUBSTANTIVE EXECUTION

The selected identity was produced by the frozen bilateral commit–reveal procedure and independently reproduced by the CFC side.

Independent CFC confirmation reports:
- selected case: `RAG-nq-test1035`;
- all 800 scores independently reproduced;
- RIDI score table matched byte-for-byte;
- no substantive CFC or RIDI evaluation had yet occurred.

## Frozen exact-line bindings

The selected pool row binds the following exact JSONL line bytes, including the terminating LF byte:

| Artifact | Frozen source reference | Expected SHA-256 |
|---|---|---|
| source A | `source_specimens_1600.jsonl#RAG-nq-test1035:A` | `60e19ea94ff13ded74e6ca19d6063909d374951f86218a9e3e68833b46126734` |
| endpoint A | selected A offline endpoint | `e03c1c6433cd197f780537a90d1541744b314cf8eb196ca426f7dc4a41779c67` |
| source B | `source_specimens_1600.jsonl#RAG-nq-test1035:B` | `018f1de8876594e57a383b69a1fcd605e811cf062695cc2ab947c737a697e308` |
| endpoint B | selected B offline endpoint | `e66408834f040464bb8146e4ed814a26f15bb871519db4194c7a764b4e8580c5` |

Pair fingerprint:

`8caf18edd9a278b6807fd98682d4faee010ae00dbccdd5eeba57c93a360721f4`

Evaluation definition:

`RIDI-RAG-NATURE-v2-PROSPECTIVE/C2/QWEN3-BM25-K10-RANDOM`

Evaluation-definition SHA-256:

`0f7babda273f68e2095343f2fb33f2dca3c8720f95ed87ca3a0f47d1b337b063`

Original support-requirement status:

`NO_AUTHORITATIVE_REQUIREMENT_SPECIFIED`

Prior public exposure:

`TRUE`

## Exact-byte extraction rule

No question text, passage text, verdict/action, rank, relevance grade, or authority fact may be reconstructed from external sources.

The exact selected records must be extracted from the already frozen/reviewed transport files:

- `source_specimens_1600.jsonl`
- `offline_endpoints_1600.jsonl`

An extracted record is accepted only if the SHA-256 of its complete original JSONL line bytes **including LF** equals the corresponding frozen digest above.

No normalization, JSON reserialization, whitespace change, field reordering, newline conversion or content repair is permitted before the exact-line identity is frozen.

## Boundary

This binding record freezes identity only. It does not expose:
- CFC mapped inputs;
- CFC authority manifests;
- CFC outputs;
- RIDI computed result;
- interpretation.

**Evidence before execution.**
