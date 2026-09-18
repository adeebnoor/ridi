# RIDI-NATURE-FRONTIER-DOWNSTREAM-v1

**Status:** publicly locked before endpoint execution.  
**Purpose:** test whether explicit identity control can reduce evidence-set turnover while preserving near-maximal updated retrieval utility, and measure the downstream language-model consequences.

## Registration boundary

This is a new prospective extension. It does not alter the registration status of any earlier RIDI experiment. The analysis code, endpoint definitions, decision rules and reporting requirements below are fixed before any endpoint output from this extension is accepted.

## 1. Experimental question

For a frozen query set with two retrieval states, compare:

1. **Reference** — baseline retrieval state;
2. **Updated-unconstrained** — the updated retrieval top-k;
3. **Frontier-controlled eta=0.0001** — minimum identity turnover subject to <=0.01% relative loss in updated rank utility;
4. **Frontier-controlled eta=0.001** — minimum identity turnover subject to <=0.1% relative loss in updated rank utility.

The primary question is whether frontier control reduces changed evidence identities while keeping updated rank utility inside the declared budget, and what happens to downstream answer correctness and answer identity under the same frozen generator.

## 2. Data freeze

Primary sample: 400 queries, exactly 100 each from Natural Questions, HotpotQA, FEVER and SciFact, drawn from frozen evaluation pools without replacement using seed `20260918`.

The query IDs, prompts, relevance judgements and candidate passages must be frozen and hashed before model generation.

If an exact 100-query eligible pool is unavailable for a dataset, all eligible queries are retained and the shortfall is reported; no replacement dataset is introduced after endpoint inspection.

## 3. Retrieval states

- Baseline retriever: BM25.
- Updated retriever: SPLADE++.
- Candidate universe for frontier computation: union of the two frozen retriever candidate lists for each query, requiring at least `2k` unique candidates.
- Retrieval scores are retained exactly as emitted by each retriever and provenance/hashes are recorded.

Primary capacity: `k=10`.

Sensitivity capacities: `k={5,20}`.

No retriever tuning is permitted on the endpoint sample.

## 4. Frontier

The exact identity–utility frontier uses the repository implementation in `src/ridi_audit/selector.py`.

Updated utility is the sum of deterministic percentile ranks under the updated retrieval scores, with document identity as final tie break.

Primary tolerance: `eta=0.001`.

Secondary locked tolerance: `eta=0.0001`.

For each query/k/eta report:

- unconstrained changed slots;
- controlled changed slots `j(eta)`;
- RIDI before and after control;
- relative updated rank-utility regret;
- avoidable-turnover fraction when unconstrained turnover > 0.

## 5. Generator and scoring

Primary generator: the same pinned Qwen3-8B revision and prompt family used in the registered RIDI RAG experiment.

Generation settings are frozen before endpoint execution. The registered strict scorer is retained as the primary correctness scorer. The existing broader answer-matching and prefix-tolerant classification rules are secondary sensitivities and may not replace the primary endpoint.

Each query is generated independently under all four retrieval states using identical decoding settings.

## 6. Primary endpoints

The experiment has two co-primary descriptive endpoints:

A. **Identity-control endpoint:** mean query-level reduction in changed slots from updated-unconstrained to frontier-controlled at `k=10, eta=0.001`.

B. **Downstream endpoint:** paired difference in benchmark-defined correctness between updated-unconstrained and frontier-controlled at `k=10, eta=0.001`.

Report both regardless of direction.

The primary analysis also reports:
- normalized answer-text disagreement;
- fraction of queries whose correctness status changes between unconstrained and controlled;
- dataset-specific results and equal-dataset-weight macro;
- 100,000 query-stratified bootstrap draws, seed `20260918`, for paired differences.

No claim of non-inferiority is made unless a separate margin was fixed before execution; the primary result is descriptive.

## 7. Retrieval-quality reporting

For each state report available benchmark retrieval measures (precision, recall, nDCG, MRR and MAP where defined) using the frozen qrels.

Because qrels may be incomplete, zero-grade is described as zero evaluation credit, not semantic irrelevance.

## 8. Sensitivities

Prespecified:
- `k=5` and `k=20`;
- `eta=0.0001` and `eta=0.001`;
- registered strict scoring;
- broader answer-match sensitivity;
- prefix-tolerant FEVER/SciFact sensitivity.

All sensitivity cells are reported. No cell may be omitted for an inconvenient direction.

## 9. Failure and missingness rules

- Query excluded only for a documented pre-endpoint technical failure that makes one of the four states unavailable.
- Exclusions are listed by query ID and reason.
- No failed query is replaced after generation begins.
- If the candidate union has fewer than `2k` unique passages, that k cell is unavailable for that query.
- No imputation of model answers, scores or relevance grades.

## 10. Interpretation boundary

The experiment can establish an end-to-end trade-off among evidence identity, the declared updated rank utility and benchmark-defined downstream answers.

It cannot establish:
- clinical or policy benefit;
- universal invariance across retrievers or generators;
- semantic irrelevance of zero-grade passages;
- that identity preservation should always be preferred;
- that eta=0.001 is a universally appropriate operational tolerance.

## 11. Audit outputs

Before any manuscript integration, archive:
- this protocol and commit SHA;
- frozen query/candidate manifest and SHA-256 hashes;
- retriever versions/revisions;
- generator revision and environment;
- raw generations;
- per-query results;
- aggregate results;
- execution log;
- SHA256SUMS.

All results are reported whether supportive, null or adverse.
