# SOURCE LOCK — AJSE-LLM-EXEC-REPRO-v1

Locked before any model output.

Datasets are deliberately disjoint from the Nature-main RAG panel.

- openai/gsm8k — test split; current repository head observed as 740312a; parquet conversion lineage e53f048.
- allenai/ai2_arc — ARC-Challenge test; repository head 210d026; parquet conversion commit 1664417.
- Rowan/hellaswag — validation; parquet repository commit 218ec52.
- tau/commonsense_qa — validation; parquet repository commit 94630fe.

For the actual execution, downloaded parquet/source bytes and the exact selected 250-row panel for each dataset MUST be hashed with SHA-256 before any generation. Those content hashes, not mutable branch names, define the frozen inputs.

Models:
- Qwen/Qwen2.5-7B-Instruct: no Qwen3 may be used. Exact downloaded model/tokenizer file hashes must be recorded before generation.
- mistralai/Mistral-7B-Instruct-v0.3 pinned to 405950b9564feeced210f7c5d8089f76237b9861.

No Nature data/result is an input to this study.
