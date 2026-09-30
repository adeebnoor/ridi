# CFC ↔ RIDI v0.2 — F0 Feasibility Workplan DRAFT R1

**Status:** F0 WORKPLAN DRAFT ONLY — NOT SIGNED / NOT APPROVED / NO CONTROLLER SELECTED / NO CONTROLLER MODIFICATION / NO ADAPTER DEVELOPMENT AUTHORIZED / NO ELIGIBILITY / NO SEED / NO SELECTION / NO EXECUTION  
**Parent review draft:** CFC ↔ RIDI v0.2 DRAFT R5  
**v0.1:** CLOSED AND IMMUTABLE

## 1. Purpose and boundary

F0 exists only to align the parties on **how implementation feasibility will be tested before any v0.2 protocol freeze**.

F0 is not:
- protocol approval;
- M1/A1/I1 approval;
- controller-baseline selection;
- authority-universe approval;
- adapter approval;
- eligibility approval;
- substantive execution authorization.

### 1.1 Before bilateral F0 sign-off

Until both parties explicitly approve the same exact F0 bytes/hash, permitted activity is limited to:

- read-only inspection of already-existing controller baselines and public/frozen implementation records;
- identification of candidate baseline references and known interface constraints;
- review of the neutral schema class and proposed feasibility criteria;
- review of already-existing authority-record classes/sources;
- drafting/reviewing F0 artifacts.

Not permitted before F0 sign-off:

- modifying CFC Anchor, CFC-next or any controller baseline;
- creating a v0.2 substantive adapter and treating it as an experiment artifact;
- creating or editing authority records for v0.2;
- private/internal controller bypasses or monkeypatches;
- substantive calibration execution;
- substantive eligibility construction;
- seed generation;
- case selection.

### 1.2 After bilateral F0 sign-off

A signed F0 authorizes **Phase F feasibility work only**, exactly as specified here.

It does not authorize:
- v0.2 protocol/annex freeze;
- substantive eligibility;
- seeds;
- substantive selection;
- substantive execution.

The controller baseline itself remains read-only. The feasibility adapter, if developed, must be a separate versioned artifact using only the bilaterally accepted F1 adapter-facing interface.

## 2. Phase F artifact responsibility and verification matrix

“Produce” means create or formally nominate the artifact.  
“Verify” means independently check the artifact against the frozen/predeclared acceptance criteria without relying on the producer’s conclusion.  
“Bilateral acceptance” requires explicit approval by **both parties of the same exact artifact identity/hash** where byte-addressable.

| Phase F artifact / decision | Primary producer | Independent verifier | Bilateral acceptance condition |
|---|---|---|---|
| **F0 workplan exact bytes** | RIDI side drafts; either side may propose revisions | CFC side reviews; RIDI rechecks final merged bytes | Both explicitly approve same SHA-256; only then Phase F work may begin |
| **F1 controller-baseline candidate inventory** | CFC side | RIDI verifies immutable refs/hashes and documented interface facts | Inventory accepted as complete enough for F1 review; no baseline selected by inventory alone |
| **F1 single baseline nomination** | CFC side | RIDI verifies version/ref/hash, public adapter-facing API and declared limitations | Both explicitly accept one exact baseline identity + approved interface contract |
| **Neutral schema class for Phase F** | RIDI side | CFC verifies required fields can be consumed without hidden case-specific assumptions | Both approve exact schema artifact/hash |
| **F2 candidate nonfixture adapter** | CFC side | RIDI reviews exact source/artifact and independently reruns public tests where permitted | Exact adapter bytes/hash accepted; no controller modification/private bypass; not yet substantive approval |
| **F3 representation-only adversarial test suite** | Joint acceptance criteria; CFC implements runnable suite | RIDI independently reruns/reviews results where permitted | All predeclared tests pass on exact F2 adapter; failures retained; criteria unchanged |
| **F4 feasibility authority-universe manifest** | CFC side identifies authority records/classes required by adapter | RIDI verifies manifest identities/provenance metadata to the extent permitted by the agreed inspection boundary | Same manifest/hash accepted; cutoff fixed; no authority record created to make a case pass |
| **F5 calibration candidate source frame** | RIDI side provides/identifies neutral source frame | CFC verifies schema compatibility and authority-state classificability | Exact source-frame manifest/hash accepted |
| **F5 deterministic calibration-case selector** | Joint rule drafted in F0/Phase F; implementation may be RIDI-side | CFC independently reproduces selection | Same COMPLETE_AUTHORITY and MISSING_AUTHORITY case IDs/hashes reproduced from frozen rule |
| **F5-A complete-authority execution bundle** | CFC side executes candidate path | RIDI verifies allowed identities/logs/tests; content access follows agreed inspection boundary | Source/authority/adapter/controller checks pass; exact artifacts/hashes recorded |
| **F5-B missing-authority execution bundle** | CFC side executes candidate path | RIDI verifies allowed identities/logs/tests; content access follows agreed inspection boundary | Predeclared missing-authority behavior reproduced exactly; no synthetic repair |
| **F6 feasibility decision record** | Each side records independent conclusion | Cross-review | Same factual status accepted: PASS or named NO-GO; disagreement remains explicit and blocks progression |

### 2.1 Verification limitations

Independent verification must not force disclosure that would violate the proposed inspection boundary.

Where RIDI is not permitted to inspect CFC-private authority content:
- CFC performs content-level validation;
- RIDI verifies exact manifest identities, hashes, public provenance references and predeclared validation evidence;
- any additional independent third-party audit, if later proposed, requires its own documented role and scope.

“No access” must never be silently converted into “verified.”

## 3. F1 baseline candidates and selection process

F0 does **not** select a controller baseline.

F0 permits read-only consideration of already-existing, immutable candidates such as:
- CFC Anchor `0.2.90rc1`;
- CFC-next `0.3.0a2`;
- another already-existing version only if added by bilateral F0 revision before F1 nomination.

For each candidate, CFC provides:
- immutable version/ref;
- source/package/wheel hash as applicable;
- public or explicitly proposed adapter-facing interface;
- documented representability/reachability constraints relevant to v0.2;
- whether substantive use would require controller modification, private state injection, monkeypatching or private/internal bypass.

### 3.1 Baseline acceptance rule

A baseline is suitable for F1 only if the intended adapter can operate without:
- modifying the frozen controller;
- monkeypatching;
- injecting unapproved private runtime state;
- using a private/internal bypass not included in the bilaterally accepted F1 interface contract;
- synthetic authority required merely to reach execution.

If no candidate satisfies this rule, record:

`F0/F1_NO_GO_BASELINE_UNSUITABLE`

and stop. Do not weaken the rule.

Once one baseline is bilaterally accepted under F1, switching baseline requires an explicit Phase F reset and renewed F1 acceptance.

## 4. Implementation boundary

### 4.1 Controller immutability

F0 never authorizes modification of:
- CFC Anchor;
- CFC-next;
- any other nominated baseline.

A modified controller is a new version/baseline and cannot inherit approval from its parent.

### 4.2 Adapter boundary

After signed F0 and accepted F1, feasibility work may create a **separate adapter artifact** only.

The adapter:
- may call only the F1-approved adapter-facing interface;
- may not patch controller code;
- may not inject hidden/private controller state;
- may not call an unapproved private authorization path;
- may not create evidence, semantic support or authority;
- may not contain case-specific exceptions;
- may not use expected CFC/RIDI outcomes or expected asymmetry.

If faithful representation requires crossing this boundary, record:

`F2_NO_GO_API_OR_IMPLEMENTATION_BOUNDARY`

and stop/reset. Do not bypass the boundary.

## 5. Predeclared failure semantics

Feasibility failure is a valid outcome.

No failure below authorizes relaxation of acceptance criteria.

### 5.1 Unsuitable controller baseline

Trigger:
- no approved candidate exposes a sufficient, reviewable adapter-facing path without prohibited modification/bypass; or
- declared controller limitations make the intended authority-state class unreachable.

Status:

`F1_NO_GO_BASELINE_UNSUITABLE`

Action:
- stop Phase F;
- retain all evidence;
- no adapter development under that baseline;
- another candidate may be considered only under the predeclared F0 candidate process before F1 acceptance, or by explicit bilateral Phase F reset after an F1 acceptance.

### 5.2 Real authority unavailable

Trigger:
- no qualifying **pre-existing** real authority records exist for the required complete-authority calibration case under the frozen/cutoff feasibility authority universe.

Status:

`F4/F5_NO_GO_REAL_AUTHORITY_UNAVAILABLE`

Action:
- stop;
- do not fabricate, solicit, label, infer or synthesize authority;
- do not lower the required authority class;
- do not substitute retrieval relevance/model output/source identity as authority.

### 5.3 Adapter-facing API incompatible

Trigger:
- the F1-approved interface cannot faithfully receive/represent the intended neutral/authority state; or
- execution would require a prohibited private/internal bypass, monkeypatch or controller modification.

Status:

`F2_NO_GO_API_INCOMPATIBLE`

Action:
- stop;
- do not use a private bypass;
- do not silently select a different controller;
- any alternative baseline/interface requires bilateral Phase F reset.

### 5.4 Failed representation-only validation

Trigger:
- F3 shows evidence/authority creation, semantic promotion, hidden fallback, case-specific behavior, non-determinism, dependency erasure, scope broadening or other predeclared violation.

Status:

`F3_NO_GO_REPRESENTATION_INVALID`

Action:
- the failing adapter version is rejected;
- failure artifacts remain retained;
- acceptance criteria are unchanged.

A purely mechanical implementation defect may be corrected only as a **new adapter version** under the same accepted F1 interface and same criteria, followed by complete F3 rerun.

If correction requires changing the interface, controller, authority rule or acceptance criterion, Phase F resets to the relevant earlier gate.

### 5.5 Complete-authority calibration path fails

Trigger:
- F5-A cannot execute faithfully even though its predeclared real authority records are present.

Status:

`F5A_NO_GO_COMPLETE_AUTHORITY_PATH`

Action:
- stop;
- determine whether failure is adapter defect, interface incompatibility or baseline limitation using the already frozen criteria;
- no eligibility/pool work begins.

### 5.6 Missing-authority calibration behavior

F5-B must produce exactly one predeclared class:

- `EXECUTABLE_MISSING_AUTHORITY`; or
- `MAPPING_NOT_EVALUABLE`.

Either can be a legitimate feasibility observation.

It is not permissible to change the intended class after seeing the result.

If the intended scientific design requires executable missing-authority cases and F5-B yields `MAPPING_NOT_EVALUABLE`, record:

`F5B_NO_GO_REQUIRED_STATE_UNREPRESENTABLE`

and stop before protocol approval.

If v0.2 instead accepts exclusion of that authority-state class, that exclusion must later be frozen in outcome-blind eligibility before seeds.

### 5.7 Verification disagreement

Trigger:
- producer and verifier cannot reproduce an artifact identity, test result or factual feasibility conclusion.

Status:

`F6_HOLD_VERIFICATION_DISAGREEMENT`

Action:
- execution/protocol progression remains blocked;
- disagreement is recorded;
- no “majority” or unilateral acceptance.

## 6. Authority and source boundaries during Phase F

### 6.1 No authority creation

Phase F may inventory and freeze **pre-existing** authority records only.

It may not:
- create new substantive authority;
- solicit a new annotation to satisfy a calibration case;
- reinterpret an existing record beyond its frozen scope;
- expand authority applicability to rescue feasibility.

### 6.2 Authority cutoff

Before F5 execution, F4 records an exact authority-record cutoff timestamp and manifest.

The F4 universe becomes the candidate substantive authority universe.

Any later change in membership, authority class, applicability rule or binding semantics requires a Phase F reset before proceeding.

### 6.3 Source availability

All F5 calibration source bytes must be durably retrievable and hash-verified before execution.

Temporary/expiring transport alone is insufficient where loss would block independent verification.

## 7. Calibration-case selection

Before either F5 case is executed, freeze:

- the candidate calibration source frame;
- deterministic selection rule for the required authority-state class;
- selected case IDs;
- exact source hashes;
- authority-state qualification reason under F4.

The selector must not use:
- CFC closure/claim state;
- RIDI PASS/FAIL;
- A/B endpoint equality/difference;
- correctness;
- expected asymmetry;
- publication convenience.

All F5/calibration cases are permanently `CALIBRATION/EXCLUDED` from v0.2 substantive selection under the case-agnostic exposure rule.

## 8. F0 acceptance package

Before F0 can be signed, freeze for review:

1. this exact F0 workplan;
2. responsibility/verification matrix;
3. baseline-candidate process;
4. implementation boundary;
5. failure-semantics table;
6. Phase F authority/source restrictions;
7. calibration-case selection rule requirements;
8. expected Phase F artifact list.

Compute SHA-256 of the exact F0 bytes.

### 8.1 Bilateral sign-off

F0 becomes **SIGNED** only when:

- Adeeb explicitly approves the same exact F0 SHA-256; and
- Krzysztof explicitly approves the same exact F0 SHA-256.

Any byte-level change after one approval invalidates that approval and requires a new F0 revision/hash.

### 8.2 Meaning of F0 sign-off

Signed F0 means only:

> The parties authorize the bounded Phase F feasibility work described in this exact workplan.

It does **not** mean:
- controller selection;
- protocol/annex approval;
- substantive authority-universe approval;
- eligibility approval;
- case selection;
- substantive execution.

## 9. Required Phase F outputs after signed F0

If F0 is signed, Phase F must produce or explicitly NO-GO on:

- F1 baseline nomination record;
- F1 baseline/interface identity manifest;
- neutral schema artifact;
- F2 adapter source/package + hash;
- F3 adversarial test suite + exact results;
- F4 authority-universe manifest + cutoff;
- calibration source-frame manifest;
- deterministic F5 selector + output;
- F5-A exact execution artifacts/logs/hashes;
- F5-B exact execution artifacts/logs/hashes;
- F6 bilateral feasibility decision.

No missing artifact is inferred from another.

## 10. Stop boundary

Until F0 is signed:

**READ-ONLY PLANNING/INSPECTION ONLY.**

After F0 is signed:

**PHASE F FEASIBILITY ONLY.**

At no point under F0 alone are eligibility construction, seeds, substantive selection or substantive execution authorized.

**Failure is evidence. Do not relax criteria to manufacture feasibility.**
