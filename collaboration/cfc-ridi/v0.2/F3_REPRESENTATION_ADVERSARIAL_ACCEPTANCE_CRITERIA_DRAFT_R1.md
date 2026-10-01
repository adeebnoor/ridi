# CFC–RIDI v0.2 — F3 Representation-Only Adversarial Acceptance Criteria DRAFT R1

**Date:** 2026-10-01  
**Status:** RIDI PROPOSAL FOR BILATERAL F3 CRITERIA FREEZE / NO F3 RESULT YET  
**Authority:** signed F0 feasibility workplan  
**F2 baseline:** bilaterally closed and immutable

## 1. Exact F2 baseline under test

Candidate:

`CFC-RIDI-F2-ADAPTER-v0.1`

Exact CFC candidate commit:

`4167783eb48e1a1677107cb1359ad9b2f890017f`

Primary adapter SHA-256:

`4b975fda6242c9a7e33d0d692705ef6fe82683dbf2bddefc0345c2e5504b480a`

No F3 test may modify these bytes.

Any adapter change creates a new F2 candidate and resets F3.

## 2. F3 responsibility boundary

Under signed F0:

- acceptance criteria are joint/bilateral;
- CFC implements the runnable F3 suite;
- RIDI independently reruns/reviews the exact suite and results;
- F3 is representation-only;
- fixture authority/verifier objects used for testing are never F4/F5 substantive authority;
- no eligibility, seed, selection or substantive RIDI/CFC execution is authorized.

## 3. General pass rule

For every adversarial mutation below, the mutation must not be silently accepted as a valid equivalent representation.

A test passes only if the frozen adapter/controller path does one of the predeclared acceptable things:

1. rejects the mutation explicitly before evaluation; or
2. reaches the accepted public Controller and produces an explicit non-closure/STOP attributable to the mutated state.

A normal evaluative/closure result that silently ignores the mutation is a failure.

No test may:
- rely on expected RIDI A/B outcome;
- use gold correctness;
- use publication-interest labels;
- create substantive authority;
- use private Anchor access;
- monkeypatch the frozen controller.

## 4. Predeclared adversarial tests

### F3-T01 — Exact F2 baseline identity

Reproduce the exact F2 adapter/component identities before every suite run.

**PASS:** all accepted bytes/hashes match.  
**FAIL:** any byte differs.

### F3-T02 — Deterministic one-arm preparation

Run the same valid neutral arm repeatedly from byte-identical input.

**PASS:** mapping/requirements artifacts are deterministic and identical.  
**FAIL:** nondeterministic semantic/authority representation appears.

### F3-T03 — Hidden neutral-field promotion

Vary bookkeeping-only neutral metadata while preserving the valid schema/bindings needed for the test.

**PASS:** no identity, authority, provenance, polarity, independence, scope, freshness, epistemic role or decision-as-of state is inferred from those bookkeeping fields.  
**FAIL:** any such state is promoted automatically.

### F3-T04 — Counterpart/withheld-state injection

Attempt to inject counterpart-arm, gold, retrieval-grade, correctness, perturbation-condition or RIDI-result fields.

**PASS:** explicit schema rejection.  
**FAIL:** hidden/extra experimental state is consumed.

### F3-T05 — Cross-case / cross-arm resolved-state substitution

Construct two valid neutral arms whose passage-level bindings can be made superficially similar, then attempt to apply resolved state from one case/arm to the other.

**PASS:** the substitution is explicitly rejected or made non-evaluable before a valid closure result.  
**FAIL:** foreign case/arm state is silently accepted.

### F3-T06 — Claim-identity substitution

Mutate the resolved claim identity/binding while leaving the neutral candidate conclusion unchanged.

**PASS:** explicit rejection or explicit Controller non-closure attributable to identity mismatch.  
**FAIL:** the altered identity is silently treated as equivalent.

### F3-T07 — Scope broadening

Provide resolved state whose declared/applicable scope is narrower than the scope requested for evaluation, or substitute an incompatible controller/decision scope.

**PASS:** explicit rejection or explicit non-closure.  
**FAIL:** scope is silently broadened.

### F3-T08 — Decision-as-of / freshness substitution

Use resolved state or attestations whose applicability does not cover the requested decision `as_of`.

**PASS:** explicit rejection or explicit non-closure.  
**FAIL:** stale or temporally incompatible state is silently accepted.

### F3-T09 — Passage-state rebinding

Swap, reorder or attach resolved passage state to a different neutral passage binding.

**PASS:** binding mismatch is detected; no valid evaluation proceeds.  
**FAIL:** semantic/authority state can migrate across passage bindings silently.

### F3-T10 — Dependency / independence preservation

Construct fixture evidence with shared lineage/failure domain and attempt to satisfy an independence requirement merely through distinct-looking evidence IDs, doc IDs or hashes.

**PASS:** independence is not inferred from identifier distinctness; missing/conflicting independence state prevents valid closure where independence is required.  
**FAIL:** distinct identifiers alone satisfy independence.

### F3-T11 — Required-support mismatch

Set an explicit support requirement greater than the verified independent support represented by the fixture state.

**PASS:** explicit non-closure/rejection.  
**FAIL:** insufficient support is silently treated as sufficient.

### F3-T12 — Host-trust / verifier mismatch

Use an unregistered verifier, wrong authority class, wrong authority ID, or otherwise incompatible host-trust registration.

**PASS:** explicit rejection or public-Controller non-closure.  
**FAIL:** incompatible trust binding is silently accepted.

### F3-T13 — Missing/malformed resolved semantic state

Remove or corrupt required identity, source semantics, provenance, evidence authority, epistemic-role, topology, snapshot or support-independence state.

**PASS:** explicit failure; no hidden fallback/default semantic authority.  
**FAIL:** the adapter invents or defaults substantive state.

### F3-T14 — Case-agnostic behavior

Repeat representative adversarial mutations across at least:
- two source datasets/tasks; and
- both arm labels where applicable.

**PASS:** the same rule class is applied without case-ID-specific exceptions.  
**FAIL:** behavior depends on a named case/arm special path.

### F3-T15 — Public-interface confinement

Trace imports and Controller calls during the runnable suite.

**PASS:** only the bilaterally accepted F1 public package/classes/methods are used; no controller-private state/module access occurs.  
**FAIL:** any private/internal bypass, monkeypatch, private-state injection or controller modification is observed.

## 5. F3 decision rule

F3 passes only if **all predeclared tests pass on the exact accepted F2 adapter**.

Required PASS status:

`F3_REPRESENTATION_ONLY_ADVERSARIAL_SUITE_PASS`

If any test fails:

`F3_NO_GO_REPRESENTATION_INVALID`

The failure artifact and exact failing adapter version must be retained.

A purely mechanical adapter defect may be corrected only as a new versioned F2 adapter candidate under the same frozen F1/schema/F3 criteria. After any adapter-code change, the complete F2 acceptance and complete F3 suite must be rerun.

No acceptance criterion may be weakened after observing a failure.

## 6. Bilateral-freeze condition

This DRAFT R1 becomes operative only after both parties explicitly accept the same exact artifact identity before CFC publishes/runs the F3 suite.

After bilateral criteria freeze:

1. CFC implements the runnable suite;
2. CFC publishes exact suite identity/hash and complete results;
3. RIDI independently reruns/reviews;
4. only matching factual results can close F3.

No F4 conclusion is implied by F3.
