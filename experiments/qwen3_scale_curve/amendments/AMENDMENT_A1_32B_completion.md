# Amendment A1 — completion of the Qwen3-32B jobs on two 80-GB GPUs

Study: RIDI-RAG-QWEN3-SCALE-CURVE-v1 (OSF whjbs; code commit 869abda18a17ba528ecfcddcb4461914b8b113c1).
Status at filing: registered BEFORE any A1 job is started.

## Why
Under the registered protocol, three of the four Qwen3-32B jobs (NQ, FEVER, SciFact) ended after three identical attempts with a technical failure (`OutOfMemoryError`) on one 80-GB GPU while generating the registered fixed batch of 16. H1 (persistence at 32B) could therefore not be evaluated. The original 0.6B–14B outputs are preserved unchanged. The initial invocation of the locked analysis stopped before producing estimates or hypothesis decisions because of the task-label mismatch documented in DEVIATION_001. No completed five-size analysis exists at filing.

## What changes
Only the hardware: the same locked runner (`run_scale_curve.py`, SHA-256 as in LOCK.json), with `device_map="auto"`, is run with exactly **two visible A100 80-GB GPUs** on a four-A100-80-GB host. The host is provisioned as four GPUs because a two-GPU A100/H100 flavor is unavailable from the current provider; CUDA_VISIBLE_DEVICES=0,1 restricts the unchanged runner to two GPUs. The other two GPUs are not exposed to the process. The runner already permits ≥1 GPU and records the device map. Nothing scientific changes: the same model revision, bfloat16 weights (no quantization), greedy decoding, max_new_tokens = 128, thinking disabled, seed 20260902, the same 800 questions, prompts and exchange, and the same fixed batch of 16 for the execution floor. The configuration hash computed by the runner does not include hardware and is therefore identical to the original attempts.

## How
- All four Qwen3-32B datasets (including HotpotQA, which succeeded originally) are run afresh in a new output directory (`ridi_scale_out_A1`), attempts 1–3 under the same failure rules. Re-running HotpotQA keeps the 32B condition homogeneous; the original HotpotQA result is reported alongside as a reproducibility check.
- No other model is re-run. No outcome file of the original run is modified.

## Analysis
The locked `aggregate_scale_curve.py` is run once, unchanged (with DEVIATION_001), on a combined directory containing the original 0.6B–14B jobs and the A1 Qwen3-32B jobs. H1–H3 and S1–S5 are reported exactly as registered. The failed initial analysis invocation and its error receipt remain part of the record. No completed original five-size analysis is claimed. The experiment operator delivers the A1 output directory without inspecting outcomes or running analysis; the investigator performs the combined analysis using DEVIATION_001.

## If A1 fails
If any A1 32B job exhausts three technical attempts, H1 is reported as not executed and no further amendment is made.
