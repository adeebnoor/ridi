# CODECHECK request status — RIDI / Nature submission

This public record documents the status of independent computational verification for the manuscript **“Performance and group-fairness audits leave AI allocations unidentified.”**

## Scope requested for independent execution

The primary locked target is the EPSS natural-update analysis (`RIDI-CYBER-NATURAL-UPDATE-v1`), including the reported top-1,000 turnover, RIDI, controls, future-KEV recovery, AUROC comparison, and identity-control results. The repository also contains the COMPAS layered-identification verification workflow.

## Existing evidence

- The author has publicly frozen the Nature submission snapshot and prospective EPSS protocol.
- An external executor independently ran the sealed EPSS package in a separate Linux/Python environment and reproduced the author’s canonical numerical result key exactly.
- That external execution is evidence of cross-environment numerical reproducibility, but it is **not** represented as a CODECHECK certificate.

## Formal CODECHECK status

A community CODECHECK is being requested through the CODECHECK register. A CODECHECK certificate has **not** yet been issued and is **not** claimed by the manuscript or repository.

## Integrity rule

No manuscript statement should be upgraded to “CODECHECK-certified” unless and until an unaffiliated CODECHECK codechecker completes the community workflow and a certificate is formally issued.
