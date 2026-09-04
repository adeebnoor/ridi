# Use RIDI in your pipeline

RIDI is intentionally framework-agnostic. If a system produces a finite set of identities—or a candidate table with identities and scores—you can audit allocation identity without retraining the model.

## RAG / retrieval

```python
from ridi_audit import compare_allocations

reference_doc_ids = [doc.id for doc in reference_hits[:10]]
updated_doc_ids = [doc.id for doc in updated_hits[:10]]

report = compare_allocations(reference_doc_ids, updated_doc_ids)
print(report)
```

Report RIDI alongside retrieval quality metrics such as recall, nDCG or MRR. RIDI answers which documents changed, not whether the retrieved evidence is correct.

## Model or data update with a top-k queue

```python
import pandas as pd
from ridi_audit import audit

before = pd.DataFrame({"id": case_ids, "score": scores_v1})
after = pd.DataFrame({"id": case_ids, "score": scores_v2})

report = audit(before, after, k=[50, 100, 500])
print(report)
```

This pattern applies to vulnerability remediation, clinical alert review, fraud investigation, inspection, hiring, grants, moderation and other capacity-limited queues.

## Compare two shortlists when scores are unavailable

```python
from ridi_audit import compare_allocations

report = compare_allocations(shortlist_a, shortlist_b)
print(report.to_markdown())
```

The direct allocation API does not require a common candidate universe or score vectors. For equal-size lists it also reports changed slots.

## Bound avoidable turnover

When paired score vectors are available:

```python
controlled = report.control(k=100, eta=0.001)
print(controlled["avoidable_turnover_fraction"])
print(controlled["selected_ids"])
```

The identity–utility frontier asks how much membership change is necessary when updated-score utility may lose at most the declared regret budget `eta`.

## What to report in a paper

At minimum, state:

1. the decision object and operational capacity;
2. the selection rule and tie handling;
3. the comparator (model/data/policy/version/representation);
4. overlap, changed slots and RIDI;
5. the conventional performance/fairness metrics relevant to the domain;
6. appropriate controls;
7. downstream outcome evidence when it is actually tested.

See the [Allocation Identity Reporting Checklist](REPORTING_CHECKLIST.md) for a publication-ready record.

## Scientific boundary

A non-zero RIDI establishes that realized membership changed. It does not by itself establish harm, benefit, unfairness, instability of every downstream output, or superiority of one system.
