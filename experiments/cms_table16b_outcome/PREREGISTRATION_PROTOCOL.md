# RIDI-CMS-TABLE16B-OUTCOME-v1

**Status:** pre-outcome public-lock package; **not an OSF preregistration until the author deposits this exact package and obtains a public timestamp.**  
**Lock date:** 2026-09-16  
**Target manuscript:** Nature main working programme, v78 → v79 candidate

## 1. Purpose

Test whether the annual CMS Hospital Value-Based Purchasing (VBP) score updates already audited for selection-identity turnover are accompanied by changes in the **actual Hospital VBP payment adjustment factor** published in official Table 16B, without treating the manuscript's analytic top-k capacity as a statutory CMS payment threshold.

CMS describes Table 16B as the actual Hospital VBP payment adjustment factor used to adjust eligible hospitals' base operating DRG payments for the fiscal year. The analysis therefore links the previously audited score update to a payment-linked outcome, but it does **not** estimate hospital-specific dollars, patient outcomes, or a causal effect of top-k membership.

## 2. What was known before this lock

Known before outcome acquisition:
- the FY2024→FY2025 and FY2025→FY2026 Total Performance Score (TPS) data and annual turnover results;
- the locked analytic capacity k=500 and deterministic CCN tie-break;
- the identity–utility frontier at eta=0.001, including the previously derived j(eta) values;
- the official CMS pages and filenames identifying FY2024, FY2025 and FY2026 Table 16B as the actual VBP factor source;
- the general CMS payment mechanism and the fact that the factor is applied to base operating DRG payments.

Not inspected before this lock in this workflow:
- hospital-level Table 16B factor values for FY2024, FY2025 or FY2026;
- any result of the factor/TPS linkage described below.

This analysis is therefore outcome-naive with respect to Table 16B factor values, but it is **not** hypothesis-naive with respect to the already-known TPS turnover result.

## 3. Official Table 16B sources

- FY2024: `https://www.cms.gov/files/zip/fy24-ipps-final-rule-16b.zip`
- FY2025: `https://www.cms.gov/files/zip/fy-2025-ipps-final-rule-table-16-b.zip`
- FY2026: `https://www.cms.gov/files/zip/fy2026-ipps-table-16b.zip`

The raw ZIP bytes and inner file bytes will be retained and hashed before analysis.

## 4. Locked TPS contrasts

### Contrast A: FY2024→FY2025
- old TPS snapshot: 2024-10-30, FY2024
- new TPS snapshot: 2025-02-19, FY2025
- locked TPS universe size expected: 2,377 CCNs
- analytic capacity: k=500
- expected unconstrained changed slots: 195
- expected identity-control j(0.001): 174

### Contrast B: FY2025→FY2026
- old TPS snapshot: 2025-11-26, FY2025
- new TPS snapshot: 2026-02-25, FY2026
- locked TPS universe size expected: 2,349 CCNs
- analytic capacity: k=500
- expected unconstrained changed slots: 202
- expected identity-control j(0.001): 181

If the normalized TPS inputs do not reproduce these four locked quantities exactly, the outcome analysis stops.

## 5. Identity definitions

For each contrast, rank the locked common TPS universe by descending TPS with lexical six-digit CCN as the final tie-break.

Membership groups at k=500 are:
- **retained:** selected in both old and new top-500;
- **entrant:** outside old top-500 and inside new top-500;
- **leaver:** inside old top-500 and outside new top-500;
- **outside:** in neither.

The top-500 capacity is an author-declared audit capacity and is **not** a CMS statutory cutoff. No statement will imply that crossing rank 500 itself changes payment.

The exact identity-control set at eta=0.001 will be recomputed with the manuscript's frozen rank-percentile utility and selector. Its use is descriptive: it identifies which selection changes were avoidable relative to that declared utility budget. It does not define a counterfactual CMS payment policy.

## 6. Primary outcome quantities

For each fiscal-year contrast, preserve and report **all** of the following, without selecting among them after seeing results.

### P1. Actual factor changes by membership group
Within each of retained, entrant, leaver and outside groups, among CCNs with Table 16B factors in both fiscal years, report:
- complete-case n and missing-factor n;
- old and new factor medians;
- factor change `new − old` expressed both as the raw multiplicative factor and as basis points (`10,000 × delta factor`);
- median, Q1, Q3, minimum and maximum factor change;
- median absolute factor change;
- counts crossing the neutral factor 1.0 in either direction;
- counts with exactly unchanged published factors.

No hypothesis test is primary because these are deterministic programme records rather than a sampled experiment. No multiplicity-adjusted claim will be constructed after inspection.

### P2. Same-reported-TPS diagnostic
Among CCNs whose published TPS is **exactly numerically equal** across the two locked snapshots, report:
- n with factors available in both years;
- n and fraction whose actual Table 16B factor differs;
- the complete distribution summaries of factor change listed above.

The manuscript may describe these as hospitals with **the same reported TPS**, not as hospitals with unchanged quality. Annual measure sets, baselines, scoring context and the exchange function can differ; numeric TPS equality does not establish equality of underlying clinical performance.

## 7. Secondary outcome quantities

### S1. Observed versus identity-controlled membership
At eta=0.001, retain the complete identity-control set and report Table 16B factor summaries for:
- entrants present in both the unconstrained updated top-500 and the identity-controlled set;
- entrants present only in the unconstrained updated top-500;
- old top-500 members retained only by identity control.

These are audit-capacity groups only. Actual CMS factors remain observed outcomes under the real programme, not counterfactual payments under the identity-control selection.

### S2. Complete-case overall reference
Report the same factor-change summaries for all CCNs in the locked TPS universe with both fiscal-year factors, to provide scale for P1/P2.

## 8. Missingness and identifiers

- CCN is treated as a six-digit string; leading zeros are preserved.
- Duplicate CCNs within one fiscal-year factor table cause an analysis stop until source provenance is resolved.
- Missing Table 16B matches remain missing. No zero, no-change or neutral-factor imputation is allowed.
- TPS and factor values are parsed from their published text as decimal numbers; no floating-point tolerance defines equality.
- Any source footnote, suppressed/non-applicable row or nonnumeric factor is retained in an audit table and excluded only from the specific numeric estimand requiring that value.

## 9. Dollar claims

No hospital-specific dollar impact is calculated from Table 16B alone. Converting the multiplicative factor to dollars requires the applicable base operating DRG payment volume/claims. The manuscript may report factor changes or basis points of the factor, not unsupported dollar totals.

## 10. Interpretation boundaries

A positive result can show that the annual score update is accompanied by changes in the actual payment adjustment factor and can localize those changes relative to the manuscript's audit-capacity membership. It does not establish:
- that top-500 entry/exit caused the payment-factor change;
- that equal TPS means equal underlying quality;
- patient benefit or harm;
- hospital-specific dollar impact;
- that identity control should replace CMS's statutory formula.

A null or weak result will be reported and will narrow the manuscript claim.

## 11. Analysis order after public registration

1. Record the public registration URL/timestamp for this exact protocol and manifest.
2. Download the three official Table 16B ZIPs.
3. Hash raw ZIP and inner files.
4. Normalize only CCN and the actual VBP payment-adjustment-factor field using source headers; log exact header names and all exclusions.
5. Normalize the already locked TPS snapshots to the schema in `NORMALIZATION_SPEC.md`.
6. Run `analyze_table16b.py` once.
7. Preserve machine-readable output and execution manifest before manuscript wording is edited.
