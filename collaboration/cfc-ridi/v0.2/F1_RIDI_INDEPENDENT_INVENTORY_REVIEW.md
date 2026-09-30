# CFC ↔ RIDI v0.2 — RIDI independent F1 descriptive-inventory review

**Review date:** 2026-09-30  
**Status:** F1 DESCRIPTIVE INVENTORY REVIEW PASS / COMPLETE ENOUGH FOR F1 NOMINATION REVIEW / NO BASELINE NOMINATED / NO F2 AUTHORIZED  
**Signed F0:** SHA-256 `22681ece0456bb92f8296ea1b699ece9480a581ea7ab5c7b563ca261901f917e`

## 1. CFC-side F1 inventory artifact

CFC publication commit:

`586cd72515246c5ad7a093a4b7532c8137ae7901`

File:

`collaboration/cfc-ridi/v0.2/F1_CFC_CANDIDATE_INVENTORY.md`

Independent RIDI byte identity:

- bytes: `6830`
- SHA-256:
  `9c05a74909b1c62bb46bfcab91a80e2eb3b7739416260c501d1f13e538763342`
- Git blob:
  `51adcc78af8a35b002800b10b276a2cc73cbcf6f`
- line endings: LF only
- terminal LF: yes

The inventory is descriptive, non-ranking and non-nominating as required by signed F0.

## 2. F0 archival mirror

CFC mirror commit:

`e52e3a990dc2ca7d7d70bc943e854691cbf11de1`

The mirror records the already-signed F0 identity:

- bytes: `16703`
- SHA-256:
  `22681ece0456bb92f8296ea1b699ece9480a581ea7ab5c7b563ca261901f917e`
- Git blob:
  `a3b14166230eec9e66716918ddbf324ed19c67df`

Result: archival symmetry established without modifying/reopening F0.

## 3. Candidate A — CFC Anchor 0.2.90rc1

### 3.1 Identity verification

The public tag:

`cfc-demonstrator-v1.0`

resolves to commit:

`ba3efb6592b4b8602799fd6ec136c0ab1edefbbe`

The exact frozen Anchor wheel at that reference is:

`demonstrator/cfc_anchor-0.2.90rc1-py3-none-any.whl`

Independent RIDI byte verification:

- bytes: `211808`
- SHA-256:
  `b3b1f11e060289afa4e7da61072f2c31be7f0da1786be90682ec307d4e1f5303`
- Git blob:
  `b1daebc044762e4f57b29f0b8975872cfe26b743`

Result: **MATCH** with the F1 inventory.

The protected frozen identity record also states:
- engine SHA-256:
  `77a7547c02ce4aac3d3abc759bbd266f4251de9149da2308454527c7f2dea5c0`
- public API contract SHA-256:
  `fee18165ea5d4a29e72137028ec3cf5c637b85c83672437b2352fc316f53b66a`
- status: `FROZEN PUBLIC API V1`.

The engine SHA above was cross-checked against the frozen identity record and the Integration Layer RC release record; this RIDI review did not independently unpack/re-hash the wheel's internal engine member.

### 3.2 Interface/boundary verification

Public Integration Layer records support the inventory statements that:
- it is a separate external layer over frozen Anchor;
- it does not modify the frozen controller;
- it preserves access to raw frozen-controller output;
- its declarative mapping is intentionally bounded;
- it does not demonstrate automatic domain-semantic interpretation or every Anchor mechanism.

These are interface facts only. They do not establish that Anchor is suitable for the RIDI v0.2 feasibility contract.

## 4. Candidate B — CFC-next 0.3.0a2

### 4.1 Frozen identity verification

Canonical frozen ref:

`frozen/cfc-next-0.3.0a2`

resolves to:

`568282c1f66af9f1f2fad8cf2b04b08226b9aea6`

The candidate source:

`cfc_next_candidate_0_3_0a2/__init__.py`

independently verifies as:

- bytes: `18023`
- SHA-256:
  `dc8ae4f2d51296d68ecf5e75ac861faf1f50f062e1761e0814ce157f08a588a7`
- Git blob:
  `8c3f915e6a902b022b877dc84dada2cc1e794619`

Result: **MATCH** with the F1 inventory and frozen manifest.

The pinned freeze manifest on main records:
- 14/14 positive cases pass;
- 12/12 negative controls fail closed;
- zero unexpected BOUND negative paths;
- promotion-readiness all gates pass;
- 14 tested state-isolation relations with no candidate authorization visible to frozen relations;
- no historical rescore;
- frozen Anchor reference not modified.

### 4.2 Internal dependency versus adapter boundary

Direct source inspection confirms:

- CFC-next `Controller` subclasses frozen Anchor `Controller`;
- the candidate imports `cfc_anchor._engine`;
- it reads/uses private controller-module constants/helpers;
- it exports `Controller`, `CANDIDATE_VERSION`, `FROZEN_REFERENCE`, and `generic_accounting_node_valid`;
- its source explicitly states that the earlier 0.3.0a1 import-time mutation was removed.

Therefore the inventory correctly distinguishes:

**candidate-internal private Anchor dependency = YES**

from:

**external adapter private bypass requirement = not established / not implied merely by that internal dependency.**

F1 nomination review must still identify the exact adapter-facing interface and demonstrate that the external v0.2 adapter would not itself require:
- `cfc_anchor._engine` access;
- controller monkeypatching;
- private-state injection;
- an unapproved private/internal authorization path.

This is a future F1/F2 gate, not a defect in the descriptive inventory.

## 5. Scope of this review

This review verifies descriptive identity/interface claims sufficiently for the next F1 step.

It does **not**:
- rank Candidate A vs Candidate B;
- nominate a baseline;
- claim either candidate satisfies the v0.2 feasibility contract;
- execute either controller;
- validate a substantive adapter;
- validate real authority availability;
- authorize F2.

## 6. F1 inventory decision

Result:

`F1_DESCRIPTIVE_INVENTORY_REVIEW_PASS`

Meaning:

> The CFC-side inventory is sufficiently complete and accurately bounded to proceed to the signed-F0 **single-baseline nomination review**.

The next artifact remains CFC-produced under signed F0:

1. nominate exactly one of the two signed-workplan candidates;
2. identify the exact adapter-facing interface proposed for Phase F;
3. state the factual reasons the nominated baseline is believed to satisfy the F1 acceptance rule;
4. retain all known limitations, including any internal private dependency;
5. make no F2 adapter implementation change before bilateral F1 acceptance.

RIDI will independently verify that nomination/interface package before recording F1 acceptance.

**Inventory review is not baseline acceptance. F1 before F2.**
