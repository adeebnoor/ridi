# AJSE-LLM-EXEC-REPRO-v1 — pre-output protocol lock

Target journal: Arabian Journal for Science and Engineering.

Scientific question: under nominally deterministic greedy decoding, can execution configuration change exact model output or task decision when model weights and prompt bytes are fixed?

## Models
1. Qwen/Qwen2.5-7B-Instruct. The run must freeze and report exact model/tokenizer file hashes before generation; no Qwen3 model is permitted.
2. mistralai/Mistral-7B-Instruct-v0.3 pinned to commit 405950b9564feeced210f7c5d8089f76237b9861.

## Benchmarks
Nature-panel datasets are prohibited. Use:
- GSM8K test;
- ARC-Challenge test;
- HellaSwag validation;
- CommonsenseQA validation.

Select 250 examples per dataset before generation using stable IDs and NumPy default_rng(20260919) without replacement where the split exceeds 250. Freeze selected-panel JSONL and source hashes before generation.

## Prompting
Fixed zero-shot task template per benchmark. Prompt bytes must be identical across execution conditions. No retrieval, tools, or external context.

## Generation
- transformers;
- bfloat16 where natively supported;
- do_sample=False;
- max_new_tokens=128;
- seed=20260919;
- torch deterministic algorithms enabled;
- TF32 disabled;
- model.eval().

## Execution conditions
Baseline: each prompt generated alone, batch size 1.

Predeclared contrasts:
A. batches of 2;
B. batches of 4;
C. batches of 8;
D. batches of 4 sorted by token length;
E. batches of 4 with deterministic long/short interleaving;
F. batches of 4 after a fixed seeded permutation of prompt order.

Prompt bytes and per-prompt generation parameters are unchanged. Outputs are restored to original IDs before comparison.

If a condition is technically unavailable because of memory, report it as unavailable; do not silently change batch size.

## Primary endpoint
Exact-output disagreement rate versus batch-size-1 baseline after stripping terminal whitespace.

Study-level primary summary: equal-weight mean exact-output disagreement across model × dataset cells for each execution condition.

## Secondary endpoints
- normalized-answer disagreement;
- benchmark correctness-status disagreement;
- correct→incorrect / incorrect→correct counts;
- token-level first-divergence position;
- SHA-256 equality of raw decoded answer strings;
- runtime and peak GPU memory.

## Inference
100,000 stratified bootstrap resamples within model × dataset cells, seed 20260919. Report 95% percentile intervals.

## Reporting rule
Every condition, including zero/null cells, is reported. No configuration may be selected post hoc as the “main” result.

## Claim boundary
Only execution-path dependence under declared models/software/hardware may be claimed. No universal nondeterminism or Nature-main allocation-identity conclusion.
