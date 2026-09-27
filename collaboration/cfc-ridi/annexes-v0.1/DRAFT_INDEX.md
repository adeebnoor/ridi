# CFC ↔ RIDI Annex Drafts v0.1

**Status: DRAFT — NOT FROZEN**

These annexes implement the pre-selection freeze gate required by the frozen Shared Case Protocol v0.1.

## Current draft identities

- `M1_Generic_CFC_Mapper_v0.1_DRAFT.md` — 7116 bytes — SHA-256 `7adc4229277280acf9f48528a74ace7df9ba28ac1295e30ced318a7c1a3ee858`
- `A1_Authority_Policy_v0.1_DRAFT.md` — 5848 bytes — SHA-256 `86f8b73bbb7e6f59aea95f2f388d15b78c3cda2d9ffc5190336b3e5a4ca64be9`
- `I1_Inspection_Matrix_v0.1_DRAFT.md` — 5250 bytes — SHA-256 `2f3a86e6e9e4b32633813bc2bd82dd2e04f55d7a643ca32780a78b997c01ae4b`

## Clarifications incorporated after Krzysztof review

1. A source case with an authoritative support requirement greater than one is ineligible for the first one-support experiment; it is not silently weakened.
2. The run is explicitly not fully blinded because both sides may see recorded A/B verdicts/actions; protection is independent execution, output sequestration and mandatory hash commitments.
3. RIDI selected identity is explicitly distinct from CFC evidence-record identity and cannot create authority or independence.
4. Applying a pre-frozen authority rule to an already existing permitted record after selection is allowed; creating a new discretionary authority assertion is not.
5. The excluded mechanical dry run must verify the frozen CFC path can execute the one-support configuration, with synthetic authority confined to the excluded dry run.

No substantive case has been selected. No selection seed has been created. No substantive shared run has been executed.
