# RIDI

## Allocation identity for capacity-limited AI

**Current manuscript:** **Identical audits can yield different AI decisions**  
**Status:** manuscript prepared for journal submission; not peer reviewed, accepted or published.

> **Core result:** an audit can remain exactly unchanged while the finite identities receiving scarce slots change — and the downstream AI decision can change with them.

**60-second experiment:** https://ridi-research-lab.onrender.com/demo/  
**Paper page:** [paper/README.md](paper/README.md)  
**RAG preregistration:** https://osf.io/txwdv/  
**Community CODECHECK request:** https://github.com/codecheckers/register/issues/208

> **Verification status (4 Sep 2026):** the sealed EPSS numerical workflow has been reproduced by two independent external executors in separate environments. A targeted blind external regeneration of the central SciFact 275 RAG case has also reproduced the substantive `SUPPORTS → REFUTES` identity-substitution reversal on a distinct GPU/software stack. These are independent computational executions, not a CODECHECK certificate. The community request is registered; formal CODECHECK has not yet begun.

---

## The missing audit object

Performance, calibration, group fairness and robustness remain necessary evaluation dimensions. For a capacity-limited system, RIDI asks one additional question:

> **Which identities actually occupy the scarce slots, and is that membership identified by the reported audit?**

For equal-size selected sets `A` and `B`:

```text
RIDI(A, B) = 1 - |A ∩ B| / |A ∪ B|
```

For equal-capacity top-`k` sets with `Delta_k = k - |A ∩ B|` changed slots:

```text
RIDI = 2*Delta_k / (k + Delta_k)
```

RIDI is **not** a replacement for AUROC, precision, recall, nDCG, calibration or fairness metrics. It makes realized membership change directly observable.

---

## Decisive preregistered RAG test

`RIDI-RAG-NATURE-v2` was preregistered before the registered language-model generation.

- 800 frozen queries: Natural Questions 250, HotpotQA 250, FEVER 150, SciFact 150.
- Every positive-qrel passage stayed at the same rank.
- Only qrel-zero (**metric-zero**) identities were replaced from the same frozen retriever top-100 pool.
- The complete relevance-grade-by-position vector remained identical.
- Precision@k, recall@k, nDCG@k, MRR@k and MAP@k therefore remained identical.
- 24,500 real-data audit-equivalence checks and 72,000 synthetic checks produced zero mismatches.

### Primary result

| Outcome | Equal-dataset-weight macro |
|---|---:|
| Canonical-output change | **32.87%** |
| Benchmark-defined correctness flip | **17.27%** |
| 95% stratified-bootstrap CI for correctness flips | **14.60–20.03%** |

Most benchmark-defined outcomes remained stable; the primary result estimates the prevalence of behavioral non-equivalence inside an exactly audit-equivalent class, not universal fragility or net harm.

### Mechanism controls

- **Order only, same membership:** 4.8% macro correctness flips, RIDI=0.
- **Identity-dose ladder:** realized RIDI `0.446 → 0.655 → 0.953`; correctness flips `6.97% → 11.07% → 17.27%`.
- Registered transport gates passed across Qwen3-8B, Mistral-7B-Instruct-v0.3 and OLMo-2-7B-Instruct, and across BM25 and SPLADE++. Contriever/SciFact is an additional dense-retrieval sensitivity.

### SciFact 275: exact audit, different decision

Claim: *“Combining phosphatidylinositide 3-kinase and MEK 1/2 inhibitors is effective at treating KRAS mutant tumors.”* Gold label: `SUPPORTS`.

The positive passage stays fixed at rank 1. Reference and identity-substituted contexts share the exact relevance-grade vector

```text
[1,0,0,0,0,0,0,0,0,0]
```

and the same registered metrics:

```text
precision@10 = 0.10
recall@10    = 0.3333
nDCG@10      = 0.4693
MRR@10       = 1.00
MAP@10       = 0.3333
```

Replacing the nine metric-zero identities changes the verdict `SUPPORTS → REFUTES` (`RIDI=0.947`). The same-query order-only permutation retains `SUPPORTS` with identical membership (`RIDI=0`).

A targeted blind external regeneration on a distinct GPU/software stack reproduced this substantive pattern: reference/identity and the membership-preserving permutation yielded `SUPPORTS`, whereas the audit-equivalent identity-substitution context yielded `REFUTES`. The external reference text prefixed the verdict with `Verdict:`, so the preregistered strict first-token parser labelled that raw output unparseable; the semantic verdict itself was unambiguous. This external run is reported as a targeted robustness/reproducibility check, not as a replacement for the preregistered aggregate endpoint.

---

## Production stress test: EPSS

A real EPSS v2→v3 production update replaced **565 of the top 1,000** remediation priorities (`RIDI=0.722`), versus **0** and **7** in adjacent same-version controls. Delayed CISA KEV results were sparse and cutoff-dependent, so turnover is not equated with harm or benefit.

The sealed deterministic EPSS workflow has now been reproduced by **two independent external executors** in separate environments. Both are reported as independent computational executions; no formal CODECHECK certificate is claimed.

---

## Constructive endpoint: identity–utility frontier

The manuscript does not stop at detecting turnover. It computes the **minimum membership change compatible with an explicit updated-score utility-regret budget**, using stored scores and no retraining.

- **GraphSAGE:** at `eta=0.001`, mean changed slots fell from **31.1 to 13.3**; **78.8%** of representation-associated turnover was avoidable (95% query-bootstrap interval **76.0–81.4%**).
- **Text retrieval:** at `k=100`, mean changed documents fell from **45.8 to 33.3**; **28.7%** of turnover was avoidable (95% interval **27.6–29.7%**) with small label-based nDCG/recall changes.
- **EPSS:** at `eta=0.0001`, **14.34%** of turnover was avoidable while retaining all 12 delayed KEV positives in the primary top-1,000 window; larger budgets trade more identity preservation against outcome retention.

The exact frontier is **Main Fig. 3** in the current manuscript.

---

## Use RIDI on your own scores

### 1. Install from source

```bash
git clone https://github.com/adeebnoor/ridi.git
cd ridi
python -m pip install .
```

### 2. Python: one obvious entry point

```python
import pandas as pd
from ridi_audit import audit

before = pd.read_csv("examples/r0.csv")
after = pd.read_csv("examples/r1.csv")

report = audit(before, after, k=[3, 5])
print(report)
```

### 3. Command line

```bash
ridi-audit compare \
  --r0 examples/r0.csv \
  --r1 examples/r1.csv \
  --id-col id \
  --score-col score \
  --k 3 5 \
  --out audit.json \
  --report audit.md
```

For minimum-turnover selection inside a utility-regret budget:

```bash
ridi-audit control \
  --r0 examples/r0.csv \
  --r1 examples/r1.csv \
  --k 5 \
  --eta 0.001
```

See [examples/README.md](examples/README.md), [docs/METHODS.md](docs/METHODS.md), and [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md).

---

## Scientific boundaries

Allocation identity measures **who receives finite action** and how that set changes. It does not by itself establish correctness, fairness, causal harm, clinical benefit or model superiority.

Important limits:

- RAG qrels are incomplete; qrel-zero passages are called **metric-zero**, not semantically irrelevant.
- Correctness is benchmark-defined under frozen task-specific rules; flips are bidirectional and no net-harm claim is made.
- The confirmatory generators are deterministic open-weight 7–8B models rather than hosted frontier systems.
- EPSS downstream-value evidence is sparse and cutoff-dependent.
- Registered RxNorm and Open Targets failures are retained as claim boundaries rather than converted into positive evidence.
- Sufficiently fine or explicitly identity-aware audits can recover membership and escape non-identification.

## Reproducibility

- **RAG preregistration:** https://osf.io/txwdv/
- **Community CODECHECK request #208:** https://github.com/codecheckers/register/issues/208
- **Local audit trail:** https://github.com/adeebnoor/ridi/issues/2

The community request is registered, but formal checking has not yet begun and **no CODECHECK certificate is claimed**.

## Author

**Adeeb Noor**  
Department of Information Technology, Faculty of Computing and Information Technology  
King Abdulaziz University, Jeddah, Saudi Arabia  
ORCID: 0000-0002-8251-1853
