# Prospective EPSS next-version protocol lock

**Public lock date:** 31 August 2026  
**Author:** Adeeb Noor  
**Current EPSS production model at lock:** v5 (`v2026.06.15`), first published 15 June 2026  
**Reference code snapshot:** `d47cc383e1a147f01d7609ecba6748e853e5e755`  
**Exposure:** the first EPSS production model-version transition after v5. The release date is externally determined by FIRST/EPSS.

This record freezes the confirmatory choices for the next EPSS model transition before that future transition occurs. It is a public protocol lock, not an OSF registration and not a claim of Zenodo deposition.

## Frozen primary hypotheses

1. **H1 — reallocation magnitude.** At `k=1000`, changed slots `Delta@1000 >= 400` and the observed change must exceed the 99th percentile of the preceding 365-day single-day within-version turnover distribution. Point prediction: 450-800, central approximately 600.
2. **H2 — performance invisibility.** At least 90% of replaced identities must be performance-invisible under the locked one-year CISA KEV outcome definition. Point prediction: at least 97%.
3. **H3 — underdetermined latitude.** Holding precision@1000 and recall@1000 exactly fixed, the constructive span in mean CVE age must be at least 4.0 years. Point prediction: at least 8 years.

The manuscript's prospective central claim is supported only if **H1 AND H2 AND H3** all hold. Any other combination is reported as partial or failed prospective replication.

## Frozen secondary hypotheses

- **H4:** H1 holds and absolute change in AUROC is below 0.05 on the identical intersection universe and identical outcome window.
- **H5:** the pre-specified sufficient zero-turnover certificate produces zero false certifications.
- **H6:** after additionally preserving selected counts within post-transition score-decile cells, residual mean-age span is above 1.0 year and residual audit-equivalent class size is above `10^40`; Holm correction applies across H4-H6.
- **H7:** direction of age shift is exploratory and explicitly not predicted.

## Frozen definitions

- Primary capacity: `k=1000`.
- Outcome: CISA KEV `dateAdded` during the one-year window after the post-transition day; 30-, 90- and 180-day windows are sensitivities.
- Candidate universe: intersection of the pre- and post-transition EPSS score files after applying the locked outcome-leakage exclusions.
- Eligible substitution pool: post-transition top 3,000 CVEs restricted to outcome-negative CVEs; top-2,000, top-5,000 and whole-universe pools are sensitivities only.
- Latitude construction: hold outcome-relevant selected identities fixed; fill remaining slots with the youngest admissible negatives for the low extremum and oldest admissible negatives for the high extremum.
- Within-version null: 365 calendar days immediately preceding the transition.
- No interim analysis and no optional stopping. The outcome-scored analysis is run once after the one-year outcome window closes.
- Any change to an estimand, threshold, cell definition, eligible pool, multiplicity rule or success criterion is a dated protocol deviation and cannot be used to relabel a failed prediction as successful.

## Implementation rule

The future execution script must implement the frozen protocol without outcome-dependent branches and emit a machine-readable result. Its exact commit and SHA-256 will be recorded before the first outcome-scored execution. The absence of a frozen script at this protocol-lock date does not permit changing any of the scientific choices listed above.

## Archive status at lock

No OSF registration, Zenodo DOI or CODECHECK certificate is claimed by this file. Those identifiers may be added later only if they are genuinely public/issued, without altering the frozen hypotheses or analysis rules.