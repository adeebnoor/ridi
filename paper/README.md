# Identical audits, different AI decisions

**Adeeb Noor**  
Department of Information Technology, Faculty of Computing and Information Technology, King Abdulaziz University, Jeddah, Saudi Arabia  
ORCID: 0000-0002-8251-1853

> **Manuscript status:** prepared for journal submission; not peer reviewed, accepted or published.

## Central result

Capacity-limited AI systems convert scores into a finite queue, shortlist, action set or context window. This manuscript asks whether a conventional aggregate audit identifies **which entities actually occupy those scarce slots**.

The decisive prospective test is a preregistered retrieval-augmented generation experiment in which the complete relevance-grade-by-position vector and all registered retrieval metrics are held exactly fixed while only passage identities assigned zero benchmark relevance are changed.

### Preregistered RAG result

- 800 frozen queries: Natural Questions 250, HotpotQA 250, FEVER 150, SciFact 150.
- Positive-qrel passages remained at the exact same ranks.
- Precision@k, recall@k, nDCG@k, MRR@k, MAP@k and the complete relevance-grade-by-position vector were identical by construction.
- 24,500 real-data audit-equivalence checks and 72,000 synthetic checks had zero mismatches.
- Equal-dataset-weight macro canonical-output change: **32.87%**.
- Equal-dataset-weight macro benchmark-defined correctness flip: **17.27%** (95% stratified-bootstrap interval **14.60–20.03%**).
- Order-only control with identical membership: **4.8%** macro correctness flips.
- Identity-dose ladder: realized RIDI **0.446 → 0.655 → 0.953**, with correctness flips **6.97% → 11.07% → 17.27%**.
- Registered transport gates passed across three generator families and both BM25 and SPLADE++; Contriever/SciFact is an additional dense-retrieval sensitivity.

For transparency, the pooled descriptive rates differ from the preregistered equal-dataset-weight macro estimands: `134/800 = 16.75%` correctness flips and `286/800 = 35.75%` canonical-output changes.

## Concrete SciFact case

Claim 275: **“Combining phosphatidylinositide 3-kinase and MEK 1/2 inhibitors is effective at treating KRAS mutant tumors.”** Gold label: `SUPPORTS`.

Both reference and identity-altered contexts have the same relevance-grade vector:

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

The positive passage stays fixed at rank 1. Replacing nine metric-zero identities changes the canonical verdict `SUPPORTS → REFUTES` (`RIDI=0.947`). The same-query order-only permutation control retains `SUPPORTS` with identical membership (`RIDI=0`).

This is an illustration of the registered aggregate result, not a separate inferential test.

## Why this is an audit-sufficiency question

The paper does **not** claim that practitioners believe nDCG mathematically determines a generated answer. The narrower point is that aggregate retrieval evaluation is used operationally to compare or select RAG configurations, while those summaries need not certify the identities occupying the finite context.

Official examples include Amazon Bedrock RAG evaluations, Microsoft Azure Architecture Center retrieval guidance, and Azure Databricks retrieval-quality evaluation.

## Cross-system evidence

- **COMPAS:** constructive audit-equivalent research cohorts show that progressively refined selected-count audits can sharply constrain membership without necessarily identifying the selected people.
- **EPSS:** the production v2→v3 update replaced 565 of the top 1,000 remediation priorities (`RIDI=0.722`) versus 0 and 7 in adjacent same-version controls. Delayed CISA KEV value was capacity-dependent, so turnover is not equated with harm.
- **CMS HVBP:** annual Total Performance Score updates provide a second independently governed production scoring system for transport.
- **Registered failures/boundaries:** RxNorm and Open Targets results are retained to show that magnitude, mechanism and downstream value are system- and cutoff-dependent.

## Scientific boundaries

Allocation identity measures **who receives finite action**. It does not by itself establish harm, benefit, individual fairness, causal fairness or model superiority.

Important limits:

- benchmark qrels are incomplete, so qrel-zero passages are called **metric-zero**, not semantically irrelevant;
- correctness flips are bidirectional and no net-harm claim is made;
- the registered generators are deterministic open-weight 7–8B models rather than hosted frontier systems;
- COMPAS is a retrospective constructive secondary analysis;
- EPSS effects are cutoff- and endpoint-specific;
- sufficiently fine or explicitly identity-aware audits can recover membership and escape non-identification.

## Reproducibility

- **RAG preregistration:** https://osf.io/txwdv/
- **Repository:** https://github.com/adeebnoor/ridi
- **Community CODECHECK #208:** https://github.com/codecheckers/register/issues/208
- **Local CODECHECK audit trail:** https://github.com/adeebnoor/ridi/issues/2

The sealed EPSS canonical numerical key has been reproduced in two external software environments. Those runs are treated as cross-environment numerical reproduction only. **No CODECHECK certificate is claimed unless and until one is formally issued.**

## Explore

- [RIDI repository home](../README.md)
- [Audit toolkit and methods](../docs/)
- [60-second identity experiment](../demo/)
- [Project source page](../projects/ridi/)
