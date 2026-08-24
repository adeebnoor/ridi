# Numerical provenance

This page prevents headline values from drifting across the manuscript, software repository and public communication. The v21 source-data workbook and locked analysis artifacts are the numerical source of record; rounded values below are for public orientation.

## Governing values

| Endpoint | Exact value in the locked artifact | Rounded public value |
|---|---:|---:|
| GraphSAGE representation AURIDI | 0.11571128244042246 | 0.11571 |
| Same-representation retraining AURIDI | 0.08051723250612079 | 0.08052 |
| Absolute AURIDI difference | 0.03519404993430166 | 0.03519 |
| 95% query-bootstrap interval, lower | 0.02183818022619023 | 0.02184 |
| 95% query-bootstrap interval, upper | 0.05118671325379347 | 0.05119 |

The relative excess is approximately 44% when the absolute difference is divided by the retraining-null AURIDI. These attribution values supersede earlier draft summaries; historical protocol outputs are not rewritten.

## Other locked endpoints

- Synthetic margin-certificate sweep: 33,958 certified cases among 168,000, with zero false certificates.
- GraphSAGE exact control: 78.8% avoidable turnover at `eta = 0.001`.
- Text-retrieval exact control: 28.7% avoidable turnover at `eta = 0.001`.
- Temporal RxNorm analysis: Spearman 0.999406 and 25 changed identities among the top 1,000.
- Delayed DDInter 2.0 curation: recovered Major/Moderate interactions increased from 17 to 19; exact zero-change control returned 17 and failed the prospectively declared 97.5% retention gate.
- EPSS v2→v3 natural update: 565 of 1,000 priorities changed (`RIDI=0.722`), versus 0 and 7 in adjacent same-version controls.
- Delayed CISA KEV at k=1,000: recovery increased from 8 to 12 while full-universe AUROC decreased from 0.664790 to 0.609685.
- EPSS exact control: the locked `eta=0.001` choice avoided 40.9% of turnover but retained 10/12 future-KEV captures and failed the 95% gate; `eta=0.0001` avoided 14.3% while retaining 12/12.

## Interpretation and archive status

The public repository is the development software companion. The complete submission source data and immutable analysis archive accompany the manuscript. Zenodo DOI `10.5281/zenodo.22072275` is reserved in a draft and must not be described as publicly available until it resolves without authentication.

DDInter 2.0 supplies later curation evidence, not clinical ground truth or patient-level benefit. KEV addition is delayed federal curation of known exploitation, not exploitation onset or complete ground truth. The EPSS extension transports the audit across a model update and does not isolate representation. GitHub protocol locks are auditable analysis locks, not independent public preregistrations; no independent-team replication is claimed before a separate team returns sealed outputs and a declaration.
