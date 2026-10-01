# CFC ↔ RIDI v0.2 — F1 bilateral exact-hash sign-off

**Sign-off date:** 2026-10-01  
**Status:** F1 BILATERALLY ACCEPTED / NEUTRAL-SCHEMA GATE NEXT / NO F2 YET  
**Signed F0:** SHA-256 `22681ece0456bb92f8296ea1b699ece9480a581ea7ab5c7b563ca261901f917e`

## Accepted baseline

`CFC Anchor 0.2.90rc1`

Frozen wheel SHA-256:

`b3b1f11e060289afa4e7da61072f2c31be7f0da1786be90682ec307d4e1f5303`

## Accepted adapter-facing interface

Artifact:

`collaboration/cfc-ridi/v0.2/F1_CFC_ANCHOR_INTERFACE_MANIFEST.md`

Exact identity:

- bytes: `4945`
- SHA-256:
  `b23719df7efd75dc4d53b33808377e1002a044a88acc5354defd06dc59829184`
- Git blob:
  `5e1bbd1823214955e962b88b3bb04af755e41586`

CFC completeness-amendment commit:

`7bc03fd1556fcc4138714de2468b88c16ef215cc`

## RIDI acceptance

RIDI independently reverified and explicitly accepted the exact baseline wheel identity and exact interface-manifest identity above.

RIDI acceptance record:

`F1_RIDI_ACCEPTANCE_PENDING_CFC_COUNTERSIGN.md`

Latest clarification commit:

`8b15e5e89ae19fa0f7e2965c4f61e5d21c25ffc3`

The accepted interface is a bounded maximum surface for the custom-Demonstrator public lifecycle used as the F1 reference. It is not a claim that every public surface exercised by every Demonstrator case is included.

## CFC countersign

CFC independently rechecked and explicitly countersigned the same exact identities.

CFC acceptance record:

`collaboration/cfc-ridi/v0.2/F1_CFC_EXACT_HASH_ACCEPTANCE.md`

CFC commit:

`0dff0482a9c828d9e225a5d593435035941b3ace`

CFC explicitly accepted:
- the same Anchor wheel SHA-256;
- the same 4,945-byte interface artifact;
- the same interface SHA-256;
- the bounded-scope clarification.

## Effect

The signed-F0 F1 bilateral-acceptance condition is satisfied.

F1 therefore fixes:
1. one controller baseline: `CFC Anchor 0.2.90rc1`;
2. one maximum adapter-facing interface: exact SHA-256
   `b23719df7efd75dc4d53b33808377e1002a044a88acc5354defd06dc59829184`.

Any later need for an additional controller-facing public class or method requires an explicit versioned F1 interface amendment and renewed bilateral acceptance before use.

## Next gate

F1 acceptance does **not** itself authorize F2.

Under signed F0, the next artifact is the **Neutral schema class for Phase F**:
- produced by RIDI;
- independently reviewed by CFC;
- accepted by both parties as the same exact artifact/hash.

Only after that neutral-schema gate closes may F2 adapter implementation begin.

v0.1 remains closed and immutable.  
F0 remains signed and immutable.

**F1 signed → neutral schema → F2.**
