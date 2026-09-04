# Changelog

All notable public changes are documented here.

## 1.1.1 — verification/documentation patch — 2026-09-04

- Synchronized the public PyPI package metadata and long description with the current researcher-facing README.
- Recorded the completed second blind external SciFact 275 regeneration by Mohammed Hamdan, including the exact `SUPPORTS / SUPPORTS / SUPPORTS / REFUTES` canonical pattern across reference, identity-control, order-only permutation and audit-equivalent identity substitution.
- Preserved the executor-declared hardware/backend deviation: frozen inputs and audit checks were unchanged, but generation used a disclosed Q4_K_M `qwen3:8b` llama.cpp/Ollama serving path on a CPU-only host rather than the frozen bf16 Hugging Face runtime.
- Retained Théophile Ossard's independent blind SciFact regeneration and its strict first-token parser boundary (`Verdict: SUPPORTS`) transparently.
- Clarified that the two targeted SciFact regenerations strengthen cross-environment robustness of the decisive case but do not replace the preregistered 800-query aggregate endpoint or constitute CODECHECK certification.
- Added public-index verification to the PyPI release workflow so future releases are reinstalled from PyPI itself after upload and smoke-tested again.
- Kept the scientific API unchanged from 1.1.0.

## 1.1.0 — researcher-first API — 2026-09-04

- Published `ridi-audit==1.1.0` to PyPI through tokenless GitHub OIDC Trusted Publishing with PyPI/Sigstore attestations.
- Added `compare_allocations(before_ids, after_ids)` and `AllocationReport`, a framework-agnostic direct path for RAG contexts, shortlists, alert queues and other already-selected finite allocations.
- Added the high-level score-table path `from ridi_audit import audit` with `AuditReport`, compact text/dictionary/Markdown output and direct identity-control selection.
- Added a zero-file CLI demo and rebuilt the Colab notebook so a new researcher can install and execute the actual package in one session.
- Added copy-paste research recipes for retrieval/RAG, top-k model or data updates and shortlist comparison.
- Added the Allocation Identity Reporting Checklist with publication-oriented capacity, comparator, controls, privacy and downstream-outcome fields.
- Added dedicated GitHub issue forms for independent replication and new-domain applications; positive, null and discrepant results are explicitly welcome.
- Rebuilt the repository and public landing pages around the scientific object—allocation identity—rather than internal development history.
- Moved historical submission, CODECHECK administration, verifier templates and superseded reporting/release notes into `archive/` while preserving Git provenance.
- Hardened the release path with exact version checks, strict Twine validation, clean-wheel installation tests, release concurrency, artifact hashes and publish attestations.
- Aligned the public narrative to the current manuscript **Identical audits can yield different AI decisions** and its three-display architecture: preregistered RAG consequence, EPSS production stress test and exact identity–utility frontier.
- Recorded that the sealed EPSS numerical workflow has been reproduced by two independent external executors in separate environments.
- Recorded two independent blind external SciFact 275 regenerations of the substantive reference/permutation `SUPPORTS` versus audit-equivalent identity-substitution `REFUTES` pattern.
- Corrected CODECHECK wording: request registered; formal checking has not begun; no certificate is claimed.
- Preserved registered failures and negative/boundary results rather than converting them into positive evidence.

## Historical — v21 external validation — 2026-08-24

- Added a prospectively locked natural update outside biomedicine: EPSS v2→v3 with delayed CISA KEV outcomes.
- Retained capacity-dependent and adverse findings, including the failed locked 95% outcome-retention gate at `eta=0.001`.
- Added same-version temporal controls, source-commit pinning, input hashes and a machine-verifiable result record.
- Added a sealed blind-run package and independence declaration for execution by a separate human team. At that historical stage no independent result had yet been returned; later returns are recorded above.

## Historical — v20 scientific alignment — 2026-08-24

- Expanded RIDI as the Reproducibility of Identity Decisions Index throughout public documentation.
- Aligned the repository with the five-part framework: Measure, Attribute, Certify, Control and Validate.
- Added the corrected GraphSAGE attribution endpoint and confidence interval from the locked v20 source data.
- Added explicit scientific-scope, outcome-gate and Zenodo-draft boundaries.
- Preserved software version 1.0.0 because this update changed documentation and scientific provenance, not the public API.

## 1.0.0 — 2026-08-24

- Public standalone RIDI repository.
- Deterministic top-*k* identity audit and Markdown reporting.
- Sufficient score-margin stability certificate.
- Exact `O(n log n)` identity–utility frontier and constrained selector.
- Command-line interfaces for audit and control.
- A dependency-free 60-second falsification experiment.
- A zero-install interactive browser laboratory and one-click Colab notebook.
- Eleven tests, including brute-force optimality, with multi-version continuous integration.
- Minimum reporting standard, methods note and interpretation boundaries.
