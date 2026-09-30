# CFC ↔ RIDI v0.2 reset proposal — R1 → R2 review map

**Status:** REVIEW AID ONLY — R2 REMAINS DRAFT / NOT APPROVED / NOT FROZEN

This file maps the four CFC-side safeguards proposed after review of the original v0.2 reset draft into DRAFT R2.

## CFC safeguard 1
> The substantive adapter must perform representation only, without generating new evidence, semantic assertions or authority.

**R2 incorporation**
- Section 2, V2 — Adapter validation.
- Section 3, R1 — Nonfixture substantive CFC adapter.
- R1 safeguard — representation-only proof.

R2 now requires explicit tests showing that the adapter cannot invent evidence, semantic support or authority and cannot upgrade missing authority from retrieval/model/RIDI fields.

## CFC safeguard 2
> Each accepted authority record should have explicit provenance, applicability scope and binding to the relevant evidence state.

**R2 incorporation**
- Section 3, R2 — Authority-schema applicability and binding.

R2 now requires authority-record provenance, immutable source/version, authority class, applicable field(s), applicability scope, decision-context binding, evidence-state binding, validation rule and explicit missing/failure behavior.

## CFC safeguard 3
> The excluded dry run should cover both a complete-authority case and a missing-authority case through the actual substantive adapter/controller path.

**R2 incorporation**
- Section 3, R3 — Two-case excluded executable dry run.

R2 now requires:
- Dry-run A: complete-authority path;
- Dry-run B: missing-authority path;
- both through the exact intended substantive adapter/controller/runner/configuration;
- both repeated after any versioned fix.

## CFC safeguard 4
> The new eligibility criteria and their application must be frozen before fresh seed commitments, without favouring cases convenient for either framework.

**R2 incorporation**
- Section 3, R5 — New eligibility criteria and gate.
- R5 safeguard — frozen application.
- Section 3, R6 — Fresh bilateral commit–reveal selection.

R2 explicitly prohibits outcome-, asymmetry-, publication- or framework-convenience-based eligibility and requires frozen criteria/checker/registry/audit/pool before seed commitments.

## Additional CFC distinction
> Preserve the distinction between adapter validation, source validation and controller closure authorization.

**R2 incorporation**
- New Section 2 — Validation-layer separation:
  - V1 Source validation;
  - V2 Adapter validation;
  - V3 Controller closure authorization.

R2 explicitly states that source PASS ≠ adapter PASS ≠ CFC ALLOW/BLOCK.

## v0.1 preservation

No v0.1 artifact is amended by R2.

R2 remains a proposal only. No implementation, new eligibility evaluation, seed generation, case selection or execution is authorized until bilateral approval and freeze.

**Review the changes before approval.**
