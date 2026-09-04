# Reproducibility guide

## Software verification

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest -q
```

The test suite covers identity and disjoint-set endpoints, deterministic score ties, certified zero-turnover examples, input validation, exact frontier optimality against brute-force enumeration, minimum-feasible-turnover selection, and the researcher-facing `audit()` API. GitHub Actions runs the suite on Python 3.10, 3.11 and 3.12.

## Minimum audit inputs

Two score tables are required. Each must contain one unique candidate identifier and one finite score, and both must contain exactly the same identities. Row order may differ. Record the source version, representation versions, score-generation procedure, cutoff, tie rule and integrity hashes outside the score tables.

## Current manuscript evidence

The current manuscript is **“Identical audits can yield different AI decisions.”** Its decisive prospective experiment is registered at:

- RAG preregistration: https://osf.io/txwdv/

The registration freezes the study matrix, query panels, prompts, model revisions, retrievers, intervention rules, falsification thresholds, analysis plan and cryptographic manifest before registered generation.

The submission reproducibility package preserves the preregistered RAG protocol and outputs, exact execution provenance and cryptographic manifests, candidate-universe hashes, row/query-level Source Data, transport analyses, adverse controls and failed gates, the SciFact illustrative case, and publication-linked derived tables.

## EPSS independent execution

The deterministic EPSS workflow (`RIDI-CYBER-NATURAL-UPDATE-v1`) has been reproduced by **two independent external executors** in separate environments. The locked headline values were reproduced, including the top-1,000 production update turnover of 565 changed priorities (`RIDI=0.722`) and the adjacent same-version controls of 0 and 7.

These runs are reported as **independent computational executions**. They are not described as journal certification or CODECHECK certification.

## Targeted SciFact 275 external regeneration

A separate blind external execution regenerated the frozen SciFact query 275 contexts on a distinct GPU/software stack using the pinned Qwen3-8B revision and deterministic decoding settings. The substantive pattern was reproduced:

- reference / identity control: `SUPPORTS` semantically,
- membership-preserving permutation: `SUPPORTS`,
- audit-equivalent identity substitution: `REFUTES`.

The regenerated reference text began with `Verdict: SUPPORTS`. Because the preregistered parser required the canonical label at the first token, that raw output was labelled `UNPARSEABLE` by the strict registered parser even though its semantic verdict was explicit. This is reported transparently as a parser-robustness boundary; no registered endpoint is silently rewritten.

## CODECHECK boundary

Community request: https://github.com/codecheckers/register/issues/208

The request is registered, but formal checking has **not yet begun** and no certificate is claimed. The CODECHECK team invited renewed contact when a public preprint exists or when the manuscript is undergoing journal review.

## Archive status

Development source is public in this repository. Do not describe a reserved or draft archival DOI as publicly available unless it resolves without authentication. When a permanent public archival record is activated, cite that record explicitly and update this page rather than inferring public status from a reserved identifier.

## Reproduction discipline

Do not replace a failed control, gate or endpoint after observing results. If an implementation error is discovered, preserve the original output, document the correction, rerun the locked estimand, and report both lineage and impact. Independent execution files should be preserved unedited with hashes and declarations.
