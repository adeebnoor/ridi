# Methods in brief

RIDI is a decision-set distance used inside an **allocation-identity audit**. The broader question is whether a declared evaluation identifies the finite entities that actually receive action, attention or context.

## Decision function

A capacity-limited decision can be written abstractly as `T_k = Phi(S, R, F, C, Z)`, where:

- `S` is source evidence;
- `R` is the operational representation;
- `F` is the inference or scoring procedure;
- `C` is the candidate universe and decision rule; and
- `Z` denotes stochasticity.

Different experiments may intervene on different components. A valid attribution design freezes or explicitly controls competing components rather than assuming every observed identity change has one cause.

## Allocation identity

For equal-size selected sets `A` and `B`, RIDI is their Jaccard distance:

`RIDI(A, B) = 1 - |A intersect B| / |A union B|`.

RIDI ranges from zero for identical membership to one for disjoint sets. Changed slots are reported alongside RIDI because they translate turnover directly into consumed finite capacity.

## Audit equivalence

Two states are audit-equivalent relative to a declared audit when every reported audit quantity under that declaration is identical. Audit equivalence does **not** automatically imply allocation equivalence. The RAG experiment makes this explicit by preserving the complete relevance-grade-by-position vector and all registered retrieval metrics while replacing only metric-zero passage identities.

## Deterministic tie handling

Candidates are ordered by descending score and then lexical candidate identity. This makes repeated score-table audits deterministic when scores tie. A deployment may use another stable tie rule, but it must declare and preserve that rule across compared states.

## Score-margin certificate

Let `gamma_k` be the baseline score gap between ranks *k* and *k*+1, and let `epsilon` be the maximum absolute paired score perturbation. If `gamma_k > 2*epsilon`, no candidate can cross the decision boundary and top-*k* identity is guaranteed unchanged.

The certificate is sufficient, not necessary. A non-certified case can still have zero turnover. Unresolved cases are not predictions of instability.

## Exact identity–utility frontier

The unconstrained updated top-*k* set maximizes updated score utility without regard to continuity. For each possible number `j` of entrants from outside the baseline set, the utility-maximizing set contains:

- the highest-updated-utility `k-j` identities from the baseline top-*k* set; and
- the highest-updated-utility `j` identities from outside it.

An exchange argument gives optimality. After sorting the two partitions, prefix sums evaluate every frontier point, giving `O(n log n)` complexity.

Given a declared utility-regret tolerance `eta`, the selector returns the smallest feasible `j`. The identity budget is therefore conditional on explicit utility/outcome tolerance; it is not a universal constant.

## Interpretation boundary

Identity continuity is neither automatically desirable nor evidence of correctness. Turnover can be beneficial, neutral or harmful. Outcome, task-performance and fairness evidence should be evaluated separately. RIDI supplies an observability/control layer for the finite allocation itself.

## Practical workflow

A reusable workflow is:

1. **Measure** realized membership change.
2. **Attribute** change only when competing mechanisms are controlled.
3. **Certify** zero-turnover cases when a sufficient margin condition fires.
4. **Control** avoidable turnover under an explicit utility-regret budget.
5. **Validate** the chosen budget against application-specific outcomes or safety gates.

Failed gates and registered null results remain part of the evidential boundary rather than being redefined after observation.
