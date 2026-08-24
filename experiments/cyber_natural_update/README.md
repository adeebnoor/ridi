# Cybersecurity natural-update validation

This directory contains the locked analysis for `RIDI-CYBER-NATURAL-UPDATE-v1`.

## Two-phase execution

1. Commit `PROTOCOL_LOCK.md`, `protocol.json` and the analysis code before downloading or parsing outcome data.
2. From that immutable commit, fetch the pinned inputs and run the analysis:

```bash
python experiments/cyber_natural_update/fetch_inputs.py \
  --out experiments/cyber_natural_update/inputs

python experiments/cyber_natural_update/run_locked_analysis.py \
  --inputs experiments/cyber_natural_update/inputs \
  --out experiments/cyber_natural_update/results
```

Inputs are excluded from Git because they are third-party public data. The input manifest and derived result tables are retained with source URLs and SHA-256 hashes.

## Locked author-run result

The production v2→v3 update changed 565 of the top 1,000 identities
(`RIDI=0.722`), compared with 0 and 7 changes in the adjacent same-version
daily controls. Top-1,000 recovery of CVEs added to CISA KEV during the next
year increased from 8 to 12 even though full-universe AUROC decreased from
0.665 to 0.610. The primary `eta=0.001` control avoided 40.9% of turnover but
retained 10 of 12 delayed outcomes, failing the locked 95% retention gate.

These are decision-system results, not estimates of exploit onset, complete
ground truth, or representation attribution. See `results/locked_results.json`.

## Blind independent execution

A second team can start with `replication/INSTRUCTIONS.md`. The sealed runner
verifies every locked file, fetches source-pinned public inputs and emits a
machine-verifiable execution record without reading the author's result file.

## Independence boundary

An execution by the manuscript author is a prospective external-outcome validation, not an independent-team replication. A second team must start from the protocol-lock commit, run the sealed package without author intervention, and return the generated execution record and file hashes before the manuscript may use the word *independent*.
