# RIDI in 60 seconds

RIDI audits **allocation identity**: who actually occupies a finite top-k action set before and after a score update or other controlled system change.

## Install

One command from GitHub:

```bash
python -m pip install "git+https://github.com/adeebnoor/ridi.git"
```

## First run — no files needed

```bash
ridi-audit demo
```

This runs a built-in synthetic audit and prints changed slots, overlap, RIDI, global Spearman agreement and the sufficient stability-certificate status. The demo is explicitly synthetic and is **not manuscript evidence**.

## Python

A fully runnable example:

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

## Input contract

Both CSV/DataFrame inputs need:

```text
id,score
candidate_1,0.913
candidate_2,0.702
...
```

They must contain the same unique candidate identities; row order may differ.

## Development install

```bash
git clone https://github.com/adeebnoor/ridi.git
cd ridi
python -m pip install -e ".[dev]"
pytest -q
```

## Interpretation

RIDI answers **who changed?** It does not by itself establish harm, fairness, correctness or model superiority. Pair identity auditing with the performance, outcome and fairness checks appropriate to your application.

For the complete API, see [API.md](API.md).
