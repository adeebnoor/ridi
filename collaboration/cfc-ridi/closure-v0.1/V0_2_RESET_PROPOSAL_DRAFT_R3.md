# CFC ↔ RIDI v0.2 — bilateral reset proposal DRAFT R3

**Status:** DRAFT FOR BILATERAL REVIEW ONLY — NOT APPROVED / NOT FROZEN / NO IMPLEMENTATION AUTHORIZATION / NO EXECUTION / NO NEW ELIGIBILITY RUN / NO NEW CASE SELECTION  
**Parent:** v0.1 pre-execution NO-GO closure remains immutable  
**Supersedes for review:** DRAFT R2 only; does not supersede any frozen v0.1 artifact  
**Purpose:** prevent recurrence of the v0.1 failure by requiring executable feasibility, frozen authority/data universes and end-to-end rehearsal before any v0.2 approval or substantive pool.

## 1. Immutable v0.1 boundary

v0.1 remains a closed historical record.

The following remain immutable and are not reused as shortcuts:
- v0.1 protocol and annexes;
- the 800-case pool;
- both seed commitments and reveals;
- all 800 selection scores;
- selected case `RAG-nq-test1035`;
- source-recovery record;
- v0.1 pre-execution NO-GO.

v0.1 established a bounded methodological finding only: the frozen pre-execution gate prevented unsupported authority mapping from becoming an experimental result.

## 2. Validation-layer separation

v0.2 preserves four distinct layers.

### V0 — Implementation feasibility

Question:

> Does one exact controller baseline plus one exact nonfixture adapter/runner path actually support the states that the proposed protocol intends to admit?

V0 must be demonstrated before bilateral protocol approval.

V0 is not a source-validation result, adapter-validation result on a substantive candidate, or controller verdict.

### V1 — Source validation

Question:

> Are the source bytes, identities, versions and declared provenance links exact and independently verifiable?

Source validation may establish:
- exact byte identity;
- immutable record/version identity;
- source existence;
- declared provenance-link integrity.

Source validation does **not** establish:
- semantic support;
- decision scope;
- freshness/validity;
- dependency/common-mode status;
- independence;
- adapter correctness;
- controller closure authorization.

### V2 — Adapter validation

Question:

> Does the frozen substantive adapter faithfully represent only what the frozen permitted evidence and authority universes support?

Adapter validation must establish that the adapter:
- performs representation only;
- creates no new evidence;
- creates no semantic assertion;
- creates no authority;
- does not infer missing authority from source identity, retrieval relevance, model output or RIDI result;
- applies only frozen authority records/rules;
- maps missing authority to the exact frozen missing-state behavior;
- emits deterministic mapping and authority manifests;
- introduces no post-selection discretionary rule.

Adapter validation does not establish controller closure authorization.

### V3 — Controller closure authorization

Question:

> Given the frozen mapped evidence state, what claim state, stop type and closure/propagation authorization does the frozen CFC controller produce?

V3 is substantive and may occur only after the selected-case pre-execution gate passes.

A V1 PASS or V2 PASS must never be reported as CFC ALLOW/BLOCK.

## 3. Phase F — mandatory feasibility package before bilateral approval

**No v0.2 protocol or annex may be bilaterally approved or frozen until Phase F passes.**

### F1 — Exact controller-baseline choice

Before adapter design is accepted, CFC must nominate exactly one controller baseline for v0.2 and freeze its identity for review.

The nomination must include:
- version/name;
- repository commit/tag or immutable release reference;
- source/package/wheel SHA-256 as applicable;
- public API/interface contract used by the adapter;
- relevant controller configuration defaults;
- known representability/reachability limitations relevant to this experiment.

The parties must explicitly agree whether v0.2 uses:
- frozen CFC Anchor `0.2.90rc1`;
- frozen CFC-next `0.3.0a2`; or
- another separately versioned and frozen baseline.

There is no post-dry-run or post-selection controller-version switch.

Existing facts are not silently generalized:
- the v0.1 custom-case path used synthetic trust fixtures;
- CFC Anchor 0.2.90rc1 has documented public-surface reachability boundaries for some decision-accounting states;
- CFC-next 0.3.0a2 is separately frozen but its freeze alone does not prove suitability for the RIDI experiment.

### F2 — Candidate nonfixture adapter implementation

Before protocol approval, CFC must provide a reviewable candidate substantive adapter implementation, not merely an adapter specification.

It must:
- accept the intended neutral source schema;
- use the nominated F1 controller baseline;
- contain no synthetic verifier/fixture path for substantive use;
- contain no case-ID-specific logic;
- have no access to expected CFC/RIDI outcomes;
- emit deterministic mapping/authority manifests;
- expose explicit failure modes.

Exact adapter bytes and test bytes are hashed for review. These are candidate feasibility artifacts, not yet the final frozen v0.2 implementation.

### F3 — Representation-only adversarial tests

The candidate adapter must pass tests proving that it cannot:
1. invent evidence;
2. invent or upgrade semantic support;
3. create authority records;
4. treat retrieval grades/ranks/model verdict/RIDI output as authority;
5. infer independence from distinct identifiers;
6. erase known lineage/dependencies;
7. broaden authority scope or applicability;
8. replace unavailable authority with fixture/synthetic verification;
9. silently coerce an unrepresentable state into a representable one.

Tests must include malformed, missing, contradictory and out-of-scope authority inputs.

### F4 — Frozen candidate authority universe for feasibility

Before the feasibility dry runs, define the exact pre-existing authority universe the candidate adapter is allowed to consult.

The feasibility authority universe must be:
- pre-existing;
- content-addressed or immutably referenced;
- independently inspectable;
- versioned/snapshotted;
- hashable as an exact manifest/corpus;
- separated from the substantive v0.2 authority-universe freeze in Phase A below.

No authority record may be created merely to make a feasibility case pass.

### F5 — Two nonfixture feasibility executions

Using the exact F1 baseline and F2 adapter:

**F5-A complete-authority case**
- same neutral schema class intended for substantive use;
- all required authority records pre-exist in F4;
- source validation succeeds;
- adapter produces complete mapped inputs/manifests;
- exact controller runner executes;
- logs, inputs, manifests and outputs are captured.

**F5-B missing-authority case**
- same neutral schema class;
- at least one required authority record is genuinely absent from F4;
- adapter must not synthesize or repair the missing authority;
- the exact path must demonstrate one of two predeclared outcomes:
  - **EXECUTABLE_MISSING_AUTHORITY**: the controller accepts the faithfully represented unknown state and produces a controller result; or
  - **MAPPING_NOT_EVALUABLE**: the state cannot be faithfully represented/executed under the nominated interface.

The outcome class itself must be fixed before substantive eligibility rules are written.

### F6 — Feasibility decision

Phase F passes only if both parties agree, from exact artifacts, that:
- a substantive nonfixture path exists;
- complete-authority execution works;
- missing-authority handling is known and deterministic;
- no synthetic authority is required;
- the controller baseline will not change after this point without reset.

If F5-B yields `MAPPING_NOT_EVALUABLE`, v0.2 may continue only if the future eligibility rules **exclude that unrepresentable authority-state class before pool freeze and before seeds**.

If the intended scientific design requires missing-authority cases to be substantively executable, F5-B must instead demonstrate `EXECUTABLE_MISSING_AUTHORITY`; otherwise v0.2 stops before protocol approval.

**Failure of Phase F ends the reset attempt without pool construction or seed generation.**

## 4. Phase A — authority and source universes before protocol freeze

### A1 — Source universe availability

Before substantive eligibility:
- identify the exact source corpus/corpora from which candidate specimens are derived;
- freeze exact hashes/manifests or durable immutable references;
- independently demonstrate that all bytes needed for any candidate can be retrieved **before** selection.

A source that can be identified only after selection is not acceptable.

This rule exists to prevent recurrence of the v0.1 post-selection source-recovery HOLD.

### A2 — Substantive authority universe freeze

Before substantive eligibility, freeze the exact universe of authority records that the substantive adapter may consult.

Freeze:
- authority corpus/snapshot manifest;
- immutable record IDs/versions;
- content hashes where available;
- issuer/source provenance;
- authority class;
- applicability scope;
- evidence-state binding fields;
- decision-context binding fields;
- validity/freshness metadata;
- dependency/lineage implications;
- validation method.

The universe may use public content-addressed references instead of embedding all bytes, but every permitted record must be fixed by an immutable identity before eligibility.

**No authority fishing after selection.**

A post-selection search for a new authority record, even from an otherwise permitted source, is prohibited unless that exact record was already included or deterministically addressable within the frozen authority universe and the lookup rule was frozen.

### A3 — Authority-schema acceptance rule

For every authority class, freeze:
- acceptance criteria;
- applicability test;
- binding test;
- conflict rule;
- missing rule;
- failure rule.

An authority record is usable only when the frozen rules mechanically bind it to the relevant evidence state.

## 5. Phase D — excluded end-to-end rehearsal before substantive eligibility

After Phase F and Phase A, but before substantive candidate eligibility/pool freeze, run an excluded bilateral rehearsal.

### D1 — CFC path

Repeat:
- one complete-authority case;
- one missing-authority case compatible with the Phase F decision;

using the **final proposed** adapter/controller/authority-universe versions.

### D2 — RIDI path

Using excluded cases from the same neutral schema:
- freeze exact RIDI inputs;
- run the exact RIDI runner intended for substantive use;
- build the exact raw-bundle schema;
- record logs/errors/version IDs.

### D3 — Bundle-commit plumbing rehearsal

For at least one excluded case:
- each side builds one immutable raw ZIP bundle;
- each publishes only SHA-256 + byte size first;
- after both commitments, exchange exact ZIPs;
- independently verify hashes;
- confirm that prohibited pre-commit fields were not exposed;
- confirm that interpretation begins only after verification.

Dry-run substantive outputs are excluded from all substantive findings.

### D4 — Rehearsal failure

Any adapter/controller/runner/bundle/interface defect triggers:
- stop;
- versioned repair;
- new exact hashes;
- repeat of the affected Phase F/A/D checks;
- no candidate pool exists yet, so there is nothing to preserve for convenience.

## 6. Phase P — versioned protocol and implementation freeze

Only after F, A and D all pass may the parties bilaterally approve and freeze v0.2.

Freeze exact identities for:
- protocol v0.2;
- M1 v0.2;
- A1 v0.2;
- I1 v0.2;
- selected controller baseline;
- substantive adapter;
- adapter validation suite;
- authority schema;
- substantive authority universe manifest;
- source-universe manifest;
- CFC runner/config;
- RIDI runner/config;
- raw-bundle schemas;
- error/no-go semantics;
- excluded rehearsal records.

Every artifact receives:
- version;
- exact bytes or immutable reference;
- SHA-256 where applicable;
- public timestamp;
- bilateral approval.

## 7. Phase E — substantive eligibility gate

Eligibility is defined and applied **only after Phase P freeze** and before fresh seed commitments.

### E1 — case-agnostic criteria

Criteria must not use:
- desired CFC result;
- desired RIDI result;
- expected asymmetry;
- publication interest;
- convenience to either framework;
- v0.1 selected-case status.

### E2 — per-candidate mechanical classification

For every candidate, the checker must classify at least:

- source bytes: AVAILABLE / NOT_AVAILABLE;
- RIDI endpoint/evaluation: APPLICABLE / NOT_APPLICABLE;
- neutral schema: VALID / INVALID;
- adapter representation: REPRESENTABLE / NOT_REPRESENTABLE;
- authority state under the frozen universe:
  - COMPLETE_AUTHORITY;
  - EXECUTABLE_MISSING_AUTHORITY;
  - UNREPRESENTABLE_MISSING_AUTHORITY;
  - CONFLICTING_AUTHORITY;
  - other predeclared class if bilaterally frozen;
- support-requirement status;
- prior public exposure.

### E3 — eligibility must follow Phase F missing-authority capability

If F5-B established only `MAPPING_NOT_EVALUABLE` for missing-authority states, then all `UNREPRESENTABLE_MISSING_AUTHORITY` candidates are ineligible **before seed commitments**.

If F5-B established `EXECUTABLE_MISSING_AUTHORITY`, the protocol must explicitly state whether that class is eligible; the decision is frozen before checker execution.

No candidate is selected first and tested for representability later.

### E4 — complete frozen application

Freeze:
1. eligibility specification;
2. checker exact bytes/hash;
3. complete candidate registry;
4. exact authority/source references used for classifications;
5. audit output;
6. exact eligible-pool bytes/hash.

The application must be independently reproducible before any seed commitment.

If the eligible pool is empty or below a bilaterally predeclared minimum, record NO-GO and stop. Do not weaken criteria.

## 8. Phase S — fresh bilateral commit–reveal

Only after the exact Phase E pool is frozen and independently reproduced:
- generate fresh seeds;
- publish fresh role-bound commitments;
- record both before reveal;
- reveal and independently verify both;
- deterministically score all frozen case IDs;
- preserve all scores;
- select exactly one case under the frozen rule.

v0.1 seeds, scores and selected case are not reused.

## 9. Selected-case pre-execution gate

After selection and before substantive execution:

1. extract and freeze exact neutral selected-specimen bytes;
2. reverify source bytes against the already-frozen source universe;
3. bind authority only from the already-frozen authority universe;
4. apply only the frozen adapter and authority rules;
5. CFC privately freezes exact mapped inputs/manifests;
6. RIDI freezes exact permitted input;
7. freeze/reverify exact runner/controller/config identities;
8. exchange only predeclared hashes/status permitted by I1;
9. verify no post-selection authority search, adapter edit, controller switch or threshold change occurred.

Because source/authority/representability were already checked during Phase E, this gate is a **reverification**, not first discovery.

Execution opens only when both sides record `PRE_EXECUTION_PASS`.

Any mismatch produces a pre-execution stop; it is not a substantive CFC/RIDI result.

## 10. Independent execution and raw-bundle commitment

If and only if the selected-case gate passes:
- CFC and RIDI execute independently;
- neither side receives the other's raw result before commitment;
- each assembles one immutable raw bundle;
- each publishes bundle SHA-256 + exact byte size only;
- after both commitments, exact bundles are exchanged;
- each verifies exact bytes/hashes;
- only then may either side inspect the other's raw result and author interpretation.

## 11. Scientific decision objects

**RIDI:** Does the frozen-equivalent A/B representation preserve the nominated downstream verdict/action under the frozen evaluation?

**CFC:** Does the represented evidence state authorize closure/propagation of the nominated claim under the frozen authority and controller rules?

The adapter is a representation layer only, not a decision-maker or authority generator.

## 12. Controller-version rule

The F1 controller baseline remains fixed through:
- feasibility;
- rehearsal;
- protocol freeze;
- eligibility;
- selection;
- pre-execution;
- substantive execution;
- raw-bundle creation.

A new CFC version, even if superior or newly frozen, requires a new versioned reset.

## 13. Explicit no-go/reset rules

Stop and version-reset if:
- Phase F cannot demonstrate the intended state class;
- source/authority universes cannot be frozen before eligibility;
- adapter requires synthetic or case-specific authority;
- adapter/controller version changes;
- dry-run bundle plumbing fails;
- eligibility is not independently reproducible;
- selected-case reverification differs from eligibility classification;
- a new authority record/search is required after selection;
- a material I1 violation occurs;
- raw bundle exact verification fails.

No quiet repair, synthetic substitution, outcome-driven eligibility edit or reselection.

## 14. Non-claims

This R3 draft:
- is not bilateral approval;
- does not authorize adapter implementation on behalf of the other party;
- does not authorize eligibility checking, seed generation, selection or execution;
- does not nominate CFC Anchor 0.2.90rc1 or CFC-next 0.3.0a2 as the v0.2 controller;
- does not claim a compliant adapter currently exists;
- does not guarantee that v0.2 will reach substantive execution;
- does not predict CFC/RIDI results;
- does not convert v0.1 NO-GO into a framework-performance result.

## 15. Approval order

There is deliberately **no protocol approval before feasibility**.

Order:

1. F1 controller-baseline nomination/review;
2. F2 candidate nonfixture adapter implementation;
3. F3 representation-only adversarial tests;
4. F4 feasibility authority-universe snapshot;
5. F5 dual authority-state feasibility executions;
6. F6 bilateral feasibility decision;
7. A1 source-universe availability freeze;
8. A2/A3 substantive authority-universe/schema freeze;
9. D1–D3 end-to-end excluded bilateral rehearsal;
10. only then: P protocol/annex/implementation bilateral freeze;
11. E eligibility specification/application/pool freeze;
12. S fresh commit–reveal selection;
13. selected-case pre-execution reverification;
14. independent substantive execution;
15. raw-bundle commitments/exchange/verification;
16. interpretation.

**Prove the path before freezing the experiment. Freeze evidence universes before eligibility. Eligibility before selection. Evidence before execution.**
