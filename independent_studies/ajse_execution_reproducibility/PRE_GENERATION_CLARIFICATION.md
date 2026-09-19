# Pre-generation execution clarification — LLM-EXEC-REPRO-AJSE-v1

**Timing:** committed before any model generation.

The scientific conditions remain solo repeat versus alternative batch composition. This clarification makes batching computationally complete while preserving exactly 150 scored targets per dataset.

For each dataset the freezer selects 152 output-blind items using the locked SHA-256 ordering. The first 150 are scored targets; the next two are support anchors only and are never included in the study denominator.

For each pinned model separately:

- tokenize all 152 fixed prompts with that model's pinned tokenizer;
- **batch4-near:** sort by tokenized input length (then item ID) and form consecutive groups of four;
- **batch4-mixed:** sort by tokenized input length, split the ordered 152 prompts into four equal strata of 38, then form 38 groups by taking position i from each stratum.

Thus every scored target occurs exactly once in each batch condition, both conditions use batch size four, and mixed groups deliberately span the length distribution without choosing co-batch prompts from model outputs. The two support anchors make 152 divisible by four and are not scored.

This clarification replaces the less efficient prose description of choosing three anchors independently for every target. It changes no model, dataset, target count, prompt, endpoint, decoding rule or statistical analysis.
