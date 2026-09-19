# PRE-OUTPUT REPAIR 1 — TruthfulQA option-label capacity

Study: LLM-EXEC-REPRO-AJSE-v1

During CPU-only pre-generation construction of the companion-batch plan, the prompt builder stopped on a TruthfulQA multiple-choice item whose option count exceeded the original A–J label string. No language model had been loaded and no endpoint output had been generated.

The prompt builder is corrected from ten labels (A–J) to the alphabet A–Z. This is a representation-capacity repair only. It does not alter the frozen dataset revisions, selected IDs, sample hashes, execution conditions, endpoints, statistical plan, or Nature firewall.

The companion plan hashes are intentionally recomputed only after this correction and will then be added to the execution lock before model generation.
