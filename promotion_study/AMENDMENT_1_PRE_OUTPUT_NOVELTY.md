# AMENDMENT 1 — PRE-OUTPUT NOVELTY REFINEMENT

Date: 19 September 2026
Study: LLM-EXEC-REPRO-AJSE-v1
Timing: **before any language-model endpoint output for this study.**

## Why this amendment exists

A pre-execution literature kill-test identified strong prior art on the general claim that LLM inference can vary with batch size, GPU count/type and numerical execution configuration:

- Yuan et al., *Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference*, NeurIPS 2025, DOI 10.52202/085713-5653.
- vLLM batch-invariance documentation explicitly targets batch-size/order independence.
- LLM-42 (2026) develops deterministic inference under dynamic batching.

Therefore, a paper whose primary contrast is isolated batch size 1 versus mixed batch size 8 would be too close to established prior art.

## Scientific refinement

The primary causal contrast is changed **before outputs** from A versus C to **B versus C**:

- B: batch size 8, seven length-matched co-tenants;
- C: batch size 8, seven co-tenants spanning predeclared prompt-length quantiles.

Thus batch size is fixed at 8. The treatment is the co-tenant composition/length geometry surrounding an unchanged target prompt.

The second primary endpoint remains final-decision divergence under the same B-versus-C contrast.

A versus C is retained and reported as a secondary batch-size-plus-composition contrast. C versus D remains the fixed-composition order/position contrast.

## What does not change

No model, dataset, selected item, tokenizer revision, prompt, batch-plan algorithm, frozen batch-plan SHA, generation setting, scorer, bootstrap seed, Nature firewall or anti-selection rule changes.

## Revised primary endpoints

1. Exact-text co-tenant-composition divergence: fraction of targets with internally stable duplicates in B and C but different B versus C decoded text.
2. Final-decision co-tenant-composition divergence: analogous B-versus-C fraction for frozen final decisions.

This amendment is motivated only by prior-art differentiation and predates endpoint generation.
