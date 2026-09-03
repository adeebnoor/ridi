# RIDI

## Allocation identity for capacity-limited AI

### Current manuscript: **Identical audits, different AI decisions**

RIDI studies a missing audit object at the score-to-action boundary: **which entities actually receive finite action, attention or context?** A system can satisfy the same reported aggregate audit while acting on different identities.

**Paper overview:** https://adeebnoor.github.io/ridi/paper/  
**Project page:** https://adeebnoor.github.io/ridi/projects/ridi/  
**60-second experiment:** https://adeebnoor.github.io/ridi/demo/  
**RAG preregistration:** https://osf.io/txwdv/  
**Community CODECHECK:** https://github.com/codecheckers/register/issues/208

> Manuscript status: prepared for journal submission; not peer reviewed, accepted or published. No CODECHECK certificate is claimed while issue #208 remains pending.

---

## The scientific object

AI evaluation usually asks how well a system predicts, ranks, calibrates or distributes outcomes across groups. Many deployed systems ultimately do something more concrete: scores become a finite queue, shortlist, top-k action set or context window.

That creates a separate object:

> **Allocation identity: which entities receive the finite slots?**

Performance and group fairness remain necessary. They answer different questions from realized membership.

| Evaluation axis | Question |
|---|---|
| Performance | How well does the system predict or rank? |
| Group fairness | How are outcomes distributed across groups? |
| Calibration / robustness | Are scores reliable or stable under specified changes? |
| **Allocation identity** | **Who actually receives the finite action, and who changed?** |

For equal-size selected sets `A` and `B`, RIDI is one operational measure:

```text
RIDI(A, B) = 1 - |A ∩ B| / |A ∪ B|
```

For equal-capacity top-`k` sets with `Delta_k = k - |A ∩ B|` changed slots:

```text
RIDI = 2*Delta_k / (k + Delta_k)
```

RIDI is **not** a replacement for AUROC, precision, recall, nDCG, calibration or fairness metrics. It makes the allocation axis directly observable.

---

## Decisive preregistered RAG test

`RIDI-RAG-NATURE-v2` was preregistered publicly before registered language-model generation.

### Frozen design

- 800 queries: Natural Questions 250, HotpotQA 250, FEVER 150, SciFact 150.
- Every positive-qrel passage in the reference top-k stayed at the same rank.
- Only qrel-zero (**metric-zero**) identities were replaced, using candidates from the same frozen retriever top-100 pool.
- The complete relevance-grade-by-position vector remained exactly identical.
- Therefore precision@k, recall@k, nDCG@k, MRR@k and MAP@k remained exactly identical.
- 24,500 real-data audit-equivalence checks and 72,000 synthetic checks produced zero mismatches.

### Primary result

In the preregistered Qwen3-8B / BM25 / k=10 random identity-replacement condition:

| Outcome | Equal-dataset-weight macro |
|---|---:|
| Canonical-output change | **32.87%** |
| Benchmark-defined correctness flip | **17.27%** |
| 95% stratified-bootstrap CI for correctness flips | **14.60–20.03%** |

For transparency, the pooled descriptive fractions are different because dataset sizes differ: correctness flips were `134/800 = 16.75%`; canonical-output changes were `286/800 = 35.75%`. The preregistered estimands are the equal-dataset-weight macro rates.

### Mechanism controls

- **Order only, same membership:** 4.8% macro correctness flips, RIDI=0.
- **Identity-dose ladder:** realized RIDI `0.446 → 0.655 → 0.953` while correctness flips increased `6.97% → 11.07% → 17.27%`.
- Registered transport gates passed across Qwen3-8B, Mistral-7B-Instruct-v0.3 and OLMo-2-7B-Instruct, and across BM25 and SPLADE++. Contriever/SciFact is an additional dense-retrieval sensitivity rather than an all-dataset gate.

### Concrete SciFact case

Claim 275: *“Combining phosphatidylinositide 3-kinase and MEK 1/2 inhibitors is effective at treating KRAS mutant tumors.”* Gold label: `SUPPORTS`.

The reference and identity-altered contexts have the same relevance-grade vector:

```text
[1,0,0,0,0,0,0,0,0,0]
```

and the same registered retrieval metrics:

```text
precision@10 = 0.10
recall@10    = 0.3333
nDCG@10      = 0.4693
MRR@10       = 1.00
MAP@10       = 0.3333
```

The sole positive-qrel passage stays fixed at rank 1. Replacing nine metric-zero identities changes the canonical verdict `SUPPORTS → REFUTES` (`RIDI=0.947`). The same-query order-only permutation control retains `SUPPORTS` with identical membership (`RIDI=0`).

This case is illustrative. The preregistered aggregate experiment supplies the inferential result.

---

## Why this is not a straw-man test

The manuscript does **not** claim that practitioners believe nDCG mathematically determines a generated answer. The narrower question is audit sufficiency.

Current official platform documentation uses aggregate retrieval evaluation to compare or select RAG configurations:

- Amazon Bedrock: RAG-evaluation results can be used to compare knowledge bases and other RAG sources and choose a RAG system for an application.
- Microsoft Azure Architecture Center: recommends precision@k, recall@k and MRR, aggregated across test queries, to evaluate retrieval.
- Azure Databricks: recommends DCG@10 as the primary metric for overall retrieval quality and connects evaluation results to choices such as hybrid search and reranking.

The RIDI experiment asks the additional question those summaries do not answer: **do they certify which identities occupy the finite context?**

---

## Evidence across systems

The empirical programme triangulates the identification result rather than assuming the same magnitude or consequence everywhere.

### COMPAS

In the public two-year research cohort (`n=6,172`), a constructed top-1,000 reference cohort has precision `0.745`, recall `0.265` and African-American share `74.7%`. Exact matching of increasingly detailed group-count audit cells sharply narrows the compatible allocation class but does not necessarily identify the selected people.

This is a retrospective research construction, **not** an observed operational supervision list and **not** a prediction that another trained scorer will realize an extremal cohort.

### EPSS

For the v2→v3 production update, `565/1,000` top remediation priorities changed (`RIDI=0.722`) versus `0` and `7` in adjacent same-version controls. Delayed CISA KEV value was capacity-dependent: the update was beneficial at the primary k=1,000 endpoint but adverse at k=100. The paper therefore does not equate turnover with harm.

### CMS HVBP

Annual Total Performance Score updates provide transport to a second independently governed production scoring system.

### Registered failures and boundary cases

RxNorm and Open Targets analyses are retained as first-class negative/boundary evidence. The identification theorem is general; large or consequential turnover is **not** claimed to be universal.

---

## From observability to control

The toolkit supports four steps:

1. **Measure** — who entered, exited or stayed?
2. **Attribute** — what changed the allocation, relative to mechanism-matched controls?
3. **Certify** — can zero turnover be guaranteed from stored score margins?
4. **Control** — what is the minimum identity change compatible with an explicit updated-score utility-regret budget?

A sufficient zero-turnover certificate is:

```text
gamma_k > 2*epsilon
```

where `gamma_k` is the baseline score margin at the top-k boundary and `epsilon` is the maximum paired score perturbation.

The control step does not enforce stability blindly. Identity change can be accepted when external outcomes justify it; only avoidable change should be constrained.

---

## Reproducibility

### RAG preregistration

Public registration: https://osf.io/txwdv/

The registration freezes the study matrix, query panels, prompts, model revisions, retrievers, intervention rules, falsification thresholds, analysis plan and cryptographic manifest before registered generation.

### CODECHECK

Community CODECHECK request:

https://github.com/codecheckers/register/issues/208

The requested scope is the deterministic EPSS natural-update workflow `RIDI-CYBER-NATURAL-UPDATE-v1`.

The sealed EPSS canonical numerical key has been reproduced in two external software environments. Those runs are treated as cross-environment numerical reproduction only. **No CODECHECK certificate is claimed unless and until one is formally issued.**

Public local tracking: https://github.com/adeebnoor/ridi/issues/2

---

## Audit your own scores

```bash
git clone https://github.com/adeebnoor/ridi.git
cd ridi
python -m pip install .
pytest -q
```

Compare two aligned score files:

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

Control avoidable turnover under a declared regret budget:

```bash
ridi-audit control \
  --r0 examples/r0.csv \
  --r1 examples/r1.csv \
  --id-col id \
  --score-col score \
  --k 5 \
  --eta 0.001 \
  --out controlled.json
```

`eta` is a domain-governance choice, not a universal threshold.

---

## Scientific boundaries

Allocation identity measures **who receives finite action** and how that set changes. It does not by itself establish correctness, fairness, causal harm, clinical benefit or model superiority.

Important limits in the current manuscript:

- RAG qrels are incomplete; qrel-zero passages are called **metric-zero**, not semantically irrelevant.
- Correctness is benchmark-defined under frozen task-specific rules; flips are bidirectional and no net-harm claim is made.
- The confirmatory generators are deterministic open-weight 7–8B models rather than hosted frontier systems.
- The COMPAS analysis is a retrospective constructive secondary analysis.
- EPSS outcome effects are cutoff- and endpoint-specific.
- Sufficiently fine or explicitly identity-aware audits can recover membership and escape the non-identification result.

---

## Citation

Software citation:

> Noor, A. (2026). *RIDI: allocation-identity audit and control toolkit* (v1.0.0). GitHub. https://github.com/adeebnoor/ridi

No archival DOI is claimed here unless its public activation is independently verified.

## Author

**Adeeb Noor**  
Department of Information Technology, Faculty of Computing and Information Technology  
King Abdulaziz University, Jeddah, Saudi Arabia  
ORCID: 0000-0002-8251-1853
