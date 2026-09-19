# Qwen3-32B scale-transfer result

Protocol: RIDI-RAG-QWEN3-32B-SCALE-v1
Status: post hoc scale-transfer extension, publicly locked before successful 32B generation; not an OSF preregistration.
Bootstrap: 100,000 dataset-stratified query resamples; seed 20260919.

| Dataset | Qwen3-32B flips | Rate | Qwen3-8B flips | 8B rate | 32B-8B | C-to-W | W-to-C | Canonical change |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| nq | 37/250 | 14.80% | 49/250 | 19.60% | -4.80 pp | 22 | 15 | 58.80% |
| hotpotqa | 25/250 | 10.00% | 27/250 | 10.80% | -0.80 pp | 12 | 13 | 44.00% |
| fever | 13/150 | 8.67% | 19/150 | 12.67% | -4.00 pp | 9 | 4 | 10.00% |
| scifact | 24/150 | 16.00% | 39/150 | 26.00% | -10.00 pp | 7 | 17 | 18.00% |

## Equal-dataset-weight macro

- Qwen3-32B correctness divergence: 12.37% (95% bootstrap 10.07-14.77%).
- Same-query Qwen3-8B macro: 17.27%.
- Paired 32B-8B difference: -4.90 pp (95% bootstrap -7.77 to -2.03 pp).
- Directional 32B changes: 50 correct-to-wrong and 49 wrong-to-correct.
- Canonical-output divergence: 32.70% (95% bootstrap 29.83-35.63%).
- Predeclared scale-transfer decision: supports transfer.

The magnitude is lower than at 8B, so the result supports persistence across scale but not scale invariance. The experiment does not establish behavior for proprietary or arbitrary large models.
