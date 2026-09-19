# Literature positioning — AJSE execution reproducibility

This note is for manuscript positioning and was drafted while the locked experiment was still running. It does not alter the protocol.

## Closest work

1. Yuan et al., **Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference**, NeurIPS 2025. The study varies evaluation batch size, GPU count/type and numerical precision, identifies floating-point non-associativity as a source of divergence, and proposes LayerCast. DOI: 10.52202/085713-5653.
2. Zhang et al., **Deterministic Inference across Tensor Parallel Sizes That Eliminates Training-Inference Mismatch**, arXiv:2511.17826. The focus is tensor-parallel-size invariance and tree-based invariant kernels.
3. Gond et al., **LLM-42: Enabling Determinism in LLM Inference with Verified Speculation**, SOSP 2026 / arXiv:2601.17768. The focus is a scheduling/verification mechanism for deterministic serving under dynamic batching.
4. Zhao et al., **CoRun: Padding is Simple and Efficient for Deterministic LLM Inference**, arXiv:2608.14376. The focus is fixed-shape scheduling and deterministic inference without batch-invariant kernels.

## Narrow contribution of the present study

The present AJSE study does **not** claim first discovery of LLM inference nondeterminism.

It isolates a narrower reproducibility question:

> At fixed batch size, fixed GPU, fixed model revision, fixed software stack and identical target prompt bytes, can changing only the **co-batch composition / padded shape** change a target model output or benchmark decision?

Design features that distinguish the study:

- fixed batch size four for both batched conditions;
- same A100 GPU type and same pinned runtime;
- target prompt and target token sequence held fixed;
- length-near versus length-mixed co-batch construction generated output-blind from a frozen 152-prompt panel;
- exact solo repeat as a negative control;
- four model families (Qwen2.5, Mistral, OLMo-2, Phi-3.5);
- two task types (multiple-choice reasoning and numerical reasoning);
- separate text-level, decision-level and correctness-level reproducibility endpoints.

If the effect is null, the paper reports the boundary: fixed-size co-batch composition may be less consequential than batch-size/GPU changes under the tested stack. If non-null, the contribution is direct evidence that the identity/length of unrelated requests sharing a batch can alter target inference even without changing batch size.

This paper must not use the Nature manuscript's allocation-identity framing or results.
