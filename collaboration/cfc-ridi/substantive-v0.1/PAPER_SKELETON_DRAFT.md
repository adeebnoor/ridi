# Paper skeleton — CFC ↔ RIDI

**Status: INTERNAL DRAFT / RESULT-NEUTRAL / NOT A CLAIM OF FINDINGS**

## Provisional title

**Separating evidence authorization from downstream action equivalence in AI systems**

Alternative neutral title:

**Evidence authorization and action equivalence assess distinct properties of AI decision pipelines**

## One-sentence question

When two AI inputs or states are equivalent under a declared evaluation, is the question of whether their evidence state is authorized to propagate the same as the question of whether they produce the same downstream decision?

## Core conceptual separation

- **CFC:** has the represented evidence state earned closure/propagation authorization under the frozen evidence, authority, scope, freshness, dependency and support rules?
- **RIDI:** under the frozen evaluation-equivalence premise, do A and B preserve the specified downstream verdict/action?
- **Joint question:** are these two properties empirically separable on a pre-specified shared specimen without collapsing one framework into the other?

No direction of association is assumed.

## Planned contribution if supported

1. A reproducible protocol for comparing evidence-state authorization with downstream action equivalence.
2. A strict separation between per-arm CFC outputs and pair-level RIDI output.
3. A worked demonstration of independent execution, frozen mapping/authority boundaries, commit–reveal case selection and raw-output commitments.
4. A bounded observation about whether the two properties coincide or diverge in the selected case.
5. A methodology for scaling to a later multi-case 2×2 study without rewriting the first result.

## Introduction structure

### 1. Evaluation equivalence is not a complete state description
Summarize why aggregate or declared evaluation equivalence does not identify every selected input, evidence state or downstream action.

### 2. Authorization is a separate question
Introduce the distinction between a claim/evidence state and whether that state is authorized to propagate.

### 3. The missing bridge
Existing evaluation audits and evidence-governance mechanisms can answer different questions. A direct, pre-specified comparison is needed.

### 4. Study objective
Test both frameworks on one jointly selected case under frozen boundaries, preserving null, negative and NOT EVALUABLE outcomes.

## Methods

### Frozen protocol and provenance
- bilateral protocol freeze;
- exact protocol SHA-256;
- public mirrors;
- no substantive selection before freeze.

### Frozen annexes
- M1 mapper;
- A1 authority policy;
- I1 inspection matrix;
- one-support bounded policy;
- cases with authoritative >1 support requirement excluded.

### Mechanical dry run
Describe as excluded integration evidence only. Do not mix its result with substantive findings.

### Eligible pool
Report pre-frozen inclusion/exclusion criteria, canonical IDs, source hashes and prior exposure. Do not discuss predicted outputs.

### Commit–reveal selection
Report:
- frozen pool SHA-256;
- ADEEB seed commitment;
- KRZYSZTOF seed commitment;
- revealed seeds;
- combined hash;
- all case scores;
- selected canonical ID.

### Independent execution
CFC and RIDI run within frozen I1 boundaries. The study is not fully blinded because both sides may see recorded A/B verdict/actions. It instead uses independent execution, output sequestration and mandatory raw-bundle hash commitments.

### CFC endpoint
Report A and B separately:
- claim state;
- stop type;
- closure/propagation authorization;
- gates/reasons;
- mapping/authority status;
- errors.

Derived pair classification:
- CFC_PAIR_ALLOW;
- CFC_PAIR_BLOCK;
- CFC_PAIR_NOT_EVALUABLE.

### RIDI endpoint
Primary:
- downstream verdict/action equivalence under the frozen comparison function.

Secondary:
- selected identity;
- allocation difference;
- correctness if independently available.

### Joint interpretation
Possible derived cells:
- CFC_PAIR_ALLOW / RIDI_PASS
- CFC_PAIR_ALLOW / RIDI_FAIL
- CFC_PAIR_BLOCK / RIDI_PASS
- CFC_PAIR_BLOCK / RIDI_FAIL

NOT EVALUABLE is reported separately and is not forced into the 2×2 matrix.

## Results placeholders

### Protocol conformance
[fill only after raw-bundle verification]

### Selected case
[fill after commit–reveal only]

### CFC per-arm results
[raw values first]

### RIDI pair result
[raw values first]

### Joint cell
[derive only after both raw bundles are verified]

### Correctness / secondary observations
[separate from primary equivalence]

## Discussion structure

1. What the observed cell means.
2. What it does **not** mean.
3. Whether authorization and downstream equivalence coincided or diverged in this bounded case.
4. Why one shared case is a mechanism/pilot result rather than a prevalence estimate.
5. Mapping and authority limitations.
6. Information overlap and incomplete blinding.
7. Why the result does not validate, subsume or rank CFC versus RIDI.
8. Pre-specified path to a multi-case extension.

## Multi-case extension — future, not part of first run

After the first bounded experiment is closed, a separately frozen extension could estimate occupancy of the four joint cells across a larger pool. That extension must have its own sampling frame, power/precision target, eligibility rules and preregistration before looking at extension outcomes.

## Relationship to the current RIDI Nature manuscript

This joint study should remain separate from the current RIDI manuscript during initial submission/review. It can be cited later as an independent follow-up if a public record exists, or used to answer reviewer questions about warranted evidence-state propagation. It should not be retrofitted into the current manuscript as if it were part of the original experimental program.

## Non-claims

A single selected case cannot establish:
- prevalence across AI systems;
- superiority of either framework;
- production readiness;
- real-world safety;
- causal benefit;
- general independence of authorization and action equivalence;
- external validation of the entire CFC or RIDI research program.
