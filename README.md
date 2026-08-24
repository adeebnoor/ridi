# RIDI

<div align="center">

## Reproducible performance does not guarantee reproducible decisions

**A small metric, a falsifiable experiment, and an exact control algorithm for systems that select a finite top-*k*.**

[![Tests](https://github.com/adeebnoor/ridi/actions/workflows/tests.yml/badge.svg)](https://github.com/adeebnoor/ridi/actions/workflows/tests.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/code-MIT-2ea44f.svg)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--8251--1853-A6CE39.svg)](https://orcid.org/0000-0002-8251-1853)

[**Try the interactive experiment**](https://htmlpreview.github.io/?https://github.com/adeebnoor/ridi/blob/main/demo/index.html) · [**Run in Colab**](https://colab.research.google.com/github/adeebnoor/ridi/blob/main/notebooks/RIDI_60_Second_Experiment.ipynb) · [**Install the toolkit**](#install)

</div>

---

## What is RIDI?

Suppose two versions of a system each select 100 candidates for human review.

- If both versions select exactly the same 100 identities, **RIDI = 0**.
- If they share 75 identities, 25 seats were replaced and **RIDI = 0.40**.
- If they share no identities, **RIDI = 1**.

RIDI is simply the Jaccard distance between two finite decision sets:

```text
RIDI(A, B) = 1 - |A ∩ B| / |A ∪ B|
```

It answers one operational question:

> **Did the same candidates receive the scarce decision slots?**

RIDI does not replace AUROC, nDCG, MRR, Spearman correlation, fairness evaluation, or domain validation. It reports a different axis that those measures do not certify: **decision identity**.

## The 60-second experiment

Can two rankings be almost identical globally while selecting completely different candidates?

```bash
python examples/identity_paradox.py
```

Expected result:

```text
Candidates (n):               10,000
Decision capacity (k):            50
Global Spearman agreement:  0.999998500
Top-k overlap:                     0 / 50
RIDI:                          1.000

Verdict: near-perfect global agreement, completely different decisions.
```

The experiment is deterministic. It swaps only two adjacent blocks of 50 ranks in a universe of 10,000. The global disturbance is tiny, but every finite decision seat changes.

For this construction:

```text
Spearman rho = 1 - 12*k^3 / (n*(n^2 - 1))
RIDI         = 1
```

As `n` grows, Spearman approaches 1 while the selected sets remain disjoint. Therefore, **no threshold on global rank agreement alone can guarantee top-*k* identity**.

<div align="center">

[![Open interactive experiment](https://img.shields.io/badge/Open-interactive_experiment-6f42c1?style=for-the-badge)](https://htmlpreview.github.io/?https://github.com/adeebnoor/ridi/blob/main/demo/index.html)
[![Open in Colab](https://img.shields.io/badge/Open_in-Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/adeebnoor/ridi/blob/main/notebooks/RIDI_60_Second_Experiment.ipynb)

</div>

The browser experiment runs locally in the page, uploads no data, and lets you change the candidate universe, decision capacity, and number of replaced seats.

## From observation to action

RIDI is not only a distance. The toolkit implements a four-part audit:

| Step | Question | Output |
|---|---|---|
| **Measure** | Which finite decision identities changed? | RIDI, changed slots, overlap |
| **Attribute** | Was the change caused by representation rather than relabelling or retraining noise? | Invariance controls and retraining null |
| **Certify** | Can zero turnover be guaranteed from stored scores? | `gamma_k > 2*epsilon` certificate |
| **Control** | How much turnover is actually needed to preserve updated utility? | Exact identity–utility frontier |

The exact selector finds the minimum-turnover top-*k* set within a prospectively declared utility-regret tolerance. Sorting dominates the calculation, giving `O(n log n)` complexity.

## Install

```bash
git clone https://github.com/adeebnoor/ridi.git
cd ridi
python -m pip install .
```

Verify the installation:

```bash
ridi-audit --version
pytest -q
```

## Audit your own scores

Prepare two CSV files containing the same candidate IDs and one score per candidate:

```bash
ridi-audit compare \
  --r0 examples/r0.csv \
  --r1 examples/r1.csv \
  --id-col id \
  --score-col score \
  --k 3 5 \
  --out audit.json \
  --report audit.md
```

The report contains:

- global Spearman agreement;
- RIDI, changed slots and overlap at each cutoff;
- the baseline boundary margin `gamma_k`;
- maximum paired score perturbation `epsilon`; and
- whether `gamma_k > 2*epsilon` certifies identical top-*k* identity.

The certificate is sufficient and one-sided. A failed certificate does not imply turnover. Once paired scores are stored, certification needs no retraining or additional inference.

## Control avoidable turnover

```bash
ridi-audit control \
  --r0 examples/r0.csv \
  --r1 examples/r1.csv \
  --id-col id \
  --score-col score \
  --k 5 \
  --eta 0.001 \
  --out controlled.json
```

`eta = 0.001` allows at most 0.1% normalized updated-score utility regret. This is a demonstration choice, not a universal standard. Real deployments should declare the tolerance prospectively from domain costs, review capacity, safety requirements, and governance policy.

## Why this matters

A system rarely acts on an entire ranking. It allocates finite attention: molecules sent to a laboratory, records assigned to reviewers, patients flagged for follow-up, or documents shown on the first page. Global performance can be stable even when those identities change.

The accompanying locked analyses span drug-interaction knowledge, graph learning and text retrieval. They show three distinct possibilities:

1. turnover can be **hidden** by global agreement;
2. turnover can be **beneficial**, so stability must not be enforced blindly; and
3. when outcomes do not justify alternatives, part of the turnover can be **avoided exactly** within a declared utility budget.

The full empirical record belongs in the manuscript and immutable archive. This repository is deliberately organized around understanding, testing and reusing the method.

## Scientific boundaries

RIDI measures turnover—not correctness, fairness, clinical benefit, causal harm, or model superiority. Representation attribution requires source evidence, inference, candidate universe, decision rules and randomness to be frozen or explicitly controlled. Drug examples in the research archive are operational selection illustrations, not prescribing guidance.

## Repository map

```text
demo/                   Zero-install browser experiment
notebooks/              One-click Colab experiment
examples/               Minimal scripts and aligned score tables
src/ridi_audit/         Metric, certificate, exact selector and CLI
tests/                  Unit and brute-force optimality tests
docs/                   Methods, interpretation and reproduction guidance
.github/workflows/      Continuous integration
```

Start with the [interactive experiment](https://htmlpreview.github.io/?https://github.com/adeebnoor/ridi/blob/main/demo/index.html), then read the [methods note](docs/METHODS.md) and [minimum reporting standard](RIDI_AUDIT_MINIMUM_REPORTING_STANDARD_v1.md).

## Citation and archive

Use [`CITATION.cff`](CITATION.cff) to cite the software:

> Noor, A. (2026). *RIDI: Decision-identity reproducibility audit* (v1.0.0). GitHub. https://github.com/adeebnoor/ridi

The archival DOI `10.5281/zenodo.22072275` is reserved and will become the citation target when its public record is activated.

## Author

**Adeeb Noor**  
Department of Information Technology, Faculty of Computing and Information Technology, King Abdulaziz University, Jeddah, Saudi Arabia  
[ORCID](https://orcid.org/0000-0002-8251-1853)

## Status

Version 1.0.0 is the public software companion to a manuscript prepared for journal submission. The manuscript is not yet peer reviewed.

