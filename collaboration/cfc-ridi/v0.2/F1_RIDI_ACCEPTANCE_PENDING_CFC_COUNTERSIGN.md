# CFC ↔ RIDI v0.2 — RIDI F1 acceptance of nominated Anchor interface

**Review date:** 2026-10-01  
**Status:** RIDI F1 ACCEPTANCE / BILATERAL F1 COUNTERSIGN PENDING / NO F2 YET  
**Signed F0:** SHA-256 `22681ece0456bb92f8296ea1b699ece9480a581ea7ab5c7b563ca261901f917e`

## 1. Nominated baseline

RIDI independently accepts the CFC-side F1 nomination of:

`CFC Anchor 0.2.90rc1`

Exact frozen wheel identity:

- bytes: `211808`
- SHA-256:
  `b3b1f11e060289afa4e7da61072f2c31be7f0da1786be90682ec307d4e1f5303`
- Git blob:
  `b1daebc044762e4f57b29f0b8975872cfe26b743`

Public release/tag reference:

- tag: `cfc-demonstrator-v1.0`
- commit:
  `ba3efb6592b4b8602799fd6ec136c0ab1edefbbe`

Protected identity record:

- engine SHA-256:
  `77a7547c02ce4aac3d3abc759bbd266f4251de9149da2308454527c7f2dea5c0`
- public API contract SHA-256:
  `fee18165ea5d4a29e72137028ec3cf5c637b85c83672437b2352fc316f53b66a`
- status:
  `FROZEN PUBLIC API V1`

## 2. CFC nomination record

CFC publication commit:

`da354fbcd3e19029a49d530e2bba5b4dae72fc6f`

Nomination artifact:

`F1_CFC_SINGLE_BASELINE_NOMINATION.md`

Independent RIDI identity:

- bytes: `4082`
- SHA-256:
  `736287961159cffbe3a95eb92bc59320ceaf43322748b4efd09bef1bc2a4f687`
- Git blob:
  `70e51214755ef2e085501806aea1e0455bce02c1`

Result:

`F1_BASELINE_NOMINATION_PASS`

## 3. Amended exact adapter-facing interface

CFC completeness amendment commit:

`7bc03fd1556fcc4138714de2468b88c16ef215cc`

Artifact:

`F1_CFC_ANCHOR_INTERFACE_MANIFEST.md`

Independent RIDI identity:

- bytes: `4945`
- SHA-256:
  `b23719df7efd75dc4d53b33808377e1002a044a88acc5354defd06dc59829184`
- Git blob:
  `5e1bbd1823214955e962b88b3bb04af755e41586`
- line endings: LF only
- terminal LF: yes

## 4. Closure of the prior interface-completeness HOLD

The prior RIDI review identified seven public commitment helpers used by the frozen public Demonstrator lifecycle but omitted from the first interface manifest.

The amended manifest now includes exactly:

- `identity_commitment(...)`
- `failure_domain_topology_commitment(...)`
- `source_semantics_commitment(...)`
- `provenance_commitment(...)`
- `evidence_authority_commitment(...)`
- `snapshot_commitment(...)`
- `support_set_independence_commitment(...)`

Direct comparison against the frozen Demonstrator custom lifecycle shows:

- every `cfc_anchor.Controller` method called by that lifecycle is present in the amended manifest;
- no Controller method listed in the amended manifest is extra relative to that demonstrated lifecycle;
- every package-level `cfc_anchor` class imported by the lifecycle is present in the amended manifest;
- no package-level class in the manifest is extra relative to that lifecycle;
- the demonstrated lifecycle contains no `cfc_anchor._engine` import;
- the demonstrated lifecycle contains no adapter-side monkeypatch/private-module access.

Therefore:

`F1_HOLD_INTERFACE_CONTRACT_INCOMPLETE = CLOSED`

## 5. RIDI F1 acceptance

RIDI explicitly accepts:

1. baseline:
   `CFC Anchor 0.2.90rc1`
   with wheel SHA-256
   `b3b1f11e060289afa4e7da61072f2c31be7f0da1786be90682ec307d4e1f5303`;

2. adapter-facing interface:
   exact 4,945-byte `F1_CFC_ANCHOR_INTERFACE_MANIFEST.md`
   with SHA-256
   `b23719df7efd75dc4d53b33808377e1002a044a88acc5354defd06dc59829184`.

This acceptance means only that the nominated baseline identity and maximum permitted controller-facing surface satisfy the signed-F0 F1 review requirement.

It does **not**:
- approve any F2 adapter implementation;
- establish neutral-schema compatibility;
- establish real authority availability;
- establish that complete- or missing-authority feasibility will pass;
- authorize substantive execution;
- freeze v0.2 protocol/M1/A1/I1;
- authorize eligibility, seeds or selection.

## 6. Bilateral F1 acceptance condition

Signed F0 requires both parties to explicitly accept one exact baseline identity and one exact adapter-facing interface contract.

RIDI has now done so.

Before F2 begins, CFC should explicitly confirm the same two exact identities:

```text
baseline_wheel_sha256 =
b3b1f11e060289afa4e7da61072f2c31be7f0da1786be90682ec307d4e1f5303

interface_manifest_sha256 =
b23719df7efd75dc4d53b33808377e1002a044a88acc5354defd06dc59829184
```

Until that exact bilateral countersign is recorded:

**NO F2 ADAPTER DEVELOPMENT.**

**F1 exact-hash acceptance before F2.**
