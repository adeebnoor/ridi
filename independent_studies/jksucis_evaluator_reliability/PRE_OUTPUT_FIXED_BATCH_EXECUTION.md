# Pre-output fixed-batch execution note — LLM-EVAL-RELIABILITY-JKSU-v1

The first GPU attempts were canceled by the compute scheduler before completing any model panel. No benchmark response content, evaluator score, model accuracy, ranking, or study endpoint from those incomplete jobs was inspected or used.

For the complete execution, generation uses a **fixed batch size of 8** in frozen manifest order. The 1,000-item panel is exactly divisible by 8. Decoder-only tokenizers use left padding; the batch grouping and order are identical for all evaluator rules because evaluator scoring occurs only after the output bytes are saved.

This is a throughput/runtime implementation choice, not an outcome-dependent scientific change. The model revisions, prompts, 1,000 frozen items, max_new_tokens=128, greedy decoding, seed, precision, evaluators and statistical endpoints remain unchanged.

All incomplete canceled jobs remain in the audit trail and are excluded from analysis.
