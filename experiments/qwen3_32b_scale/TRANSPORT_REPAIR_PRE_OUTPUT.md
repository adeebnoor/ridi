# PRE-OUTPUT TRANSPORT REPAIR — Qwen3-32B scale transfer

Protocol: `RIDI-RAG-QWEN3-32B-SCALE-v1`

**Timing:** committed before any successful Qwen3-32B model generation or endpoint output.

The temporary Firestorage share used to transport the exact original post-registration control archive unexpectedly contained a second file (`prepared-v4-nq.zip`) in addition to `RIDI_RAG_NATURE_CONTROL_POSTREG_20260902.zip`. The initial runner required each share to contain exactly one file and would therefore have stopped before model loading.

The transport function is repaired to select the control and primary-results archives by **exact filename**. Dataset chunk shares remain byte-concatenated in their locked order. Every reconstructed archive is still required to match its predeclared full-file SHA-256 before extraction, and the runner still verifies the registered bundle, frozen manifest, document identities, panel membership and dataset prompt-manifest SHA-256 before loading Qwen3-32B.

No scientific element changes:
- same 800 registered queries;
- same BM25/k=10 reference and random document identities;
- same prompt bytes and scorers;
- same Qwen3-32B revision;
- same generation settings;
- same endpoint and predeclared transfer boundaries.

No Qwen3-32B endpoint was inspected before this repair.
