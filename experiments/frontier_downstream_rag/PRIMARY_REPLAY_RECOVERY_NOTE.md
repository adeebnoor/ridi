# PRIMARY REPLAY RECOVERY NOTE

The completed full Qwen3-8B frontier/downstream executions produced all 12 prespecified states for each frozen query. Their temporary result-archive URLs expired before durable retrieval, while the aggregate summaries and raw-output hashes remained in the execution logs.

To recover the paired per-query records needed for the locked bootstrap, this script deterministically regenerates **only the already-defined primary contrast** (k=10 updated-unconstrained vs k=10, eta=0.001 frontier-controlled) using the identical frozen panel, model revision, prompt lock, seed, greedy decoding and software stack.

This replay is not a new endpoint, does not select or exclude queries, and cannot change the previously completed aggregate result. Its role is compact result recovery and reproducibility. The replayed aggregate must match the original completed full-state summaries before use.

## First compact replay mismatch

The first compact replay used batch size 8, whereas the completed full-state generation had used batch size 4. Although the frozen identity/frontier quantities were reproduced exactly, the batch-8 replay differed by one or two benchmark-correctness cases in NQ, FEVER and SciFact. Those batch-8 replay outputs are therefore **not used** for endpoint analysis. This indicates a small numerical/inference-path sensitivity to batch composition despite greedy decoding and deterministic-algorithm settings.

A second compact replay is required at **batch size 4**, matching the completed full-state execution. It must reproduce the original per-dataset aggregate summaries before its per-query pairs are accepted for the locked bootstrap. This recovery rule was written before the batch-4 replay was launched.
