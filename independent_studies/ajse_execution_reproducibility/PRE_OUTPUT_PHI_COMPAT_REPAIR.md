# Pre-output Phi-3.5 Transformers compatibility repair

**Timing:** documented after the initial Phi-3.5 jobs failed on the first generation call and before any Phi-3.5 benchmark response was produced.

The pinned model revision loaded successfully, but `trust_remote_code=True` selected the repository's older `modeling_phi3.py`, whose generation helper expects the removed `DynamicCache.seen_tokens` attribute under Transformers 4.57.6. The failure occurred before the first response was returned.

Repair: load the exact same pinned weights/config/tokenizer revision through the native Phi-3 implementation shipped in Transformers 4.57.6 (`trust_remote_code=False`).

No model weights/revision, dataset, frozen panel, prompt, endpoint, seed, decoding rule, evaluator or statistical analysis changes. The runtime implementation choice is recorded explicitly in the execution manifest.
