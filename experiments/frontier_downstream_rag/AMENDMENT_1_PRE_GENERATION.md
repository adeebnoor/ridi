# AMENDMENT 1 — pre-generation common-universe correction

Protocol: `RIDI-NATURE-FRONTIER-DOWNSTREAM-v1`

**Timing:** this amendment is public after successful BM25/SPLADE++ retrieval and before any Qwen3-8B generation or downstream correctness endpoint from this extension.

## Why an amendment is required

The original implementation clarification attempted to use the union of BM25 top-100 and SPLADE++ top-100 while requiring every union member to have an emitted score in both retrievers' top-1,000 runs. The successful retrieval run `35350211540` showed that this cross-score completeness rule would make the planned balanced sample infeasible: only 44 HotpotQA queries and 1 SciFact query met that rule before gold mapping. Proceeding would therefore replace the planned broad sample with an extreme high-overlap subset.

No language-model output has been generated or inspected for this extension. The information motivating this amendment is retrieval-overlap feasibility only.

## Corrected fixed candidate universe

For each query, define the frontier candidate universe as:

[
C_q = mathrm{Top1000}_{BM25}(q) cap mathrm{Top1000}_{SPLADE++}(q).
]

Both retrievers therefore provide genuine emitted scores for every candidate in (C_q); no score is imputed or censored.

A query is eligible when:

1. both top-1,000 runs are complete;
2. (|C_q| ge 40), so the largest prespecified capacity (k=20) satisfies (nge2k);
3. the benchmark task gold outcome can be mapped from the same public source-mapping rules used in the registered RIDI RAG work.

Gold mappability is metadata eligibility, not a model outcome. For each dataset, 100 query IDs are sampled without replacement from the sorted eligible IDs using NumPy `default_rng(20260918)`, before model generation.

## Consequence for interpretation

The extension now estimates frontier/downstream behavior on a **common-retrievable candidate universe**, not the full corpus and not the union of the retrievers' surfaced candidates. This restriction must be stated wherever the extension is reported.

All other locked elements remain unchanged:

- BM25 baseline and SPLADE++ update;
- k=10 primary, k={5,20} sensitivity;
- eta=0.001 primary, eta=0.0001 secondary;
- Qwen3-8B generator family and frozen scoring rules;
- paired identity-control and downstream endpoints;
- full reporting regardless of direction.

## Prior technical failures

The preceding assembly attempt also exposed a syntax defect and, for NQ, the fact that the public gold mapper does not map every BEIR query. Neither failure produced a model output. The corrected assembler therefore treats exact gold mapping as an explicit pre-generation eligibility condition rather than requiring all benchmark queries to map.

No further candidate-universe or eligibility change is permitted after the amended 400-query sample and frontier states are frozen.
