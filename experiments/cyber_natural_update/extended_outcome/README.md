# EPSS delayed-outcome sensitivity

Analysis ID: `RIDI-EPSS-EXTENDED-OUTCOME-v1`

This is a **post hoc sensitivity** extending follow-up of the locked EPSS v2→v3 analysis. It does not replace or relabel the original 365-day outcome window, which remains primary.

## Fixed elements

- Parent protocol: `RIDI-CYBER-NATURAL-UPDATE-v1`.
- Same source-pinned EPSS snapshots for 5–8 March 2023.
- Same source-pinned CISA KEV snapshot.
- Same candidate-universe intersection.
- Same exclusion of CVEs in KEV on or before 6 March 2023.
- Same descending EPSS score and lexical CVE tie-break.
- Same capacities: 100, 500, 1,000 and 5,000; k=1,000 is the primary reporting capacity.

## Added horizons

The original window is 8 March 2023 through 7 March 2024. Two descriptive calendar-horizon sensitivities are added without changing any selection rule:

- 8 March 2023 through 7 March 2025.
- 8 March 2023 through 7 March 2026.

The script aborts unless it first reproduces the locked one-year quantities: 195,886 candidates, 58 future KEV positives in the locked universe, and top-1,000 recovery of 8 under v2 versus 12 under v3.

## Interpretation

The longer windows increase follow-up time and may increase the number of observed delayed KEV additions. They are retrospective sensitivities, not preregistered endpoints, and must not be used to overwrite the original one-year result. Counts do not establish that EPSS changes caused exploitation or KEV inclusion.

## Run

```bash
python experiments/cyber_natural_update/fetch_inputs.py --out /tmp/ridi_epss_inputs
python experiments/cyber_natural_update/extended_outcome/run_extended_outcome.py \
  --inputs /tmp/ridi_epss_inputs \
  --out /tmp/ridi_epss_extended
```
