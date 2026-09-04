# RIDI

## Allocation identity for capacity-limited AI

**Current manuscript:** **Identical audits can yield different AI decisions**

![version](https://img.shields.io/badge/ridi--audit-1.1.0-1f6feb) ![python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-3776ab) ![license](https://img.shields.io/badge/license-MIT-2ea44f) ![status](https://img.shields.io/badge/manuscript-prepared%20for%20submission-6f42c1)

> **Core result:** an audit can remain exactly unchanged while the finite identities receiving scarce slots change — and the downstream AI decision can change with them.

<p align="center">
  <img src="assets/ridi_graphical_abstract.svg" alt="RIDI graphical abstract: identical audits can yield different AI decisions" width="100%">
</p>

**Try it:** [60-second interactive experiment](https://ridi-research-lab.onrender.com/demo/) · [Quick Start](docs/QUICKSTART.md) · [Python API](docs/API.md) · [Paper page](paper/README.md) · [RAG preregistration](https://osf.io/txwdv/) · [CODECHECK request #208](https://github.com/codecheckers/register/issues/208)

> **Verification status — 4 Sep 2026:** the sealed EPSS numerical workflow has been reproduced by **two independent external executors** in separate environments. A targeted blind external regeneration of the central SciFact 275 case has reproduced the substantive `SUPPORTS → REFUTES` identity-substitution reversal on a distinct GPU/software stack. These are independent computational executions, not a CODECHECK certificate. The community request is registered; formal CODECHECK has not yet begun.

---

## Use RIDI in 30 seconds

### 1. Install

```bash
python -m pip install "git+https://github.com/adeebnoor/ridi.git"
```

### 2. First run — no files needed

```bash
ridi-audit demo
```

The built-in example is synthetic and is **not manuscript evidence**. It exists so a new user can see changed slots, overlap, RIDI, rank agreement and stability-certificate output immediately after installation.

### 3. Python — fully runnable

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

Move directly from measurement to control:

```python
controlled = report.control(k=5, eta=0.001)
print(controlled["avoidable_turnover_fraction"])
print(controlled["selected_ids"])
```

### Your own CSVs

```bash
ridi-audit compare \
  --r0 before.csv \
  --r1 after.csv \
  --k 10 50 100 \
  --out audit.json \
  --report audit.md
```

```bash
ridi-audit control \
  --r0 before.csv \
  --r1 after.csv \
  --k 100 \
  --eta 0.001
```

---

## What RIDI asks

Performance, calibration, group fairness and robustness remain necessary evaluation dimensions. RIDI asks one additional question for finite queues, shortlists, top-k action sets and context windows:

> **Which identities actually occupy the scarce slots, and is that membership identified by the reported audit?**

For equal-size selected sets `A` and `B`:

```text
RIDI(A, B) = 1 - |A ∩ B| / |A ∪ B|
```

For equal-capacity top-`k` sets with `Delta_k = k - |A ∩ B|` changed slots:

```text
RIDI = 2*Delta_k / (k + Delta_k)
```

RIDI is **not** a replacement for AUROC, precision, recall, nDCG, calibration or fairness. It makes realized membership change observable.

---

## Decisive preregistered RAG test

`RIDI-RAG-NATURE-v2` was preregistered before the registered language-model generation.

- **800 frozen queries:** Natural Questions 250, HotpotQA 250, FEVER 150, SciFact 150.
- Positive-qrel passages stayed at the **same ranks**.
- Only qrel-zero (**metric-zero**) identities were replaced from the same frozen top-100 pool.
- The complete relevance-grade-by-position vector remained identical.
- Precision@k, recall@k, nDCG@k, MRR@k and MAP@k remained identical.
- **24,500 real-data** and **72,000 synthetic** audit-equivalence checks produced zero mismatches.

| Outcome | Equal-dataset-weight macro |
|---|---:|
| Canonical-output change | **32.87%** |
| Benchmark-defined correctness divergence | **17.27%** |
| 95% stratified-bootstrap CI | **14.60–20.03%** |

Most benchmark-defined outcomes remained stable. The primary result estimates the prevalence of behavioral non-equivalence **inside an exactly audit-equivalent class**; it is not a claim of universal fragility or net harm.

### SciFact 275: same audit, different decision

The positive passage stays fixed at rank 1. Reference and identity-substituted contexts share the same relevance vector and registered metrics:

```text
[1,0,0,0,0,0,0,0,0,0]
precision@10 = 0.1000
recall@10    = 0.3333
nDCG@10      = 0.4693
MRR@10       = 1.0000
MAP@10       = 0.3333
```

Replacing nine metric-zero identities changes `SUPPORTS → REFUTES` (`RIDI=0.947`). The same-query order-only permutation retains `SUPPORTS` with identical membership (`RIDI=0`).

A targeted blind external regeneration on a distinct GPU/software stack reproduced the substantive pattern. Its reference text began `Verdict: SUPPORTS`, which the preregistered strict first-token parser labelled unparseable even though the semantic verdict was explicit. The raw discrepancy is retained transparently rather than silently changing the registered parser.

---

## Production stress test: EPSS

A real EPSS v2→v3 update replaced **565 of the top 1,000** remediation priorities (`RIDI=0.722`), versus **0** and **7** in adjacent same-version controls.

The locked EPSS numerical workflow has been reproduced by **two independent external executors** in separate environments. Delayed CISA KEV evidence is sparse and cutoff-dependent, so turnover is not equated with harm or benefit.

---

## From observability to control

The exact **identity–utility frontier** computes the minimum membership change compatible with an explicit updated-score utility-regret budget, using stored scores and **no retraining**.

- **GraphSAGE:** at `eta=0.001`, changed slots **31.1 → 13.3**; **78.8%** avoidable turnover (95% CI **76.0–81.4%**).
- **Text retrieval:** at `k=100`, changed documents **45.8 → 33.3**; **28.7%** avoidable (95% CI **27.6–29.7%**).
- **EPSS:** at `eta=0.0001`, **14.34%** of turnover is avoidable while retaining **12/12** delayed KEV positives; at `eta=0.001`, more turnover is avoided but only **10/12** are retained.

The exact frontier is **Main Fig. 3** in the current manuscript.

---

## Scientific boundaries

Allocation identity measures **who receives finite action** and how that set changes. It does not by itself establish correctness, fairness, causal harm, clinical benefit or model superiority.

- RAG qrels are incomplete; qrel-zero passages are called **metric-zero**, not semantically irrelevant.
- Correctness is benchmark-defined; flips are bidirectional and no net-harm claim is made.
- Confirmatory generators are deterministic open-weight 7–8B models rather than hosted frontier systems.
- EPSS downstream-value evidence is sparse and cutoff-dependent.
- Registered RxNorm and Open Targets failures are retained as claim boundaries rather than converted into positive evidence.
- Sufficiently fine or explicitly identity-aware audits can recover membership and escape non-identification.

---

## Reproducibility and documentation

- [Quick Start](docs/QUICKSTART.md)
- [Python API](docs/API.md)
- [Documentation index](docs/README.md)
- [Methods](docs/METHODS.md)
- [Reproducibility guide](docs/REPRODUCIBILITY.md)
- [Current results at a glance](docs/RESULTS_AT_A_GLANCE.md)
- [FAQ](docs/FAQ.md)
- [RAG preregistration](https://osf.io/txwdv/)
- [Community CODECHECK request #208](https://github.com/codecheckers/register/issues/208)

The CODECHECK request is registered, but formal checking has not yet begun and **no certificate is claimed**.

## Citation

If you use RIDI or `ridi-audit`, please cite the software using [`CITATION.cff`](CITATION.cff) and the accompanying manuscript when a public bibliographic record is available.

## Author

**Adeeb Noor**  
Department of Information Technology, Faculty of Computing and Information Technology  
King Abdulaziz University, Jeddah, Saudi Arabia  
ORCID: 0000-0002-8251-1853
