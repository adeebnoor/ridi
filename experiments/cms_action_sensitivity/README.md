# CMS action-sufficiency rule-version sensitivity

**Status:** post hoc mechanistic/scope audit. This analysis does not replace the prospectively registered Table 16B linkage at OSF 9guc5 and is not presented as preregistered.

The purpose is to test whether the previously noted cross-year payment-factor movement at unchanged published Total Performance Score (TPS) can be interpreted as hidden action reallocation. It cannot.

## Key result

Within a fixed fiscal-year conversion rule, repeated published TPS values mapped to the same actual Table 16B factor:

| Fiscal year | Repeated TPS levels | Hospitals covered | Discordant factor levels |
|---|---:|---:|---:|
| FY2024 | 402 | 2,200 | 0 |
| FY2025 | 432 | 2,245 | 0 |
| FY2026 | 453 | 2,106 | 0 |

Across adjacent fiscal years, the same numerical TPS usually mapped to a different factor. This is consistent with annual recalculation of the exchange-function slope and the FY2026 score-divisor change from 100 to 110. Each annual TPS also reflects a new performance period.

Therefore the Nature working manuscript treats CMS as a **boundary/falsification case**: action sufficiency must be evaluated for a specified, versioned conversion rule. Cross-year payment-factor movement is not used as evidence of concealed hospital reprioritisation.

## Reproducibility

- Workflow: `.github/workflows/cms_action_sensitivity.yml`
- Analysis: `run_sensitivity.py`
- Successful GitHub Actions run: `35513132415`
- Artifact: `cms-action-sufficiency-sensitivity-v1`
- Artifact SHA-256: `c39cdb91945f0eff4bba9b9e692776ed175f7ea009ceef4617e4aac3eb52c37c`

The parser discovers TPS data by required column signature rather than assuming a fixed archive filename, because the FY2026 hospital archive changed file naming.

## Interpretation boundary

- No dollar revenue estimate is inferred.
- No causal effect of TPS or RIDI on payment is claimed.
- No patient-outcome or hospital-quality effect is inferred.
- The analytic top-k CMS exercise is a score-landscape stress test, not a statutory programme cutoff.
- Historical fiscal years with materially different scoring regimes are not pooled merely to increase the number of annual transitions.
