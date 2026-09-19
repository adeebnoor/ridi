# NOVELTY AUDIT — AJSE STUDY

Audit date: 19 September 2026
Timing: before model endpoint generation.

## Closest work found

1. Yuan, J. et al. **Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference.** NeurIPS 2025. DOI: 10.52202/085713-5653.
   - Establishes that batch size, GPU count/type and limited-precision numerics can alter greedy LLM outputs and benchmark accuracy.
   - Introduces LayerCast mitigation.
   - Consequence for this study: do **not** claim discovery that batch size or numerical execution can matter.

2. vLLM **Batch Invariance** documentation (current 2026).
   - Defines batch-invariant serving as independence from batch size/order and supplies a beta implementation.
   - Consequence: do not claim that the concept of batch invariance is new.

3. Gond et al. **LLM-42: Enabling Determinism in LLM Inference with Verified Speculation** (2026; SOSP 2026 artifact/public preprint).
   - Treats dynamic-batching nondeterminism as a systems problem and proposes verified speculation.
   - Consequence: this paper is not positioned as a new deterministic-serving algorithm.

4. Patodiya, **Same Request, Different Answer: Quantization Amplifies Cache-Induced Divergence in LLM Serving** (arXiv:2609.04748, September 2026).
   - Studies cache state/quantization with serial batch-size-one agentic workloads.
   - Consequence: do not fold cache-state or quantization claims into the present paper.

## Remaining target gap

The amended primary question is narrower:

> At a fixed batch size of eight, does changing only the co-tenant prompt-length/composition regime surrounding an unchanged target alter exact output or final benchmark decision under a fully recorded deterministic configuration?

The design then separates:
- fixed-size composition regime B vs C (primary);
- batch-size-plus-composition A vs C (secondary);
- same membership with reversed order/target position C vs D (secondary);
- within-path repeatability from between-path divergence.

## Safe novelty language

Preferred:
- "We isolate fixed-size co-tenant composition as an execution factor..."
- "We distinguish within-path repeatability from fixed-size composition invariance..."
- "We quantify when execution-path differences propagate to benchmark decisions..."

Avoid:
- "first demonstration that batching changes LLM outputs"
- "first deterministic LLM inference study"
- "batch invariance is a new concept"

## Submission-time novelty check

Repeat the literature search immediately before submission and revise claims if new peer-reviewed work has appeared.
