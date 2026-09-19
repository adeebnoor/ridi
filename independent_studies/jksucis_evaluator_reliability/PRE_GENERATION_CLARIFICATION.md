# Pre-generation sampling clarification — LLM-EVAL-RELIABILITY-JKSU-v1

**Timing:** committed before any model generation.

Frozen evaluation splits:

- ARC-Challenge: `test`;
- OpenBookQA: `test`;
- CommonsenseQA: `validation` because the public test split has blank gold labels;
- BIG-Bench Hard: `test`.

The predeclared finite-label BBH task pool is:

- date_understanding
- disambiguation_qa
- geometric_shapes
- logical_deduction_five_objects
- movie_recommendation
- ruin_names
- salient_translation_error_detection
- temporal_sequences

Each BBH item has explicit labelled options and a single parenthesized gold label. The 250 scored BBH items are selected output-blind from the pooled 2,000 items by the locked SHA-256 ordering.

No scientific endpoint or evaluator rule changes.
