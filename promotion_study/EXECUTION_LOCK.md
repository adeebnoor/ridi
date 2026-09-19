# EXECUTION LOCK — LLM-EXEC-REPRO-AJSE-v1

Frozen before endpoint generation.

## Model revisions
- Qwen/Qwen2.5-7B-Instruct: `a09a35458c702b33eeacc393d103063234e8bc28`
- mistralai/Mistral-7B-Instruct-v0.3: `c170c708c41dac9275d15a8fff4eca08d52bab71`

## Dataset revisions
- TIGER-Lab/MMLU-Pro: `b189ec765aa7ed75c8acfea42df31fdae71f97be`
- openai/gsm8k: `740312add88f781978c0658806c59bc2815b9866`
- allenai/ai2_arc: `210d026faf9955653af8916fad021475a3f00453`
- truthfulqa/truthful_qa: `741b8276f2d1982aa3d5b832d3ee81ed3b896490`

These revisions were resolved before any model generation for this study.

## Runtime constraints
The run must abort if any model or dataset revision differs from this lock.
No quantization.
No Nature-main benchmark/data/result may be imported.


## Frozen sample manifest

The 600-target panel was frozen before any generation.

- MMLU-Pro: population 12,032; selected 150; selected-manifest SHA-256 `8507196db29ea8a1f470245d65ae71a7a917ec95cb45db3eaed77427619afd77`
- GSM8K: population 1,319; selected 150; SHA-256 `d1326d2138bd189f90d9966497373e1a9da9c001e8f536af167393c779d66f11`
- ARC-Challenge: population 1,172; selected 150; SHA-256 `65ea6957753ff6f9a83a5ccda41bad7b70540eee449e77f5a7f2fa4b069e46db`
- TruthfulQA multiple-choice: population 817; selected 150; SHA-256 `55a5578ac2b64e2ffaa3932d30062030c1c22d9d9b731ac59ff9302dded221e1`
- top-level frozen-manifest SHA-256 `fe9254c1e0117eefdca85d4ccf09c9529caad7d544425d3e24225dbcf48e880e`

Reconstruction rule: derive the study-defined stable ID and canonical row SHA-256 for every row, sort by stable ID, then select 150 without replacement using NumPy `default_rng(20260919)`. The same RNG instance is advanced dataset-by-dataset in the protocol order MMLU-Pro, GSM8K, ARC-Challenge, TruthfulQA. The runner must reproduce every per-dataset hash above before loading either language model.