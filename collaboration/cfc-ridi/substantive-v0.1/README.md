# CFC ↔ RIDI substantive-run preparation v0.1

**Status: PREPARATORY / NOT FROZEN / NO SUBSTANTIVE CASE SELECTED**

This directory contains neutral infrastructure for the future substantive shared-case run under the frozen CFC ↔ RIDI Shared Case Protocol v0.1.

It does **not**:
- freeze an eligible pool;
- create or reveal a selection seed;
- select a substantive case;
- execute a substantive CFC or RIDI run;
- amend the frozen protocol, M1, A1 or I1;
- alter either controller.

## Frozen references

Protocol SHA-256:

`d6bc94e90be4ac01bd8ee60f32aa3045dd827f4f3e9e64a68b82191615138571`

Frozen annex SHA-256 values:

- M1: `7adc4229277280acf9f48528a74ace7df9ba28ac1295e30ced318a7c1a3ee858`
- A1: `86f8b73bbb7e6f59aea95f2f388d15b78c3cda2d9ffc5190336b3e5a4ca64be9`
- I1: `2f3a86e6e9e4b32633813bc2bd82dd2e04f55d7a643ca32780a78b997c01ae4b`

## Files

- `ELIGIBILITY_CRITERIA_DRAFT.md` — proposed outcome-independent pool rules.
- `eligible_pool_TEMPLATE.tsv` — schema only; contains no substantive candidates.
- `tools/protocol_selection.py` — deterministic pool hashing, seed-commit verification and case scoring.
- `tools/verify_raw_bundle.py` — immutable ZIP/hash-manifest verifier.
- `raw_bundle_manifest_TEMPLATE.tsv` — required bundle manifest schema.
- `PAPER_SKELETON_DRAFT.md` — result-neutral manuscript structure.
- `tests/test_protocol_infra.py` — local tests for byte conventions and selection logic.

Nothing in this directory should be described as preregistered or frozen unless separately approved and timestamped.
