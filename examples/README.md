# Minimal example

`r0.csv` and `r1.csv` contain the same ten candidate identities under two score states. Scores differ slightly and some local ordering changes.

## Python

```python
import pandas as pd
from ridi_audit import audit

before = pd.read_csv("examples/r0.csv")
after = pd.read_csv("examples/r1.csv")

report = audit(before, after, k=[3, 5])
print(report)

controlled = report.control(k=5, eta=0.001)
print(controlled)
```

## CLI

```bash
ridi-audit compare --r0 examples/r0.csv --r1 examples/r1.csv --k 3 5
ridi-audit control --r0 examples/r0.csv --r1 examples/r1.csv --k 5 --eta 0.001
```

The example is synthetic and demonstrates file format, API behavior and command behavior only. It is not evidence for the manuscript's empirical claims.
