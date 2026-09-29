# CFC ↔ RIDI deterministic case selection v0.1

**Selection date:** 2026-09-29  
**Status:** CASE SELECTED DETERMINISTICALLY / SPECIMEN INSTANTIATION NEXT / NO SUBSTANTIVE CFC OR RIDI EXECUTION YET

## Frozen inputs

Frozen eligible-pool SHA-256:

```text
ebb7e660199687650a5c03888839401cc6f88f5b3fe6a55a77649bb855a43ade
```

Candidate count: **800**

ADEEB revealed seed:

```text
127e996682ca08fe2905828ad00bf4c1cb808745fe6af50df7ae5d540fa8bb5a
```

ADEEB commitment:

```text
f4991d7a1828c2864f5aa3ef8a2cc65b16bd78f2f2e81e529fa33bc832d2e61b
```

KRZYSZTOF revealed seed:

```text
ab479e0750734f5e1c428f65bf621df87fb468e5bb607fa794c3dab95fadf198
```

KRZYSZTOF commitment:

```text
2fb9682ab752db2f021abc3d97cf5ca447a14779c4990039ec6407b04f2f7b02
```

Both role-specific seed commitments independently verify exactly.

## Combined selection hash

Frozen formula:

```text
SHA256("CFC-RIDI-SELECT-v0.1|" + seed_ADEEB + "|" + seed_KRZYSZTOF + "|" + pool_sha256_hex)
```

Combined SHA-256:

```text
b7b4ee510bbd2f3063141ebcb36290a3f08cee74df43ab780e6423673e23c223
```

## Deterministic scoring

For every frozen canonical case ID:

```text
score(ID) = SHA256("CFC-RIDI-CASE-v0.1|" + combined_hex + "|" + ID)
```

All 800 scores are preserved in `SELECTION_SCORES.tsv`, ordered from lowest to highest hexadecimal score with canonical case ID as the exact-tie secondary key.

## Selected case

Lowest score:

```text
case_id=RAG-nq-test1035
score=00086dd4952f8a8e053371f86ef4cc7dff696c16f77a03c1f4ec1704a3b7925a
```

Therefore the deterministic selected case is:

# `RAG-nq-test1035`

Frozen selected-row bindings:

- pair fingerprint: `8caf18edd9a278b6807fd98682d4faee010ae00dbccdd5eeba57c93a360721f4`
- source A SHA-256: `60e19ea94ff13ded74e6ca19d6063909d374951f86218a9e3e68833b46126734`
- offline endpoint A SHA-256: `e03c1c6433cd197f780537a90d1541744b314cf8eb196ca426f7dc4a41779c67`
- source A ref: `source_specimens_1600.jsonl#RAG-nq-test1035:A`
- source B SHA-256: `018f1de8876594e57a383b69a1fcd605e811cf062695cc2ab947c737a697e308`
- offline endpoint B SHA-256: `e66408834f040464bb8146e4ed814a26f15bb871519db4194c7a764b4e8580c5`
- source B ref: `source_specimens_1600.jsonl#RAG-nq-test1035:B`
- evaluation definition: `RIDI-RAG-NATURE-v2-PROSPECTIVE/C2/QWEN3-BM25-K10-RANDOM`
- evaluation-definition SHA-256: `0f7babda273f68e2095343f2fb33f2dca3c8720f95ed87ca3a0f47d1b337b063`
- original support requirement: `NO_AUTHORITATIVE_REQUIREMENT_SPECIFIED`
- prior public exposure: `TRUE`

Eligibility rationale from the frozen pool:

> Primary registered RAG reference/random pair; exact grade-vector equality verified structurally; endpoints hash-bound without comparing outputs; no authoritative source support-count rule specified.

## Boundary

The selected identity is now fixed. No quiet reselection is permitted.

This record does **not** inspect or interpret the selected A/B substantive outputs, and it does not run either controller.

The next protocol step is mechanical instantiation of the selected specimen under the already-frozen M1/A1/I1 rules, followed by freezing the exact specimen and mapped per-arm inputs/hashes before independent CFC and RIDI execution.

**Evidence before execution.**
