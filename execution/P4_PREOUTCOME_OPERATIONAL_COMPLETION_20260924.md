# RIDI Nature P4 pre-outcome operational completion — 24 September 2026

Status: **locked before any new P4 machine-judge output**.

This note completes two implementation details that were insufficiently explicit in the public OSF registration `ms4w8`. The registration fixed the P4 endpoint and required **two LLM judges from different model families**, but it did not name their exact model identifiers or immutable revisions. That omission is disclosed here rather than treated as if the identities had been fully preregistered.

## Judge identities fixed before P4 output

The machine-judge stage will use the two already pinned open models named elsewhere in the filed protocol:

1. `Qwen/Qwen3-8B`, revision `b968826d9c46dd6066d109eabc6255188de91218`.
2. `allenai/OLMo-2-1124-7B-Instruct`, revision `470b1fba1ae01581f270116362ee4aa1b97f4c84`.

They are from different model families. Qwen thinking remains disabled. Both use deterministic greedy generation with at most 8 new tokens.

Because exact judge identities were not stated in the OSF filing, results from this machine-judge stage will be described as **pre-outcome operationally completed after registration**, not as fully preregistered with respect to judge identity.

## Frozen prompt and endpoint

The original `p4_semantic_audit.py` prompt and P4 decision rule are unchanged:

- every exchanged passage is judged YES/NO for whether it contains any information that could help answer the question or support/refute the claim, including partial, indirect or misleading evidence;
- the clean-query subset requires every exchanged passage to be judged uninformative by **both** judges and no normalized QA gold string;
- the registered correctness-change endpoint and bootstrap rule are unchanged.

No threshold, exclusion rule, query panel, scorer, or outcome definition is altered.

## Operational batch correction

The frozen implementation used a hard-coded batch of 256 judge prompts. With GPU inference this is an execution-risk parameter, not a scientific endpoint. Before any P4 output, the operational copy is changed only to:

- accept immutable model revisions explicitly;
- record model revision in each output row; and
- make judge batch size configurable, defaulting to 32.

The prompt strings and per-passage inputs are unchanged. Batch size will not be analyzed as a scientific factor.

Operational script SHA-256:
`1a004ec44252f5e75d8dae6a10d9bb6a7df3ae0f5e16c2bde0ad598c040bc294`.

## Human annotation remains blocked

The registered human-audit stage is **not authorized by this addendum**. No human annotation, recruitment, or consent activity will begin before the King Abdulaziz University institutional determination and satisfaction of any applicable requirements.

## Interpretation

This addendum is a provenance correction, not a retroactive amendment of the OSF registration. P4 findings will explicitly disclose this timing and will not be used to claim that the omitted judge identities were prospectively registered.
