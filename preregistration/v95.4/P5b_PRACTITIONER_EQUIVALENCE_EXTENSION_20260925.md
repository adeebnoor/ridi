# P5b — Practitioner-defined retrieval equivalence extension

**Status:** pre-generation registration.  
**Date:** 25 September 2026.  
**Relation to P5:** P5b is a new, explicitly post-P5 extension. The original P5 remains unchanged and negative at its registered inferential gate (0/760 qualified pair×dataset cells under joint nDCG@10 + Recall@10 TOST with Holm correction). No P5 answer-generation stage was entered. P5b does not relabel, relax, or replace P5.

## Motivation and estimand

P5 asked whether retrieval systems could be demonstrated statistically equivalent within a 0.01 margin. In ordinary model comparison, however, a practitioner commonly sees point estimates on a leaderboard/dashboard and treats two systems as practically tied when the displayed difference is small. P5b estimates downstream answer instability under that practitioner-facing definition.

The estimand is conditional on the same frozen 20-configuration retrieval roster, the same common BM25 top-100 candidate pools, the same datasets, and the same frozen qualification/estimation split as P5. It is not a prevalence claim over all retrieval systems.

## Frozen information available at registration

Known before P5b:
- Original P5 qualification result: 0/760 cells qualified under the registered inferential equivalence gate.
- P5 diagnostic resolution and all P1–P4 results are known.
- No P5 or P5b generator outputs exist on the P5 estimation split.

No P5b answer generation may occur before this file is committed.

## Dataset and split

Primary datasets are unchanged: Natural Questions, HotpotQA, FEVER and SciFact.

The frozen P5 sample and seeded SHA-256 split are reused without resampling:
- Natural Questions: 300 total = 120 qualification + 180 estimation.
- HotpotQA: 300 total = 125 qualification + 175 estimation.
- FEVER: 300 total = 120 qualification + 180 estimation.
- SciFact: 149 total = 55 qualification + 94 estimation.
- Total estimation queries: **629**.

The qualification split alone determines pair eligibility. Generator output is never read during qualification.

## Frozen roster and retrieval

The P5 20-configuration roster is reused without adding, removing, tuning, or replacing a configuration. Every configuration reranks the same frozen BM25 top-100 candidate pool. Retrieval depth for the comparison metric is k=10.

## P5b qualification rule — practitioner equivalence

For each unordered configuration pair within each dataset:

1. Compute mean nDCG@10 separately for the two configurations on that dataset's frozen **qualification split**.
2. Let `delta = mean_nDCG10_A - mean_nDCG10_B`.
3. The pair×dataset cell qualifies for P5b iff **abs(delta) < 0.01**.

This is a point-estimate rule only. There is:
- no TOST requirement;
- no Recall@10 gate;
- no p-value;
- no multiple-testing correction.

The strict operator is `< 0.01`, not `<= 0.01`.

All qualifying cells are carried forward. No pair may be selected or removed based on answer outcomes, Jaccard distance, model identity, apparent effect size, or convenience. If zero cells qualify, P5b stops and no generation occurs.

## Generation

Generation uses the same P5 prompt construction, passage truncation, frozen estimation queries, and top-10 contexts specified in the P5 code freeze.

Primary generator:
- provider/access route: OpenAI API;
- requested model: `gpt-5.6-sol`;
- independent repeats: **2 per context/system**, matching the frozen P5 default;
- maximum requested output: 128 new tokens in the P5 interface; if the provider rejects `max_tokens`/temperature for the reasoning model, the frozen OpenAI backend switches to `max_completion_tokens=max(128,1024)=1024` and records that temperature was unsupported;
- requested seed in the frozen OpenAI backend: 20260902;
- temperature 0 only where supported; otherwise no unsupported temperature is forced;
- exact returned model identifier and system fingerprint, when supplied by the API, are archived for every call.

No generation begins until qualification is complete and the full qualifying-cell list plus its input hashes are archived.

## Outcome and repeat floor

Primary answer endpoint is the original P5 semantic-answer disagreement endpoint:
- exact normalized answer identity first;
- if strings differ, the frozen P5 semantic judge determines `EQUIVALENT` versus `DIFFERENT`;
- judge failures are missing and reported, never silently recoded.

For each qualifying pair×dataset cell:
- between-system disagreement is computed on the frozen 60% estimation split;
- the matched repeat floor is the disagreement between the two independent generations of the **same** context/system;
- primary cell estimand is **semantic-answer-disagreement excess = between-system disagreement − matched repeat floor**.

The registered P5 pair-specific query bootstrap is retained: 5,000 query resamples for a 95% interval.

## Practitioner-facing prevalence summaries

P5b reports, over all qualifying pair×dataset cells:
1. the number and fraction of estimation queries whose answers differ between practitioner-equivalent retrieval systems;
2. the corresponding matched repeat-floor rate;
3. repeat-adjusted disagreement excess;
4. the distribution of cell-level excesses;
5. the fraction of qualified cells with excess >= 0.05, with uncertainty from the same finite-roster query-resampling bootstrap used in P5.

Dataset-specific results are reported before any pooled summary. Because cells share retrieval configurations, cells are not treated as independent replications. No super-population claim over unseen retrieval systems is made.

## Reporting rule

The manuscript must distinguish:
- **P5:** preregistered inferential-equivalence test; gate failed; no prevalence estimate under that definition.
- **P5b:** post-P5, pre-generation practitioner-defined extension using a point-difference rule.

P5b will be labelled as a new extension registered after the negative P5 qualification result. Results are reported regardless of direction or magnitude.