# Results at a glance

These values summarize the manuscript's locked analyses and are provided for orientation. The immutable archive is the source of record.

| Analysis | Finding | Interpretation boundary |
|---|---|---|
| RxNorm 2022→2023 / DDInter | Spearman 0.999406; 25 of top 1,000 identities replaced; RIDI 0.04878 | Operational selection movement, not clinical harm |
| Delayed DDInter curation outcome | Major/Moderate interactions recovered 17→19; +3 Major entered, −1 Moderate left | Demonstrates beneficial turnover in this test; not independent-team replication |
| Synthetic certificate sweep | 33,958 of 168,000 cases certified; zero false certificates | Certificate is sufficient, not necessary |
| GraphSAGE attribution | AURIDI 0.11571 vs retraining 0.08052; absolute difference 0.03519 (95% query-bootstrap interval 0.02184–0.05119); 44% relative excess; AUROC 0.91772 vs 0.91747 | Single graph/task scope is reported explicitly |
| GraphSAGE identity control | 78.8% avoidable turnover at 0.1% utility-regret tolerance | Conditional on the declared tolerance and utility |
| Text retrieval identity control | 28.7% avoidable turnover at the same tolerance | Different frontier geometry explains domain variation |
| External retention gate | 89.5% retention versus 97.5% pre-specified gate | Adverse boundary result preserved; stability is not correctness |
| EPSS v2→v3 natural update | 565 of top 1,000 priorities changed; RIDI 0.722; adjacent daily controls changed 0 and 7 | Model-update transport test, not representation attribution |
| Delayed CISA KEV outcome | At k=1,000 recovery rose 8→12 despite AUROC 0.665→0.610; at k=100 recovery fell 4→2 | Benefit is capacity-dependent; KEV dateAdded is delayed curation, not exploit onset |
| EPSS identity control | Locked `eta=0.001` avoided 40.9% but retained 10/12 and failed 95% gate; `eta=0.0001` avoided 14.3% and retained 12/12 | Score regret alone does not choose the safe identity budget |

The DDInter 2.0 comparison is delayed curation evidence, not clinical ground truth, prescribing guidance or evidence of patient benefit. Cross-domain analyses establish transportability of the audit, not universal effect sizes or harms. The author-run EPSS analysis has a public blind-run package, but no independent-team result is claimed yet.
