# RIDI in 60 seconds

RIDI audits **allocation identity**: who actually occupies a finite top-k action set before and after a score update or representation change.

## Install

```bash
git clone https://github.com/adeebnoor/ridi.git
cd ridi
python -m pip install .
```

## Python

```python
import pandas as pd
from ridi_audit import audit

before = pd.read_csv("examples/r0.csv")
after = pd.read_csv("examples/r1.csv")

report = audit(before, after, k=[3, 5])
print(report)
```

Expected output is a compact allocation audit containing, for each requested cutoff, the selected-set overlap, changed slots, RIDI and score-margin stability information.

## CLI

```bash
ridi-audit compare \
  --r0 examples/r0.csv \
  --r1 examples/r1.csv \
  --id-col id \
  --score-col score \
  --k 3 5
```

## Control turnover inside a utility budget

```bash
ridi-audit control \
  --r0 examples/r0.csv \
  --r1 examples/r1.csv \
  --k 5 \
  --eta 0.001
```

`eta=0.001` means the selected set may lose at most 0.1% of updated-score utility relative to the unconstrained updated top-k solution.

## Interpretation

RIDI answers **who changed?** It does not by itself establish harm, fairness, correctness or model superiority. Pair identity auditing with the performance, outcome and fairness checks appropriate to your application.
