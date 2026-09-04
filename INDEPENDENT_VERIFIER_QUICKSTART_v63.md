# Independent verifier quickstart — Nature v63

**Manuscript:** *Identical audits, different AI decisions*  
**Scope:** independent execution of the locked EPSS natural-update analysis only (`RIDI-CYBER-NATURAL-UPDATE-v1`). The v63 manuscript changes are editorial and do not alter this computational scope.

## Goal
Produce an execution result in your own environment and determine whether the locked machine-readable outputs reproduce exactly. This is an execution check, not a manuscript review.

## Independence
Before running, please disclose any current or prior personal, professional, academic, supervisory or financial relationship with Adeeb Noor that could affect whether the run can be described as independent. A disclosed relationship does not invalidate the computation, but it changes how the evidence is labelled.

## Entry point
Use the repository root `codecheck.yml` together with:

- `README_CODECHECK_ENTRYPOINT.md`
- `COMMUNITY_CODECHECK_SCOPE_2026-08-31.md`

The target outputs include candidate-universe size, top-1,000 changed slots, RIDI@1,000, pre/post within-version controls, future-KEV recovery, full-universe AUROC values, and the two identity-control operating points.

## Blind-execution rule
Do not inspect or compare against the author's canonical result key before completing the execution. Record any dependency problem, ambiguity, deviation, failure or discrepancy rather than correcting it to match the manuscript.

## Record
Please retain date/UTC time, operating system, Python and key dependency versions, repository commit or sealed-package identifier, commands executed, produced machine-readable outputs and SHA-256 hashes, and whether the values match exactly after the run is complete.

## Return
If you are willing to provide a signed declaration, use `INDEPENDENT_EXECUTION_DECLARATION_TEMPLATE_v63.md` as the content checklist. A formal CODECHECK certificate is a separate process and is not implied by this independent run.
