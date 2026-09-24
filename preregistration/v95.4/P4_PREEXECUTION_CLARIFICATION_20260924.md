# P4 pre-execution clarification — 24 September 2026

## Status

This is a **post-registration, pre-execution clarification** to OSF registration `ms4w8`.
The filed registration specified that P4 would use "two prespecified LLM judges from different model families" but inadvertently did not name the exact judge model identifiers or immutable revisions. No real-model P4 judge output and no P4 human annotation existed when this clarification was first committed.

Because the exact IDs were omitted from the filed text, P4 will be reported as **prospectively amended before execution**, not as an untouched preregistered endpoint. No threshold, endpoint, sample, prompt, clean-subset rule, bootstrap rule, or human-audit sample size is changed.

## Final frozen machine judges

Judge 1:
- Model: `Qwen/Qwen3-32B`
- Immutable revision: `9216db5781bf21249d130ec9da846c4624c16137`
- Family: Qwen3

Judge 2:
- Model: `microsoft/phi-4`
- Immutable revision: `2db69c1c3e91a05d2c64a3185acfbaf36f744e25`
- Family: Phi3/Phi-4
- License: MIT

Rationale fixed before P4 study output: two independently developed open-weight instruction-tuned model families, both runnable through the same Transformers causal-language-model path. Qwen3-32B was already frozen elsewhere in the registered extension as the P5 semantic-equivalence judge. Phi-4 provides a family-diverse second judgement model and passed the non-study semantic control described below.

## Pre-execution technical and capability-control record

All checks below used generic, non-study prompts. No P4 passage, clean-subset status, or correctness-change outcome had been observed.

1. The first clarification named `mistralai/Mistral-Small-3.1-24B-Instruct-2503` (revision `68faf511d618ef198fef186659617cfd2eb8e33a`) as Judge 2. Its non-study smoke test failed before inference because the frozen `AutoModelForCausalLM` execution path rejected `Mistral3Config`. No P4 item was processed.
2. A technically compatible alternative, `allenai/OLMo-2-1124-13B-Instruct` (revision `3a5c85baefbb1896a54d56fe2e76c0395627ddf4`), returned `NO` to a generic positive control in which the passage explicitly stated that Paris is the capital of France. Because this raised a pre-study semantic-quality concern, OLMo2 was not used on P4 data.
3. Before final locking, candidate judges were evaluated on a four-item generic control set using the exact P4 question/passage prompt form: two obvious informative passages and two clearly irrelevant passages. Qwen3-32B scored 4/4; Microsoft Phi-4 scored 4/4; NousResearch Hermes-3-Llama-3.1-8B also scored 4/4. Phi-4 was selected before any P4 study output because it is a larger independently developed family with a permissive MIT license and the same executable causal-LM path.

This model choice is therefore a documented **pre-execution amendment based only on technical/capability controls, not study outcomes**.

## Frozen inference implementation

- Exact P4 judgement prompt: unchanged from the v95.4 code freeze `08_New_Experiments/p4_semantic_audit.py` (SHA-256 `b512706885796c2100f285380bcb5018785b2a00022508059d37606ddf8d1e1f`).
- Output vocabulary: exactly `YES` or `NO`; any other output is missing/unparsed.
- Greedy decoding; sampling disabled.
- `max_new_tokens=8`.
- bfloat16 inference.
- deterministic-algorithm mode enabled; TF32 disabled.
- fixed generation batch size: 8 passages.
- every one of the 14,586 exchanged query–passage items is judged by both models.
- gold-string detection and the clean-query definition are unchanged from the frozen P4 code.
- source contexts SHA-256: `1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1`.

The explicit batch size and revision arguments are implementation clarifications required to make the previously frozen P4 code executable with immutable local model versions. They do not change the scientific endpoint.

## Human annotation

The registered 200-item blinded human audit remains **blocked** until King Abdulaziz University issues the institutional determination and all applicable requirements are satisfied. No human annotation is authorized by this clarification.

## Reporting rule

P4 is labelled supported only if the original registered rule is met in the clean subset:
1. correctness-change point estimate >= 0.05, and
2. the lower 95% stratified-bootstrap bound > 0.02.

If the rule fails, it will be reported as failure. No alternative judge, threshold, prompt, subset definition, or exclusion rule will replace it after results are observed.
