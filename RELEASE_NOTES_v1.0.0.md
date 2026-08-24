# RIDI v1.0.0

The first standalone public release of the RIDI decision-reproducibility toolkit.

## What is included

- deterministic top-*k* identity comparison;
- RIDI, changed slots and global Spearman reporting;
- the sufficient score-margin certificate `gamma_k > 2*epsilon`;
- the exact `O(n log n)` identity–utility frontier;
- minimum-turnover selection under a declared utility-regret budget;
- command-line and Python interfaces;
- brute-force optimality tests and multi-version continuous integration; and
- the RIDI Audit Minimum Reporting Standard v1.

## Scientific use

RIDI is intended to complement performance, robustness and fairness evaluation in systems that allocate finite decision capacity. It measures identity turnover; it does not establish correctness, clinical utility, fairness or harm. Attribution to representation requires a controlled intervention and mechanism-matched controls.

## Verification

The release source and wheel are accompanied by SHA-256 checksums. The repository test suite passes on Python 3.10, 3.11 and 3.12.

## Citation

Use the repository's `CITATION.cff`. The archival DOI `10.5281/zenodo.22072275` is reserved and becomes the citation target when its public record is activated.

