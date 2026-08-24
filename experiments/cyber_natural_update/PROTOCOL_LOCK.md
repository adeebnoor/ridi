# RIDI-CYBER-NATURAL-UPDATE-v1

## Purpose

This prospective analysis tests decision identity across a naturally deployed, non-biomedical update in a real vulnerability-prioritization system. FIRST replaced EPSS v2 with EPSS v3 in production on 7 March 2023. The experiment asks whether that update changed which vulnerabilities would receive finite review capacity and whether the changed identities were later added to the US Cybersecurity and Infrastructure Security Agency Known Exploited Vulnerabilities (CISA KEV) catalog.

This is an **operational model-update extension**, not a representation-attribution experiment. It tests transport of the RIDI decision-identity framework to another component of `T_k = Phi(S,R,F,C,Z)` and must not be described as isolating `R`.

## Locked inputs

- Treatment baseline: EPSS v2 scores published 6 March 2023.
- Treatment update: EPSS v3 scores published 7 March 2023.
- Pre-update temporal control: EPSS v2, 5 March versus 6 March 2023.
- Post-update temporal control: EPSS v3, 7 March versus 8 March 2023.
- External outcome: CISA KEV `dateAdded`.
- EPSS source: official historical score repository, `empiricalsec/epss_scores`, source commit `3b3ae5b793011090800848c75ceea4cecaa9d309` observed at protocol preparation.
- KEV source: official CISA mirror, `cisagov/kev-data`, source commit `fea466c2e713d1f44e74c903ad4f60b81470bb22` observed at protocol preparation.

The analysis script records SHA-256 checksums of every downloaded input. Historical EPSS files are pinned to the source commit. The KEV catalog is pinned to the stated commit and filtered only by its `dateAdded` field.

## Candidate universe

The universe is the lexical-sorted intersection of CVE identifiers present in all four EPSS files. CVEs already present in KEV on or before 6 March 2023 are excluded. This prevents known prior outcomes from entering the future-outcome evaluation. No filtering uses post-update outcome status.

## Deterministic decisions

Candidates are ordered by descending EPSS score and then lexical CVE identifier. Locked cutoffs are `k={100,500,1000,5000}`; `k=1000` is primary. The same candidate universe and tie rule are used in both treatment arms and both temporal controls.

## Primary decision-identity endpoint

At `k=1000`, report global Spearman agreement, changed slots and RIDI for the 6→7 March model update. The update is considered distinguishable from ordinary daily motion only if its changed-slot count exceeds both temporal controls at the same cutoff. All cutoffs and controls are retained regardless of this gate.

## Delayed external outcome

The primary external window is 8 March 2023 through 7 March 2024 inclusive. A positive outcome is a candidate CVE whose CISA KEV `dateAdded` lies in that window. Sensitivity windows ending 30, 90 and 180 days after 7 March 2023 are reported without replacing the primary window.

At each cutoff, report:

1. future-KEV captures in the v2 and v3 decision sets;
2. the difference `v3 - v2`;
3. future-KEV captures among entrants, leavers and retained identities; and
4. full-universe AUROC and deterministic average precision for v2 and v3 scores.

The outcome is classified as beneficial when v3 captures more future KEV entries, neutral when counts are equal and adverse when it captures fewer. KEV addition is delayed federal curation of known exploitation, not the date exploitation began and not complete ground truth.

## Exact identity control

At the primary cutoff, compute the exact identity–utility frontier using v3 percentile utility. The locked primary tolerance is `eta=0.001`; the sensitivity ladder is `{0,0.0001,0.001,0.005,0.01}`. The controlled set passes the external-retention gate only if it reduces changed slots and retains at least 95% of the future-KEV captures in the unconstrained v3 top-1000 set. A failed gate is an adverse boundary result and is not used to change the endpoint.

## Analysis rules

- No cutoff, window, tie rule, tolerance or gate may change after outcome inspection.
- All zero, neutral and adverse findings are retained.
- The model-update result must not be labelled representation attribution.
- The analysis is executed by the manuscript author and is not an independent-team replication.
- Independent replication requires a separately identified team to run the sealed package from the locked commit and return its machine-verifiable execution record.

Protocol prepared before downloading or parsing the four EPSS score files or the KEV outcome file in this workspace.
