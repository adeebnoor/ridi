# Numerical provenance

This page prevents headline values from drifting across the manuscript, Source Data, preregistered outputs and public repository. The current manuscript is **“Identical audits, different AI decisions.”** The submission Source Data file is `RIDI_Nature_Source_Data_v58.xlsx`; frozen primary artifacts remain the numerical source of record.

## Preregistered RAG — decisive prospective result

Protocol: `RIDI-RAG-NATURE-v2`  
Registration: https://osf.io/txwdv/

| Endpoint | Preregistered result |
|---|---:|
| Frozen queries | 800 |
| Equal-dataset-weight macro canonical-output change | 32.87% |
| 95% stratified-bootstrap CI | 29.77–36.00% |
| Equal-dataset-weight macro correctness flip | 17.27% |
| 95% stratified-bootstrap CI | 14.60–20.03% |
| Order-only macro correctness flip | 4.8% |
| Audit-equivalence checks | 24,500 real-data + 72,000 synthetic; 0 mismatches |

Registered identity-dose series at k=10:
- ~25% substitution: realized RIDI 0.446; correctness flips 6.97%.
- ~50% substitution: realized RIDI 0.655; correctness flips 11.07%.
- ~100% substitution: realized RIDI 0.953; correctness flips 17.27%.

Registered transport gates passed across Qwen3-8B, Mistral-7B-Instruct-v0.3 and OLMo-2-7B-Instruct, and across BM25 and SPLADE++; Contriever/SciFact is an additional dense-retrieval sensitivity.

## Constructive COMPAS audit

Public two-year research cohort: n=6,172; positives=2,809. The research top-1,000 has precision@1,000=0.745 and recall=0.265. The executor-facing value key records audit-equivalence classes of approximately 10^1094 under outcome counts alone, 10^1048 after binary-race refinement, 10^113 after risk-decile refinement and 10^109 after sex refinement. Thirty-two extremal allocations were constructed with zero audited-statistic mismatches.

These are constructive research cohorts, not observed operational supervision lists and not predictions from a particular trained model family.

## EPSS deterministic operational stress test

Protocol: `RIDI-CYBER-NATURAL-UPDATE-v1`.

- v2→v3 top-1,000 changed slots: 565; RIDI=0.7220447284.
- Adjacent same-version top-1,000 controls: 0 and 7 changed slots.
- Delayed CISA KEV recovery at k=1,000: 8→12.
- Full-universe AUROC: 0.6647895356→0.6096852762.
- Exact identity control at eta=0.0001 avoided 14.34% of turnover while retaining 12/12 future-KEV hits.
- eta=0.001 avoided 40.88% but retained 10/12 and failed the 95% external-retention gate.

The sealed canonical numerical result key has been reproduced exactly in two external software environments. These runs are cross-environment numerical reproductions, not neutral person-level certification.

## Other locked/supportive endpoints retained in v58

- Synthetic margin-certificate sweep: 33,958 certified cases among 168,000, with zero false certificates.
- GraphSAGE exact control: 78.8% avoidable turnover at eta=0.001.
- Text-retrieval exact control: 28.7% avoidable turnover at eta=0.001.
- Registered RxNorm and Open Targets results are retained as claim-bounding failures/limits rather than hidden exceptions.
- CMS HVBP annual score updates are a retrospective transport check; the analytical top-k is not a statutory CMS cutoff and no payment or clinical-effect estimate is claimed.

## Source-data and archive status

`RIDI_Nature_Source_Data_v58.xlsx` is the submission workbook for Figs. 1–4 and Extended Data Figs. 1–9, with panel-level provenance to frozen artifacts. Public development code and reproducibility documentation are at https://github.com/adeebnoor/ridi.

Do **not** describe Zenodo DOI `10.5281/zenodo.22072275` as public unless it resolves without authentication. A reserved/draft identifier is not evidence of a public immutable archive.

## CODECHECK status

Community request: https://github.com/codecheckers/register/issues/208  
Status as of 4 September 2026: open; certificate pending.

The register entry was opened under an earlier working title, but the requested deterministic EPSS workflow is unchanged. No CODECHECK certification is claimed unless and until a certificate is formally issued.

## Interpretation boundary

Allocation identity measures who or what receives finite action. It does not by itself establish harm, benefit, individual fairness, causal fairness or model superiority. RAG qrel-zero passages are therefore described as **metric-zero**, not semantically irrelevant; correctness flips are bidirectional; KEV addition is delayed federal curation rather than exploitation onset or complete ground truth.
