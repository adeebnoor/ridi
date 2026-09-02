# RIDI / Allocation Identity — Nature-main novelty defense

**Status:** pre-outcome positioning, frozen before any real LLM generation.

## The claim we make

The contribution is **not** that evaluation metrics can be imperfect, that LLMs can be sensitive to context, that multiple allocations can have equal utility, or that evaluation protocols can be non-identifying in general.

The narrower and stronger claim is:

> In a finite-capacity decision, an aggregate audit can be exactly correct on every quantity it reports while failing to identify **which entities actually received the scarce capacity**. This allocation-identity omission defines an audit-equivalence class of realized decisions. The class can be characterized exactly, its remaining log-cardinality can be bounded without probabilistic assumptions, and downstream behavior can be tested prospectively while the published audit vector is held exactly fixed.

This is the proposed new evaluation object: **allocation identity**.

## Formal object

For feasible finite allocations `T ∈ Ω` and a reported audit map `A: Ω → Y`, define

`[T]_A = {S ∈ Ω : A(S) = A(T)}`.

An audit is **allocation-identifying at T** iff `|[T]_A| = 1`.

The deterministic unresolved identity burden is

`log2 |[T]_A|`

bits of log-cardinality ambiguity. This is **not Shannon entropy** and no probability distribution is assumed. Any fixed-length code that uniquely distinguishes members of the class requires at least `ceil(log2 |[T]_A|)` additional bits.

For a fixed downstream map `g`, audit-equivalent allocations are behaviorally invariant iff `g` is constant on every relevant audit-equivalence class (equivalently, `g` factors through `A`). The prospective RAG experiment tests this invariance by moving allocation identity while holding the audit vector exactly fixed.

## Closest prior art and boundary

### Jain et al., FAccT 2025 — Allocation Multiplicity

DOI: `10.1145/3715275.3732138`

They study the existence and recovery of multiple near/equal-utility allocations, especially through Rashomon/model multiplicity. We **do not claim** to originate allocation multiplicity.

Our estimand differs: the partition is induced by **what the published audit retains**, not by a Rashomon set or utility tolerance. Non-identification can therefore exist for one fixed system and one realized decision even when model multiplicity is absent.

### Luo et al., 2026 — Protocol-Level Identifiability Audit

arXiv: `2608.13326`

They ask whether an observation protocol separates behavioral policies that differ on an estimand. We **do not claim** to originate evaluation identifiability.

Our contribution specializes a different object: finite-capacity **allocation identity** under aggregate evaluation. The intervention operates inside an exactly audit-equivalent class of allocations and asks whether downstream system behavior changes when only membership identity changes.

### RAG metric-utility / distractor literature

Prior work shows that IR metrics may misalign with downstream RAG utility and that distractors can change model answers. We **do not claim** either phenomenon as new.

Our prospective test is stricter: precision, recall, nDCG, MRR, MAP and the full relevance-grade-by-position vector are held exactly fixed while document membership identity is changed by preregistered doses. The estimand is therefore **within-audit-class identity sensitivity**, not ordinary metric correlation or distractor robustness.

### Terminology collision

A 2026 SSRN paper uses the phrase **Behavioral Sufficiency Problem** for a governance argument unrelated to this theorem. Do not use that phrase as a named contribution. Use `allocation-identifying audit`, `audit-equivalence class`, and `within-class behavioral invariance`.

## Nature-level empirical chain

The paper should establish one claim through multiple layers, not present unrelated experiments:

1. **General theorem:** aggregate audit maps induce decision-equivalence classes; identification is equivalent to singleton classes; refinement cannot increase ambiguity.
2. **Exact finite-capacity specialization:** compute class size / identity ambiguity and constructive collision witnesses.
3. **Deployed-domain instantiations:** show the omission in operational finite-capacity settings such as vulnerability prioritization and criminal-justice allocation, without overstating causal consequences.
4. **Prospective AI pipeline test:** RAG identity-dose intervention at 25%, 50%, 100% replacement under exact audit equivalence, with permutation at RIDI=0 as an order control.
5. **Transport:** tasks, model families, retrievers, and capacities.
6. **Remedy:** report allocation identity or a cryptographic identity digest / allocation certificate alongside aggregate performance and group-fairness summaries when decisions are capacity-limited.

## Claims explicitly prohibited

Do not write any of the following:

- “first identifiability framework for AI evaluation”;
- “first demonstration of allocation multiplicity”;
- “first evidence that RAG metrics miss downstream utility”;
- “qrel-zero documents are semantically irrelevant”;
- “log2 class size is entropy”;
- “same metrics necessarily imply different outcomes.”

The prospective experiment is allowed to falsify downstream divergence. The structural allocation-identification result does not depend on a positive LLM result.

## Editorial one-sentence test

If the abstract can be reduced to “RAG metrics are imperfect,” the manuscript is not Nature-main ready.

If the evidence supports the following sentence, the manuscript has a defensible broad claim:

> Evaluations of capacity-limited AI systems are incomplete when they report aggregate performance without preserving the identity of the entities that actually received the finite decision capacity.
