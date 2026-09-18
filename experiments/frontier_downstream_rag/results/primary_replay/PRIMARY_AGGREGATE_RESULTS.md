# Frontier → downstream primary result

Protocol: RIDI-NATURE-FRONTIER-DOWNSTREAM-v1  
Primary cell: k=10, eta=0.001  
Bootstrap: 100,000 dataset-stratified query resamples; seed 20260918.

| Dataset | Updated acc. | Controlled acc. | Δ acc. | Correctness status changed | Answer text changed | Changed slots | Controlled slots | Slot reduction | Avoidable fraction |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| nq | 45.0% | 46.0% | +1.0 pp | 1.0% | 2.0% | 5.72 | 5.41 | 0.31 | 6.80% |
| hotpotqa | 32.0% | 32.0% | +0.0 pp | 0.0% | 4.0% | 6.31 | 6.09 | 0.22 | 3.48% |
| fever | 82.0% | 83.0% | +1.0 pp | 1.0% | 1.0% | 5.73 | 5.44 | 0.29 | 5.62% |
| scifact | 70.0% | 67.0% | -3.0 pp | 3.0% | 4.0% | 5.15 | 4.60 | 0.55 | 12.09% |

## Equal-dataset-weight macro

- Mean changed slots: 5.7275 → 5.3850; reduction 0.3425 (95% bootstrap interval 0.2950–0.3925).
- Query-mean avoidable-turnover fraction among changed queries: 7.00% (95% interval 5.84–8.25%).
- Updated vs controlled benchmark accuracy: 57.25% vs 57.00%; paired difference -0.25 pp (95% interval -1.25 to +0.75 pp).
- Correctness status changed in 1.25% of queries (95% interval 0.25–2.50%).
- Normalized answer text changed in 2.75% (95% interval 1.25–4.50%).
- Directional correctness changes: 2 improved, 3 worsened; answer text changed in 11/400 queries.

These results do not establish non-inferiority or downstream benefit. They show the realized finite-panel trade-off under the locked rank-utility budget.
