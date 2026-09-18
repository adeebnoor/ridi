# Technical deviation — durable raw-output transport, 18 September 2026

Protocol: `RIDI-NATURE-FRONTIER-DOWNSTREAM-v1`

The first generation execution, Hugging Face Job `6aad4e0a51992417dfcc6f64`, ran the locked model, prompts, states and scorers. It completed the Natural Questions panel and had reached 70/100 HotpotQA queries when it was cancelled.

The reason for cancellation was **output retention only**. The runner uploaded the completed NQ result ZIP to tmpfiles.org and printed its SHA-256, but an independent GitHub Actions archiver retrieved non-matching bytes from that URL and a subsequent relay request received HTTP 403. Because the protocol requires raw generations to be archived, continuing the remaining datasets would have risked completing endpoints without durable raw-output retention.

The NQ aggregate summary had become visible in the job log before this transport problem was diagnosed. No scientific or analytic parameter was changed after seeing that summary. In particular, the frozen 400-query panel, model/revision, prompts, k values, eta values, state construction, decoding, scorers, primary contrast and locked aggregate-analysis code remain unchanged.

The only runner change is to emit the already-created result ZIP as base64 chunks to the job log after each dataset completes. These chunks are a byte-preserving transport of the archive and do not enter model inference or scoring.

The complete four-dataset execution is rerun from the start under the unchanged generation/scoring lock. The first partial execution remains part of the public audit trail and is not treated as an independent replicate.
