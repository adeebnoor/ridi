# RIDI — measure and budget selection change in ranking updates

> **Research + open-source audit toolkit.** RIDI measures how much a ranking update changes the selected items and computes the **exact minimum turnover compatible with a declared rank-utility budget**.

[![tests](https://github.com/adeebnoor/ridi/actions/workflows/tests.yml/badge.svg)](https://github.com/adeebnoor/ridi/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/ridi-audit.svg)](https://pypi.org/project/ridi-audit/)
![python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-3776ab)
![license](https://img.shields.io/badge/license-MIT-2ea44f)
![status](https://img.shields.io/badge/manuscript-working%20version-6f42c1)

<p align="center">
  <a href="./"><b>Project page</b></a> ·
  <a href="demo/"><b>SciFact demo</b></a> ·
  <a href="https://pypi.org/project/ridi-audit/"><b>PyPI</b></a> ·
  <a href="https://osf.io/txwdv/"><b>RAG preregistration</b></a> ·
  <a href="paper/README.md"><b>Paper & evidence</b></a>
</p>

---

## The problem

A ranking system can be updated while its summary evaluation remains stable or improves. But a team acts on a **finite selection**: passages in a context window, vulnerabilities in a review queue, documents in a shortlist, or relationships proposed for follow-up.

RIDI asks two questions that aggregate scores do not answer:

1. **What changed in the selected set?**
2. **How much of that change was actually required by the updated scoring objective?**

The first is a measurement problem. The second is a constrained optimization problem.

---

## The constructive result: the identity–utility frontier

For a baseline top-k set and updated scores, RIDI computes the best attainable updated-score utility for every possible number of replacements. The exact optimum with exactly `j` outsiders is obtained by retaining the highest-ranked incumbents and adding the highest-ranked outsiders. Sorted prefix sums evaluate the full trade-off curve in `O(n log n)` time, dominated by sorting.

Given a declared relative utility-loss tolerance `eta`, the frontier returns the **minimum number of replacements** compatible with that budget.

```python
import pandas as pd
from ridi_audit import audit

before = pd.read_csv("before.csv")
after = pd.read_csv("after.csv")

report = audit(before, after, k=[10, 50, 100])
controlled = report.control(k=100, eta=0.001)
```

The resulting avoidable-turnover fraction is conditional on the stated objective and tolerance. It is **not** a claim that preserving old selections is always desirable.

---

## Measuring selection identity

Already have two selected lists?

```python
from ridi_audit import compare_allocations

reference = ["doc-1", "doc-2", "doc-3", "doc-4"]
updated   = ["doc-1", "doc-2", "doc-9", "doc-4"]

print(compare_allocations(reference, updated))
```

For equal-size selected sets `A` and `B`, RIDI reports changed slots and the Jaccard distance:

```text
RIDI(A, B) = 1 - |A ∩ B| / |A ∪ B|
```

RIDI complements conventional evaluation; it does not replace AUROC, precision, recall, nDCG, calibration, robustness, safety or fairness.

---

## Evidence behind the research program

### 1) Exact evaluation equality can leave membership unresolved

A preregistered retrieval experiment held a fixed language model and the **complete assessed relevance-grade sequence** constant while replacing only passages that earned zero credit under the benchmark audit. Thus `precision@k`, `recall@k`, `nDCG@k`, `MRR@k` and `MAP@k` were numerically identical.

- **800 frozen queries** across Natural Questions, HotpotQA, FEVER and SciFact.
- Primary benchmark-defined correctness-change rate: **17.27%** (95% stratified-bootstrap interval **14.60–20.03%**, equal weight across datasets).
- Direction: **60 correct→incorrect** and **74 incorrect→correct**; this is not a net-harm claim.
- Order-only control with unchanged membership: **4.80%**.
- For none of the 800 primary queries did the grade-by-position audit uniquely identify passage membership; the median number of compatible passage sets exceeded **10¹²**.

This experiment does **not** claim to discover that context matters. Prior work already established context sensitivity and imperfect alignment between retrieval metrics and downstream accuracy. The narrower result is that **exact equality in the tested audit does not identify the evidence or certify behavioral equivalence**.

A post hoc formatting sensitivity rescored all 300 FEVER/SciFact primary queries under two declared prefix-tolerant rules. Both rules agreed: **53 classification correctness changes** (two-dataset mean **17.67%**) versus **58** (**19.33%**) under the registered strict parser. The registered four-dataset endpoint remains unchanged. No longer-generation sensitivity has yet been completed.

### 2) A production update changed scarce priorities

For the EPSS v2→v3 production update:

- **565 / 1,000** priorities changed (`RIDI=0.722`).
- Adjacent same-version controls changed **0** and **7** slots.
- Subsequent KEV hits at the primary cutoff increased from **8 to 12**, while full-pool AUROC decreased from **0.665 to 0.610**.
- At a **0.01%** rank-utility tolerance, the exact frontier avoided **14.34%** of replacements while retaining all **12** later KEV hits.
- At **0.1%**, **40.88%** were avoided but only **10/12** later KEV hits were retained.

These sparse retrospective outcomes do not establish causal benefit. They show why the utility budget and downstream outcome must both remain visible.

### 3) Avoidable turnover differs across domains

At a locked **0.1%** rank-utility budget:

- **GraphSAGE / biomedical knowledge graph:** mean avoidable turnover **78.8%** (95% interval **76.0–81.4%**).
- **20 Newsgroups retrieval, k=100:** mean avoidable turnover **28.7%** (95% interval **27.6–29.7%**).

The contrast is the point: how much churn an update requires is measured rather than assumed.

Exploratory drug-interaction and medication-context analyses are retained as boundary tests, not as clinical validation. No patient harm, delivered-alert effect or clinical interchangeability claim is made.

---

## Verification boundaries

- The sealed EPSS numerical workflow was reproduced by **two external executors** in separate environments.
- Both executors performed targeted blind regeneration of the illustrative SciFact 275 case.
- Hamdan's disclosed Q4_K_M serving path reproduced a strict-scored correctness change.
- Ossard used the pinned Qwen3-8B Hugging Face revision; his reference began `Verdict: SUPPORTS` and was rejected by the frozen strict parser, so his run reproduced the substantive SUPPORTS→REFUTES contrast but **not** the strict-scored correctness change.
- These targeted checks do **not** independently replicate the aggregate 800-query endpoint.
- **No formal CODECHECK certificate has been issued.** Register issue #208 was closed with an invitation to return once a public preprint is available or the manuscript is under journal review.

[Evidence and manuscript synopsis →](paper/README.md)

---

## Current manuscript direction

**Working title:** *Measuring and controlling what changes when a ranking system is updated*

The current frontier-led working manuscript treats the RAG experiment as evidence that evaluation equality can leave selection identity unresolved, then makes the constructive contribution central: the **identity–utility frontier** provides an exact, auditable budget for selection turnover.

The working manuscript is **not peer reviewed, accepted or published**. Registered failures (RxNorm and Open Targets), parser limitations, sparse EPSS outcomes and exploratory clinical boundaries are retained in the research record.

---

## Install

```bash
pip install ridi-audit
ridi-audit demo
```

Resources:

- [60-second Quick Start](docs/QUICKSTART.md)
- [Python API](docs/API.md)
- [Use cases](docs/USE_CASES.md)
- [Allocation Identity Reporting Checklist](docs/REPORTING_CHECKLIST.md)
- [Reproducibility guide](docs/REPRODUCIBILITY.md)
- [RAG preregistration](https://osf.io/txwdv/)
- [CODECHECK register issue #208](https://github.com/codecheckers/register/issues/208)

---

## Citation

If you use RIDI or `ridi-audit`, cite the software through [`CITATION.cff`](CITATION.cff) and cite the accompanying manuscript when a public bibliographic record becomes available.

**Adeeb Noor**  
Department of Information Technology, Faculty of Computing and Information Technology  
King Abdulaziz University, Jeddah, Saudi Arabia  
ORCID: 0000-0002-8251-1853
