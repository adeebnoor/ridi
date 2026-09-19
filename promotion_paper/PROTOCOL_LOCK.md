# JKSUCIS-EVALUATOR-RELIABILITY-v1 — pre-output protocol lock

Target journal: Journal of King Saud University – Computer and Information Sciences.

Scientific question: can reasonable benchmark evaluation pipelines applied to the same fixed LLM outputs materially change measured accuracy, pairwise model ordering, or the statistical conclusion about which model performs better?

## Independence from Nature
No Nature-panel dataset, Qwen3 result, retrieval intervention, RIDI metric, frontier analysis, EPSS/CMS data, or Nature figure/table is permitted.

## Models
Use five open instruction models spanning families/sizes, pinned to immutable revisions before generation:
- Qwen2.5-3B-Instruct;
- Qwen2.5-7B-Instruct;
- Mistral-7B-Instruct-v0.3;
- a current open Microsoft Phi instruct checkpoint;
- a current open Google Gemma instruct checkpoint.

If licensing/access prevents one planned model, replacement must be documented before any endpoint is computed.

## Benchmarks
New, non-Nature panel:
- MMLU-Pro;
- GPQA, if its public licensing permits;
- BBH short-answer/multiple-choice tasks;
- TruthfulQA where gold evaluation is well-defined.

Freeze 200 examples per benchmark where available using outcome-blind seed 20260919. Freeze raw source hashes and selected IDs before generation.

## Generation
One fixed zero-shot prompt per benchmark; greedy decoding; max_new_tokens=128; no retrieval; no tools. Raw answer strings are generated once and then frozen. Evaluators operate only on those fixed outputs.

## Evaluators
E1 strict first admissible answer token/label;
E2 case/punctuation/whitespace normalized exact;
E3 wrapper-tolerant extraction of a final-answer marker or admissible label;
E4 deterministic structured-regex extraction using only benchmark-valid labels/patterns;
E5 constrained-format rerender is sensitivity-only and uses a separate generation run.

No LLM-as-judge is permitted in the primary analysis.

## Primary endpoints
1. Per-model accuracy spread: max(E1–E4) minus min(E1–E4).
2. Pairwise ranking reversals: whether sign(accuracy_A − accuracy_B) changes across E1–E4.
3. Study-level proportion of model-pair × benchmark comparisons with at least one ranking reversal.

## Secondary endpoints
- examples whose correctness status changes across evaluators;
- pairwise evaluator agreement;
- paired-bootstrap significance-conclusion changes;
- deterministic error taxonomy: wrapper text, multiple labels, answer restatement, punctuation/casing, numeric formatting.

## Statistical plan
100,000 paired stratified bootstrap resamples within benchmark, seed 20260919. Report all 10 model pairs across every benchmark.

## Strong-result rule
Ranking reversals are scientifically notable but not required. If none occur, report score spreads and upper bounds without changing endpoints.

## Claim boundary
Only evaluator-induced measurement instability under the declared tasks/parsers may be claimed. The Nature-main selected-membership claim is prohibited.
