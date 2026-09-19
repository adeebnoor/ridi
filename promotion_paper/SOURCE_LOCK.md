# SOURCE LOCK — JKSUCIS-EVALUATOR-RELIABILITY-v1

Locked before any model output.

Nature-panel datasets are prohibited.

Primary benchmark sources:
- TIGER-Lab/MMLU-Pro: test split, 12,032 examples; data-upload lineage 24ac2da. Sample 200 by frozen seed.
- lukaemon/bbh: parquet conversion 982bb89. Predeclared subsets: date_understanding, disambiguation_qa, logical_deduction_five_objects, sports_understanding. Retain all 250 rows per subset and stratify by task.
- allenai/openbookqa: main/test, parquet conversion 388097e. Sample 200 by frozen seed.
- TruthfulQA multiple-choice static source if a clean immutable mirror is frozen before generation; otherwise use allenai/winogrande winogrande_xl validation, parquet conversion 01e7417, with the fallback declared before any output.

Every downloaded source file and selected panel must receive a SHA-256 content hash before generation. Mutable 'main' branches are not accepted as the execution lock.

No Nature result, output, figure, or score is an input.
