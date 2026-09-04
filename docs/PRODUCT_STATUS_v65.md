# RIDI repository/product lock — v65 preparation

Date: 2026-09-04

This note records repository-facing changes made while the Nature manuscript remains scientifically locked pending the final independent RAG return.

## Public-facing scientific state

- Manuscript title aligned to **Identical audits can yield different AI decisions**.
- Main narrative aligned to three displays: preregistered RAG consequence, EPSS production update, exact identity–utility frontier.
- EPSS sealed numerical workflow independently reproduced by two external executors in separate environments.
- A targeted blind external regeneration of SciFact query 275 reproduced the substantive `SUPPORTS → REFUTES` identity-substitution reversal on a distinct GPU/software stack. It is reported as a targeted robustness/reproducibility check, not as a replacement for the preregistered aggregate endpoint.
- Community CODECHECK request #208 is registered; formal checking has not begun and no certificate is claimed.

## Product goals

The public repository should present, in order:

1. the scientific object (allocation identity),
2. the decisive result,
3. the production stress test,
4. the constructive identity–utility frontier,
5. a one-entry-point Python API and CLI,
6. transparent reproducibility status and scientific boundaries.

Historical submission/version records are provenance, not the primary researcher experience.
