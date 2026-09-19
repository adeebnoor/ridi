# PRE-OUTPUT AMENDMENT 1 — JKSUCIS-EVALUATOR-RELIABILITY-v1

Timing: before any model generation or evaluator endpoint.

The original protocol listed GPQA conditionally. The official GPQA Hugging Face repository requires acceptance of gated access conditions. To avoid introducing an access-dependent sample and to keep the study immediately reproducible, GPQA is removed BEFORE any output is generated.

The four frozen benchmark families are now:
1. TIGER-Lab/MMLU-Pro — test; data upload lineage 24ac2da (current repository metadata may advance independently).
2. lukaemon/bbh — parquet BIG-Bench Hard tasks; conversion commit 982bb89. Four predeclared task subsets will be used: date_understanding, disambiguation_qa, logical_deduction_five_objects, and sports_understanding; all 250 rows from each subset are retained, and task is a stratification variable.
3. allenai/openbookqa — main/test; parquet conversion commit 388097e; all 500 rows are eligible and 200 are sampled outcome-blind.
4. TruthfulQA multiple-choice — use a fixed Apache-2.0 parquet/csv mirror whose exact source bytes are hashed before generation; if no clean static mirror can be frozen, TruthfulQA is replaced before generation by allenai/winogrande (winogrande_xl validation; parquet commit 01e7417).

No primary endpoint, evaluator definition, bootstrap plan, or Nature firewall changes.
