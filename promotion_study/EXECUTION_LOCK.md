# EXECUTION LOCK — EVAL-RANK-JKSUCIS-v1

Frozen before endpoint generation.

## Model revisions
- Qwen/Qwen2.5-3B-Instruct: `aa8e72537993ba99e69dfaafa59ed015b17504d1`
- microsoft/Phi-3.5-mini-instruct: `2fe192450127e6a83f7441aef6e3ca586c338b77`
- HuggingFaceTB/SmolLM2-1.7B-Instruct: `31b70e2e869a7173562077fd711b654946d38674`

## Dataset revisions
- tau/commonsense_qa: `94630fe30dad47192a8546eb75f094926d47e155`
- allenai/openbookqa: `388097ea7776314e93a529163e0fea805b8a6454`
- Rowan/hellaswag: `218ec52e09a7e7462a5400043bb9a69a41d06b76`
- google/boolq: `35b264d03638db9f4ce671b711558bf7ff0f80d5`

These revisions were resolved before any model generation for this study.

## Runtime constraints
The run must abort if any revision differs from this lock.
One raw generation per model/item is shared by all evaluators.
No Nature-main or AJSE empirical output may be imported.
