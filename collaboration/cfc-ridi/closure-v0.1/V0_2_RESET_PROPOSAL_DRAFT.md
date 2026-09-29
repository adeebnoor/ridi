# CFC ↔ RIDI v0.2 — bilateral reset proposal DRAFT

**Status:** DRAFT FOR DISCUSSION ONLY — NOT APPROVED / NOT FROZEN / NO NEW CASE SELECTION

This document proposes the minimum changes required to make a future substantive CFC ↔ RIDI execution faithfully runnable without weakening the v0.1 evidence discipline.

## Reset trigger

v0.1 stopped because the selected neutral specimen and original source bytes were available, but the available frozen CFC substantive execution path could not produce an authorized mapped input under M1/A1 without relying on synthetic fixture authorities.

## Required v0.2 work before any new pool or seed

### R1 — Nonfixture substantive CFC adapter
Create an explicit experiment-specific adapter that:
- accepts the neutral selected-case/source schema;
- maps absent authority facts to `NOT_SUPPLIED` / `UNRESOLVED`;
- does not require synthetic verifier fixtures to execute;
- preserves provenance, lineage, dependency and scope unknowns honestly;
- emits the machine-readable M1 mapping manifest required by the protocol.

The adapter must be frozen by exact bytes/hash before any new case selection.

### R2 — Authority-schema applicability
Define, before selection, which already-existing records may support:
- semantic support;
- validity/freshness;
- decision scope;
- provenance/lineage;
- dependency/common mode;
- independence.

If a class has no pre-existing authoritative evidence, the frozen behavior must be explicit: `NOT_SUPPLIED`, `UNRESOLVED`, or `MAPPING_NOT_EVALUABLE`. No post-selection authority creation.

### R3 — Executable interface test
Before any new substantive pool:
- perform a mechanical excluded dry run through the exact nonfixture substantive adapter/controller path;
- demonstrate that required unknowns can be represented without fixture laundering;
- freeze runner/config/controller/adapter hashes;
- record exact expected output schema and error behavior.

### R4 — Annex revision
Issue versioned M1/A1/I1 v0.2 only if needed to describe the compliant adapter/interface precisely.

Any change requires:
- exact new artifact bytes;
- new SHA-256 values;
- bilateral line-by-line approval;
- explicit supersession statement that v0.1 remains immutable.

### R5 — New eligibility gate
The future candidate pool must be rebuilt/rechecked under v0.2 if the revised executable/authority requirements affect case evaluability.

No previously selected v0.1 case receives preferential treatment.

### R6 — New commit–reveal selection
Only after v0.2 protocol/annex/adapter/dry-run/pool freeze:
- create fresh independent seeds;
- publish fresh commitments;
- reveal only after both commitments;
- select a new case deterministically.

The v0.1 seeds, selected case and scores must not be reused as a v0.2 shortcut.

## Research question retained

The scientific distinction remains:

- RIDI: does the frozen-equivalent A/B representation preserve the nominated downstream verdict/action?
- CFC: does the represented evidence state authorize closure/propagation of the nominated claim?

v0.2 should enable both questions to be executed without changing either question after selection.

## Non-claim

This draft does not assert that a compliant adapter can necessarily be built, that v0.2 will execute, or that either framework will produce an asymmetric result.

**Draft before reset. Freeze before selection.**
