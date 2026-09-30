# CFC ↔ RIDI v0.2 — bilateral reset proposal DRAFT R4

**Status:** PRE-SEND DRAFT R5 FOR BILATERAL REVIEW — NOT APPROVED / NOT FROZEN / NO IMPLEMENTATION AUTHORIZATION / NO ELIGIBILITY RUN / NO SEED / NO SELECTION / NO EXECUTION  
**Parent:** v0.1 pre-execution NO-GO closure remains immutable  
**Supersedes for review:** DRAFT R4 only; no frozen v0.1 artifact is changed  
**Purpose:** require executable feasibility, frozen evidence universes, exposure controls and end-to-end rehearsal before any v0.2 experimental freeze.

## 1. Immutable v0.1 boundary

v0.1 remains closed and immutable.

The following are historical records only:
- v0.1 protocol and M1/A1/I1;
- v0.1 800-case pool;
- both v0.1 seed commitments/reveals;
- all v0.1 selection scores;
- selected case `RAG-nq-test1035`;
- exact source recovery;
- v0.1 pre-execution NO-GO.

v0.1 established a bounded methodological finding: the pre-execution gate prevented unsupported authority mapping from becoming an experimental result.

It did **not** produce a substantive CFC or RIDI result.

## 2. Four validation layers

### V0 — Implementation feasibility
Can one exact controller baseline plus one exact nonfixture adapter/runner path actually represent and execute the authority-state classes the proposed experiment intends to admit?

V0 must pass before bilateral protocol approval.

### V1 — Source validation
Are source bytes/identities/versions exact and independently verifiable?

V1 may establish source existence and exact identity. It does not establish semantic support, scope, validity, dependency, independence, adapter correctness or controller authorization.

### V2 — Adapter validation
Does the frozen adapter represent only what the frozen permitted evidence/authority universes support?

V2 must prove representation only: no evidence generation, no semantic assertion generation, no authority generation or upgrade, no post-selection discretion.

### V3 — Controller closure authorization
Given a frozen mapped evidence state, what claim state, stop type and closure/propagation authorization does the exact frozen controller produce?

V3 is substantive and occurs only after selected-case pre-execution PASS.

**V1 PASS ≠ V2 PASS ≠ V3 ALLOW/BLOCK.**

## 3. Exposure firewall

To avoid adapter tuning or evaluation contamination:

1. `RAG-nq-test1035` is permanently excluded from the v0.2 substantive pool.
2. Every case used in:
   - adapter development;
   - adapter validation;
   - feasibility testing;
   - complete-authority rehearsal;
   - missing-authority rehearsal;
   - RIDI plumbing rehearsal;
   - bundle-commit rehearsal;
   is permanently marked **CALIBRATION/EXCLUDED** for v0.2 substantive selection.
3. Calibration-case IDs and hashes are frozen before substantive eligibility.
4. No substantive candidate may be moved into calibration after eligibility begins unless the entire eligibility/pool phase resets before seeds.
5. Prior exposure for all remaining candidates is recorded.

This exclusion is procedural contamination control, not an outcome-based exclusion.

## 4. Phase F — mandatory implementation feasibility before bilateral approval

**No v0.2 protocol, annex, pool or seed may be approved/frozen before Phase F passes.**

### F0 — Bilateral feasibility-workplan sign-off

Before either party spends implementation effort on v0.2, both sides must first approve a **feasibility workplan only** covering:
- the F1 controller-baseline candidates to be considered;
- the required neutral schema class;
- representation-only acceptance criteria;
- the authority classes to be tested;
- the two calibration-case requirements;
- the prohibited synthetic/private-bypass mechanisms;
- the artifacts/hashes/logs expected from Phase F.

F0 is not protocol approval, annex approval, controller selection, eligibility approval, or execution authorization. It exists to prevent either side from implementing against assumptions the other side has not agreed to.

If F0 is not agreed, no adapter implementation work is treated as part of v0.2.

### F1 — Exact controller-baseline nomination

CFC nominates exactly one controller baseline, including:
- version/name;
- immutable repository/release reference;
- exact source/package/wheel SHA-256 as applicable;
- public adapter-facing API contract;
- controller defaults relevant to the experiment;
- known representability/reachability limitations.

The parties explicitly decide whether the baseline is frozen CFC Anchor `0.2.90rc1`, frozen CFC-next `0.3.0a2`, or another separately frozen version.

Known implementation facts are not silently generalized:
- the existing custom-case runner uses synthetic case-scoped trust fixtures;
- CFC Anchor 0.2.90rc1 has documented public-surface reachability boundaries for some decision-accounting states;
- CFC-next 0.3.0a2 is separately frozen, but that freeze alone does not demonstrate a nonfixture RIDI adapter.

No controller-version switch is allowed after F1 without resetting Phase F.

### F2 — Candidate nonfixture substantive adapter

Before protocol approval, CFC provides a reviewable candidate implementation that:
- accepts the intended neutral schema class;
- uses the exact F1 controller;
- has no synthetic verifier/fixture route for substantive execution;
- contains no case-ID-specific logic;
- has no access to expected CFC/RIDI results;
- emits deterministic mapping and authority manifests;
- exposes explicit errors/no-go states;
- cannot invoke an alternate controller path;
- uses only the adapter-facing API/interface explicitly declared under F1;
- does not monkeypatch the controller, inject private runtime state, or call an unapproved private/internal authorization path unless that exact interface is itself explicitly versioned, frozen and bilaterally accepted as part of F1.

Exact candidate adapter/test bytes are hashed for review.

### F3 — Representation-only adversarial suite

Tests must prove the adapter cannot:
1. invent evidence;
2. invent/upgrade semantic support;
3. create/upgrade authority;
4. treat retrieval rank/grade/metric, model output or RIDI result as authority;
5. infer independence from distinct-looking IDs;
6. erase known lineage/dependencies;
7. broaden scope/applicability;
8. replace missing authority with fixture/synthetic verification;
9. coerce an unrepresentable state into a representable one;
10. switch controller/config based on case content.

Include malformed, missing, contradictory, stale and wrong-scope inputs.

### F4 — Feasibility authority universe

Before feasibility execution, identify an exact pre-existing authority universe:
- content-addressed/immutably referenced;
- versioned/snapshotted;
- independently inspectable by the party/role permitted under the proposed inspection boundary;
- exact manifest/hash recorded.

No authority record may be created to make a calibration case pass.

### F5 — Two real nonfixture feasibility cases

Both use the same neutral schema class intended for substantive v0.2 and are permanently excluded by Section 3.

**F5-A complete-authority**
- required source records exist;
- all required authority records pre-exist in F4;
- adapter emits complete mappings/manifests;
- exact F1 controller executes through the intended substantive runner/config.

**F5-B missing-authority**
- required source exists;
- at least one required authority class is genuinely absent from F4;
- adapter does not synthesize/repair it;
- exact path demonstrates one predeclared class:
  - `EXECUTABLE_MISSING_AUTHORITY`; or
  - `MAPPING_NOT_EVALUABLE`.

The class must be known before substantive eligibility rules are written.

### F6 — Feasibility decision

Phase F passes only if both parties agree from exact artifacts that:
- a substantive nonfixture path exists;
- complete-authority execution works;
- missing-authority behavior is deterministic and known;
- no synthetic trust is needed;
- controller and adapter identities are fixed for the next phases.

If F5-B = `MAPPING_NOT_EVALUABLE`, that authority-state class must be excluded by substantive eligibility before seeds.

If the intended scientific design requires missing-authority cases to execute, F5-B must instead demonstrate `EXECUTABLE_MISSING_AUTHORITY`; otherwise stop before protocol approval.

## 5. Phase A — freeze source, authority, temporal and decision-context universes

### A1 — Durable source universe

Before substantive eligibility:
- identify every source corpus from which candidates can be derived;
- freeze exact manifest/hashes or immutable content-addressed references;
- prove all bytes needed for every possible candidate are retrievable before selection.

**Temporary expiring shares alone are not sufficient.**

At least one durable route must exist for the duration of the experiment, e.g.:
- commit-pinned Git object/LFS;
- DOI/archive deposit;
- immutable object store;
- exact-byte public mirror with hash.

This prevents another post-selection source-recovery HOLD.

### A2 — Substantive authority universe

Before eligibility, freeze the exact universe the adapter may consult.

For each permitted authority record freeze:
- immutable ID/version;
- content hash where available;
- issuer/source provenance;
- authority class;
- applicability scope;
- evidence-state binding fields;
- decision-context binding fields;
- validity/freshness metadata;
- dependency/lineage implications;
- validation method.

No post-selection authority fishing.

A record not fixed or deterministically addressable under the frozen manifest/rule before eligibility is unavailable for v0.2.

### A3 — Authority acceptance rules

For each authority class freeze:
- acceptance rule;
- applicability test;
- binding test;
- conflict rule;
- missing rule;
- validation/failure rule.

### A4 — Temporal reference freeze

Before eligibility freeze:
- exact decision/evaluation `as_of` semantics;
- timezone/date representation;
- validity/freshness cutoff rule;
- handling of undated records;
- prohibition on substituting file modification time unless explicitly authoritative.

No post-selection date movement.

### A5 — Claim and decision-context contract

Before eligibility freeze:
- claim/conclusion construction rule from the recorded downstream endpoint;
- decision-context identifier/template;
- scope-binding rule;
- subject/entity/event/version binding rule;
- prohibited use of the model output as evidence/authority.

No case-specific claim rewriting after selection.

### A6 — Support-requirement contract

Before eligibility freeze:
- experimental required support count;
- handling of original authoritative support requirements;
- rule for cases with source requirements stricter than experimental policy;
- independence requirements, if any.

No silent weakening of original support requirements.

## 6. Phase D — excluded end-to-end bilateral rehearsal

Only after F and A pass, and before substantive eligibility.

### D1 — CFC final-path rehearsal
Repeat the complete-authority and missing-authority calibration cases using the **final proposed** controller, adapter, authority universe and runner/config.

### D2 — RIDI final-path rehearsal
On excluded calibration cases from the same neutral schema:
- freeze exact RIDI input;
- execute exact intended RIDI runner;
- capture versions/logs/errors;
- build exact raw-bundle schema.

### D3 — Commit/exchange plumbing rehearsal
For at least one excluded case:
1. each side builds one immutable raw ZIP;
2. each publishes only ZIP SHA-256 + byte size;
3. after both commitments, exchange exact ZIPs;
4. verify exact bytes independently;
5. verify pre-commit inspection boundaries;
6. only then inspect the counterpart result.

Calibration outputs are excluded from substantive findings.

### D4 — Failure behavior
Any defect triggers versioned repair and repetition of affected F/A/D checks. No substantive candidate pool exists yet.

## 7. Phase P — bilateral protocol/implementation freeze

Only after F, A and D pass may v0.2 be approved/frozen.

Freeze exact identities for:
- protocol v0.2;
- M1/A1/I1 v0.2;
- F1 controller baseline;
- substantive adapter;
- adapter validation suite;
- source-universe manifest;
- substantive authority-universe manifest;
- authority schema;
- temporal/as-of contract;
- claim/decision-context contract;
- support-requirement contract;
- CFC runner/config;
- RIDI runner/config;
- RIDI evaluation definition/scorer;
- raw-bundle schemas;
- error/no-go semantics;
- calibration-case exclusion manifest;
- excluded rehearsal records.

Every artifact has an exact version/reference, hash where applicable, timestamp and bilateral approval.

## 8. Phase E — outcome-blind substantive eligibility

Eligibility occurs only after Phase P and before seeds.

### E1 — prohibited eligibility information

Eligibility must not use:
- CFC claim state, gates or closure result;
- RIDI PASS/FAIL;
- equality/difference of A/B downstream endpoint values beyond presence/applicability checks;
- correctness;
- desired asymmetry;
- publication interest;
- convenience to either framework.

### E2 — mapping-only checker

The eligibility checker may:
- verify exact source availability;
- validate neutral schema;
- verify endpoint presence/evaluation applicability;
- run the frozen adapter in **mapping-only / validation-only mode**;
- classify authority availability under the frozen authority universe;
- validate support-requirement compatibility.

The eligibility checker must **not**:
- call the CFC substantive evaluation/closure function;
- compute or inspect CFC gates/claim state/closure;
- compute RIDI PASS/FAIL;
- compare canonical A/B endpoint values for equality/difference;
- inspect correctness.

If the adapter has no separable mapping-only mode, v0.2 eligibility is NO-GO until such a mode is frozen and validated.

### E3 — per-candidate classification

Classify at minimum:
- source: AVAILABLE / NOT_AVAILABLE;
- RIDI evaluation: APPLICABLE / NOT_APPLICABLE;
- schema: VALID / INVALID;
- adapter: REPRESENTABLE / NOT_REPRESENTABLE;
- authority state:
  - COMPLETE_AUTHORITY;
  - EXECUTABLE_MISSING_AUTHORITY;
  - UNREPRESENTABLE_MISSING_AUTHORITY;
  - CONFLICTING_AUTHORITY;
  - other predeclared frozen class;
- support requirement: COMPATIBLE / INCOMPATIBLE;
- calibration/exposure status.

### E4 — feasibility-consistent eligibility

If F5-B established only `MAPPING_NOT_EVALUABLE`, all unrepresentable missing-authority cases are ineligible before seeds.

If F5-B established `EXECUTABLE_MISSING_AUTHORITY`, the protocol must have predeclared whether that class is included.

No case is selected first and tested for representability afterward.

### E5 — freeze application

Freeze:
1. eligibility specification;
2. exact checker bytes/hash;
3. complete candidate registry;
4. exact source/authority references used by classifications;
5. audit output;
6. exact eligible pool bytes/hash.

Independent reproduction is required before seeds.

If the pool is empty or below a bilaterally predeclared minimum, record NO-GO; do not relax criteria.

## 9. Phase S — fresh commit–reveal

Only after Phase E exact pool freeze and independent reproduction:
- fresh independent seeds;
- role-bound commitments;
- both commitments before reveal;
- independent reveal verification;
- deterministic full-pool scores;
- one selected case under the frozen rule.

v0.1 seeds/scores/case are not reused.

## 10. Selected-case pre-execution reverification

After selection:
1. exact neutral selected bytes are extracted/frozen;
2. source identity is reverified against the **Phase A1 source-universe manifest**;
3. authority records are bound only from the **Phase A2 substantive authority universe**;
4. frozen adapter is rerun mapping-only;
5. eligibility classification must reproduce exactly;
6. CFC privately freezes substantive mapped inputs/manifests;
7. RIDI freezes permitted exact input;
8. controller/runner/config identities are reverified;
9. only I1-permitted hashes/status are exchanged.

This is reverification, not first discovery.

Any difference from frozen eligibility classification is a pre-execution NO-GO/reset.

## 11. Independent substantive execution

Only after both sides publish `PRE_EXECUTION_PASS`:
- CFC and RIDI execute independently;
- neither sees counterpart raw result before bundle commitment;
- each builds one immutable raw bundle;
- each publishes SHA-256 + exact byte size only;
- after both commitments, exact bundles are exchanged and independently verified;
- interpretation starts only after verification.

## 12. Controller-version immutability

The F1 controller remains unchanged through:
feasibility → rehearsal → protocol freeze → eligibility → selection → pre-execution → execution → raw bundle.

A newly released or superior CFC version requires a new versioned reset.

## 13. Inspection-boundary rule for authority material

Before Phase P, the parties must freeze I1 v0.2 rules specifying exactly which authority-universe contents each side may inspect.

If disclosure of CFC authority content to RIDI could reveal/influence the CFC substantive result:
- RIDI receives only the predeclared manifest identities/metadata necessary for protocol verification;
- CFC performs content-level authority verification;
- any independent third-party/content audit, if used, is separately recorded.

Protocol agreement on authority schema/universe identity does not require prohibited pre-commit substantive disclosure.

## 14. Explicit reset/no-go rules

Reset/stop if:
- F feasibility fails;
- source or authority universes cannot be durably frozen;
- no real complete-authority calibration case exists;
- adapter requires synthetic/case-specific authority;
- missing-authority behavior conflicts with intended eligibility;
- temporal/context/support rules are not frozen;
- eligibility requires CFC/RIDI substantive outcomes;
- mapping-only eligibility is impossible;
- independent eligibility reproduction fails;
- selected-case reverification differs;
- post-selection source/authority search is required;
- controller/adapter/threshold changes;
- material I1 violation;
- raw-bundle verification fails.

No quiet repair, synthetic substitution, outcome-driven eligibility edit or reselection.

## 15. Scientific decision objects

**RIDI:** Does the frozen-equivalent A/B representation preserve the nominated downstream verdict/action under the frozen evaluation?

**CFC:** Does the represented evidence state authorize closure/propagation of the nominated claim under the frozen authority/controller rules?

The adapter is representation only.

## 16. Non-claims

R5:
- is a draft, not approval;
- does not select a CFC baseline;
- does not claim a compliant adapter exists;
- does not authorize eligibility, seed generation, selection or execution;
- does not predict outcomes;
- does not convert v0.1 NO-GO into substantive evidence.

## 17. Required order

1. bilateral F0 feasibility-workplan sign-off;
2. controller nomination;
3. candidate nonfixture adapter;
4. adversarial representation-only validation;
5. feasibility authority snapshot;
6. complete + missing-authority feasibility executions;
7. bilateral feasibility decision;
8. durable source universe;
9. substantive authority universe + rules;
10. temporal/claim/context/support contracts;
11. bilateral excluded end-to-end rehearsal;
12. protocol/annex/implementation freeze;
13. outcome-blind eligibility + independent reproduction;
14. fresh commit–reveal;
15. selected-case reverification;
16. independent execution;
17. raw-bundle commitment/exchange;
18. interpretation.

**Prove the executable path before approving the protocol. Freeze the evidence universe before eligibility. Keep eligibility outcome-blind. Eligibility before selection. Evidence before execution.**
