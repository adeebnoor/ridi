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

## Independence boundary

An execution by the manuscript author is a prospective external-outcome validation, not an independent-team replication. A second team must start from the protocol-lock commit, run the sealed package without author intervention, and return the generated execution record and file hashes before the manuscript may use the word *independent*.
