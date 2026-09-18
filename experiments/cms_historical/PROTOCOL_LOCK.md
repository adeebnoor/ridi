# RIDI-CMS-HVBP-HISTORICAL-EXTENSION-v1

**Status:** public outcome-naive analysis lock for historical hospital-level TPS outcomes.  
**Repository:** `adeebnoor/ridi`  
**Scope:** CMS Hospital Value-Based Purchasing (HVBP), FY2017–FY2021.  
**Important registration boundary:** this is a public, timestamped GitHub protocol lock. It is not represented as an OSF preregistration.

## 1. Why this extension exists

The current manuscript's CMS TPS/frontier analysis contains two adjacent post-pause annual transitions (FY2024→FY2025 and FY2025→FY2026). The original TPS/frontier protocol was locally locked before score inspection but was not publicly preregistered. A later OSF registration prospectively locked the separate FY2024–FY2026 Table 16B payment-factor linkage and does not retroactively register the TPS/frontier analysis.

This historical extension is designed to address temporal breadth without rewriting that history.

## 2. Knowledge state at lock

Before this protocol was made public:

- the author knew the two post-pause TPS/frontier results and the Table 16B linkage results reported in the working manuscript;
- the general allocation-identity hypothesis and exact identity–utility frontier were already developed;
- official CMS methodology documents for FY2017–FY2021 had been screened in `experiments/cms_table16b/HISTORICAL_METHODOLOGY_ELIGIBILITY_AUDIT.md`;
- that methodology screen concluded that no adjacent FY2017–FY2021 pair met a deliberately strict same-regime invariance rule;
- **historical hospital-level FY2017–FY2021 TPS values were not acquired or inspected for that screen**.

The historical extension is therefore not hypothesis-naive. It is prospectively locked only with respect to the historical hospital-level TPS outcomes described below.

## 3. Questions

1. Across every retrievable adjacent pre-pause transition FY2017→FY2018, FY2018→FY2019, FY2019→FY2020 and FY2020→FY2021, how many hospitals change membership in a top-k audit selection?
2. For each transition, what is the exact minimum number of replacements compatible with a declared updated rank-utility budget?
3. How sensitive are the results to k, eta and cutoff ties?

No claim of a stable long-run annual CMS turnover rate is permitted.

## 4. Two prespecified strata

### A. Strict same-regime replication

The already-completed methodology eligibility audit is retained unchanged. Under its strict rule—same measure set, domain structure/weights and material performance-period/scoring definitions—no FY2017–FY2021 adjacent pair qualified. No hospital-level outcome analysis will be relabelled as same-regime replication.

### B. All-transition historical extension

All four adjacent fiscal-year pairs will be analysed if official hospital-level TPS files can be retrieved, regardless of methodology changes. The methodology-change annotations from the prior audit will remain visible for every pair.

This stratum asks a narrower descriptive question: what happened to selection identity across actual annual programme updates? It will **not** be pooled with FY2024→FY2026 as though all years shared one scoring regime.

## 5. Official source and deterministic file selection

The sole primary source is the CMS Provider Data Catalog hospitals archive aggregate endpoint:

`https://data.cms.gov/provider-data/api/1/archive/aggregate/theme/hospitals/relative`

For each target fiscal year FY in {2017, 2018, 2019, 2020, 2021}:

1. define the fiscal-year window as 1 October of FY-1 through 30 September of FY;
2. from official CMS theme-level hospital archive snapshots whose archive date falls in that window, choose the **latest dated snapshot**;
3. download that official archive ZIP;
4. require a member whose basename is `hvbp_tps.csv` (case-insensitive);
5. require identifiable Facility ID, Fiscal Year and Total Performance Score columns;
6. retain rows whose parsed Fiscal Year equals the target FY and whose TPS is finite.

If a target FY cannot be recovered under these rules, it is reported unavailable. No alternate date, mirror, manually chosen file or imputation may substitute in the locked primary execution.

Raw ZIP and extracted TPS SHA-256 hashes, archive dates, URLs, row counts and parser decisions must be recorded before analysis outputs are accepted.

## 6. Candidate universe and ranking

For each adjacent pair:

- candidate universe = intersection of Facility IDs with finite TPS in both fiscal years;
- Facility IDs are canonicalized as zero-padded six-character strings when numeric;
- scores are ordered descending;
- Facility ID lexical order is the final deterministic tie break.

No hospital is imputed across years.

## 7. Capacities

Primary audit capacity:

- `k = 500`

Prespecified sensitivity capacities:

- `k = 100`
- `k = 1,000`

A capacity is omitted only when the common candidate universe has fewer than k hospitals.

## 8. Endpoints

For every transition and k:

- common-universe size;
- Spearman rank correlation on the common universe;
- changed slots `Delta = k - |A ∩ B|`;
- RIDI/Jaccard distance `2Delta / (k + Delta)`;
- tie-minimised changed slots over all valid choices within old and new cutoff ties.

For the exact identity–utility frontier, updated-score utility is the deterministic percentile-rank utility implemented in `src/ridi_audit/selector.py`, with Facility ID as final tie break.

Primary tolerance:

- `eta = 0.001` (0.1% relative loss in updated rank utility).

Prespecified tolerance ladder:

- `eta ∈ {0, 0.0001, 0.001}`.

For every k and eta report:

- `j(eta)`, the minimum replacements satisfying the budget;
- realised relative rank-utility regret;
- controlled RIDI;
- avoidable-turnover fraction `1 - j(eta)/Delta` when `Delta > 0`.

## 9. Statistical treatment

These are exact finite-transition descriptives.

- No null-hypothesis significance test is primary.
- No transition may be dropped because its direction or magnitude is inconvenient.
- No superpopulation confidence interval for "CMS years" is claimed.
- Across the four historical transitions, any median or range is descriptive only.
- Historical transitions are not pooled with FY2024→FY2026 to estimate a single annual rate.

## 10. Tie sensitivity

Because TPS is discrete, the deterministic lexical tie-break result is primary for reproducibility. A prespecified all-valid-cutoff-ties sensitivity reports the minimum possible changed membership over every valid top-k selection at the old and new cutoff scores.

This sensitivity may change changed-slot counts but does not replace the deterministic primary result.

## 11. Missing-data and failure rules

- If an official archive snapshot is absent, report it.
- If `hvbp_tps.csv` is absent, report it.
- If the target fiscal year is absent from the selected file, report it.
- If required columns cannot be identified, report it.
- Do not switch to a different archive date after seeing any TPS values.
- Failed or zero-turnover transitions remain in the report.

## 12. Permitted interpretation

The historical extension may support statements about descriptive selection turnover and exact score-utility trade-offs across the analysed annual CMS programme updates.

It may **not** be used to claim:

- hospital or patient harm;
- causal effects of turnover;
- incorrect CMS payment policy;
- a statutory top-k cutoff;
- a stable long-run annual turnover rate;
- comparability of FY2017–FY2021 scoring regimes;
- prospective registration of the original FY2024–FY2026 TPS/frontier analysis.

## 13. Execution and audit trail

The first locked execution must use the code committed with this protocol. Outputs are written to a GitHub Actions artifact and are not auto-committed. Any later code change requires a dated deviation note and a fresh execution; the original output remains retained.

The pre-existing methodology eligibility audit remains unchanged and is cited as prior knowledge rather than rewritten after seeing outcomes.
