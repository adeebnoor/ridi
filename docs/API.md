# Python API

RIDI has two researcher-facing entry points. Use the lightest one that matches the data your pipeline already exposes.

## 1. Selected identities only — `compare_allocations`

If you already have the finite sets that received action, this is the shortest path.

```python
from ridi_audit import compare_allocations

reference = ["doc-17", "doc-4", "doc-92", "doc-31"]
alternative = ["doc-17", "doc-4", "doc-11", "doc-31"]

report = compare_allocations(reference, alternative)
print(report)
```

Typical output:

```text
RIDI Allocation Comparison
--------------------------
Before size:   4
After size:    4
Overlap:       3
Changed slots: 1
RIDI:          0.400000
```

This works directly for retrieved-document IDs, shortlists, alert queues, remediation lists or any other realized finite allocation. The two lists may have different sizes; `changed_slots` is defined only when capacity is equal.

Useful methods and attributes:

```python
report.ridi
report.overlap
report.changed_slots
report.removed_ids
report.added_ids
report.to_dict()
report.to_markdown()
```

## 2. Candidate scores — `audit`

Use `audit` when you have the same candidate universe scored before and after a model, data, policy or representation change.

```python
import pandas as pd
from ridi_audit import audit

before = pd.read_csv("before.csv")
after = pd.read_csv("after.csv")
report = audit(before, after, k=[10, 50, 100])
print(report)
```

### `audit(before, after, *, k, id_col="id", score_col="score")`

Rows may appear in different orders. Candidate identities are aligned deterministically by `id_col`.

### `AuditReport`

```python
result_dict = report.to_dict()
markdown = report.to_markdown()
controlled = report.control(k=100, eta=0.001)
```

Important attributes:

- `report.n_candidates`
- `report.global_spearman`
- `report.cutoffs`

Each cutoff contains:

- `k`
- `ridi`
- `changed_slots`
- `overlap`
- `gamma_k`
- `epsilon`
- `margin_certified`

## Identity control

`report.control(k=..., eta=...)` returns the exact minimum-turnover selected set satisfying the declared updated-score utility-regret budget.

Returned fields include:

- `eta`
- `j_eta`
- `delta_unconstrained`
- `avoidable_turnover_fraction`
- `utility`
- `utility_star`
- `utility_regret`
- `ridi_unconstrained`
- `ridi_controlled`
- `selected_ids`

## Low-level API

Advanced users may import:

```python
from ridi_audit import (
    audit_scores,
    deterministic_topk,
    margin_certificate,
    ridi,
    identity_utility_frontier,
    select_identity_control,
)
```

Use `compare_allocations` for realized identity lists and `audit` for full score tables. The low-level functions are intended for custom research workflows.

## Scope

The software audits membership change and score-boundary stability. It does not infer causal harm, fairness, correctness or benefit from RIDI alone.
