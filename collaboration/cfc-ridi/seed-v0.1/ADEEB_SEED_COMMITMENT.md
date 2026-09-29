# CFC ↔ RIDI seed commit–reveal v0.1 — ADEEB commitment

**Commitment date:** 2026-09-29  
**Participant:** ADEEB  
**Branch:** `commit/cfc-ridi-seed-v0.1`  
**Status:** ADEEB COMMITMENT PUBLISHED / ADEEB SEED NOT REVEALED / KRZYSZTOF COMMITMENT PENDING / NO CASE SELECTION / NO SUBSTANTIVE EXECUTION

## Chronology gate

This commitment is created only after RIDI publicly verified completion of the bilateral exact-byte eligible-pool mirror.

RIDI post-publication verification commit:

`fc83818855296feabe0dcb6de8167af39b0edac6`

Frozen eligible-pool SHA-256:

`ebb7e660199687650a5c03888839401cc6f88f5b3fe6a55a77649bb855a43ade`

CFC final mirror head independently verified by RIDI:

`3b0dba0021139b4e948af18051a283f5ea4ad17f`

## ADEEB seed commitment

A fresh private 256-bit seed was generated after the chronology gate above.

The seed itself is intentionally **not** recorded in this repository.

Frozen commitment formula:

```text
SHA256("CFC-RIDI-SEED-v0.1|ADEEB|<64-lowercase-hex-seed>")
```

ADEEB commitment:

```text
f4991d7a1828c2864f5aa3ef8a2cc65b16bd78f2f2e81e529fa33bc832d2e61b
```

## Stop condition

ADEEB must not reveal the private seed until KRZYSZTOF has independently generated a private seed and publicly committed its corresponding commitment.

No combined selection hash may be computed, no case score may be computed, and no case may be selected before both commitments are public.

After both commitments are public, the parties may reveal their seeds. Each reveal must verify against its participant-specific commitment before the combined selection hash is computed.

No seed reveal, case selection or substantive controller execution is performed by this record.

**Evidence before selection.**
