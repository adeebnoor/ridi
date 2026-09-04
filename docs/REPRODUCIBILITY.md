# Reproducibility guide

## Install and verify the software

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install ridi-audit==1.1.1
ridi-audit --version
ridi-audit demo
```

For development verification:

```bash
git clone https://github.com/adeebnoor/ridi.git
cd ridi
python -m pip install -e ".[dev]"
pytest -q
```

GitHub Actions tests Python 3.10, 3.11 and 3.12. The PyPI release workflow performs strict metadata validation, a clean-wheel smoke test before publication, and then installs the newly published version again from the **public PyPI index** and smoke-tests the CLI and API.

## Current manuscript evidence

The current manuscript is **“Identical audits can yield different AI decisions.”** Its decisive prospective experiment is registered at https://osf.io/txwdv/.

The registration freezes the study matrix, query panels, prompts, model revisions, retrievers, intervention rules, falsification thresholds, analysis plan and cryptographic manifest before registered generation.

## EPSS independent execution

The deterministic EPSS workflow (`RIDI-CYBER-NATURAL-UPDATE-v1`) has been reproduced by **two independent external executors** in separate environments. The locked headline values were reproduced, including 565 changed priorities in the top 1,000 (`RIDI=0.722`) and adjacent same-version controls of 0 and 7.

These are **independent computational executions**, not journal certification or CODECHECK certification.

## SciFact 275 — two blind external regenerations

The targeted SciFact 275 behavioral reversal has now been regenerated **twice independently and blind**.

### Mohammed Hamdan

The frozen audit checks passed with no mismatches. Reference and identity-control outputs were `SUPPORTS`, and the identity output was byte-identical to reference. The membership-preserving permutation remained `SUPPORTS`; the audit-equivalent identity substitution produced `REFUTES` (`RIDI=0.947368...`).

The executor's host could not run the pinned bf16 Hugging Face stack. The same frozen inputs and prompt conditioning were therefore served through a disclosed `qwen3:8b` Q4_K_M llama.cpp/Ollama path. No frozen input or runner file was modified. This is a **cross-serving/quantization robustness regeneration**, not an exact backend reproduction.

### Théophile Ossard

A separate blind regeneration on a distinct GPU/software stack reproduced the same substantive reference/permutation `SUPPORTS` versus identity-substitution `REFUTES` pattern. The regenerated reference began with `Verdict: SUPPORTS`; the preregistered strict first-token parser therefore labelled that raw output `UNPARSEABLE` despite its unambiguous semantic verdict. The parser discrepancy is retained transparently.

Together, these runs support robustness of the **SciFact 275 phenomenon**. They do not replace the preregistered aggregate 800-query endpoint.

## PyPI software release

`ridi-audit==1.1.1` is published at https://pypi.org/project/ridi-audit/ through GitHub OIDC Trusted Publishing. The publication workflow generated PyPI/Sigstore attestations after tests, strict Twine checks and an isolated wheel-install smoke test. A subsequent job installed `1.1.1` from the public PyPI index and successfully ran the CLI demo and Python API smoke test.

Published SHA-256 digests for 1.1.1:

- wheel: `b91dcf6cf227a3a579d88318029c02d78e378d16510a2223d17223acbf7bb6f7`
- source distribution: `a2af6f98171cb5b5a307911eeca2824dd401e014d595c6af69c94ddcf3d5440e`

Software publication is not evidence of peer review or scientific certification.

## CODECHECK boundary

Community request: https://github.com/codecheckers/register/issues/208

The request is registered, but formal checking has **not begun** and no certificate is claimed. The CODECHECK team invited renewed contact when a public preprint exists or when the manuscript is undergoing journal review.

## Reproduction discipline

Do not replace a failed control, gate or endpoint after observing results. If an implementation error is discovered, preserve the original output, document the correction, rerun the locked estimand, and report lineage and impact. Independent execution files should be preserved unedited with hashes and declarations.
