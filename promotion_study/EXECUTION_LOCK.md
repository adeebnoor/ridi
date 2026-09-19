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


## Frozen sample manifest

The 1,000-item panel was frozen before any model generation.

- CommonsenseQA: population 1,221; selected 250; selected-manifest SHA-256 `1c03091e297f8b046bc00a9d9b038a51336df0ee9295fd33cb3b84ed2168cbc7`
- OpenBookQA: population 500; selected 250; SHA-256 `362801e4353ac9a4cc911a5cca9f8bb9fff8a61bbf57fd4a5b400c04aaf1bb43`
- HellaSwag: population 10,042; selected 250; SHA-256 `00ef02b156210ce9201508e7d77e28c97774f5d54388e32f11423673e554d816`
- BoolQ: population 3,270; selected 250; SHA-256 `e08437f808e9a8fe9c9f8c5aca6cea30875c5560ba3500c2c5529183608b440c`
- top-level frozen-manifest SHA-256 `e5312700b428fc11ce3edb5e6e2a5efe4f86e31335be705b954e4e769b1962a3`

Reconstruction rule: derive the study-defined stable ID and canonical row SHA-256 for every row, sort by stable ID, then select 250 without replacement using NumPy `default_rng(20260919)`. The same RNG instance is advanced dataset-by-dataset in the protocol order CommonsenseQA, OpenBookQA, HellaSwag, BoolQ. The runner must reproduce every per-dataset hash above before loading a model.

## Frozen generation path and evaluator code

- generation batch size: **1** for every model/item;
- one raw generation per model/item is reused by all five evaluators;
- greedy decoding, max_new_tokens=96, seed=20260919;
- evaluator implementation is frozen in `promotion_study/evaluators.py` before any endpoint generation;
- evaluator unit tests must pass before execution;
- unresolved evaluator outputs count as incorrect for benchmark accuracy and are also reported separately.

The evaluation treatment never triggers regeneration, so evaluator comparisons operate on byte-identical raw model output.
