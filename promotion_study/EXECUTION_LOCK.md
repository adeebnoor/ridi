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
