# GENERATION AND SCORING LOCK — RIDI-NATURE-FRONTIER-DOWNSTREAM-v1

**Locked before Qwen3-8B endpoint generation.**

Frozen 400-query panel commit: `f98be71b4402d95a3337dac78f272c3aa55cbd62`.

This document fixes the language-model generation and scoring implementation for the frontier → downstream RAG extension. It does not alter the candidate universe, query sample, frontier, k values or eta values already frozen under `PROTOCOL_LOCK.md` and `AMENDMENT_1_PRE_GENERATION.md`.

## Model and inference

- model: `Qwen/Qwen3-8B`
- immutable revision: `b968826d9c46dd6066d109eabc6255188de91218`
- unquantized bfloat16 weights
- model-native chat template
- `enable_thinking=False`
- `max_new_tokens=128`
- greedy decoding: `do_sample=False`
- seed: `20260902`
- deterministic PyTorch algorithms enabled
- TF32 disabled
- `CUBLAS_WORKSPACE_CONFIG=:4096:8`
- no endpoint-dependent retry, prompt change or decoding change is permitted

The target software stack is the stack recorded for the prior Qwen3-8B robustness execution: torch 2.11.0+cu128, transformers 4.57.6, huggingface_hub 0.36.2 and accelerate 1.14.0. If the exact stack cannot be installed, execution stops before generation; any repair must be timestamped before endpoint output.

## States

For every one of the 400 frozen queries, all prespecified capacities are generated:

- k ∈ {5, 10, 20}
- reference (BM25 ordering)
- updated-unconstrained (SPLADE++ ordering)
- frontier-controlled eta=0.0001
- frontier-controlled eta=0.001

This yields 12 responses per query and 4,800 responses in total.

No state may be omitted because another state has an inconvenient result.

## Prompt instantiation

The extension uses the same task family as the registered RIDI RAG experiment, but this new extension prompt is fixed here explicitly and is **not represented as byte-identical to the earlier 800-query prompt bundle**.

### Natural Questions and HotpotQA

System message:

`Use the provided passages to answer the question. Return only the shortest answer that directly answers the question. Do not include citations or explanations.`

User message:

```
Passages:
[1] <title>
<text>

[2] <title>
<text>
...
Question: <query>
Answer:
```

### FEVER and SciFact

System message:

`Use the provided passages to classify the claim. Return exactly one label: SUPPORTS, REFUTES, or NOT_ENOUGH_INFO.`

User message:

```
Passages:
[1] <title>
<text>

[2] <title>
<text>
...
Claim: <query>
Label:
```

Passage order is exactly the order stored in the frozen state. Passage text is the already-frozen first 1,200 Unicode characters. No qrel value, score, frontier status or document identifier is shown to the generator.

## Primary scoring

### QA

Before exact matching:
1. remove numeric square-bracket citations such as `[1]` and `[1, 2]`;
2. Unicode NFKC normalize;
3. case-fold;
4. remove punctuation;
5. remove English articles `a`, `an`, `the`;
6. collapse whitespace.

A response is correct if the resulting string exactly equals any normalized accepted answer.

### Classification

The primary parser accepts a canonical verdict only if it is the first non-whitespace token:

`SUPPORTS`, `REFUTES`, or `NOT_ENOUGH_INFO`.

Wrappers such as `Verdict: SUPPORTS` are not accepted by the primary parser.

## Locked scoring sensitivities

- QA: accepted-answer substring after the same normalization.
- FEVER/SciFact: wrapper-tolerant parser permitting opening Markdown and one of `Verdict:`, `Answer:`, `Label:`, or `Classification:` before the canonical label.

Sensitivities do not replace the primary endpoint.

## Normalized answer disagreement

For the answer-identity endpoint, raw responses are NFKC-normalized, numeric citation markers are removed, case is folded and whitespace is collapsed. Punctuation is retained. Two responses disagree when these normalized strings differ.

## Primary downstream contrast

At `k=10, eta=0.001`, compare frontier-controlled versus updated-unconstrained:

- paired benchmark-defined correctness difference (controlled minus updated);
- correctness-status disagreement;
- normalized answer-text disagreement.

The identity-control endpoint remains the already-frozen changed-slot reduction.

All four datasets are reported separately and with an equal-dataset-weight macro. The predeclared 100,000-draw dataset-stratified bootstrap uses seed `20260918`.

## Execution integrity

Each dataset execution must verify the frozen sample gzip SHA-256 from `FROZEN_PANEL_MANIFEST.json` at commit `f98be71b4402d95a3337dac78f272c3aa55cbd62` before model loading.

Raw generations, per-query scoring, environment metadata, hashes and aggregate summaries are archived whether supportive, null or adverse.
