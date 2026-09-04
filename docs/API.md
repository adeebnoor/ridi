# Python API

## High-level entry point

```python
from ridi_audit import audit
```

### `audit(before, after, *, k, id_col="id", score_col="score")`

Audits allocation identity between two pandas DataFrames containing the same candidate universe.

```python
import pandas as pd
from ridi_audit import audit

before = pd.read_csv("before.csv")
after = pd.read_csv("after.csv")
report = audit(before, after, k=[10, 50, 100])
```

Rows may appear in different orders. Candidate identities are aligned deterministically by `id_col`.

### `AuditReport`

```python
print(report)
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

The high-level API is recommended for ordinary use because it handles table alignment and preserves the aligned inputs for downstream control.

## Scope

The software audits membership change and score-boundary stability. It does not infer causal harm, fairness, correctness or benefit from RIDI alone.
