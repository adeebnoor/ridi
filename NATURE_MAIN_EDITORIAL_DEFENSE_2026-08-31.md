# Nature main — editorial defense map

This note records the manuscript's intended editorial logic and the evidence supporting it.

## Central discovery

The manuscript's primary contribution is not a new audit metric. It establishes a general identification failure: aggregate performance and group-fairness summaries constrain cells of a finite allocation but do not identify which individuals receive the scarce action. Consequently, two allocations can be audit-equivalent while disagreeing on decision identity.

## Why the result is broad

The claim is tested across heterogeneous real-world settings rather than inferred from a single application: criminal-risk ranking (COMPAS), hospital payment ranking (CMS HVBP), vulnerability prioritization (EPSS), and additional knowledge-graph/text settings. These systems differ in domain, institution, data-generating process, update mechanism, and operational meaning of the finite decision set.

## Why this is not a collection of case studies

The empirical systems are adversarial tests of a common identification theorem. They play distinct roles: exact construction of audit-equivalent allocations; natural-update evidence in deployed systems; controllability of decision-identity turnover; and registered/null tests that constrain overgeneralization.

## Falsification and boundaries

Registered negative results are retained prominently. The paper does not claim that every model update causes decision-identity instability, nor that identity should always be stabilized. The proposed reporting requirement is outcome-gated: decision identity matters when a score is converted into a finite allocation of review, funding, intervention, or attention.

## Reproducibility status

The computational workflow is public and frozen. External execution has reproduced the canonical EPSS numerical key in an independent environment. A community CODECHECK has been requested; no CODECHECK certificate is claimed until formally issued.

## Authorship interpretation

Single authorship reflects responsibility for synthesis and analysis, not dependence on a single data-generating source. The empirical evidence arises from independently governed public systems and includes prospective locking, controls, and falsification tests. No honorary or cosmetic co-authorship should be added merely to signal breadth.
