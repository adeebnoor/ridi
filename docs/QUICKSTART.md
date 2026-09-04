# RIDI in 60 seconds

RIDI audits **allocation identity**: who actually occupies a finite action set before and after a system change.

[Open the runnable notebook in Colab](https://colab.research.google.com/github/adeebnoor/ridi/blob/main/notebooks/RIDI_60_Second_Experiment.ipynb)

## Install

```bash
pip install ridi-audit
```

PyPI: https://pypi.org/project/ridi-audit/

## Fastest path: you already have two selected lists

```python
from ridi_audit import compare_allocations

before = ["doc-1", "doc-2", "doc-3", "doc-4"]
after  = ["doc-1", "doc-2", "doc-9", "doc-4"]

report = compare_allocations(before, after)
print(report)
```

Output:

```text
RIDI Allocation Comparison
--------------------------
Before size:   4
After size:    4
Overlap:       3
Changed slots: 1
RIDI:          0.400000
```

That is enough for RAG contexts, shortlists, alert queues and other pipelines that already expose selected identity lists.

## Score-table path

Use `audit()` when you have the same candidate universe with paired scores.

```python
import pandas as pd
from ridi_audit import audit

before = pd.DataFrame({
    "id": ["a", "b", "c", "d", "e", "f"],
    "score": [0.99, 0.94, 0.90, 0.85, 0.81, 0.76],
})
after = pd.DataFrame({
    "id": ["a", "b", "c", "d", "e", "f"],
    "score": [0.98, 0.93, 0.72, 0.86, 0.80, 0.89],
})

report = audit(before, after, k=[3, 5])
print(report)
```

Move directly from measurement to minimum-turnover control:

```python
controlled = report.control(k=5, eta=0.001)
print(controlled["avoidable_turnover_fraction"])
print(controlled["selected_ids"])
```

## Zero-file CLI demo

```bash
ridi-audit demo
```

The built-in demo is synthetic and is **not manuscript evidence**. It exists so a new user can inspect changed slots, overlap, RIDI, rank agreement and the stability certificate immediately after installation.

## Your own CSVs

```bash
ridi-audit compare \
  --r0 before.csv \
  --r1 after.csv \
  --id-col id \
  --score-col score \
  --k 10 50 100
```

Control turnover inside a utility budget:

```bash
ridi-audit control \
  --r0 before.csv \
  --r1 after.csv \
  --k 100 \
  --eta 0.001
```

`eta=0.001` means the selected set may lose at most 0.1% of normalized updated-score utility relative to the unconstrained updated top-k solution.

## Development install

```bash
git clone https://github.com/adeebnoor/ridi.git
cd ridi
python -m pip install -e ".[dev]"
pytest -q
```

## Interpretation

RIDI answers **who changed?** It does not by itself establish harm, fairness, correctness or model superiority. Pair allocation-identity auditing with the performance, outcome and fairness checks appropriate to your application.

Next: [Use cases](USE_CASES.md) · [Python API](API.md) · [Reporting checklist](REPORTING_CHECKLIST.md) · [Evidence](../paper/README.md)
