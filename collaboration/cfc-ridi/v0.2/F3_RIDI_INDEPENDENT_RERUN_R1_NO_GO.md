# CFC–RIDI v0.2 — RIDI Independent F3 R1 Rerun and NO-GO Confirmation

**Review date:** 2026-10-01  
**Status:** RIDI INDEPENDENT RERUN CONFIRMS F3 NO-GO / REPRESENTATION INVALID  
**Authority:** signed F0 feasibility workplan  
**F3 criteria:** bilaterally frozen R1  
**F2 baseline:** immutable `CFC-RIDI-F2-ADAPTER-v0.1`

## Exact frozen suite rerun

CFC frozen suite commit:

`657fb9a0b2b8e1d384cfdee7119fc190c628d4c7`

CFC freeze ref:

`freeze/cfc-ridi-v0.2-f3-suite-r1-failed`

RIDI independently verified that the freeze ref resolves exactly to the suite commit above and reproduced the exact suite component byte lengths, SHA-256 values and Git blob identities before execution.

The immutable F2 adapter and exact Anchor wheel identities were also reproduced before the rerun.

## Independent RIDI execution

RIDI workflow:

`CFC-RIDI F3 independent RIDI rerun`

RIDI run ID:

`36883727462`

RIDI workflow commit:

`0760e64176d8ab42940d0bf505d4202e0b3b6ec1`

The run used Python 3.12 and executed the exact frozen CFC F3 suite from the exact frozen commit.

F2 representation baseline reproduced:

`PASS 8/8`

## Reproduced F3 result

Tests:

- total: `15`
- PASS: `14`
- FAIL: `1`

Failing test:

`F3-T05 — Cross-case / cross-arm resolved-state substitution`

Reproduced finding:

`mutation was silently ignored; diagnostic result identical to control`

The RIDI rerun reproduced the same final result file identity reported by CFC:

- bytes: `76129`
- SHA-256: `0c5dbdb3071e69988f76dd6573c1e5a8c43edfaf85716a21355d87a6e1febf14`

Thus the independent RIDI rerun reproduced not only the same 14/15 outcome and T05 classification, but the exact result bytes/hash.

## RIDI decision

Result:

`F3_NO_GO_REPRESENTATION_INVALID`

RIDI confirms the CFC-side F3 R1 NO-GO for the exact frozen F2 adapter v0.1.

No F4 progression is authorized.

The failing F2 adapter remains retained unchanged.

The next permitted action is a new versioned F2 adapter candidate addressing the T05 case/arm binding defect, under the unchanged frozen F1 interface, neutral schema and F3 criteria.

That new candidate requires:

1. new exact F2 identity/hash;
2. complete independent RIDI F2 review;
3. bilateral F2 exact-hash acceptance;
4. complete T01–T15 F3 rerun under the unchanged frozen criteria.

No criterion is weakened and no prior failure is removed.
