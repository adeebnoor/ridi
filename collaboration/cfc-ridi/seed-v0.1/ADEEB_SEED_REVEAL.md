# CFC ↔ RIDI seed commit–reveal v0.1 — ADEEB reveal

**Reveal date:** 2026-09-29  
**Participant:** ADEEB  
**Branch:** `reveal/cfc-ridi-seed-v0.1`  
**Status:** ADEEB SEED REVEALED AND SELF-VERIFIED / KRZYSZTOF SEED REVEAL PENDING / NO CASE SELECTION / NO SUBSTANTIVE EXECUTION

## Prior public commitment

ADEEB commitment publication commit:

`e16b607c1989cafa313845d7abf816147d10905e`

Previously published ADEEB commitment:

```text
f4991d7a1828c2864f5aa3ef8a2cc65b16bd78f2f2e81e529fa33bc832d2e61b
```

Both ADEEB and KRZYSZTOF commitments were public before this reveal.

KRZYSZTOF commitment commit verified by RIDI:

`9421294146d3b0af1c094f13279b77feec83228e`

KRZYSZTOF public commitment:

```text
2fb9682ab752db2f021abc3d97cf5ca447a14779c4990039ec6407b04f2f7b02
```

## ADEEB seed reveal

The already-committed ADEEB 32-byte seed, encoded as exactly 64 lowercase hexadecimal characters, is:

```text
127e996682ca08fe2905828ad00bf4c1cb808745fe6af50df7ae5d540fa8bb5a
```

Frozen verification formula:

```text
SHA256("CFC-RIDI-SEED-v0.1|ADEEB|127e996682ca08fe2905828ad00bf4c1cb808745fe6af50df7ae5d540fa8bb5a")
```

Recomputed SHA-256:

```text
f4991d7a1828c2864f5aa3ef8a2cc65b16bd78f2f2e81e529fa33bc832d2e61b
```

Result: **MATCH** with the pre-existing public ADEEB commitment.

Frozen eligible-pool SHA-256:

```text
ebb7e660199687650a5c03888839401cc6f88f5b3fe6a55a77649bb855a43ade
```

## Stop condition

The KRZYSZTOF seed has not yet been revealed to RIDI.

Therefore RIDI does not compute:
- the combined selection hash;
- per-case scores;
- a selected case.

After KRZYSZTOF reveals the exact 64-lowercase-hex seed, RIDI must first independently verify:

```text
SHA256("CFC-RIDI-SEED-v0.1|KRZYSZTOF|<revealed-seed>")
=
2fb9682ab752db2f021abc3d97cf5ca447a14779c4990039ec6407b04f2f7b02
```

Only after that MATCH, and re-verification of the frozen pool hash, may deterministic selection be computed under the frozen protocol.

**Evidence before selection.**
