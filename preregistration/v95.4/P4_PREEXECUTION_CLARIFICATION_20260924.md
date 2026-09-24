# P4 pre-execution clarification — 24 September 2026

## Status

This is a **post-registration, pre-execution clarification** to OSF registration `ms4w8`.
The filed registration specified that P4 would use "two prespecified LLM judges from different model families" but inadvertently did not name the exact judge model identifiers or immutable revisions. No real-model P4 judge output and no P4 human annotation existed when this clarification was committed.

Because the exact IDs were omitted from the filed text, P4 will be reported as **prospectively amended before execution**, not as an untouched preregistered endpoint. No threshold, endpoint, sample, prompt, clean-subset rule, bootstrap rule, or human-audit sample size is changed.

## Frozen machine judges

Judge 1:
- Model: `Qwen/Qwen3-32B`
- Immutable revision: `9216db5781bf21249d130ec9da846c4624c16137`
- Family: Qwen3

Judge 2:
- Model: `mistralai/Mistral-Small-3.1-24B-Instruct-2503`
- Immutable revision: `68faf511d618ef198fef186659617cfd2eb8e33a`
- Family: Mistral3

Rationale fixed before P4 output: two independently developed open-weight instruction-tuned model families, both large enough for semantic evidence judgement and runnable under the available frozen execution environment. Qwen3-32B was already frozen elsewhere in the registered extension as the P5 semantic-equivalence judge; Mistral provides the required family-diverse second judge.

## Frozen inference implementation

- Exact P4 judgement prompt: unchanged from the v95.4 code freeze `08_New_Experiments/p4_semantic_audit.py`.
- Output vocabulary: exactly `YES` or `NO`; any other output is missing/unparsed.
- Greedy decoding; sampling disabled.
- `max_new_tokens=8`.
- bfloat16 inference.
- deterministic-algorithm mode enabled; TF32 disabled.
- fixed generation batch size: 8 passages.
- every one of the 14,586 exchanged query–passage items is judged by both models.
- gold-string detection and the clean-query definition are unchanged from the frozen P4 code.

The explicit batch size and revision arguments are implementation clarifications required to make the previously frozen P4 code executable with immutable local model versions. They do not change the scientific endpoint.

## Human annotation

The registered 200-item blinded human audit remains **blocked** until King Abdulaziz University issues the institutional determination and all applicable requirements are satisfied. No human annotation is authorized by this clarification.

## Reporting rule

P4 is labelled supported only if the original registered rule is met in the clean subset:
1. correctness-change point estimate >= 0.05, and
2. the lower 95% stratified-bootstrap bound > 0.02.

If the rule fails, it will be reported as failure. No alternative judge, threshold, prompt, subset definition, or exclusion rule will replace it after results are observed.
