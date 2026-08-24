# Methods in brief

## Decision function

RIDI formalizes a finite top-*k* decision as `T_k = Phi(S, R, F, C, Z)`, where:

- `S` is source evidence;
- `R` is the operational representation;
- `F` is the inference or scoring procedure;
- `C` is the candidate universe and decision rule; and
- `Z` denotes stochasticity.

A representation intervention compares `R0` with `R1` while freezing or explicitly controlling the remaining inputs.

## Decision identity

For equal-size decision sets `A` and `B`, RIDI is their Jaccard distance:

`RIDI(A, B) = 1 - |A intersect B| / |A union B|`.

RIDI ranges from zero for identical decision identities to one for disjoint sets. Changed slots are reported alongside RIDI because they translate turnover directly into consumed decision capacity.

## Deterministic tie handling

Candidates are ordered by descending score and then lexical candidate identity. This makes repeated audits deterministic when scores tie. A deployment may use another stable tie rule, but it must declare and preserve that rule across representations.

## Score-margin certificate

Let `gamma_k` be the baseline score gap between ranks *k* and *k*+1, and let `epsilon` be the maximum absolute paired score perturbation. If `gamma_k > 2*epsilon`, no candidate can cross the decision boundary and top-*k* identity is guaranteed unchanged.

The certificate is sufficient, not necessary. A non-certified case can still have zero turnover. Its operational value is that stored paired scores can be certified in sorting time with no retraining or additional inference.

## Exact identity–utility frontier

The unconstrained updated top-*k* set maximizes updated score utility without regard to continuity. For each possible number `j` of entrants from outside the baseline set, the utility-maximizing set contains:

- the highest-updated-utility `k-j` identities from the baseline top-*k* set; and
- the highest-updated-utility `j` identities from outside it.

An exchange argument proves optimality: replacing any selected candidate by a higher-utility candidate from the same partition improves utility without changing `j`. After sorting the two partitions, prefix sums evaluate every frontier point. Total complexity is `O(n log n)`.

Given a prospectively declared utility-regret tolerance `eta`, the selector returns the smallest feasible `j`. The resulting identity budget is a policy tool analogous to a risk budget: it defines acceptable turnover conditional on an explicit tolerance, not an intrinsic universal constant.

## Interpretation boundary

Identity continuity is neither automatically desirable nor evidence of correctness. Independent outcome evidence may justify turnover. RIDI supplies the missing measurement and control layer so that continuity, utility and evidence can be evaluated separately.

