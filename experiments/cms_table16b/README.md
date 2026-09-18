# Prospectively registered CMS Table 16B linkage

This folder records the completed outcome-linkage extension used in the RIDI Nature working manuscript.

- Public preregistration: https://osf.io/9guc5/
- Protocol ID: `RIDI-CMS-HVBP-TABLE16B-v1`
- Registration was public before the FY2024–FY2026 IPPS Table 16B binary outcome files used here were downloaded, opened, parsed or inspected.
- Linkage key: CMS Certification Number (CCN).
- Primary annual capacity: k=500.
- Frontier tolerance: eta=0.001 (0.1% relative updated rank-utility loss).
- Bootstrap: 100,000 transition-stratified resamples; seed 20260916.

## Locked frontier reproduced before payment-factor results were accepted

| Transition | Observed replacements | Minimum at eta=0.001 | Rank-utility regret |
|---|---:|---:|---:|
| FY2024→FY2025 | 195 | 174 | 0.0009273454032447684 |
| FY2025→FY2026 | 202 | 181 | 0.0009921372408863474 |

## Preregistered outcome linkage

- Exactly unchanged published TPS: payment adjustment factor changed in 14/15 FY2024→FY2025 transitions and 5/5 FY2025→FY2026 transitions (**19/20 pooled**).
- Frontier-displaceable transition identities: n=84, mean absolute factor change 0.0065247939.
- Stable comparison transitions: n=4,642, mean absolute factor change 0.0055049779.
- Transition-stratified mean difference: 0.001019816; 95% bootstrap interval [0.0000774031, 0.0020078839].
- FY2026 had seven TPS-only CCNs without Table 16B factor matches; no values were imputed.

The analysis is descriptive. It does not convert factors to dollars, attribute factor changes causally to RIDI or ranking churn, assess patient outcomes or hospital quality, label CMS policy as beneficial/harmful, or treat top-500 as a statutory CMS cutoff.

## Official outcome files

| FY | Official CMS ZIP | ZIP SHA-256 | Workbook SHA-256 |
|---|---|---|---|
| 2024 | https://www.cms.gov/files/zip/fy24-ipps-final-rule-16b.zip | 6ef86dd51b7abdb2b2a4a3c76d41a947c3d85ac400249f384c0a3733c65533bf | 8b794e600eeb9fa67e34e1b7f79bcfd639fc7fa039efb72f104435626b061e68 |
| 2025 | https://www.cms.gov/files/zip/fy-2025-ipps-final-rule-table-16-b.zip | d484ede3f9828fceba55ce1e8e418e2b693eb220518d52dd177c3bcb7ac2c5df | a0011fd31d9f0dc5f55684b1a2d79e729a210d22cef921e26fee98f3a594ad43 |
| 2026 | https://www.cms.gov/files/zip/fy2026-ipps-table-16b.zip | 8ad7910ee4e6fbc77819e03d594f954d53e46323f3d0bc3e5165c85551b2f20f | 0d7d0bf506ee16740d28b97083e8bc983c658f1526573ceceaedd62073b8cd78 |

The full byte-preserved execution package is maintained with the manuscript Source Data / author archive rather than duplicating binary CMS files in Git.
