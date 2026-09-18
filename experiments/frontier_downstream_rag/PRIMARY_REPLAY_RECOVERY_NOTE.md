# PRIMARY REPLAY RECOVERY NOTE

The completed full Qwen3-8B frontier/downstream executions produced all 12 prespecified states for each frozen query. Their temporary result-archive URLs expired before durable retrieval, while the aggregate summaries and raw-output hashes remained in the execution logs.

To recover the paired per-query records needed for the locked bootstrap, this script deterministically regenerates **only the already-defined primary contrast** (k=10 updated-unconstrained vs k=10, eta=0.001 frontier-controlled) using the identical frozen panel, model revision, prompt lock, seed, greedy decoding and software stack.

This replay is not a new endpoint, does not select or exclude queries, and cannot change the previously completed aggregate result. Its role is compact result recovery and reproducibility. The replayed aggregate must match the original completed full-state summaries before use.

## First compact replay mismatch

The first compact replay used batch size 8, whereas the completed full-state generation had used batch size 4. Although the frozen identity/frontier quantities were reproduced exactly, the batch-8 replay differed by one or two benchmark-correctness cases in NQ, FEVER and SciFact. Those batch-8 replay outputs are therefore **not used** for endpoint analysis. This indicates a small numerical/inference-path sensitivity to batch composition despite greedy decoding and deterministic-algorithm settings.

A second compact replay is required at **batch size 4**, matching the completed full-state execution. It must reproduce the original per-dataset aggregate summaries before its per-query pairs are accepted for the locked bootstrap. This recovery rule was written before the batch-4 replay was launched.

## Second replay and exact execution-path recovery

The batch-size-4 compact replay still generated only two prompts per query (updated and primary controlled) rather than the twelve prompts produced by the completed full-state execution. Its aggregate matched the batch-8 compact replay, not the original full-state aggregate. Thus **batch composition / tensor shape**, not merely the nominal batch-size argument, changes a very small number of greedy Qwen3-8B outcomes under this stack.

Those two-state replays are not used for endpoint inference. The accepted recovery must reproduce the original execution path exactly: for each query, instantiate all 12 prespecified prompts in the original order (k=5,10,20 × reference, updated, eta=0.0001, eta=0.001), generate them in consecutive batches of four, and only then extract the k=10 updated and eta=0.001 pair for compact logging. The aggregate must match the already-completed full-state summaries before per-query records are accepted.
