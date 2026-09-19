# LLM-EXEC-REPRO-AJSE-v1 — PRE-OUTPUT PROTOCOL LOCK

Target journal: **Arabian Journal for Science and Engineering**

Status: protocol fixed before any endpoint generation for this study.

## Research question

Do nominally deterministic large-language-model generations remain invariant when the target prompt is unchanged but the execution path changes through batching and batch composition?

## Models

Primary models:
1. `Qwen/Qwen2.5-7B-Instruct`, immutable revision `a09a35458c702b33eeacc393d103063234e8bc28`.
2. `mistralai/Mistral-7B-Instruct-v0.3`, immutable revision `c170c708c41dac9275d15a8fff4eca08d52bab71`.

An optional third-model sensitivity may be added only if its exact revision and access are frozen in a pre-output amendment. It cannot replace either primary model or redefine the primary endpoints.

## Benchmarks — all outside Nature main

- MMLU-Pro
- GSM8K
- ARC-Challenge
- TruthfulQA multiple-choice

No NQ, HotpotQA, FEVER or SciFact item may enter this study.

## Frozen sample

Primary target: 150 items per benchmark = 600 prompts per model.

Sampling must be deterministic and outcome-blind:
- use the designated public evaluation split;
- derive a stable item identifier;
- sort by identifier;
- sample with NumPy `default_rng(20260919)`;
- save the complete selected-ID manifest and SHA-256 before generation.

No item may be removed based on model output.

## Prompting

A single task-family template is frozen before generation. The model may provide concise reasoning, but the final decision must appear on a dedicated last line beginning `FINAL:`.

Generation:
- native chat template;
- greedy decoding (`do_sample=False`);
- max_new_tokens = 96;
- seed = 20260919;
- no quantization;
- bfloat16 where supported;
- PyTorch deterministic algorithms enabled;
- TF32 disabled;
- `CUBLAS_WORKSPACE_CONFIG=:4096:8`;
- exact software/GPU environment recorded.

The same tokenized target prompt must be used across compared execution conditions.

## Execution conditions

For every target prompt:

A. **Isolated**: target generated alone, batch size 1.

B. **Length-matched batch**: target generated in a fixed batch of 8 with seven outcome-blind companion prompts from the same benchmark chosen to minimize absolute token-length difference.

C. **Mixed-length batch**: target generated in a fixed batch of 8 with seven outcome-blind companions spanning predeclared token-length quantiles.

D. **Mixed-length reversed order**: exact same eight prompts as C, reversed batch order.

Each condition is run twice. Duplicate runs test within-path repeatability and are not averaged away.

Companion selection is frozen from prompt token lengths before any generation.

## Primary endpoints

1. **Exact-text execution divergence**: fraction of target prompts whose decoded completion differs byte-for-byte between A and C while both within-condition duplicates are internally identical.

2. **Final-decision execution divergence**: fraction whose frozen `FINAL:` decision differs between A and C under the task-specific scorer, again requiring within-condition duplicate stability.

## Secondary endpoints

- A vs B, A vs D, C vs D divergence;
- normalized-text divergence;
- within-path repeatability failure rate;
- divergence by benchmark and model;
- association with prompt length and companion-length dispersion;
- correctness transition counts where gold labels permit scoring.

## Statistical analysis

- report every model × benchmark cell, including zero or adverse findings;
- equal-benchmark macro rates per model;
- pooled rates as secondary only;
- 100,000 prompt-level stratified bootstrap replicates within benchmark, seed `20260919`;
- paired bootstrap for condition differences;
- no query/item exclusion after generation;
- no claim of universal nondeterminism from two models or four benchmarks.

A result is scientifically interpretable even if exact-text divergence occurs without decision divergence; the two are distinct endpoints.

## Claim boundary

This study concerns reproducibility under specified transformers/PyTorch GPU execution paths. It does not establish instability for every serving stack, proprietary API, hardware architecture or decoding regime.

## Anti-selection rule

No new execution condition, model, benchmark, parser or threshold may be promoted to primary after endpoint output is visible. Any later sensitivity must be labeled post hoc.
