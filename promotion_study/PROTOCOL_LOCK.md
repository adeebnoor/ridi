# EVAL-RANK-JKSUCIS-v1 — PRE-OUTPUT PROTOCOL LOCK

Target journal: **Journal of King Saud University – Computer and Information Sciences**

Status: protocol fixed before model endpoint generation for this study.

## Research question

Can reasonable deterministic evaluator implementations change absolute benchmark scores or reverse the apparent ranking of language models when the underlying raw model outputs are held fixed?

## Models

Three primary open models, intentionally different from the Nature Qwen3 primary/scale experiments:
1. `Qwen/Qwen2.5-3B-Instruct`
2. `microsoft/Phi-3.5-mini-instruct`
3. `HuggingFaceTB/SmolLM2-1.7B-Instruct`, immutable revision `31b70e2e869a7173562077fd711b654946d38674`

Before the first successful generation, exact immutable revisions for models 1 and 2 must be appended in `EXECUTION_LOCK.md`. Model identities cannot change after output inspection.

## Benchmarks — distinct from Nature and AJSE primary panels

- CommonsenseQA
- OpenBookQA
- HellaSwag
- BoolQ

No MMLU-Pro, GSM8K, ARC-Challenge or TruthfulQA item from the AJSE primary design is used here.
No Nature benchmark is used.

Primary sample: up to 250 evaluation items per benchmark. If a public evaluation split contains fewer, use the full split. Selection is frozen outcome-blind by stable ID before generation.

## Single generation, multiple evaluators

For every model × item there is exactly one saved raw generation used by all evaluator pipelines. Evaluators do not trigger regeneration.

Prompt asks for a concise answer and requires a final line of the form `FINAL: <choice>` or `FINAL: yes/no` as appropriate.

Generation:
- native chat template;
- greedy decoding;
- max_new_tokens = 96;
- seed = 20260919;
- model-specific immutable revisions;
- environment and raw-output SHA-256 recorded.

## Predeclared evaluators

E1. **Anchored-final**: score only the content following the last syntactically valid `FINAL:` marker.

E2. **First-valid-choice**: first unambiguous valid option/boolean token in the completion.

E3. **Last-valid-choice**: last unambiguous valid option/boolean token in the completion.

E4. **Wrapper-tolerant**: deterministic normalization of common wrappers/punctuation followed by anchored answer extraction.

E5. **Option-text matcher**: deterministic normalized exact match to an answer-option text when no valid symbolic answer is available; ambiguous multiple matches score unresolved rather than guessed.

All parser code must be frozen before raw outputs are scored.

## Primary endpoints

1. **Pairwise model-ranking reversal rate** across benchmark × model-pair comparisons between E1 and E2. A reversal requires opposite nonzero signs in accuracy difference; ties are reported separately, not forced into reversals.

2. **Evaluator-induced decision disagreement**: item-level proportion for which E1 and E2 assign different scored decisions to the same raw output.

## Secondary endpoints

- score deltas across all evaluator pairs;
- ranking reversals for E1 vs E3/E4/E5;
- unresolved/abstention rates;
- model × benchmark interaction;
- whether ranking changes remain after excluding outputs that fail to contain any explicit final-answer marker;
- calibration is not claimed unless probabilities are explicitly available.

## Statistical analysis

- report all model × benchmark × evaluator cells;
- 100,000 item-level bootstrap replicates within benchmark, seed `20260919`;
- for each model pair, bootstrap the accuracy difference under each evaluator;
- report reversal only from observed signs; additionally report bootstrap frequency of sign disagreement as uncertainty, not as a posterior probability;
- no evaluator may be dropped because it yields an inconvenient result;
- no LLM-as-a-judge in the primary analysis.

## Strong-result criterion without outcome shopping

The paper's strongest supported conclusion will be chosen only from the predeclared hierarchy:
1. ranking reversal, if observed;
2. otherwise statistically/quantitatively meaningful score instability;
3. otherwise evaluator robustness with bounded differences.

Null robustness is publishable and must not trigger evaluator replacement.

## Claim boundary

This study evaluates benchmark implementation sensitivity. It does not claim that benchmark labels are wrong, that one evaluator is universally correct, or that model capability itself changes when only the parser changes.

## Anti-overlap rule

No Nature or AJSE result may be inserted as empirical evidence. Related work may cite public literature only; unpublished related manuscripts are handled through journal disclosures rather than data reuse.
