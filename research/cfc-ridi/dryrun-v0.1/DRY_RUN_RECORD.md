# CFC ↔ RIDI — Excluded Mechanical Dry Run v0.1

**Status:** PASS — EXCLUDED MECHANICAL DRY RUN ONLY  
**Date:** 2026-09-28 (Asia/Riyadh) / 2026-09-27 UTC  
**GitHub Actions run:** https://github.com/adeebnoor/ridi/actions/runs/36353521373  
**RIDI dry-run workflow commit:** `19c47ec79ec9ea97ac6780781e9c043dfb83e18a`

## Frozen inputs referenced

Parent protocol SHA-256:

`d6bc94e90be4ac01bd8ee60f32aa3045dd827f4f3e9e64a68b82191615138571`

Frozen annex SHA-256 values:

- M1: `7adc4229277280acf9f48528a74ace7df9ba28ac1295e30ced318a7c1a3ee858`
- A1: `86f8b73bbb7e6f59aea95f2f388d15b78c3cda2d9ffc5190336b3e5a4ca64be9`
- I1: `2f3a86e6e9e4b32633813bc2bd82dd2e04f55d7a643ca32780a78b997c01ae4b`

## Pinned CFC execution identity

- CFC repository commit: `8baf013c96a3954df9679ddeefcd689c49b8b132`
- Frozen CFC Anchor wheel: `cfc_anchor-0.2.90rc1-py3-none-any.whl`
- Wheel SHA-256 verified by workflow: `b3b1f11e060289afa4e7da61072f2c31be7f0da1786be90682ec307d4e1f5303`
- Engine SHA-256: `77a7547c02ce4aac3d3abc759bbd266f4251de9149da2308454527c7f2dea5c0`
- Mandatory gate count returned: 49
- Persistence schema returned: `DECISION_PERSISTENCE_HISTORY_V6`
- Runner: Ubuntu 24.04 / Python 3.12.3

## Dry-run input

```json
{
  "conclusion": "POSITIVE",
  "required_independent_supports": 1,
  "provenance_shape": "DISTINCT",
  "independence_authority": "NONE",
  "scope": "EXPECTED",
  "evidence": [
    {"polarity": "POSITIVE", "validity": "CURRENT"}
  ]
}
```

## Acceptance result

The pinned frozen CFC path executed the one-support configuration successfully.

Observed mechanical output:

- claim state: `VERIFIED`
- `control_closure`: `true`
- engine SHA matched the frozen identity
- one-support input was preserved as `required_independent_supports = 1`
- independence authority remained `NONE`
- scope remained `EXPECTED`
- no execution error was reported

Workflow acceptance markers:

```text
DRY_RUN_STATUS=PASS
ONE_SUPPORT_PATH_EXECUTED=true
SYNTHETIC_FIXTURE_SCOPE=EXCLUDED_DRY_RUN_ONLY
SUBSTANTIVE_CASE_SELECTED=false
SUBSTANTIVE_RUN_EXECUTED=false
```

The published CFC `verify_custom.py` regression was also run in the same pinned environment and returned `PASS` for all 8 published custom cases.

## Authority boundary

This run intentionally uses the demonstrator's synthetic custom-fixture authority path. That use is permitted only because this run is explicitly excluded and mechanical.

No synthetic/fixture authority from this run is transferred to, promoted into, or accepted as authority for a substantive shared case.

## Interpretation boundary

This dry run establishes only that the frozen CFC execution path can mechanically execute the annex-approved one-support configuration under the demonstrator fixture.

It is not:
- a substantive CFC ↔ RIDI result;
- evidence of a selected shared case;
- evidence of real-world authority/provenance;
- evidence that CFC or RIDI passed a joint substantive test;
- a test of the requirement for two independent supports.

No substantive case, pool selection seed, or substantive shared run was created by this dry run.
