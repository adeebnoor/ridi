# MANUSCRIPT BLUEPRINT — JKSUCIS

Working title (result-neutral):
**Evaluator sensitivity in language-model benchmarking: A controlled study with fixed model outputs**

Target: ≤6,000 words, double-anonymized main manuscript.

## Abstract
Problem → fixed-output multi-evaluator design → primary model-ranking/disagreement endpoints → result → benchmark-governance implication.

## 1. Introduction
Benchmark rankings depend on both model output and deterministic post-processing.
Gap: evaluator implementation is often treated as invisible plumbing.
Question: can plausible evaluator choices change score comparisons when raw outputs are identical?

## 2. Related work
LLM benchmarking; answer extraction; exact match/normalization; evaluation reliability; model ranking uncertainty. No unpublished Nature numerical result.

## 3. Materials and methods
3 models × CommonsenseQA/OpenBookQA/HellaSwag/BoolQ.
1,000 frozen items/model.
Batch-size-one deterministic generation.
Same saved raw output passed to E1–E5.

## 4. Evaluators and endpoints
E1 anchored final.
E2 first valid choice.
E3 last valid choice.
E4 wrapper tolerant.
E5 option-text deterministic fallback.
Primary: E1-vs-E2 ranking reversal and item-level decision disagreement.
Predeclared conclusion hierarchy retained even if reversal count is zero.

## 5. Results
5.1 Output/evaluator resolution rates.
5.2 Absolute score sensitivity.
5.3 Pairwise model-ranking stability/reversals.
5.4 Which output forms create evaluator disagreement.
5.5 Robustness across evaluators E3–E5.

## 6. Discussion
Evaluator code as part of a benchmark's measurement specification.
Practical recommendations: publish parser code, unresolved rates, raw outputs/hashes, and sensitivity across plausible deterministic extraction rules.

## 7. Limitations
Three open models; four discrete-answer benchmarks; no claim that one parser is universally correct; no capability-change claim.

## 8. Conclusion
State only the strongest rung supported by the locked hierarchy.

### Preplanned displays
Fig. 1 fixed-output evaluator design.
Fig. 2 accuracy by evaluator/model/benchmark.
Fig. 3 model-pair difference under E1 vs E2 with sign/reversal indication.
Fig. 4 unresolved and item-level evaluator disagreement.
Table 1 frozen models/datasets.
Table 2 all 12 pairwise ranking comparisons.
