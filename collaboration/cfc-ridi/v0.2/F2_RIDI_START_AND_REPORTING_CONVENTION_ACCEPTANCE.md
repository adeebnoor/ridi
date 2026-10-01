# CFC–RIDI v0.2 — RIDI F2 Start Record and Reporting-Convention Acceptance

**Date:** 2026-10-01  
**Status:** F2 MAY BEGIN / RIDI REPORTING-CONVENTION ACCEPTANCE / PENDING CFC COUNTERSIGN  
**Authority:** signed F0 feasibility workplan  
**Neutral-schema status:** bilaterally exact-hash closed

## 1. Start boundary

Phase F neutral schema R1 was bilaterally closed at RIDI commit:

`4bb4e352e20132248a0edba15fd9080505ddf3da`

Frozen baseline branch:

`freeze/cfc-ridi-v0.2-neutral-schema-r1`

Closure result:

`PHASE_F_NEUTRAL_SCHEMA_R1_BILATERAL_EXACT_HASH_CLOSED`

Under signed F0, F2 may now begin.

F2 implementation responsibility remains exactly as predeclared:

- primary producer: CFC side;
- independent verifier: RIDI side;
- controller baseline: read-only;
- adapter: separate, versioned, nonfixture artifact;
- only the bilaterally accepted F1 adapter-facing interface may be used;
- no private bypass, monkeypatch, private-state injection, controller modification, semantic promotion, authority creation, case-specific exception or expected-outcome conditioning is permitted.

## 2. F2 NO-GO reporting convention

RIDI accepts the existing reporting-convention artifact exactly as present on the frozen baseline:

`collaboration/cfc-ridi/v0.2/F2_NO_GO_REPORTING_CONVENTION_DRAFT.md`

Exact repository identity:

- bytes: `2181`
- Git blob: `97d9f476b938888a7101ccfb5f17b7fab9353796`

RIDI accepts its two-level interpretation:

- primary status: `F2_NO_GO_API_OR_IMPLEMENTATION_BOUNDARY`
- reason code `API_INCOMPATIBLE` for the signed-F0 `F2_NO_GO_API_INCOMPATIBLE` case;
- other documented reason codes remain exactly as written in the convention.

This acceptance changes no F0 criterion, trigger, stop condition or implementation boundary.

The convention becomes operative only after CFC explicitly accepts the same exact artifact identity before the first F2 classification.

## 3. Next required CFC artifact

The next producer-side artifact is the exact F2 candidate nonfixture adapter source/package plus identity/hash.

RIDI will then:

1. verify that the adapter uses only the accepted F1 surface;
2. verify that the neutral-schema contract is preserved;
3. review the exact source artifact;
4. independently rerun public tests where permitted;
5. retain any failure without weakening the frozen criteria.

No F3/F4/F5 conclusion is implied by starting F2.

## 4. Current RIDI status

`F2_RIDI_READY_FOR_CFC_CANDIDATE_ADAPTER`

and

`F2_REPORTING_CONVENTION_RIDI_ACCEPTED_PENDING_CFC_COUNTERSIGN`
