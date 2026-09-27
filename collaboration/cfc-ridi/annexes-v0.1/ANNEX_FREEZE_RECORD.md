# CFC ↔ RIDI Annexes v0.1 — Bilateral Freeze Record

**Status:** FROZEN  
**Freeze date:** 2026-09-28  
**Parent protocol:** CFC ↔ RIDI Shared Case Protocol v0.1  
**Protocol SHA-256:** `d6bc94e90be4ac01bd8ee60f32aa3045dd827f4f3e9e64a68b82191615138571`

## Frozen annex artifacts

- **M1 — Generic CFC Mapper v0.1**  
  SHA-256: `7adc4229277280acf9f48528a74ace7df9ba28ac1295e30ced318a7c1a3ee858`

- **A1 — Authority Policy v0.1**  
  SHA-256: `86f8b73bbb7e6f59aea95f2f388d15b78c3cda2d9ffc5190336b3e5a4ca64be9`

- **I1 — Inspection Matrix v0.1**  
  SHA-256: `2f3a86e6e9e4b32633813bc2bd82dd2e04f55d7a643ca32780a78b997c01ae4b`

## Bilateral approvals

**Krzysztof Sliwka:** independently reviewed the updated annexes from the public RIDI branch, independently verified their SHA-256 hashes against the draft index, and formally approved the exact hashes above for bilateral freeze.

**Adeeb Noor:** approves the same exact annex bytes and hashes for freeze with no further substantive changes.

## Clarifications frozen into the annexes

1. Cases with an authoritative original support requirement greater than one are ineligible for the bounded first one-support experiment; the source requirement is not silently weakened.
2. The experiment is not described as fully blinded. It uses independent execution, output sequestration and mandatory raw-bundle hash commitments, while acknowledging overlap in access to recorded A/B verdict/action values.
3. RIDI selected identity is distinct from CFC evidence-record identity and cannot itself establish CFC authority or independence.
4. Pre-frozen authority rules may be applied mechanically after case selection to already-existing permitted records; new discretionary authority assertions after learning the selected case are prohibited.
5. The excluded mechanical dry run must confirm that the frozen CFC path executes the one-support configuration, with synthetic/fixture authority confined strictly to that excluded dry run.

## State at annex freeze

- No substantive case has been selected.
- No substantive selection seed has been created or revealed.
- No substantive shared run has been executed.
- The next permitted step is the explicitly excluded mechanical dry run.
- Synthetic/fixture authority is allowed only in that excluded dry run and has no authority in the substantive run.

Any byte-level modification to M1, A1 or I1 requires a new version, new hashes and renewed bilateral approval.
