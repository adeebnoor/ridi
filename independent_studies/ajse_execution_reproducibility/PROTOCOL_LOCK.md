# LLM-EXEC-REPRO-AJSE-v1 — public pre-output protocol lock

**Target journal:** Arabian Journal for Science and Engineering (Computer Science / Systems Engineering)

**Status:** independent clean-room study, locked before model generation.

## Research question

Do identical target prompts produce invariant model outputs under nominally deterministic greedy decoding when only the execution batch configuration changes?

The study is about computational reproducibility of inference. It does **not** study allocation identity, retrieval membership, RIDI, ranking turnover or any operational system from the Nature manuscript.

## Frozen models

- Qwen/Qwen2.5-7B-Instruct — revision `a09a35458c702b33eeacc393d103063234e8bc28`
- mistralai/Mistral-7B-Instruct-v0.3 — revision `c170c708c41dac9275d15a8fff4eca08d52bab71`
- allenai/OLMo-2-1124-7B-Instruct — revision `470b1fba1ae01581f270116362ee4aa1b97f4c84`
- microsoft/Phi-3.5-mini-instruct — revision `2fe192450127e6a83f7441aef6e3ca586c338b77`

No quantization and no model substitution after outcome inspection.

## Frozen datasets

- TIGER-Lab/MMLU-Pro — revision `b189ec765aa7ed75c8acfea42df31fdae71f97be`
- openai/gsm8k — revision `740312add88f781978c0658806c59bc2815b9866`

Neither dataset occurs in the Nature-main experimental panels.

## Sampling lock

Use 150 target items from the MMLU-Pro test split and 150 from the GSM8K test split, for 300 target prompts total.

Items are selected without model output by sorting eligible stable item identifiers by SHA-256 of `study_id|dataset|item_id|20260919` and taking the first 150 per dataset. The exact panel manifest and prompt hashes must be archived before GPU generation.

## Prompting

MMLU-Pro: present the question and labelled choices, request concise reasoning, and require a final line `Final answer: <letter>`.

GSM8K: present the problem, request concise step-by-step reasoning, and require a final line `Final answer: <number>`.

Prompts are fixed before generation and hashed byte-for-byte.

## Execution conditions

Each target prompt is generated under four conditions:

1. **solo-1** — target alone, batch size 1;
2. **solo-2** — an exact repeat of solo-1, serving as a within-condition negative control;
3. **batch4-near** — target in a batch of four with three predeclared prompts nearest in tokenized input length;
4. **batch4-long** — target in a batch of four with three predeclared prompts from the longest-length anchor pool, forcing a different padded tensor shape.

The target prompt bytes, target token IDs, attention-mask semantics, model revision, decoding rule and maximum generation length are unchanged across conditions. Co-batch prompts are not scored as target observations.

If a model requires left padding for batched decoder-only generation, that padding convention is held constant across both batch conditions and recorded. No post-output padding-side change is permitted.

## Generation lock

- greedy decoding; `do_sample=False`;
- seed 20260919;
- deterministic PyTorch algorithms requested;
- TF32 disabled;
- bfloat16 where supported by the pinned model;
- native chat template for each model;
- no quantization;
- MMLU-Pro max_new_tokens=96;
- GSM8K max_new_tokens=192;
- exact Python / torch / transformers / CUDA / GPU metadata recorded.

## Primary endpoints

For each model and dataset:

1. exact decoded-text disagreement of each alternative execution condition versus solo-1;
2. decision disagreement after a frozen task-specific answer extractor.

The predeclared negative-control rate is solo-2 versus solo-1.

A target with any output difference remains in the analysis; no inconvenient target may be removed after generation.

## Secondary endpoints

- first differing generated-token position;
- normalized textual disagreement;
- correctness change relative to benchmark gold;
- disagreement rate by input-length quartile;
- batch4-long minus batch4-near paired disagreement difference.

## Inference

Report all model × dataset × condition cells.

Primary summary: equal-dataset-weight disagreement rate for each model and execution condition, with 100,000 dataset-stratified bootstrap resamples, seed 20260919.

No minimum effect threshold is required for publication. A null result is retained. The study does not claim hardware universality from one GPU type.

## Claim boundary

The experiment can establish execution-configuration sensitivity for the exact pinned models, software stack and GPU runtime tested. It cannot establish that all deterministic LLM inference is non-reproducible, nor can it attribute a mismatch to a specific CUDA kernel without a separate mechanistic experiment.
