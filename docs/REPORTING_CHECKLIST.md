# Allocation Identity Reporting Checklist

This checklist is a practical reporting record for capacity-limited AI evaluations. It is not a journal mandate and does not replace domain-specific performance, fairness, safety or causal analysis.

## Minimum record

### 1. Decision object
State what can receive action: person, document, vulnerability, alert, hospital, case, grant, transaction, etc.

### 2. Capacity
Report `k`, a threshold or a budget. Say whether it is operationally real or only analytical.

### 3. Selection rule
Specify score direction, top-k/threshold logic, exclusions and deterministic tie handling.

### 4. Comparator
Define what changed between the two allocations: model version, data update, representation, policy, retriever, prompt, seed or time point.

### 5. Candidate universe
If using paired score tables, state whether the candidate universe is identical. If it changes, say so explicitly and use direct allocation comparison when appropriate.

### 6. Allocation identity
Report at each prespecified capacity:

- overlap;
- changed slots for equal-capacity allocations;
- RIDI or a justified alternative membership measure.

### 7. Conventional evaluation
Report the metrics appropriate to the field—performance, calibration, ranking quality, group fairness, robustness, safety or cost. Allocation identity complements these metrics; it does not replace them.

### 8. Controls
Use the strongest mechanism-matched control available: no-change, relabel, within-version, seed/retraining null, order-only, or another falsification condition.

### 9. Score-margin certificate
When paired score vectors are comparable, report `gamma_k`, `epsilon` and whether the sufficient condition `gamma_k > 2*epsilon` certifies zero turnover.

### 10. Downstream consequence
If the study claims that membership change matters, define the downstream outcome and temporal direction independently. Do not infer harm or benefit from turnover alone.

### 11. Identity-control budget
If turnover is constrained, state the utility-regret tolerance `eta` and how it was selected. Prefer prospective domain justification over post-hoc tuning.

### 12. Privacy
Do not publish protected identities merely to satisfy allocation reporting. Public reporting can use stable pseudonyms, hashes/commitments, aggregate turnover counts, or secure auditor-only mappings as appropriate.

### 13. Failures and protocol lineage
Retain null results, failed registered gates, implementation corrections and deviations from the original protocol.

## Suggested methods sentence

> We audited allocation identity at the prespecified capacity by reporting selected-set overlap, changed slots and RIDI alongside the domain’s conventional evaluation metrics; tie handling, comparator definition and controls were fixed as described below.

Adapt the sentence to the actual design rather than copying claims the study did not test.

## Suggested results sentence

> At capacity `k=___`, `___` of `___` selected identities were replaced (`RIDI=___`) while `___` remained in both allocations.

Only add claims about performance, fairness, harm, benefit or causality when those endpoints were separately evaluated.

## Machine-readable output

`ridi-audit` can generate a compact record directly:

```python
from ridi_audit import audit

report = audit(before, after, k=[10, 50, 100])
print(report.to_markdown())
```

For already-selected identity lists:

```python
from ridi_audit import compare_allocations

report = compare_allocations(before_ids, after_ids)
print(report.to_markdown())
```
