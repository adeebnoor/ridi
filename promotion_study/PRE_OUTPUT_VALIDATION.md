# PRE-OUTPUT VALIDATION — LLM-EXEC-REPRO-AJSE-v1

Date: 19 September 2026

Status: **no language-model endpoint output has been generated for this study.**

Completed before output:
- Nature firewall publicly locked.
- Scientific protocol publicly locked.
- Two model revisions publicly frozen.
- Four dataset revisions publicly frozen.
- 600-target sample reconstructed independently from pinned sources and matched all four pre-output selected-manifest SHA-256 values.
- Qwen2.5-7B and Mistral-7B tokenizer-specific companion batch plans computed before generation and frozen by SHA-256.
- TruthfulQA option-label capacity repair documented before model output.
- Final runner and analyzer compile successfully.
- The runner hard-fails on frozen sample mismatch or companion-plan mismatch.
- The runner verifies that the target's non-padding token IDs are unchanged under batching.
- CPU-only preflight did not load either causal language model.

Compute status:
- Available local hardware is not adequate for the two locked unquantized 7B models.
- The connected Hugging Face Jobs service returned HTTP 402 Payment Required during compute preflight.
- The protocol is **not** weakened, quantized, resampled or resized in response. GPU generation remains pending.

This document records execution readiness, not a scientific result.
