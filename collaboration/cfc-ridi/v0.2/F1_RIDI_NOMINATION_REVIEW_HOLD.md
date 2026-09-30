# CFC ↔ RIDI v0.2 — RIDI F1 nomination review HOLD

**Review date:** 2026-10-01  
**Status:** BASELINE IDENTITY PASS / NOMINATION RECORD PASS / INTERFACE CONTRACT INCOMPLETE / F1 NOT YET ACCEPTED / NO F2 AUTHORIZED  
**Signed F0:** SHA-256 `22681ece0456bb92f8296ea1b699ece9480a581ea7ab5c7b563ca261901f917e`

## 1. CFC nomination package

Publication commit:

`da354fbcd3e19029a49d530e2bba5b4dae72fc6f`

Nomination artifact:

`F1_CFC_SINGLE_BASELINE_NOMINATION.md`

Independent RIDI identity:
- bytes: `4082`
- SHA-256: `736287961159cffbe3a95eb92bc59320ceaf43322748b4efd09bef1bc2a4f687`
- Git blob: `70e51214755ef2e085501806aea1e0455bce02c1`

Interface artifact:

`F1_CFC_ANCHOR_INTERFACE_MANIFEST.md`

Independent RIDI identity:
- bytes: `4296`
- SHA-256: `d87392892ea878c81d3649641c3dbe56d4fc3c39c3c7fde5dab8577342a1756f`
- Git blob: `32e78190d57d5846bcd4f284f24306f70c0004e8`

Both are LF-only and terminal-LF terminated.

## 2. Baseline identity verification

Nominated baseline:

`CFC Anchor 0.2.90rc1`

Independent checks already completed:
- wheel bytes: `211808`;
- wheel SHA-256:
  `b3b1f11e060289afa4e7da61072f2c31be7f0da1786be90682ec307d4e1f5303`;
- public tag `cfc-demonstrator-v1.0` resolves to
  `ba3efb6592b4b8602799fd6ec136c0ab1edefbbe`;
- protected identity records:
  engine SHA-256 `77a7547c02ce4aac3d3abc759bbd266f4251de9149da2308454527c7f2dea5c0`;
  public API contract SHA-256 `fee18165ea5d4a29e72137028ec3cf5c637b85c83672437b2352fc316f53b66a`;
  status `FROZEN PUBLIC API V1`.

Result:

`F1_BASELINE_IDENTITY_PASS`

No ranking against CFC-next is implied.

## 3. Adapter-boundary verification

The frozen Demonstrator custom path imports only the public `cfc_anchor` package surface and does not import `cfc_anchor._engine`.

It demonstrates that an external layer can instantiate and call the frozen Anchor without:
- modifying controller code;
- adapter-side monkeypatching;
- private-state injection;
- direct `_engine` access.

The nomination's public-only boundary is therefore supported in principle.

## 4. Interface completeness issue

The proposed interface manifest states that the F2 adapter may use **only** the listed Controller methods.

Direct inspection of the frozen public Demonstrator lifecycle shows that the same public lifecycle also calls the following public Controller commitment helpers:

- `identity_commitment(...)`
- `failure_domain_topology_commitment(...)`
- `source_semantics_commitment(...)`
- `provenance_commitment(...)`
- `evidence_authority_commitment(...)`
- `snapshot_commitment(...)`
- `support_set_independence_commitment(...)`

These helpers bind the generated drafts/evidence/snapshot state to the public attestation objects subsequently passed to the listed `install_verified_*` / `verify_*` methods.

They are not listed in Section 3 of the proposed F1 interface manifest, even though the manifest simultaneously states that no method outside its list is authorized for F2.

Therefore, as written, the interface contract is not yet demonstrably sufficient to reproduce the public Demonstrator attestation lifecycle without exceeding its own allowed method list.

This is an **interface-contract completeness issue**, not a rejection of Anchor and not evidence that private access is required.

## 5. Required F1 clarification/amendment

Before bilateral F1 acceptance, CFC should do one of the following:

### Option A — explicit public-helper amendment

Add the exact required public commitment helper methods to the F1 interface manifest, retaining:
- no `cfc_anchor._engine`;
- no private registry access;
- no controller modification;
- no monkeypatching;
- no synthetic authority promotion.

### Option B — exact lifecycle explanation

Demonstrate, using only the currently listed interface, how the F2 adapter can create/receive correctly bound attestations for the required draft/evidence/snapshot lifecycle **without** calling those commitment helpers and without using any unlisted/private surface.

If Option B is chosen, the exact alternative authority/attestation binding path must itself be frozen in the F1 interface contract before acceptance.

## 6. Acceptance state

Current result:

`F1_HOLD_INTERFACE_CONTRACT_INCOMPLETE`

Meaning:
- Anchor identity: PASS;
- nomination is within signed F0 scope: PASS;
- public-only adapter boundary: supported;
- exact proposed adapter-facing surface: **not yet complete enough for bilateral F1 acceptance**.

No F2 adapter work is authorized.

A corrected interface manifest does **not** require reopening F0 or v0.1. It requires only a versioned F1 interface amendment and renewed independent RIDI verification before bilateral F1 acceptance.

**Close the interface before building the adapter.**
