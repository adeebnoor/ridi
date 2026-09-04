# ridi-audit 1.1.0

First PyPI release candidate for the researcher-first RIDI toolkit.

## Researcher-facing API

- `compare_allocations(before_ids, after_ids)` for already-selected finite allocations such as RAG contexts, shortlists and queues.
- `audit(before, after, k=...)` for paired score tables.
- `AuditReport.control(k=..., eta=...)` for exact minimum-turnover selection within an explicit updated-score utility-regret budget.
- deterministic tie handling, changed-slot reporting, RIDI, margin certification and Markdown/dictionary exports.

## Reproducibility and adoption

- one-click Colab experiment;
- 60-second Quick Start;
- use-case recipes;
- publication reporting checklist;
- independent-replication and new-domain GitHub issue forms;
- CI on Python 3.10, 3.11 and 3.12.

## Supply-chain and release security

The PyPI release uses GitHub OIDC Trusted Publishing with no stored PyPI API token. The workflow separates build/test from the OIDC publishing job, validates package metadata strictly, installs and smoke-tests the built wheel in a fresh environment, prints artifact hashes, and uploads PyPI/Sigstore attestations.

## Scientific scope

RIDI measures allocation-identity change at a finite score-to-action boundary. It does not by itself establish correctness, harm, benefit, fairness, causal effect or model superiority. The accompanying manuscript remains separate from software release status.

## Links

- Repository: https://github.com/adeebnoor/ridi
- PyPI after first publication: https://pypi.org/project/ridi-audit/
- Colab: https://colab.research.google.com/github/adeebnoor/ridi/blob/main/notebooks/RIDI_60_Second_Experiment.ipynb
- Reporting checklist: https://github.com/adeebnoor/ridi/blob/main/docs/REPORTING_CHECKLIST.md
- Evidence overview: https://github.com/adeebnoor/ridi/blob/main/paper/README.md
