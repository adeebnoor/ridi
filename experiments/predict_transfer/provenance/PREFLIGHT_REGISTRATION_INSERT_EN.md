## Tokenizer-only preflight counts (before registration and generation)

Preflight completed without loading model weights or generating model responses. The source archives and all 73 registered artifacts passed SHA-256 verification. The original exclusion filter was recovered byte-for-byte and matched the prespecified SHA-256; it was not rebuilt.

| Benchmark | Archive queries | Registered eligible | Frozen-panel exclusion | Additional known-source exclusion | Duplicate exclusion | Context-length exclusion | Fresh eligible | Selected n |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Natural Questions | 2255 | 2255 | 250 | 300 | 0 | 0 | 1705 | 250 |
| HotpotQA | 7405 | 7405 | 250 | 300 | 0 | 0 | 6855 | 250 |
| FEVER | 6656 | 6656 | 150 | 311 | 78 | 0 | 6117 | 300 |
| SciFact | 299 | 299 | 150 | 149 | 0 | 0 | 0 | 0 |

Included benchmarks: nq, hotpotqa, fever. Total selected n = 800; planned model-by-draw-by-benchmark units = 24.

Exclusions are sequential and mutually exclusive. Counts are bounded by the registered prepared-v4 input archives; the SciFact archive contains 299 queries. Eligibility uses the unchanged registered select_universal_panel with limit=len(queries). All three contexts were rendered with each of the five tokenizers, preserving the frozen runner’s chat-rendering and special-token handling. The context gate reserved 128 output tokens, with limits of 40,960 for each Qwen3 model and 4,096 for OLMo-2. Token sequences were never truncated.

Benchmarks below 75 fresh eligible questions are excluded. The prespecified SciFact-to-FEVER reallocation and sampling seed 20261012 were applied. Sampling preserves input query order. The optional pre-generation AI-judge covariate was not collected. Known limitations of unrecovered project input history remain unchanged.

OLMo-2-0325-32B-Instruct revision: `b96024342a77a69aa0dda815c3454a671f477463`. No thinking block was produced by its tokenizer-only template probe.

FRESH_PANEL.json SHA-256: `6bf4deffdf1c6b961f5f0762626edbef1a68ba5b49d3d26d23022b3c87f00b54`. This receipt is not a scientific lock; the runner, configuration and panel must be locked and published after registration and before generation.
