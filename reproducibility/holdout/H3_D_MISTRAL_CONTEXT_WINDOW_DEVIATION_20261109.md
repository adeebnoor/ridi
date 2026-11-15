# H3 D pre-generation operational deviation — Mistral context window
Date: 2026-11-09 (pre-D generation).

Original W generation used max_model_len=8192 for Mistral-7B-Instruct-v0.3. Frozen full-corpus H3 D prompts were independently tokenized before any D generation (1500 cells); one FEVER case, qid=202303, contains 10,794 input tokens, exceeding 8,192. Initial preflight FAILURE is retained with its SHA-256.

**Change:** Set D Mistral runtime max_model_len from 8192 to 16,384 for all 1500 D prompts; 128 output tokens unchanged. This is a runtime accommodation, not a modification to the prompt text, gold labels, retrieval rankings, order, context, model revision, seed, decoding or scorer. The 1500 frozen input-token hashes stay identical. Qwen context remains 32,768 and previous W runs remain untouched.

**Source of hardware/model support:** published Mistral-7B-Instruct-v0.3 model configuration documents max_position_embeddings=32768 (https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3/blob/708a0609e640ac1edfb9020a7c934f51d34d6c79/config.json). A 16,384-token runtime context is below this supported model maximum. Actual A100 vLLM allocation and token-replay gates must pass before inference.

**Deviation disclosure:** This is a post-freeze, pre-D-outcome implementation change relative to the 8,192-token W configuration. It must be declared in manuscript methods and appropriate OSF amendment before presenting H3 D results as formally confirmatory. The different runtime limit could affect resource scheduling, though input strings and deterministic generation settings are unchanged. No case is silently excluded, shortened, or imputed. Never label this a preregistered configuration.
