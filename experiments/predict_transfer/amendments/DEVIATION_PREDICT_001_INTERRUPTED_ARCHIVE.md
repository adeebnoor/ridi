# RIDI-PREDICT-v1: interrupted-archive exception approved by the investigator

STATUS: Investigator approved on 2026-10-10T21:02:38Z (2026-10-11 00:02:38 Asia/Riyadh). Public filing must precede any continuation. This document does not assert that a restart has occurred.

Registration: https://osf.io/xrzp5/
Frozen science commit: 1a665c54c645993f6912e4ad5bab10d0e3bb382b
LOCK SHA-256: bbecf34ab12308687643e41f90060d2066c62646a0aa006efab73671614044e2

## Observed event

The original predictor job 6aca94bafee2c9007018c7e8 and target job 6aca94c5fee2c9007018c7f4 were observed CANCELED. The provider cancellation cause and exact provider cancellation time are unknown. The two affected scientific runners independently recorded `failed`, `failure_kind=technical`, `error_type=InfrastructureInterrupted`, at 2026-10-10T20:04:09Z. These are authenticated original runner statuses, not externally invented classifications.

Affected attempts:

| Model | Dataset | Draw | Attempt |
|---|---|---|---|
| qwen3-1.7b | hotpotqa | A | 1 |
| qwen3-32b | nq | A | 1 |

The complete retained snapshots were recovered: 708 predictor log lines containing 624 complete encrypted packets, and 438 target log lines containing 401 complete encrypted packets. There are no sequence gaps within those retained snapshots; this does not establish preservation of bytes never emitted. The final full attempt archives and child logs for the two interrupted attempts were not found. All available partial-output packets are preserved: 24 for the interrupted HotpotQA attempt and 398 for the interrupted NQ attempt. Their answer contents remain unopened.

Two earlier qwen3-1.7b/NQ attempts, draw A and draw B, succeeded. Their authenticated technical statuses, full encrypted archives and child logs are preserved. No other unit has a recorded start in the recovered logs. No scientific analysis or early outcome inspection has been performed.

## Approved limited exception

The investigator accepts the absence of the final full archives and child logs ONLY for the two interrupted attempt-1 identities listed above, while retaining every recovered byte, original technical status, provider receipt, packet manifest, and this disclosure. Missing data will never be regenerated or represented as preserved. Failed attempts will not enter scientific analysis.

After public filing and before any scientific restart, the continuation will:

1. Keep both successful qwen3-1.7b/NQ units without rerunning them.
2. Start the two interrupted units at attempt 2, retaining attempt 1 as a recorded technical failure. Attempt 3 is allowed only after a newly recorded technical failure; counts are never reset.
3. Start the remaining 20 unstarted units at attempt 1, preserving their original relative order within each execution group.
4. Preserve all frozen scientific files and configuration hashes, models, datasets, draws, panel, seeds, prompts, thresholds, native BF16, batch 16, and prescribed hardware visibility.
5. Require complete authenticated archives and child logs for every subsequent attempted unit; no additional missing-archive exception is implied.
6. Run the frozen analysis once only after all 24 units reach the registered terminal condition and transport checks pass, subject solely to this explicitly identified exception.

The change concerns transport completeness after an infrastructure interruption. No hypothesis, scientific threshold, analysis specification or successful output is changed. The investigator approved this limited exception in the study conversation before continuation. OSF publication evidence and the continuation submission receipts will establish the prospective filing order. No filing timestamp or restart is asserted in this document.
