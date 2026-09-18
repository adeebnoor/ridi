# PRIMARY REPLAY RECOVERY NOTE

The completed full Qwen3-8B frontier/downstream executions produced all 12 prespecified states for each frozen query. Their temporary result-archive URLs expired before durable retrieval, while the aggregate summaries and raw-output hashes remained in the execution logs.

To recover the paired per-query records needed for the locked bootstrap, this script deterministically regenerates **only the already-defined primary contrast** (k=10 updated-unconstrained vs k=10, eta=0.001 frontier-controlled) using the identical frozen panel, model revision, prompt lock, seed, greedy decoding and software stack.

This replay is not a new endpoint, does not select or exclude queries, and cannot change the previously completed aggregate result. Its role is compact result recovery and reproducibility. The replayed aggregate must match the original completed full-state summaries before use.
