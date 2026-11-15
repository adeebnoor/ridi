# RIDI-CONFIRM-C Source Data (commercial-model replication of the held-out test)
Registration: https://osf.io/anbjd/ (DOI 10.17605/OSF.IO/ANBJD), addendum v1.3 (`ADDENDUM_FOR_OSF.md`, SHA-256 6b62c1f7a5a58d629533bcfd0213c214996395eb81264c6b91e5bffd257d2b1e). Criterion not met (H1c supported only for gemini-3.8-flash).

| File | Content |
|---|---|
| `RESULTS.md`, `results_summary.json`, `H1_H4_commercial.json` | Report written by the frozen analysis script (H1c–H4c, format-scorer sensitivity, completion, spend). `H1_H4_commercial.json` SHA-256 692a8318af1e667f2aafe9ffdb2ba9be3f110be213c708ea3928c53dc19ef553 |
| `scores_commercial.csv` | Correctness scores from the frozen scorer, SHA-256 70d4c6990235099a8f0379f793b0f7e0177d0f21266fde9f1109e2fd3d35b6ec. Regenerated on 13 Nov 2026 from the raw outputs with `code/score_and_analyze.py`; the report above was reproduced byte for byte |
| `runs/<model>/raw_outputs.jsonl.gz`, `run_meta.json` | Raw model outputs (gzip; the SHA-256 of the decompressed file equals `raw_outputs_sha256` in `run_meta.json`), 7,500 calls per model |
| `SPEND_LEDGER_final.json`, `RUN_LOG.md`, `logs/` | Spend ledger (total US$60.12 including technical checks), run log, supervisor and runner logs (stalls, restarts, the 02:06:45 restart on the rented host) |
| `code/` | Runner, pinned settings, technical-check script, supervisor, analysis wrappers. SHA-256 values are in `MANIFEST_SHA256.txt` |
| `MANIFEST_SHA256.txt` | Hashes of the frozen inputs (prompts, flags, scorer adapter, scorer, analysis script), the code and the addendum |

Not distributed: the frozen prompt files (large; hashes are in the manifest and the prompts are those of RIDI-CONFIRM, registered at https://osf.io/794p5/), API keys (never written to disk). To re-run the analysis: place `frozen_inputs/` (from the RIDI-CONFIRM archive) next to `code/`, decompress the raw outputs into `runs/<model>/raw_outputs.jsonl` and run `python code/score_and_analyze.py --gold frozen_inputs/holdout_1500_gold.jsonl`.
