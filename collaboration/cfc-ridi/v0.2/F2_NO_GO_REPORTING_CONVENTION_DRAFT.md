# CFC ↔ RIDI v0.2 — F2 NO-GO reporting-label convention DRAFT

**Status:** DRAFT FOR BILATERAL REVIEW BEFORE FIRST F2 CLASSIFICATION  
**Does not modify signed F0:** SHA-256 `22681ece0456bb92f8296ea1b699ece9480a581ea7ab5c7b563ca261901f917e`

## Problem

Signed F0 contains two related labels:

1. `F2_NO_GO_API_OR_IMPLEMENTATION_BOUNDARY`
2. `F2_NO_GO_API_INCOMPATIBLE`

Their triggers overlap. The CFC-side F0 approval requested consistent interpretation before any F2 classification.

## Proposed convention

Use a two-level reporting structure rather than treating the labels as competing outcomes.

### Canonical F2 primary status

```text
F2_NO_GO_API_OR_IMPLEMENTATION_BOUNDARY
```

Use this as the **primary F2 NO-GO status** whenever faithful representation would require crossing the accepted F1 implementation/interface boundary.

### Reason codes

Report one or more exact reason codes underneath the primary status:

- `API_INCOMPATIBLE` — F1-approved adapter-facing API cannot faithfully receive/represent the intended state.
- `PRIVATE_BYPASS_REQUIRED` — execution would require an unapproved private/internal authorization path.
- `MONKEYPATCH_REQUIRED` — execution would require monkeypatching controller behavior.
- `PRIVATE_STATE_INJECTION_REQUIRED` — execution would require unapproved hidden/private runtime state.
- `CONTROLLER_MODIFICATION_REQUIRED` — execution would require modifying the frozen baseline.
- `OTHER_IMPLEMENTATION_BOUNDARY` — another boundary violation explicitly documented before classification.

Thus the signed-F0 label `F2_NO_GO_API_INCOMPATIBLE` is interpreted as the specific case:

```text
primary_status = F2_NO_GO_API_OR_IMPLEMENTATION_BOUNDARY
reason_code    = API_INCOMPATIBLE
```

## Non-change rule

This convention:
- changes no F0 acceptance criterion;
- changes no trigger;
- weakens no stop condition;
- authorizes no implementation;
- merely normalizes reporting so one failure is not classified under two competing top-level labels.

It becomes operative only after both parties explicitly accept this convention before the first F2 classification.

**Normalize reporting; do not normalize away failure.**
