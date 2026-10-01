# CFC–RIDI v0.2 — RIDI Independent F3 R1 Rerun PASS on F2 v0.2

**Review date:** 2026-10-01  
**Status:** RIDI INDEPENDENT RERUN PASS  
**Authority:** signed F0 feasibility workplan  
**F2 baseline:** `CFC-RIDI-F2-ADAPTER-v0.2`, bilaterally exact-hash closed  
**F3 criteria:** bilaterally frozen R1, unchanged

## Exact frozen inputs

F2 v0.2 candidate:

`930d7b0119159eaedbaf947691d9510b4c61d81c`

F2 v0.2 primary adapter SHA-256:

`15b7d01787237b2e5f0d1ca106c4e84aaf1976a2512179c79c458fe3d80e634b`

F3 criteria SHA-256:

`f9640dbaec55a2b381a159825fe27a9e87502b75b20bbfbcf4382ca44cd887a2`

CFC frozen F3 rerun commit:

`c14dc6030f80f036757214627b011385e31768f7`

CFC F3 freeze ref:

`freeze/cfc-ridi-v0.2-f3-r1-pass-v02`

RIDI independently verified that the freeze ref resolves exactly to the rerun commit above.

## Independent RIDI rerun

RIDI workflow:

`CFC-RIDI F3 v0.2 independent RIDI rerun`

RIDI run ID:

`36922057099`

RIDI workflow commit:

`bb8ad9c65307e9b5cdbcfc63f75e0b8f6baf8117`

Before executing F3, RIDI independently reproduced:

`PASS 10/10`

for the exact frozen F2 v0.2 baseline.

RIDI also reproduced the exact F3 suite identities before execution.

## Reproduced F3 result

Tests:

- total: `15`
- PASS: `15`
- FAIL: `0`

Overall result:

`F3_REPRESENTATION_ONLY_ADVERSARIAL_SUITE_PASS`

The previously failing:

`F3-T05 — Cross-case / cross-arm resolved-state substitution`

now independently reproduces PASS under the unchanged frozen criterion.

RIDI verified that T05 passes by explicit pre-evaluation binding rejection:

`RIDI_F3_V02_T05_EXPLICIT_BINDING_REJECTION_PASS`

The rejection is attributable to `BindingError` from the v0.2 root `neutral_arm_binding`.

## Exact result reproduction

RIDI independently reproduced the same result file identity reported by CFC:

`F3_RESULTS.json`

- bytes: `69494`
- SHA-256: `13dfe40f255e0398b971e90b3ea10cae164205ae5b345d7980c77b50a7b80e7b`

Result:

`RIDI_F3_V02_REPRODUCED_15_15_PASS`

The independent RIDI Actions artifact is separately packaged and therefore has its own ZIP identity:

- artifact ID: `11192456500`
- artifact ZIP bytes: `8791`
- artifact ZIP SHA-256: `77a7f425c80d0564d8324efc0881efba6f8fc4c0dc4bdd2495646e279c4c9bcb`

The contained result JSON is byte-identical to the CFC result identity above.

## RIDI decision

RIDI independently confirms:

`F3_REPRESENTATION_ONLY_ADVERSARIAL_SUITE_PASS`

for exact F2 adapter v0.2 under unchanged frozen F3 Criteria R1.

The prior v0.1 F3 NO-GO remains retained and unchanged as historical evidence.

This F3 PASS does not establish any F4 authority-universe or F5 calibration result.
