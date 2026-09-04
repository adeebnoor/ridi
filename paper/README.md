# Identical audits can yield different AI decisions

**Adeeb Noor**  
Department of Information Technology, Faculty of Computing and Information Technology, King Abdulaziz University, Jeddah, Saudi Arabia  
ORCID: 0000-0002-8251-1853

> **Manuscript status:** prepared for journal submission; not peer reviewed, accepted or published.

## Central result

Capacity-limited AI systems convert scores into finite queues, shortlists, action sets or context windows. This manuscript asks whether the reported audit identifies **which entities actually occupy those scarce slots**.

The decisive prospective test is a preregistered retrieval-augmented generation experiment in which the complete relevance-grade-by-position vector and every registered retrieval metric are held exactly fixed while only metric-zero passage identities are changed.

### Preregistered RAG result

- 800 frozen queries: Natural Questions 250, HotpotQA 250, FEVER 150, SciFact 150.
- Positive-qrel passages remained at the exact same ranks.
- Precision@k, recall@k, nDCG@k, MRR@k, MAP@k and the complete relevance-grade-by-position vector were identical by construction.
- 24,500 real-data audit-equivalence checks and 72,000 synthetic checks had zero mismatches.
- Equal-dataset-weight macro canonical-output change: **32.87%**.
- Equal-dataset-weight macro benchmark-defined correctness flip: **17.27%** (95% stratified-bootstrap interval **14.60–20.03%**).
- Order-only control with identical membership: **4.8%** macro correctness flips.
- Identity-dose ladder: realized RIDI **0.446 → 0.655 → 0.953**, with correctness flips **6.97% → 11.07% → 17.27%**.

Most benchmark-defined outcomes remained stable. The confirmatory result estimates the prevalence of behavioral non-equivalence inside an exactly audit-equivalent class; it is not a claim of universal fragility or net harm.

## Concrete SciFact case

Claim 275: **“Combining phosphatidylinositide 3-kinase and MEK 1/2 inhibitors is effective at treating KRAS mutant tumors.”** Gold label: `SUPPORTS`.

Reference and identity-substituted contexts share the same relevance-grade vector

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

The positive passage stays fixed at rank 1. Replacing nine metric-zero identities changes the verdict `SUPPORTS → REFUTES` (`RIDI=0.947`). The same-query order-only permutation retains `SUPPORTS` with identical membership (`RIDI=0`).

### Independent blind regeneration

The substantive SciFact pattern has now been regenerated **twice by independent external executors without access to the held author comparison result before return**.

- **Mohammed Hamdan:** the frozen audit checks passed with no mismatches; reference and identity-control outputs were `SUPPORTS`, with the identity output byte-identical to reference; the order-only permutation remained `SUPPORTS`; the audit-equivalent identity substitution produced `REFUTES`. Because the executor's host could not run the pinned bf16 Hugging Face stack, the same frozen inputs and prompt conditioning were served through a disclosed `qwen3:8b` Q4_K_M llama.cpp/Ollama path. This is therefore a cross-serving/quantization robustness regeneration rather than a byte-identical pipeline reproduction.
- **Théophile Ossard:** a separate blind regeneration on a distinct GPU/software stack reproduced the same substantive reference/permutation `SUPPORTS` versus identity-substitution `REFUTES` pattern. His regenerated reference began with `Verdict: SUPPORTS`, so the preregistered strict first-token parser labelled that raw output unparseable despite an unambiguous semantic verdict. That parser boundary is retained transparently rather than silently corrected.

These targeted external runs support robustness of the **SciFact 275 behavioral reversal**. They do not replace the preregistered aggregate 800-query endpoint and are not presented as CODECHECK certification.

## Production stress test

**EPSS:** the production v2→v3 update replaced **565 of the top 1,000** remediation priorities (`RIDI=0.722`), versus **0** and **7** in adjacent same-version controls. Delayed CISA KEV evidence was sparse and cutoff-dependent, so turnover is not equated with harm or benefit.

The sealed deterministic EPSS workflow has been reproduced by **two independent external executors** in separate environments. These are independent computational executions; no CODECHECK certificate is claimed.

## Constructive solution: exact identity–utility frontier

**Main Fig. 3** presents the exact identity–utility frontier: the minimum membership change compatible with an explicit updated-score utility-regret budget, using stored scores and no retraining.

- **GraphSAGE:** at `eta=0.001`, mean changed slots fall from **31.1 to 13.3**; **78.8%** of representation-associated turnover is avoidable (95% query-bootstrap interval **76.0–81.4%**).
- **Text retrieval:** at `k=100`, mean changed documents fall from **45.8 to 33.3**; **28.7%** is avoidable (95% interval **27.6–29.7%**) with small label-based nDCG/recall changes.
- **EPSS:** at `eta=0.0001`, **14.34%** of turnover is avoidable while retaining all 12 delayed KEV positives in the primary top-1,000 window.

The constructive claim is deliberately bounded: identity preservation is useful only inside an explicit outcome- or utility-checked budget.

## Registered failures and boundaries

RxNorm and Open Targets registered tests are retained as failures/boundaries rather than recast as positive evidence. Earlier exploratory COMPAS and crude CVE-year analyses remain archived but do not support the current main claims.

## Reproducibility

- **RAG preregistration:** https://osf.io/txwdv/
- **Repository:** https://github.com/adeebnoor/ridi
- **PyPI package:** https://pypi.org/project/ridi-audit/
- **Community CODECHECK request #208:** https://github.com/codecheckers/register/issues/208

The community CODECHECK request is registered; formal checking has not yet begun and **no certificate is claimed**.

## Scientific boundaries

Allocation identity measures **who receives finite action**. It does not by itself establish harm, benefit, individual fairness, causal fairness or model superiority. Benchmark qrels are incomplete, so qrel-zero passages are called **metric-zero**, not semantically irrelevant. Correctness flips are bidirectional. Confirmatory generators are deterministic open-weight 7–8B models rather than hosted frontier systems. EPSS downstream-value effects are cutoff- and endpoint-specific. Sufficiently fine or explicitly identity-aware audits can recover membership and escape non-identification.

## Use or test the idea

- [Install `ridi-audit` from PyPI](https://pypi.org/project/ridi-audit/)
- [Open the 60-second notebook in Colab](https://colab.research.google.com/github/adeebnoor/ridi/blob/main/notebooks/RIDI_60_Second_Experiment.ipynb)
- [60-second Quick Start](../docs/QUICKSTART.md)
- [Python API](../docs/API.md)
- [Copy-paste use cases](../docs/USE_CASES.md)
- [Allocation Identity Reporting Checklist](../docs/REPORTING_CHECKLIST.md)
- [Independent replication / new-domain issue forms](https://github.com/adeebnoor/ridi/issues/new/choose)
- [RIDI repository home](../README.md)
