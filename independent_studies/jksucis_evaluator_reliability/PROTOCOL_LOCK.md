# LLM-EVAL-RELIABILITY-JKSU-v1 — public pre-output protocol lock

**Target journal:** Journal of King Saud University – Computer and Information Sciences

**Status:** independent clean-room study, locked before model generation.

## Research question

Can predeclared evaluator/parsing rules applied to the **same model outputs** change benchmark accuracy, model ordering, or statistical conclusions about which model performs better?

This study evaluates benchmark measurement reliability. It does **not** use RIDI, allocation identity, retrieval-membership equivalence, the Nature RAG panels, EPSS, CMS or any Nature-main result.

## Frozen models

- Qwen/Qwen2.5-7B-Instruct — revision `a09a35458c702b33eeacc393d103063234e8bc28`
- mistralai/Mistral-7B-Instruct-v0.3 — revision `c170c708c41dac9275d15a8fff4eca08d52bab71`
- allenai/OLMo-2-1124-7B-Instruct — revision `470b1fba1ae01581f270116362ee4aa1b97f4c84`
- microsoft/Phi-3.5-mini-instruct — revision `2fe192450127e6a83f7441aef6e3ca586c338b77`

## Frozen datasets

- allenai/ai2_arc — revision `210d026faf9955653af8916fad021475a3f00453`; ARC-Challenge only
- allenai/openbookqa — revision `388097ea7776314e93a529163e0fea805b8a6454`
- tau/commonsense_qa — revision `94630fe30dad47192a8546eb75f094926d47e155`
- lukaemon/bbh — revision `982bb89fd79532a8ac676a61fc42eb1aeec63f99`; only tasks with unambiguous finite answer labels selected before generation

None is a Nature-main experimental dataset.

## Sampling lock

Use 250 eligible items from each of ARC-Challenge, OpenBookQA and CommonsenseQA plus 250 eligible BBH items pooled across the predeclared finite-label tasks, for 1,000 items total.

Selection is output-blind: sort stable item identifiers by SHA-256 of `study_id|dataset|item_id|20260919` and take the first required items. Exact IDs, gold labels and prompt hashes are frozen before GPU generation.

## Prompting and generation

Generate **one free-form response per model per item**. The prompt requests a short explanation and ends with: `End with: Final answer: <choice label>`.

- greedy decoding; `do_sample=False`;
- seed 20260919;
- deterministic PyTorch algorithms requested;
- TF32 disabled;
- no quantization;
- max_new_tokens=128;
- native chat template;
- exact software/GPU environment archived.

No response is regenerated because a parser fails.

## Frozen evaluator family

Every saved response is scored under all evaluators:

**E1 strict-final-line**  
Accept only a final non-empty line exactly matching `Final answer: <valid label>` after Unicode normalization and surrounding-whitespace removal.

**E2 tolerant-final-line**  
On the final non-empty line, accept the first valid label following case-insensitive variants of `final answer`, allowing markdown wrappers and punctuation.

**E3 last-valid-label**  
Extract the last standalone valid choice label anywhere in the response.

**E4 choice-text**  
If no label is used, match a uniquely normalized answer-choice text on the final non-empty line; ambiguous multiple matches remain unparsed.

**E5 frozen-hybrid**  
Apply E2, then E4 if E2 is unparsed. E5 is the predeclared reference evaluator for descriptive benchmark accuracy, but all evaluator comparisons are reported.

Unparsed outputs count as incorrect for benchmark accuracy and are also reported separately.

## Primary endpoints

1. **Strict ranking reversal:** for a dataset and model pair, model A accuracy > model B under one evaluator and A < B under another.
2. **Conclusion instability:** evaluator change alters whether the 95% paired bootstrap interval for model A minus model B excludes zero, or reverses its sign.
3. **Absolute score range:** max minus min accuracy across E1–E5 for each model × dataset cell.

## Secondary endpoints

- unparsed-output rate by evaluator;
- item-level correctness discordance across evaluators;
- overall equal-dataset model ranking under each evaluator;
- Kendall rank agreement across evaluator-specific model rankings;
- task-format strata and response-length strata.

## Statistical lock

For every evaluator, model-pair and dataset, use 100,000 paired item bootstrap resamples with seed 20260919. For overall summaries, resample within dataset and weight datasets equally.

All 5 evaluators and all pairwise model comparisons are retained. No parser is discarded because it produces an inconvenient ranking.

No family-wise error-control claim is made; confidence intervals describe evaluator sensitivity.

## Claim boundary

The study can show that benchmark conclusions depend on evaluator implementation for the tested generative multiple-choice setting. It cannot establish unreliability of every benchmark or every structured-constrained evaluation system.
