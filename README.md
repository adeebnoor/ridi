# RIDI

## Allocation identity for capacity-limited AI

### Current manuscript: **Identical audits, different AI decisions**

RIDI studies a missing audit object at the score-to-action boundary: **which entities actually receive finite action, attention or context?** A system can satisfy the same reported aggregate audit while acting on different identities.

**GitHub-native paper page:** [paper/README.md](paper/README.md)  
**Paper HTML source:** [paper/index.html](paper/index.html)  
**RIDI project source:** [projects/ridi/](projects/ridi/)  
**60-second experiment:** https://ridi-research-lab.onrender.com/demo/  
**RAG preregistration:** https://osf.io/txwdv/  
**Community CODECHECK:** https://github.com/codecheckers/register/issues/208

> **Status:** manuscript prepared for journal submission; not peer reviewed, accepted or published. No CODECHECK certificate is claimed while issue #208 remains pending.

---

## The scientific object

Performance, group fairness, calibration and robustness remain necessary evaluation dimensions. RIDI asks a different question for finite-capacity systems:

> **Which identities occupy the scarce slots, and is that membership identified by the reported audit?**

For equal-size selected sets `A` and `B`, one operational measure is

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

`RIDI-RAG-NATURE-v2` was preregistered publicly before registered language-model generation.

### Frozen design

- 800 queries: Natural Questions 250, HotpotQA 250, FEVER 150, SciFact 150.
- Every positive-qrel passage stayed at the same rank.
- Only qrel-zero (**metric-zero**) identities were replaced from the same frozen retriever top-100 pool.
- The complete relevance-grade-by-position vector remained exactly identical.
- Precision@k, recall@k, nDCG@k, MRR@k and MAP@k therefore remained exactly identical.
- 24,500 real-data audit-equivalence checks and 72,000 synthetic checks produced zero mismatches.

### Primary result

In the preregistered Qwen3-8B / BM25 / k=10 random identity-replacement condition:

| Outcome | Equal-dataset-weight macro |
|---|---:|
| Canonical-output change | **32.87%** |
| Benchmark-defined correctness flip | **17.27%** |
| 95% stratified-bootstrap CI for correctness flips | **14.60–20.03%** |

For transparency, the pooled descriptive fractions differ because dataset sizes differ: correctness flips were `134/800 = 16.75%`; canonical-output changes were `286/800 = 35.75%`. The preregistered estimands are the macro rates.

### Mechanism controls

- **Order only, same membership:** 4.8% macro correctness flips, RIDI=0.
- **Identity-dose ladder:** realized RIDI `0.446 → 0.655 → 0.953`; correctness flips `6.97% → 11.07% → 17.27%`.
- Registered transport gates passed across Qwen3-8B, Mistral-7B-Instruct-v0.3 and OLMo-2-7B-Instruct, and across BM25 and SPLADE++. Contriever/SciFact is an additional dense-retrieval sensitivity rather than an all-dataset gate.

### Concrete SciFact case

Claim 275: *“Combining phosphatidylinositide 3-kinase and MEK 1/2 inhibitors is effective at treating KRAS mutant tumors.”* Gold label: `SUPPORTS`.

Reference and identity-altered contexts share the same relevance-grade vector:

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

The positive passage stays fixed at rank 1. Replacing nine metric-zero identities changes the canonical verdict `SUPPORTS → REFUTES` (`RIDI=0.947`). The same-query order-only permutation retains `SUPPORTS` with identical membership (`RIDI=0`).

This case is illustrative; the preregistered aggregate experiment supplies the inferential result.

---

## Why this is an audit-sufficiency question

The manuscript does **not** claim that practitioners believe nDCG mathematically determines a generated answer. The narrower point is that aggregate retrieval evaluation is used operationally to compare or select RAG configurations, while those summaries need not certify the identities occupying the finite context. Official examples are documented by Amazon Bedrock, Microsoft Azure Architecture Center and Azure Databricks.

---

## Evidence across systems

- **COMPAS:** constructive audit-equivalent research cohorts show that progressively refined selected-count audits can sharply constrain membership without necessarily identifying the selected people.
- **EPSS:** the production v2→v3 update replaced `565/1,000` remediation priorities (`RIDI=0.722`) versus 0 and 7 in adjacent same-version controls. Delayed CISA KEV value was capacity-dependent, so turnover is not equated with harm.
- **CMS HVBP:** annual Total Performance Score updates provide a second independently governed production scoring system for transport.
- **Registered failures/boundaries:** RxNorm and Open Targets results are retained to show that magnitude, mechanism and downstream value are system- and cutoff-dependent.

---

## From observability to control

The toolkit supports four steps:

1. **Measure** — who entered, exited or stayed?
2. **Attribute** — what changed the allocation relative to mechanism-matched controls?
3. **Certify** — can zero turnover be guaranteed from stored score margins?
4. **Control** — what is the minimum identity change compatible with an explicit updated-score utility-regret budget?

A sufficient zero-turnover certificate is

```text
gamma_k > 2*epsilon
```

where `gamma_k` is the baseline score margin at the top-k boundary and `epsilon` is the maximum paired score perturbation.

---

## Reproducibility

### RAG preregistration

https://osf.io/txwdv/

The registration freezes the study matrix, query panels, prompts, model revisions, retrievers, intervention rules, falsification thresholds, analysis plan and cryptographic manifest before registered generation.

### CODECHECK

Community request: https://github.com/codecheckers/register/issues/208  
Local audit trail: https://github.com/adeebnoor/ridi/issues/2

The sealed EPSS canonical numerical key has been reproduced in two external software environments. Those runs are treated as cross-environment numerical reproduction only. **No CODECHECK certificate is claimed unless and until one is formally issued.**

---

## Audit your own scores

```bash
git clone https://github.com/adeebnoor/ridi.git
cd ridi
python -m pip install .
pytest -q
```

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

---

## Scientific boundaries

Allocation identity measures **who receives finite action** and how that set changes. It does not by itself establish correctness, fairness, causal harm, clinical benefit or model superiority.

Important limits:

- RAG qrels are incomplete; qrel-zero passages are called **metric-zero**, not semantically irrelevant.
- Correctness is benchmark-defined under frozen task-specific rules; flips are bidirectional and no net-harm claim is made.
- The confirmatory generators are deterministic open-weight 7–8B models rather than hosted frontier systems.
- COMPAS is a retrospective constructive secondary analysis.
- EPSS outcome effects are cutoff- and endpoint-specific.
- Sufficiently fine or explicitly identity-aware audits can recover membership and escape non-identification.

## Author

**Adeeb Noor**  
Department of Information Technology, Faculty of Computing and Information Technology  
King Abdulaziz University, Jeddah, Saudi Arabia  
ORCID: 0000-0002-8251-1853
