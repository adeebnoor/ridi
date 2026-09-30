# CFC ↔ RIDI v0.2 — F0 bilateral sign-off record

**Sign-off date:** 2026-09-30  
**Status:** F0 SIGNED / PHASE F FEASIBILITY AUTHORIZED ONLY / NO CONTROLLER SELECTED / NO PROTOCOL FREEZE / NO ELIGIBILITY / NO SEED / NO SELECTION / NO SUBSTANTIVE EXECUTION

## Signed F0 identity

Exact artifact:

`F0_FEASIBILITY_WORKPLAN_DRAFT_R1.md`

- exact bytes: `16703`
- SHA-256:
  `22681ece0456bb92f8296ea1b699ece9480a581ea7ab5c7b563ca261901f917e`
- Git blob:
  `a3b14166230eec9e66716918ddbf324ed19c67df`

## CFC-side approval

Krzysztof Śliwka independently reported byte-level verification of the exact F0 artifact:

- bytes: `16703`;
- SHA-256: `22681ece0456bb92f8296ea1b699ece9480a581ea7ab5c7b563ca261901f917e`;
- result: **MATCH — PASS**.

He explicitly approved that exact SHA-256 and limited the approval to the bounded Phase F feasibility work in those bytes.

His approval explicitly did **not** approve:
- a controller baseline;
- controller modification;
- substantive execution;
- protocol/annex freeze;
- eligibility;
- seeds;
- selection.

## RIDI-side approval

Adeeb Noor independently reverified the exact same commit-pinned bytes and obtained:

- bytes: `16703`;
- SHA-256: `22681ece0456bb92f8296ea1b699ece9480a581ea7ab5c7b563ca261901f917e`;
- Git blob: `a3b14166230eec9e66716918ddbf324ed19c67df`;
- result: **MATCH — PASS**.

RIDI then explicitly approved the same exact SHA-256.

## Meaning of sign-off

The bilateral F0 condition is therefore satisfied.

The only newly authorized work is:

> **Phase F feasibility work exactly as bounded by the signed F0 workplan.**

The next gate is **F1 baseline candidate inventory / nomination review**.

No baseline is selected by this record.

Before any F2 adapter development:
1. the F1 baseline inventory must be produced and independently reviewed;
2. exactly one baseline + adapter-facing interface must be bilaterally accepted under F1;
3. prohibited controller modification/private bypass conditions remain in force.

## Minor F2 reporting-label point

The CFC-side approval noted a documentation point: the two F2 API/implementation-boundary NO-GO labels should be interpreted consistently before classification.

This does not change the signed F0 artifact.

A separate reporting-convention draft may be reviewed before any F2 classification. Until bilaterally accepted, it has no effect on F0 acceptance criteria or failure triggers.

## Immutable boundaries

- v0.1 remains closed and immutable.
- signed F0 bytes remain immutable.
- any change to F0 requires a new revision/hash/sign-off.
- feasibility failure remains a valid outcome.

**F0 signed. Phase F only. Evidence before execution.**
