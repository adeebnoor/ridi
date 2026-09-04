# Examples

These examples are intentionally small and synthetic. They demonstrate API behavior and file formats; they are **not evidence for the manuscript’s empirical claims**.

## 1. Selected identities only

```python
from ridi_audit import compare_allocations

before = ["doc-1", "doc-2", "doc-3", "doc-4"]
after  = ["doc-1", "doc-2", "doc-9", "doc-4"]

print(compare_allocations(before, after))
```

Use this pattern for RAG contexts, shortlists, alert queues or any pipeline that already exposes the selected IDs.

## 2. Paired score tables

`r0.csv` and `r1.csv` contain the same ten candidate identities under two score states.

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

## 3. CLI

```bash
ridi-audit demo
ridi-audit compare --r0 examples/r0.csv --r1 examples/r1.csv --k 3 5
ridi-audit control --r0 examples/r0.csv --r1 examples/r1.csv --k 5 --eta 0.001
```

## Research recipes

For RAG, model/data updates, remediation queues and shortlist comparisons, see [`docs/USE_CASES.md`](../docs/USE_CASES.md). For a publication-ready minimum record, see [`docs/REPORTING_CHECKLIST.md`](../docs/REPORTING_CHECKLIST.md).
