# OSF preregistration: extensions P1-P6 — v95.4 READY TO FILE

**STATUS: READY TO FILE.** Historical registered assets, scorer, prompts and outputs have been recovered and verified; P6 provenance and OSF `7cah9` have been resolved; and the reviewed experiment code has been frozen before any new P1–P6 model output. The planned P4 human-annotation activity is **conditional on a pending King Abdulaziz University institutional determination**: no human annotation, recruitment or consent activity will begin until the institution has determined the applicable review/consent requirements and those requirements have been satisfied. Filing this preregistration locks the P4 design in advance; it does not authorize the human-annotation activity. Once filed, thresholds, rosters, splits, prompts and endpoints are locked; any later deviation must be dated and reported.

## Title

Evaluation-equivalent retrieval and generation: execution floor, replacement variability, semantic audit, frontier-model
transfer, natural prevalence in a prespecified retrieval roster, and a production score update (extensions to OSF txwdv)

## Study information

**Background.** The registered experiment (OSF txwdv) held the benchmark relevance grade at every retrieved rank fixed
while exchanging grade-zero passages and found correctness changes in 17.27% of 800 queries (equal-dataset macro) for
Qwen3-8B. Those outcomes are already known to the author. P1-P4 reuse the known query panel as prespecified extensions;
P5 uses previously unused queries and is the confirmatory natural-prevalence analysis.

**Hypotheses / decision rules.**

- **H-P1 (frontier/API transfer):** for each API model named below, the point estimate of excess correctness-change
  (reference-vs-exchanged change minus that model's own reference repeat floor) is at least 0.05 **and** the lower 95%
  bootstrap bound for excess is above 0. This dual criterion separates a prespecified practical-effect threshold from
  evidence that the excess is positive. Primary repeat floor: reference run 0 versus reference run 1; the maximum of all
  reference-repeat pairs is a sensitivity.
- **H-P2 (execution floor):** for Qwen3-8B, the point estimate of correctness-change excess over the prespecified primary
  batch-regime floor is at least 0.05 **and** the lower 95% bootstrap bound is above 0. Primary floor: `single` versus `fixed:16` on the reference context, where `single` reproduces the registered one-prompt-per-forward-pass execution structure. Sensitivity: the worst per-query reference disagreement over all prespecified regime pairs (`single`, `fixed:16`, `shuffled:16:1`, `shuffled:16:2`).
- **H-P3 (replacement variability):** descriptive; no directional hypothesis. Primary estimand: per-query probability of
  a correctness change across the registered draw plus four new frozen draws. Report the distribution, any-draw rate and
  majority-draw rate.
- **H-P4 (semantic audit):** within queries for which every exchanged passage is judged uninformative by both prespecified
  LLM judges and contains no normalized QA gold string, the point estimate of correctness-change rate is at least 0.05
  **and** its lower 95% stratified-bootstrap bound is above 0.02. This is deliberately described as a *judged-uninformative*
  subset, not proof of semantic irrelevance.
- **H-P5 (natural prevalence; primary):** within the **fixed prespecified roster** and primary datasets, after qualification
  for equivalence in nDCG@10 and Recall@10, at least 25% of qualified pair×dataset cells have mean semantic-answer
  disagreement excess of at least 0.05 over the matched repeat floor. Report both (a) the point-threshold share and
  (b) the stricter share whose pair-specific 95% bootstrap lower bound is at least 0.05. The criterion must hold for the
  prespecified API generator and for at least one of the two prespecified open generators. A query-resampling bootstrap
  gives uncertainty for the finite-roster share; it does **not** generalize to all retrieval systems.
- **H-P6 (EPSS v4→v5 update):** retrospective/descriptive. OSF `7cah9` was registered on 25 August 2026, after the v5 release of 15 June 2026, and explicitly labels v2–v5 analyses retrospective while prospectively locking only the next post-v5 release. P6 therefore does **not** claim preregistered confirmation. Turnover at k=1,000 is compared with the two adjacent same-version daily changes; the exact minimum replacement at 0.1% relative probability loss is reported; KEV capture within 30, 60 and 90 days is descriptive.

## Design plan

Computational study with one planned human-annotation component in P4. The KAU institutional determination for that component is pending as of 23 September 2026. A request covering the current manuscript and the planned limited annotation has been prepared for the Local Committee for Medical and Biological Ethics. **No P4 human annotation will begin until KAU has determined the applicable review/consent requirements and all required approvals, consent procedures or other conditions have been satisfied.** The eventual committee name, determination type, reference number and date will be archived and reported before the human-annotation stage starts. The preregistration of P4 therefore precedes both the ethics determination and the collection of any human-annotation data.

### Generators

- Open generator 1: `Qwen/Qwen3-8B`, revision `b968826d9c46dd6066d109eabc6255188de91218`,
  thinking disabled, greedy decoding, 128 new tokens.
- Open generator 2 (P5): `allenai/OLMo-2-1124-7B-Instruct`, revision `470b1fba1ae01581f270116362ee4aa1b97f4c84`.
- API generator (P1 and P5): OpenAI `gpt-5.6-sol`, provider OpenAI, frozen/access date 23 September 2026. The exact returned provider model identifier and system fingerprint, when present, are archived for every call. Temperature 0 is used where supported; unsupported decoding controls are recorded. API repeat disagreement is the primary stochasticity control.

### Prompts and scoring

- P1-P4 use the **exact registered 800-query prompt strings embedded in the recovered contexts** and the **exact frozen registered scorer** from OSF `txwdv`. Frozen scorer: `08_New_Experiments/frozen_registered/scoring.py`, SHA-256 `5b9f02f7a8bcd4df98f3bf28e66017e86e4cfa3e36d495acb6d1e2828488c7ee`. Frozen prompt module: `08_New_Experiments/frozen_registered/prompts.py`, SHA-256 `381cd2f539fc0216a07a3d72a955a6f5590d8779548b99371180f723b550ab9a`. The scorer adapter calls the historical module's `canonical_answer()` and `is_correct()` functions without changing its scoring rules. Fallback scoring is forbidden for confirmatory P1-P4.
- P5 uses `08_New_Experiments/ridi_exp/prompts.py`, SHA-256 `1dd9a924cb9b4c1e7a86a4c207bc3d2307072c498b3ee52da4e438e209c7a4bc`. Each retrieved passage is truncated to
  1,200 Unicode characters before prompt construction. FEVER/SciFact use exactly three labels: `SUPPORTS`, `REFUTES`,
  `NOT_ENOUGH_INFO`.
- P5 semantic-equivalence judge: `Qwen/Qwen3-32B`, revision `9216db5781bf21249d130ec9da846c4624c16137`. Frozen prompt: `08_New_Experiments/P5_SEMANTIC_JUDGE_PROMPT_v95.3.txt`, SHA-256 `4314a9b5d2136eabdf966b8789978137cbcd34e1b0ffa70136bdecfdd3cbe633`. Different strings count as disagreement only when the judge returns the exact token `DIFFERENT`; exact `EQUIVALENT` means equivalent. Any other output is missing and is reported, never silently classified. A human audit of judge decisions is reported.

## Sampling plan

- **P1-P4:** the registered 800 queries: 250 Natural Questions, 250 HotpotQA, 150 FEVER, 150 SciFact. No new query sampling. Recovered exact reference+registered-random contexts with embedded frozen prompt strings: `08_New_Experiments/data/contexts_800.jsonl`, 1,600 rows, SHA-256 `1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1`. Recovery validation against the OSF frozen panel, registered intervention algorithm, grade vectors and archived document identities found zero mismatches. Frozen BM25 top-100 pools for P3: `08_New_Experiments/data/pools_800.jsonl`, 800 rows, SHA-256 `d6ebce72f70301cc0bcdd97c21cd10e8fca3f5a853f73a4649dcf89ab3536bf0`.
- **P3:** four new replacement draws per query from the frozen top-100 pools, seed `20260925`; together with the registered
  draw this yields five draws per query.
- **P4:** all exchanged passages are machine-judged; a human sample of 200 unique query–passage items is drawn with seed `20260926`. Annotation-order seeds are `20260927` and `20260928`. Sampling/export code may be frozen before the institutional determination, but the files will not be shown to annotators and no human labels will be collected until the KAU requirements described above are satisfied.
- **P5 primary datasets:** Natural Questions, HotpotQA, FEVER and SciFact; 300 previously unused qrel-bearing queries per
  dataset where at least 300 eligible unused queries exist, after excluding the registered 800. If a dataset has fewer than
  300 eligible queries, all eligible queries are retained and the shortfall is reported; no replacement dataset is introduced.
  Split by seeded SHA-256 hash (`20260928`) into 40% qualification and 60% estimation. Every configuration reranks the same
  frozen BM25 top-100 candidate pool. This candidate-pool conditioning is part of the estimand.
- **P5 secondary transport datasets (descriptive; not counted in H-P5):** FiQA and TREC-COVID, same sampling/split rules,
  answer-disagreement endpoint only unless independently sourced task-appropriate gold answers are frozen before generation.
- **P5 roster:** the 20 configurations in `p5_roster_template.yaml`, file SHA-256 `f5cb668a6d7188290b7e77e3d52a0bb7607550d3de89b3d5da68c249e82d099e`. All 17 learned retrieval/reranking models are pinned to full immutable commits in `06_Provenance/P5_MODEL_PIN_PROVENANCE_v95.3.md`; the three corrected Cross-Encoder repository IDs are frozen in that roster. No configuration may be added or removed after qualification.
- **P6:** EPSS daily files bracketing the v5 release and one same-version adjacent day on each side. KEV catalogue freeze acquired 23 September 2026 from the official CISA `cisagov/kev-data` mirror at commit `43e8cd69d9dde4353897ca63f8a172c1b071de21` (catalogue version `2026.09.22`, release timestamp `2026-09-22T19:02:09.9788Z`, 1,721 entries). P6 uses `known_exploited_vulnerabilities.csv`, Git blob `1340d4fc1292edf2397700dbf302fd91cefb8632`, SHA-256 `76e153792b614abdc46708c01b856c27c01ef8d893f284a666a3b2c5c8391500`. JSON cross-check: blob `2191fec68db30cf8385df92f1d7a224fcbc5221a`, SHA-256 `b912a7f9a4c4630455d09b04946664a5dccd8b1a7c987010d89793e1a5b78c91`. Provenance record: `06_Provenance/P6_KEV_SNAPSHOT_LOCK_v95.4.json`. Universe excludes KEV additions on or before the pre-update day.

## Variables

- Correctness change: indicator that benchmark-defined correctness differs between two conditions for a query.
- Semantic answer disagreement: normalized outputs differ and the prespecified semantic judge does not judge them equivalent.
- Repeat floor: the same endpoint between two generations of an identical context. P1 uses independent API repeats; P2 uses
  registered batch regimes; P5 uses two runs with changed batch companions for local generators and independent repeats for API.
- Excess: paired query-level disagreement/change minus the corresponding repeat-floor quantity.
- Jaccard distance: set distance between top-10 retrieved identities (descriptive association in P5).

## Analysis plan

- P1-P4 rates: equal-dataset-weight macro is primary where inherited from the registered design; pooled rates are reported alongside.
- Intervals: dataset-stratified bootstrap, 100,000 resamples for primary macros; 20,000 for excess unless otherwise stated.
- P2: primary and worst-case floor rules are fixed above. The recovered historical execution code confirms that the original registered Qwen3-8B generation called one prompt per forward pass. Byte identity is therefore assessed for the `single` regime against the recovered archived registered outputs. Registered reference+random generation archive: `08_New_Experiments/data/registered_generations_primary_800.jsonl`, 1,600 rows, SHA-256 `e7d1c8c06eece5482f632d628f933741ebbfc379ae01a99a293abdd9debf929c`. Replay of the exact recovered scorer reproduced canonical answers and correctness for all 1,600 archived outputs with zero mismatches.
- P5 qualification: paired two one-sided t-tests on per-query nDCG@10 and Recall@10, equivalence margin 0.01, joint p equal
  to the maximum of the two p-values, Holm correction within dataset, alpha 0.05. Qualification uses only the 40% split and
  reads no generator output. All tested pairs are reported.
- P5 inference: pair×dataset mean semantic-disagreement excess on the 60% split; pair-specific query bootstrap (5,000) for
  the 95% interval; share meeting the 0.05 threshold; query-resampling bootstrap (5,000, seed `20260929`) for the share while
  holding the roster fixed. Mean excess with a two-way query×pair bootstrap is secondary/descriptive. Pairs share
  configurations and are **not independent replications**. No super-population claim over unseen retrievers is made.
- P5 association with Jaccard distance is descriptive and does not define qualification or support.
- P6: exact frontier as in `05_Reproduction/run_probability_frontier.py`; tolerance ladder
  {0, 0.0001, 0.001, 0.005, 0.01, 0.05}. Wilson intervals are descriptive.

## Inference criteria

A confirmatory hypothesis is labelled supported only if **every** condition written above is met exactly. Failure is reported
as failure and narrows the manuscript claim. Thresholds, roster membership, dataset roles, prompts, judge, splits and endpoints
are not changed after results are seen.

## Data exclusion and missing data

No outcome-dependent exclusion. API errors are retried up to six attempts; contexts still failing are reported and excluded
from both conditions of the affected paired contrast. Unparsed outputs are scored according to the frozen scorer; P1-P4 do not
substitute the fallback scorer. P5 judge failures are reported and are not silently interpreted as disagreement or equivalence.

## Scope and interpretation

- P1-P4 extend a query panel whose original outcomes are already known; they are not a fresh prevalence estimate.
- P5 is confirmatory on previously unused queries, but its prevalence estimate is conditional on the prespecified 20-configuration
  roster and common BM25 top-100 pool.
- A zero benchmark grade is not treated as proof of semantic irrelevance.
- The study tests action/answer disagreement under evaluation equivalence; it does not infer harm, benefit or clinical consequence.

## Registration, code and audit lock

- Code directory: `08_New_Experiments`. Reviewed code-freeze artifact committed on the dedicated GitHub preregistration branch at commit `fb29c4cdbaed7598412081b14a4b9183c0f78177`; artifact path `preregistration/v95.4/RIDI_v95.4_GitHub_Code_Freeze_20260923.zip`; artifact SHA-256 `075e925ddca308a456b61e74fc3c3b5c85e3e1f597bacbc33ebcfb0b2f020e5e`; Git blob `d47e5f96c508fc9023520b9b05e4f86b23031f73`. The later branch-tip commit only removed a temporary import workflow and does not change this scientific code-freeze artifact.
- Required pre-run checks: `python tests/test_pipeline.py`; `check_contexts.py ... --registered-panel --require-prompt`; scorer
  SHA check; no unresolved model-revision placeholders or other placeholder markers in the filed registration.
- Relation to P6: OSF `7cah9` was publicly registered on `2026-08-25T10:09:55.185626Z`. Its registration text states that v2–v5 analyses were retrospective and that the confirmatory data are the first future EPSS file whose model-version header differs from `v2026.06.15`. Consequently, the present v4→v5 P6 analysis is explicitly retrospective/descriptive and is not presented as prospective confirmation under `7cah9`.