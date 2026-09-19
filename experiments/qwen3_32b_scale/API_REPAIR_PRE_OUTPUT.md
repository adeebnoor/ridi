# PRE-OUTPUT API-COMPATIBILITY REPAIR

Protocol: `RIDI-RAG-QWEN3-32B-SCALE-v1`

All four first execution jobs stopped after source/archive verification and **before prompt-manifest verification, model loading, or Qwen3-32B generation** because the scale runner called the frozen helper `load_run` with three positional arguments. The original registered helper signature is `load_run(path, fmt="trec")`.

The scale runner is corrected to call `load_run(root / rp, "trec")`, exactly matching the original registered `run_cell.py` implementation.

No source, query, context, prompt, model, generation setting, scorer, endpoint, or decision boundary changes.
