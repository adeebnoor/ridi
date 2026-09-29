# CFC ↔ RIDI selected specimen v0.1 — RIDI-side identity freeze

**Freeze date:** 2026-09-29  
**Branch:** `freeze/cfc-ridi-selected-specimen-v0.1`  
**Status:** SELECTED SPECIMEN IDENTITY FROZEN / EXACT NEUTRAL RECORD BYTES AWAITING PUBLIC RE-EXPOSURE / CFC MAPPED-INPUT HASH FREEZE PENDING / RIDI INPUT HASH FREEZE PENDING / NO SUBSTANTIVE EXECUTION

## Selection authority

Deterministic selection record commit:

`4592e0b5de1cd34a6db8f7219512dd1d535f11a7`

Selected case:

`RAG-nq-test1035`

Selected score:

`00086dd4952f8a8e053371f86ef4cc7dff696c16f77a03c1f4ec1704a3b7925a`

Combined selection SHA-256:

`b7b4ee510bbd2f3063141ebcb36290a3f08cee74df43ab780e6423673e23c223`

Frozen eligible-pool SHA-256:

`ebb7e660199687650a5c03888839401cc6f88f5b3fe6a55a77649bb855a43ade`

Independent CFC-side selection confirmation received by RIDI:
- filename: `CFC_RIDI_Independent_Selection_Confirmation_2026-09-29.pdf`
- bytes: `28192`
- SHA-256: `8208810a35b099734048559309f6582477059196daef748106973bea7b9d07c2`

That confirmation independently reproduces both seed commitments, the frozen pool, the combined selection hash, all 800 scores and the selected case.

## Frozen annex identities

The already-frozen pre-selection annexes remain unchanged:

- M1 — Generic CFC Mapper v0.1  
  SHA-256: `7adc4229277280acf9f48528a74ace7df9ba28ac1295e30ced318a7c1a3ee858`
- A1 — Authority Policy v0.1  
  SHA-256: `86f8b73bbb7e6f59aea95f2f388d15b78c3cda2d9ffc5190336b3e5a4ca64be9`
- I1 — Inspection Matrix v0.1  
  SHA-256: `2f3a86e6e9e4b32633813bc2bd82dd2e04f55d7a643ca32780a78b997c01ae4b`

Any mapper, authority-policy or inspection-matrix change requires a versioned reset. No case-specific amendment is permitted.

## Selected neutral-record bindings

The selected pool row freezes the following exact record identities:

### Arm A

- source reference: `source_specimens_1600.jsonl#RAG-nq-test1035:A`
- source exact-line SHA-256: `60e19ea94ff13ded74e6ca19d6063909d374951f86218a9e3e68833b46126734`
- offline endpoint exact-line SHA-256: `e03c1c6433cd197f780537a90d1541744b314cf8eb196ca426f7dc4a41779c67`

### Arm B

- source reference: `source_specimens_1600.jsonl#RAG-nq-test1035:B`
- source exact-line SHA-256: `018f1de8876594e57a383b69a1fcd605e811cf062695cc2ab947c737a697e308`
- offline endpoint exact-line SHA-256: `e66408834f040464bb8146e4ed814a26f15bb871519db4194c7a764b4e8580c5`

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

## Byte-level specimen gate still required

The bindings above identify the exact selected records, but the four exact neutral JSONL records are not yet present on this public specimen-freeze branch.

Before substantive execution, the bilateral specimen gate requires public re-exposure or mutually accessible exact-byte copies of:

1. selected source record A, LF-terminated, exact SHA-256 `60e19ea94ff13ded74e6ca19d6063909d374951f86218a9e3e68833b46126734`;
2. selected endpoint record A, LF-terminated, exact SHA-256 `e03c1c6433cd197f780537a90d1541744b314cf8eb196ca426f7dc4a41779c67`;
3. selected source record B, LF-terminated, exact SHA-256 `018f1de8876594e57a383b69a1fcd605e811cf062695cc2ab947c737a697e308`;
4. selected endpoint record B, LF-terminated, exact SHA-256 `e66408834f040464bb8146e4ed814a26f15bb871519db4194c7a764b4e8580c5`.

The exact-byte copies must verify against these already-frozen identities. No regenerated or normalized substitute is permitted.

## I1 pre-execution separation

Before raw-bundle commitments:

- RIDI/Adeeb must **not** inspect the CFC mapped per-arm input, CFC mapping manifest content, CFC authority-manifest content, CFC gates/reasons or CFC result.
- CFC/Krzysztof may inspect the neutral A/B records and the recorded A/B verdict/action as permitted by I1, but must not inspect the computed RIDI output bundle or interpretation.

Therefore CFC mechanical instantiation must occur privately on the CFC side under frozen M1/A1/I1. Before CFC substantive execution, CFC should publicly timestamp only the exact hashes/byte sizes of its frozen mapped inputs and associated mapping/authority manifests, not disclose their contents to RIDI.

RIDI will independently freeze its own exact selected-pair input and hashes before RIDI substantive execution.

## Remaining pre-execution gate

Substantive execution is prohibited until all of the following are recorded:

1. exact selected neutral record bytes independently verify to the four frozen hashes above;
2. RIDI selected-pair input bytes and hash are frozen;
3. CFC mapped arm-A and arm-B input hashes are frozen under M1/A1/I1;
4. CFC mapping-manifest and authority-manifest hashes are frozen;
5. both sides confirm that no prohibited pre-commit inspection occurred.

Only then may the two sides execute independently and sequester their raw outputs.

The previously documented upstream provenance limitation remains unchanged.

**Evidence before execution.**
