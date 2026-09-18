# Execution record — RIDI-CMS-HVBP-HISTORICAL-EXTENSION-v1

The historical-extension protocol and executable analysis were made public before the first historical hospital-level TPS acquisition attempt.

- Protocol/code lock commit: `5f151cbe3e2c2dfbe06fdb901289c32314472eb4`
- Lock timestamp (Git commit): 2026-09-18T11:29:43Z
- First GitHub Actions execution: run `35339908821`
- Run conclusion: success
- Output artifact ID: `10544681697`
- Output artifact digest: `sha256:26ddf7a0feb32d5fb3ccc871b3c298a7a97dc7d9405683591707a2106fe19072`
- Execution time recorded by output: 2026-09-18T11:30:06.884048Z

## Outcome

The locked official-archive recovery rule did not produce an adjacent FY2017–FY2021 TPS pair.

- FY2017 and FY2018: no official theme-level hospital archive snapshot existed inside the prespecified fiscal-year windows returned by the locked CMS archive endpoint.
- FY2019 and FY2020: the prespecified latest official snapshots were downloaded and hashed, but neither contained `hvbp_tps.csv`.
- FY2021: the prespecified snapshot contained `hvbp_tps.csv` with 2,676 finite TPS rows.

The protocol forbade switching to an alternate archive date, mirror or substitute source after seeing this outcome. No historical turnover/frontier estimate was therefore generated.

## Interpretation

This is an outcome of the locked historical extension, not evidence that earlier CMS years had zero turnover. It documents that the prespecified official archive route could not recover a comparable adjacent hospital-level TPS pair. The original FY2024→FY2026 TPS/frontier analysis remains locally locked rather than publicly preregistered, and the separate OSF Table 16B registration remains prospective only for the payment-factor linkage.
