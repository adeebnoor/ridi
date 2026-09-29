# CFC ↔ RIDI selected specimen v0.1 — RIDI input freeze

**Freeze date:** 2026-09-29  
**Status:** NEUTRAL SPECIMEN BYTES FROZEN / RIDI INPUT FROZEN / CFC MAPPED-INPUT HASH FREEZE PENDING / NO SUBSTANTIVE EXECUTION

## Exact neutral specimen

The selected neutral records were extracted byte-for-byte from the previously frozen candidate-registry transport and independently matched against the four hashes frozen by the selected pool row.

Transport ZIP SHA-256:

`2b96ee5319cb93bce9b752fb4c6c3353c0e0463d8cd11e79f0dd682423093b00`

Selected case:

`RAG-nq-test1035`

Exact record hashes:

- source A: `60e19ea94ff13ded74e6ca19d6063909d374951f86218a9e3e68833b46126734`
- endpoint A: `e03c1c6433cd197f780537a90d1541744b314cf8eb196ca426f7dc4a41779c67`
- source B: `018f1de8876594e57a383b69a1fcd605e811cf062695cc2ab947c737a697e308`
- endpoint B: `e66408834f040464bb8146e4ed814a26f15bb871519db4194c7a764b4e8580c5`

The exact records are public under `collaboration/cfc-ridi/specimen-v0.1/neutral/`.

## RIDI selected-pair input

The exact RIDI input is:

`collaboration/cfc-ridi/specimen-v0.1/RIDI_SELECTED_PAIR_INPUT.json`

Exact UTF-8 bytes:

`1719`

SHA-256:

`4e6abbec8344e6869a3a103763b529799a35f8dc52ecba0037f5bc9695b3ce53`

This input contains only fields permitted to the RIDI side by frozen I1.

It records:

- the frozen evaluation-definition identity;
- exact source and endpoint record hashes;
- A/B selected passage identities and relevance-grade vectors;
- the recorded offline raw and canonical outputs;
- the model/revision identity;
- ground-truth correctness explicitly withheld until post-commit secondary analysis.

No CFC authority record, CFC mapped input, CFC gate/reason or CFC result is included or inspected.

## Frozen RIDI comparison surface

For this registered RAG evaluation, the primary shared-protocol endpoint is the recorded downstream verdict/action equivalence. The operational recorded field supplied to the frozen input is the registered canonical output for each arm, and the comparison surface is exact canonical-output equality.

The input freeze itself does **not** record a RIDI PASS/FAIL result. The result will be computed only during substantive RIDI execution after the bilateral pre-execution hash gate is complete.

## Remaining gate

RIDI substantive execution remains prohibited until CFC records, without revealing the mapped contents to RIDI:

1. mapped CFC arm-A input SHA-256 and byte size;
2. mapped CFC arm-B input SHA-256 and byte size;
3. CFC mapping-manifest SHA-256 and byte size;
4. CFC authority-manifest SHA-256 and byte size;
5. confirmation that the frozen M1/A1/I1 hashes were used unchanged;
6. confirmation that no prohibited cross-side pre-commit inspection occurred.

After those hashes are frozen, both sides may execute independently. Each side must then assemble one exact immutable raw bundle and publish only its bundle SHA-256 and byte size before exchange.

**Evidence before execution.**
