# CFC ↔ RIDI v0.2 — bilateral reset proposal DRAFT R2

**Status:** DRAFT FOR BILATERAL REVIEW ONLY — NOT APPROVED / NOT FROZEN / NO EXECUTION / NO NEW CASE SELECTION  
**Parent:** v0.1 pre-execution NO-GO closure remains immutable  
**Purpose:** incorporate the minimum v0.2 reset plus four additional safeguards proposed by the CFC side before any bilateral approval.

## 1. Immutable v0.1 boundary

v0.1 remains a closed historical record.

The following are not modified, reused as shortcuts, or retroactively reinterpreted:
- v0.1 protocol and annexes;
- the 800-case pool;
- both seed commitments and reveals;
- all 800 selection scores;
- selected case `RAG-nq-test1035`;
- source-recovery record;
- v0.1 pre-execution NO-GO.

v0.1 established a bounded methodological finding only: the frozen pre-execution gate prevented unsupported authority mapping from becoming an experimental result.

## 2. Validation-layer separation

v0.2 must preserve three distinct validation layers.

### V1 — Source validation

Question:

> Are the source bytes, identities, versions and declared provenance links exact and independently verifiable?

Source validation may establish:
- exact byte identity;
- immutable record/version identity;
- source existence;
- declared provenance-link integrity.

Source validation does **not** by itself establish:
- semantic support;
- decision scope;
- freshness/validity;
- dependency/common-mode status;
- independence;
- controller closure authorization.

### V2 — Adapter validation

Question:

> Does the frozen substantive adapter faithfully represent only what the permitted pre-existing evidence and authority records support?

Adapter validation must establish that the adapter:
- performs representation only;
- creates no new evidence;
- creates no semantic assertion;
- creates no authority;
- does not infer missing authority from source identity, retrieval relevance, model output or RIDI result;
- maps missing authority to the frozen explicit missing-state behavior;
- emits deterministic mapping and authority manifests;
- introduces no post-selection discretionary rule.

Adapter validation does **not** establish controller closure authorization.

### V3 — Controller closure authorization

Question:

> Given the frozen mapped evidence state, what claim state, stop type and closure/propagation authorization does the frozen CFC controller produce?

Controller authorization is a substantive controller result and may be produced only after:
- source validation passes as required;
- adapter validation passes;
- exact mapped inputs/manifests/configuration are frozen;
- the bilateral execution gate is open.

A source PASS or adapter PASS must never be reported as a CFC ALLOW/BLOCK result.

## 3. Required v0.2 work before any new pool or seed

### R1 — Nonfixture substantive CFC adapter

Create an explicit experiment-specific adapter that:
- accepts the neutral candidate/source schema;
- maps absent authority facts to the exact frozen missing-state behavior;
- executes without synthetic fixture authorities;
- preserves provenance, lineage, dependency, scope, validity and independence unknowns honestly;
- emits the machine-readable M1 mapping manifest required by the protocol;
- has no access to expected CFC/RIDI outcomes;
- has no case-specific special rules.

#### R1 safeguard — representation-only proof

Before freeze, the adapter must pass explicit tests demonstrating that it:
1. copies/transforms only permitted pre-existing fields under frozen rules;
2. cannot invent evidence records;
3. cannot generate semantic-support assertions;
4. cannot promote source identity/retrieval metadata/model output into authority;
5. cannot create or upgrade authority records;
6. maps unknown or unavailable authority exactly to `NOT_SUPPLIED`, `UNRESOLVED`, or `MAPPING_NOT_EVALUABLE` as frozen.

The representation-only test suite and adapter exact bytes/hash must be public and frozen before any new case selection.

### R2 — Authority-schema applicability and binding

Before selection, define each accepted authority class and its exact acceptance rule.

For every authority record accepted by v0.2, the frozen schema must include:
- authority-record ID;
- issuer/source;
- immutable source/version reference;
- content hash where available;
- provenance of the authority record itself;
- authority class;
- applicable field(s);
- applicability scope;
- decision-context binding rule;
- evidence-state binding rule;
- validity/freshness rule if applicable;
- dependency/lineage implications if applicable;
- validation method;
- explicit failure/missing behavior.

An authority record is usable only when its pre-frozen applicability and binding rules mechanically match the relevant evidence state.

No post-selection authority creation, reinterpretation, scope expansion or binding repair is permitted.

If an authority class has no qualifying pre-existing record, the frozen behavior must be explicit:
`NOT_SUPPLIED`, `UNRESOLVED`, or `MAPPING_NOT_EVALUABLE`.

### R3 — Two-case excluded executable dry run

Before any substantive pool is frozen, run the **actual nonfixture substantive adapter/controller path** on two excluded integration cases.

#### Dry-run A — complete-authority case

Must demonstrate:
- source validation succeeds;
- every required authority class is supplied by qualifying pre-existing records;
- adapter emits complete mapped input and manifests;
- controller executes through the exact planned substantive runner/configuration;
- output schema, errors, hashes and logs are captured.

The purpose is interface/execution validation only. The result is excluded from substantive findings.

#### Dry-run B — missing-authority case

Must demonstrate:
- source bytes may be valid while one or more authority classes are absent;
- adapter preserves absence without fixture laundering;
- missing authority flows through the exact planned substantive path as the frozen explicit state;
- the system produces the predeclared `NOT_SUPPLIED` / `UNRESOLVED` / `MAPPING_NOT_EVALUABLE` behavior as applicable;
- no synthetic authority is introduced merely to make the runner complete.

Both dry runs must use the exact adapter/controller/runner/configuration intended for the substantive experiment.

If either dry run exposes an interface or authority-schema defect:
- stop;
- revise/version;
- obtain renewed bilateral approval;
- repeat both excluded dry runs;
- do not freeze a candidate pool beforehand.

### R4 — Versioned protocol and annex freeze

Issue v0.2 versions of protocol/M1/A1/I1 only where required to describe the compliant substantive path precisely.

Every changed artifact requires:
- exact versioned bytes;
- SHA-256;
- public timestamp;
- line-by-line bilateral review;
- bilateral approval;
- explicit statement that v0.1 remains immutable.

Freeze additionally:
- substantive adapter exact bytes/hash;
- representation-only validation tests/hash;
- controller/runner/config exact identities;
- authority-schema exact bytes/hash;
- output bundle schema;
- error/no-go behavior.

No case selection is permitted before this freeze is complete.

### R5 — New eligibility criteria and gate

Define and freeze eligibility criteria **before fresh seed commitments**.

Eligibility criteria must be case-agnostic and must not use:
- desired CFC result;
- desired RIDI result;
- expected asymmetry;
- publication interest;
- prior convenience to either framework.

At minimum, each candidate must be mechanically testable for:
- required neutral source fields;
- exact source-byte availability;
- required endpoint availability for RIDI;
- applicability of the frozen evaluation definition;
- whether the frozen adapter can represent the candidate without case-specific logic;
- authority-state classification under pre-frozen rules;
- any protocol-level support-requirement restriction;
- prior public exposure.

#### R5 safeguard — frozen application

Freeze:
1. eligibility specification;
2. checker exact bytes/hash;
3. complete candidate registry;
4. audit output;
5. exact eligible-pool bytes/hash.

The entire application must be independently reproducible before any seed commitment.

No candidate may be added, removed or reclassified after seed commitment except through an explicit bilateral versioned reset.

No v0.1 selected case receives preferential inclusion or exclusion.

### R6 — Fresh bilateral commit–reveal selection

Only after v0.2 protocol/annex/adapter/dry-run/eligibility/pool freeze:
- each party creates a fresh independent seed;
- each publishes a fresh role-bound commitment;
- both commitments are recorded before either reveal;
- both seeds are revealed and independently verified;
- selection is deterministic over the exact frozen v0.2 pool;
- full case scores are preserved;
- the selected case is not substituted for convenience.

v0.1 seeds, scores and selected case are not reused.

## 4. Pre-execution gate for the v0.2 selected case

After deterministic selection and before substantive execution:

1. freeze exact neutral selected specimen bytes;
2. verify source bytes independently;
3. apply only the already-frozen adapter and authority schema;
4. CFC privately freezes exact mapped inputs and manifests;
5. RIDI freezes its permitted exact input;
6. freeze exact runner/controller/config identities;
7. exchange only the predeclared cryptographic identities/status permitted by I1;
8. verify that no post-selection authority, mapper or threshold change occurred.

Execution gate opens only if both sides explicitly record **PRE-EXECUTION PASS**.

Any failure produces a pre-execution stop, not a substantive framework result.

## 5. Independent substantive execution and raw-bundle commit

If and only if the v0.2 pre-execution gate passes:
- RIDI and CFC execute independently;
- neither side receives the other's raw result before bundle commitment;
- each side assembles one immutable raw bundle;
- each first publishes only bundle SHA-256 + byte size;
- exact bundles are exchanged only after both commitments exist;
- each bundle is independently verified before interpretation.

Ground-truth correctness remains secondary/post-commit according to I1 unless v0.2 explicitly changes and bilaterally freezes that rule.

## 6. Scientific decision objects retained

The scientific distinction remains unchanged.

**RIDI:** Does the frozen-equivalent A/B representation preserve the nominated downstream verdict/action under the frozen evaluation?

**CFC:** Does the represented evidence state authorize closure/propagation of the nominated claim under the frozen authority and controller rules?

The adapter is not a third decision-maker. It is a frozen representation layer only.

## 7. Explicit no-go / reset rules

A versioned reset is required if, after selection:
- source bytes do not verify;
- authority applicability cannot be established under the frozen schema;
- a required unknown cannot be represented faithfully;
- the adapter requires case-specific logic;
- any new authority record would need to be created;
- a mapping/threshold/inspection rule would need amendment;
- a material inspection-boundary violation occurs;
- committed raw bundles fail exact verification.

There is no quiet repair, reselection or synthetic substitution.

## 8. Non-claims

This R2 draft:
- is not bilateral approval;
- does not authorize implementation or execution;
- does not assert that a compliant nonfixture adapter already exists;
- does not guarantee that v0.2 will reach substantive execution;
- does not predict CFC or RIDI outcomes;
- does not convert the v0.1 pre-execution NO-GO into a substantive controller result.

## 9. Proposed approval order

Before v0.2 may be labeled FROZEN, approve in this order:

1. validation-layer separation V1–V3;
2. R1 adapter contract + representation-only safeguards;
3. R2 authority schema + provenance/scope/binding requirements;
4. R3 two-case excluded dry-run design;
5. R4 versioned protocol/annex/implementation freeze package;
6. R5 eligibility criteria/checker/registry/pool procedure;
7. R6 fresh commit–reveal procedure;
8. pre-execution gate;
9. raw-bundle commitment/exchange procedure;
10. reset/no-go rules and non-claims.

**Draft before freeze. Freeze before eligibility. Eligibility before selection. Evidence before execution.**
