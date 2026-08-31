# RIDI

<div align="center">

## Decision identity for capacity-limited AI

### Performance and group-fairness audits can be exactly unchanged while the identities receiving finite capacity change

**RIDI is the measurement and control toolkit for a broader result: aggregate audits identify cells, not allocations.**

[![Tests](https://github.com/adeebnoor/ridi/actions/workflows/tests.yml/badge.svg)](https://github.com/adeebnoor/ridi/actions/workflows/tests.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/code-MIT-2ea44f.svg)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--8251--1853-A6CE39.svg)](https://orcid.org/0000-0002-8251-1853)

[**Try the interactive experiment**](https://htmlpreview.github.io/?https://github.com/adeebnoor/ridi/blob/main/demo/index.html) · [**Run in Colab**](https://colab.research.google.com/github/adeebnoor/ridi/blob/main/notebooks/RIDI_60_Second_Experiment.ipynb) · [**Install**](#install)

</div>

---

![RIDI framework: measure, attribute, certify, control and validate decision identity](assets/ridi-framework.svg)

## The discovery

Capacity-limited AI systems do not act on an entire score distribution. They allocate a finite number of action slots: vulnerabilities enter remediation queues, people enter supervision or review, hospitals enter oversight cohorts, documents enter inspection queues, and candidates enter follow-up lists.

The manuscript associated with this repository identifies an **allocation-identification failure** at that score-to-action boundary.

If an audit observes only finitely many outcome, protected-group or rank-position cells, then fixing the selected count inside each audited cell does **not** identify which members occupy those cells. Identities can be substituted within a cell while every reported quantity derived from those cell counts remains exactly unchanged.

For cells `c` containing `N_c` candidates from which `m_c` are selected, the compatible allocation class contains at least

```text
product_c binomial(N_c, m_c)
```

allocations.

This is not a claim that performance or fairness are unimportant. It is a statement about **what those summaries can and cannot identify**. Performance and group-fairness audits can be necessary and still be insufficient to tell us who received scarce capacity.

> **Aggregate audits identify cells, not allocations.**

The practical implication is simple: wherever scores become finite action, **allocation identity should be reported as a scientific estimand alongside performance and group fairness**.

## RIDI is an instrument, not the theorem

The **Reproducibility of Identity Decisions Index (RIDI)** measures change between two equal-capacity decision sets:

```text
RIDI(A, B) = 1 - |A ∩ B| / |A ∪ B|
```

- identical allocations: `RIDI = 0`
- partial replacement: `0 < RIDI < 1`
- disjoint allocations: `RIDI = 1`

RIDI does not replace AUROC, precision, recall, nDCG, Spearman correlation, calibration or fairness metrics. It reports the allocation axis that those summaries do not, in general, identify.

For equal-size top-`k` sets, if `Delta_k = k - |A ∩ B|` is the number of changed slots, then

```text
RIDI = 2*Delta_k / (k + Delta_k)
```

## Why the result is general

The identification result is induced by the **information retained by the audit**, not by a specific architecture, dataset or application. The empirical programme is therefore used as adversarial triangulation of the theorem rather than as a claim that every domain has the same turnover rate or consequence.

The main evidence includes:

- **COMPAS:** in the public two-year cohort (`n=6,172`), a top-1,000 cohort has precision `0.745`, recall `0.265` and African-American share `74.7%`. Even when racial composition is matched exactly inside outcome cells, the audit-equivalent class remains about `10^1048` cohorts; age and sex composition remain free until those dimensions are audited explicitly.
- **EPSS:** for the v2→v3 production update, `565/1,000` top priorities changed while adjacent same-version controls changed `0` and `7`. The v3 top-1,000 contained 12 vulnerabilities that later entered CISA KEV; even holding all 12 fixed, precision/recall leave `988/1,000` acted-on identities unresolved.
- **CMS HVBP:** successive annual Total Performance Score updates changed `195/500` and `202/500` hospitals in declared audit cohorts, while matched same-year controls changed none. This is transport to a second independently governed production scoring system, not a claim about clinical or payment effects.
- **Controlled mechanism tests:** graph and text experiments show how representation changes can alter surfaced identities even when conventional performance moves little, while matched controls delimit attribution.
- **Registered failures:** RxNorm and Open Targets analyses are retained as first-class negative evidence. They show that the magnitude, mechanism and external value of identity change are system- and cutoff-dependent. The theorem is general; consequential turnover is not claimed to be universal.

## From observability to control

The toolkit operationalizes five distinct questions:

| Step | Question | Output |
|---|---|---|
| **Measure** | Which finite decision identities changed? | RIDI, changed slots, overlap |
| **Attribute** | What mechanism produced the change? | matched controls and invariance tests |
| **Certify** | Can zero turnover be guaranteed? | score-margin certificate |
| **Control** | How much change is actually required to retain updated utility? | exact identity–utility frontier |
| **Validate** | Was the changed allocation externally justified? | pre-specified outcome gate |

A sufficient zero-turnover certificate is available from stored paired scores. If the baseline top-`k` score margin `gamma_k` exceeds twice the maximum paired perturbation `epsilon`, then top-`k` identity is certified unchanged:

```text
gamma_k > 2*epsilon
```

The exact selector then finds the minimum-turnover top-`k` set within a prospectively declared updated-score utility-regret tolerance. Stability is therefore not enforced blindly: identity change can be accepted when independent outcomes justify it, and only unnecessary change should be constrained.

## 60-second paradox

Run:

```bash
python examples/identity_paradox.py
```

A deterministic construction can produce near-perfect global rank agreement while completely replacing the top-`k` decision set:

```text
Candidates (n):               10,000
Decision capacity (k):            50
Global Spearman agreement:  0.999998500
Top-k overlap:                     0 / 50
RIDI:                          1.000
```

As `n` grows, Spearman correlation approaches one while the selected sets remain disjoint. No threshold on global rank agreement alone can therefore certify top-`k` identity.

## Install

```bash
git clone https://github.com/adeebnoor/ridi.git
cd ridi
python -m pip install .
pytest -q
```

## Audit your own scores

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

The report includes global Spearman agreement, RIDI, changed slots, overlap, the cutoff margin `gamma_k`, maximum paired perturbation `epsilon`, and the zero-turnover certificate status.

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

`eta` is a domain-governance choice, not a universal threshold. It should be declared prospectively from utility, capacity, safety and policy constraints.

## Independent reproducibility and CODECHECK

The locked EPSS natural-update workflow is designed for execution outside the author environment. Executor-facing instructions, manifests and machine-readable output records are included in the repository and referenced from [`codecheck.yml`](codecheck.yml).

A **community CODECHECK is publicly registered and pending independent assignment**:

- CODECHECK register: [codecheckers/register#208](https://github.com/codecheckers/register/issues/208)
- current registered state: `community` / `needs codechecker`
- requested workflow: `RIDI-CYBER-NATURAL-UPDATE-v1`

Separate external environments have reproduced the canonical numerical result key. Those runs are treated as cross-environment numerical reproduction only. **No CODECHECK certificate is claimed unless and until the community workflow is completed and a certificate is formally issued.**

Public tracking: [RIDI issue #2](https://github.com/adeebnoor/ridi/issues/2).

## Prospective falsification

The next EPSS production-version test is publicly locked in [`PROSPECTIVE_EPSS_NEXT_VERSION_PROTOCOL_LOCK_2026-08-31.md`](PROSPECTIVE_EPSS_NEXT_VERSION_PROTOCOL_LOCK_2026-08-31.md). The point is not to accumulate supportive examples; it is to make the allocation-identification programme prospectively falsifiable.

## Scientific boundaries

RIDI measures allocation turnover, not correctness, fairness, causal harm, clinical benefit or model superiority. The theorem applies to audits that factor through finite outcome/group/position summaries; explicitly identity-aware, individual-fairness or causal-fairness analyses can escape that information loss. Empirical effect sizes, mechanisms and consequences remain system- and cutoff-dependent.

The public COMPAS analysis is a retrospective secondary analysis of the published two-year research cohort. Constructive extremal cohorts show what the audited summaries cannot exclude; they are not predictions that a particular alternative scorer will produce those cohorts.

## Repository map

```text
demo/                   Zero-install browser experiment
notebooks/              One-click Colab experiment
examples/               Minimal scripts and aligned score tables
experiments/            Locked analyses and replication packages
src/ridi_audit/         Metric, certificate, exact selector and CLI
tests/                  Unit and brute-force optimality tests
docs/                   Methods, interpretation and reproduction guidance
.github/workflows/      Continuous integration
```

## Manuscript

**Performance and group-fairness audits leave AI allocations unidentified**  
Article prepared for submission to *Nature*.

The manuscript's central claim is the allocation-identification theorem. RIDI is the accompanying measurement/control framework rather than the discovery itself.

## Citation

Use [`CITATION.cff`](CITATION.cff) to cite the software:

> Noor, A. (2026). *RIDI: decision-identity audit and control toolkit* (v1.0.0). GitHub. https://github.com/adeebnoor/ridi

No archival DOI is claimed here unless its public activation has been independently verified.

## Author

**Adeeb Noor**  
Department of Information Technology, Faculty of Computing and Information Technology, King Abdulaziz University, Jeddah, Saudi Arabia  
[ORCID 0000-0002-8251-1853](https://orcid.org/0000-0002-8251-1853)

## Status

The repository is public and actively supports the current Nature submission package. The community CODECHECK request is registered as `codecheckers/register#208` and awaits assignment. The manuscript has not been accepted or peer reviewed. No CODECHECK certificate, institutional ethics determination or archival DOI is claimed unless and until it is formally issued or independently verified.
