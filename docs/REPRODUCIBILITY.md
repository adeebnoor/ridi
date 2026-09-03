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

## Current manuscript evidence

The current manuscript is **“Identical audits, different AI decisions.”** Its decisive prospective experiment is registered at:

- RAG preregistration: https://osf.io/txwdv/

The registration freezes the study matrix, query panels, prompts, model revisions, retrievers, intervention rules, falsification thresholds, analysis plan and cryptographic manifest before registered generation.

The submission reproducibility package preserves:

- the preregistered RAG protocol and analysis outputs;
- exact execution provenance and cryptographic manifests;
- candidate-universe integrity hashes;
- row-level/query-level results and Source Data;
- transport analyses, adverse controls and failed gates;
- the SciFact illustrative case; and
- publication figures/derived tables needed to trace headline values.

## EPSS independent-execution boundary

The deterministic EPSS workflow (`RIDI-CYBER-NATURAL-UPDATE-v1`) is prepared for independent execution under community CODECHECK issue #208:

https://github.com/codecheckers/register/issues/208

The sealed canonical numerical result key has been reproduced exactly in two external software environments. Those runs are reported only as cross-environment numerical reproduction. **No CODECHECK certificate is claimed unless and until one is formally issued.**

## Archive status

Development source is public in this repository. The submission package includes the complete current Source Data workbook and manuscript-linked result summaries. Do not describe a reserved or draft archival DOI as publicly available unless it resolves without authentication. When a permanent public archival record is activated, cite that record explicitly and update this page rather than inferring public status from a reserved identifier.

## Reproduction discipline

Do not replace a failed control, gate or endpoint after observing results. If an implementation error is discovered, preserve the original output, document the correction, rerun the locked estimand, and report both lineage and impact.
