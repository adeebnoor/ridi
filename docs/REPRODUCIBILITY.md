# Reproducibility guide

## Software verification

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest -q
```

The test suite covers:

- identity and disjoint-set endpoints;
- deterministic score ties;
- certified zero-turnover examples;
- input validation;
- exact frontier optimality against brute-force enumeration; and
- minimum-feasible-turnover selection.

GitHub Actions runs the suite on Python 3.10, 3.11 and 3.12.

## Minimum audit inputs

Two aligned tables are required. Each must contain one unique candidate identifier and one finite score. Both tables must contain exactly the same identities. Record the source version, representation versions, score-generation procedure, cutoff, tie rule and integrity hashes outside the score tables.

## Confirmatory archive

The manuscript archive preserves:

- prospectively locked protocols;
- exact execution provenance;
- candidate-universe integrity hashes;
- query-level results and source data;
- adverse controls and failed gates; and
- publication figures.

Large artifacts are not duplicated in Git because immutable archival storage is the authoritative distribution channel. The reserved project DOI is `10.5281/zenodo.22072275`; this document will link to the public record after activation.

## Reproduction discipline

Do not replace a failed control, gate or endpoint after observing results. If an implementation error is discovered, preserve the original output, document the correction, rerun the locked estimand, and report both lineage and impact.

