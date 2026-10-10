# Is the blind spot of a fixed evaluation a property of the question? A preregistered transfer test on fresh questions with independent exchanges

**Study ID:** RIDI-PREDICT-v1
**Author:** Adeeb Noor, King Abdulaziz University (arnoor@kau.edu.sa; ORCID 0000-0002-8251-1853)
**Parent registrations:** OSF txwdv (primary experiment), OSF ms4w8 (registered extensions P1–P5), OSF whjbs (scale curve, with Amendment A1)
**Related registrations:** OSF kdawx (P7, an earlier registered prediction study; result disclosed in §1.2), OSF qsc5b (P8), OSF pu3mb with technical amendment 2ecnm (P13) and OSF jwhuz (P13R); P13 and P13R terminated before analysis and their inputs are excluded here (§2.1)
**Template:** OSF Preregistration (standard). Filed before any output of this study is generated.

---

## 1. Study information

### 1.1 Background

The parent study exchanged uncredited (grade-zero) passages at random inside frozen BM25 top-10 search results, keeping every credited passage at its rank. Every grade-based retrieval score was therefore identical by construction.

On a frozen panel of 800 questions from four BEIR benchmarks, answer correctness changed beyond a repeat-execution floor at every Qwen3 size from 0.6B to 32B (OSF whjbs with Amendment A1). The registered cross-scale analysis (S4) found that the same questions tend to change across sizes (permutation p < 10⁻⁴).

**A known alternative explanation.** Grade-zero passages are unjudged rather than certified irrelevant. A question might therefore change across models simply because one particular exchange inserted or removed informative text (a distractor or incomplete-qrels effect), or because the question is hard for every model. This study is designed to separate those explanations from a question-level property.

### 1.2 Disclosure of the motivating exploratory results (frozen panel; post hoc)

All results in this section come from the frozen panel. They are post hoc, and all models saw the **same** exchange draw. They motivated the study and set its thresholds (§1.5).

**Fragility score.** We define a fragility score as the number of the three small models (Qwen3-1.7B, 4B and 8B) whose correctness changed on a question. It predicted Qwen3-32B changes with AUC 0.736 (95% CI 0.685–0.786).

| Fragility score | Questions | Qwen3-32B change rate |
|---|---:|---:|
| 0 | 580 | 5.5% |
| 1 | 145 | 27.6% |
| 2 | 67 | 34.3% |
| 3 | 8 | 50.0% |

**Adjusted analysis.** We fitted a logistic model with the following covariates:

- whether an exchanged passage contained the gold-answer string;
- whether either AI judge flagged an exchanged passage;
- how many of the small models were correct on the reference context (linear and quadratic terms);
- whether Qwen3-32B was correct on the reference context;
- the small models' repeat-floor changes;
- benchmark.

With these covariates, the odds ratio per unit of the score was 2.72 (95% Wald CI 2.05–3.59). Adding the score raised the AUC from 0.687 to 0.775. A placebo score built from the small models' floor changes had an AUC of 0.53.

**Content-clean strata.** Within these strata the AUC was lower and imprecise:

- 0.623 (bootstrap 95% CI 0.50–0.76) among 282 question-answering items with no gold-answer string in any exchanged passage (16 changed);
- 0.563 (0.42–0.72) among 93 questions with no exchanged passage flagged by either judge (10 changed).

**What these results cannot show.** Because every model saw the same exchanged passages, these results cannot separate a question-level property from the effect of particular passages. **The primary test below uses an independent exchange draw for the predictors, which has never been run on any panel.**

**Earlier registered prediction attempt (P7, OSF kdawx).** P7 tested whether Qwen3-8B's own reference-context decision margin identifies the questions whose correctness an exchange changes. Its registered input-change AUC was 0.657 (95% paired-bootstrap interval 0.607–0.710), and its registered criteria were not met. P7 used the model's own uncertainty on one context. The present study tests a different predictor: whether *other* models change under an *independent* exchange. The P7 result is the reason H3 conditions on difficulty and why the decision thresholds below are modest.

**Fresh panel.** No question of the fresh panel defined below appears in the project's recovered input records (§2.1). This statement covers recovered project inputs only. It says nothing about unrecovered history or about the models' pretraining data.

### 1.3 Research questions

- **RQ1.** On fresh questions, does a fragility score computed from small models under an **independent** exchange draw predict which questions change correctness under the registered exchange in Qwen3-32B?
- **RQ2.** Does the same score predict changes in a large model from another developer, OLMo-2-0325-32B-Instruct?
- **RQ3.** Does the score add predictive value beyond answer-string content, question difficulty and repeat instability?

### 1.4 Hypotheses

**Notation.**

- F_B is the number of predictor models (0–3) whose correctness changes under exchange draw B, an independent seed.
- A target's change indicator is measured under exchange draw A, the registered seed.

**Hypotheses.**

- **H1 (within-family transfer).** For Qwen3-32B, the pooled AUC of F_B is at least 0.60, and its 95% lower bound exceeds 0.55.
- **H2 (cross-family transfer).** The same holds for OLMo-2-0325-32B-Instruct.
- **H3 (beyond content, difficulty and instability; tested per target as H3a and H3b).** The logistic model has the following covariates:
  - G, an indicator that an exchanged passage contains a normalized gold-answer string;
  - the number of predictors correct on the reference context (linear and quadratic);
  - whether the target is correct on the reference context;
  - the predictors' repeat-floor changes;
  - benchmark indicators;
  - the AI-judge flag, if it is recorded before generation (§2.6).

  In this model, the odds ratio per unit of F_B has a 95% Wald lower bound above **1.3**, which is the smallest effect of interest.

**Prerequisite for each hypothesis.** A target must show an equal-benchmark excess of intervention change over its own execution floor, with a 95% lower bound above 2 percentage points (inherited from txwdv). Otherwise its hypotheses are reported as *not evaluable*, not as falsified.

### 1.5 Decision rules (per target)

| Hypothesis | Supported | Falsified | Otherwise |
|---|---|---|---|
| H1, H2 | AUC ≥ 0.60 and 95% lower bound > 0.55 | 95% upper bound < 0.55 | inconclusive |
| H3 | 95% Wald lower bound of the adjusted OR > 1.3 | 95% Wald upper bound < 1.3 | inconclusive |

The thresholds were set **after** seeing the same-draw frozen-panel results in §1.2. They are deliberately lower than those results, because an independent draw removes the shared-content component and the effect under F_B is expected to be smaller. F_B itself has never been observed.

No α-adjustment is applied. All hypotheses are reported regardless of outcome.

**Expected precision.** At a change rate of about 12% (about 100 positives), the AUC interval is about ±0.05. For OLMo-2, at a 5% change rate (about 40 positives), it is about ±0.08, so an inconclusive result is possible. This is stated now and will not be reinterpreted later.

---

## 2. Design

### 2.1 Fresh panel

**Eligibility.** For each benchmark, eligible questions are those that satisfy the registered panel-eligibility criteria of txwdv. That means the same code (`panels.select_universal_panel` eligibility), the same runs, `panel_ks` and `pool_depth`.

**Exclusions.**

- The 800 frozen-panel questions.
- Every question in the project's known-source input filter: 10,177 input records and 7,280 unique normalized question hashes (filter SHA-256 bc2aecee5a27fc33b75e5caf5c000764ee1c88598533075ace19884a8c613df8). The filter was built from the recovered input records of the project's earlier studies, including txwdv, ms4w8 (P1–P5), P7, P8, P13 and P13R (known-source ledger SHA-256 c22a1384e5befbe44031f0728938e0a1ba433c982657dd41dee1bf7cefd8b0b2). Input history that could not be recovered is listed in a separate unresolved-history inventory (SHA-256 bd887e5791cf2bc5ea740dec6350c54728e2f08bd627ebb7c2d3313edb775d9b) and is reported as a limitation. Matching uses the normalized question text (NFKC, Unicode casefold, whitespace split and join; SHA-256 of the UTF-8 bytes), compared across all benchmark labels, not only by question identifier.
- Within-panel duplicates of the same normalized question (the first in original order is kept).
- The context-length gate below.

**Context-length gate (applied before sampling, identical for all models).** At preflight, the reference, draw A and draw B prompts of every otherwise eligible question are rendered with each model's tokenizer and chat template. A question is ineligible if, for any model, a prompt plus 128 generated tokens exceeds that model's maximum position count (4,096 for OLMo-2-0325-32B-Instruct; the value in each Qwen3 model configuration otherwise). No prompt is truncated. The number removed per benchmark is reported.

**Expected effect on SciFact.** The BEIR SciFact test queries are the original labelled development claims, and 299 of these 300 claims already occur in the project's recorded inputs. SciFact is therefore expected to fall below the 75-question minimum and be excluded. If it is excluded, its 150 questions are reallocated to FEVER (target n = 300), so that the verdict task keeps its share. This rule is fixed before the eligibility counts are seen.

**Sampling.** Simple random sampling with seed 20261012:

| Benchmark | Target n |
|---|---:|
| Natural Questions | 250 |
| HotpotQA | 250 |
| FEVER | 150 |
| SciFact | 150 |

If fewer remain, all eligible questions are used. A benchmark with fewer than 75 eligible questions is excluded from the study: no jobs are run for it, and the locked `predict_config.json` lists only the included benchmarks.

**Preflight before filing.** Tokenizer-only eligibility preflight has completed without loading model weights or generating answers. The observed counts and exclusion breakdown are appended in Section 8. The prespecified rules were applied without resampling or changes to thresholds.

**Freezing.** The following are written to `FRESH_PANEL.json` and hashed in `LOCK.json` before any generation:

- question identifiers in original order;
- the document identities of the reference context, draw A and draw B;
- prompt manifests;
- G;
- the AI-judge flag, if recorded (§2.6).

### 2.2 Exchanges

| Draw | Exchange | Seed |
|---|---|---|
| Draw A | registered grade-preserving random exchange (`build_equivalent`, variant `random`, identifier `"<dataset>:bm25"`) | 20260902 |
| Draw B | the same procedure | **20261016** |

The number of questions whose draw A and draw B exchanged contexts are identical is reported. The primary analysis uses all questions; a secondary analysis excludes the identical ones.

Prompts, passage truncation (1,200 characters) and the scorer are the registered txwdv artifacts, verified by SHA-256.

### 2.3 Conditions (per model, per draw, per question)

These are identical to OSF whjbs:

- reference_single;
- random_single (the draw's exchanged context);
- reference_fixed16 (the execution floor).

### 2.4 Models and jobs

| Role | Key | Model | Revision | Draws |
|---|---|---|---|---|
| Predictor | qwen3-1.7b | Qwen/Qwen3-1.7B | 70d244cc86ccca08cf5af4e1e306ecf908b1ad5e | A, B |
| Predictor | qwen3-4b | Qwen/Qwen3-4B | 1cfa9a7208912126459214e8b04321603b3df60c | A, B |
| Predictor | qwen3-8b | Qwen/Qwen3-8B | b968826d9c46dd6066d109eabc6255188de91218 | A, B |
| Target | qwen3-32b | Qwen/Qwen3-32B | 9216db5781bf21249d130ec9da846c4624c16137 | A |
| Target | olmo2-32b | allenai/OLMo-2-0325-32B-Instruct | b96024342a77a69aa0dda815c3454a671f477463 | A |

After the prespecified eligibility exclusions and SciFact-to-FEVER reallocation, the study includes NQ (250), HotpotQA (250) and FEVER (300): 800 fresh questions. This gives 24 model-by-benchmark-by-draw units: 18 predictor units and 6 target units. No SciFact generation unit is run. The nominal four-benchmark plan would have contained 32 units.

- Qwen3-0.6B is not a predictor. This was fixed in advance because it returned a constant label on the verdict benchmarks in OSF whjbs.
- **Why OLMo-2-0325-32B-Instruct.** It comes from a different developer (Allen Institute for AI) with a different architecture, tokenizer and training data, and its weights and training data are fully public. The OLMo-2 family was a registered transfer family in txwdv and ms4w8. It runs in the same two-GPU configuration as Qwen3-32B and is supported by the transformers version used in OSF whjbs (4.57.6). Its 4,096-position limit is handled by the context-length gate (§2.1).

**Generation settings.**

- greedy decoding;
- `max_new_tokens = 128`;
- chat template with `enable_thinking=False` where supported;
- bfloat16 weights, no quantization;
- seed 20260902;
- deterministic algorithms;
- 32B-class models on two 80-GB GPUs (the Amendment A1 configuration).

### 2.5 Blinding

Correctness is written only to files. No result file is opened, and no partial aggregate is computed, until every job is terminal.

### 2.6 Optional pre-generation covariate

If the operator runs the frozen P4 judgement prompt of ms4w8 with both registered judges on the fresh panel's exchanged passages **before** any generation, the indicator "any exchanged passage flagged by either judge" (`exchanged_judge_flag_any`) is added to the H3 model.

The optional pre-generation AI-judge covariate was not collected. H3 uses the remaining prespecified covariates.

---

## 3. Variables

| Variable | Definition |
|---|---|
| Intervention change | Correctness differs between reference_single and random_single (per model, per draw) |
| Floor change | Correctness differs between reference_single and reference_fixed16 |
| F_B / F_A | Number of predictors with an intervention change under draw B / draw A |
| G | Any exchanged passage of draw A (added or removed) contains a normalized gold-answer string (QA tasks only; 0 for verdict tasks). Computed before generation |
| Target excess | Equal-benchmark mean of the intervention-change rate minus the floor-change rate |

---

## 4. Analysis plan

### 4.1 Confirmatory analysis

The locked script `analyze_predict.py` (SHA-256 in `LOCK.json`, verified with `--lock`) runs **once**, after all jobs are terminal.

**Bootstrap.**

- 100,000 resamples of questions within benchmark (seed 20261013), shared across targets;
- 95% percentile intervals;
- logistic odds ratios with Wald intervals.

**Not executed.** If any benchmark job of a model fails all three attempts, that model is reported as not executed.

### 4.2 Secondary analyses (descriptive)

- **S1.** Same-draw AUC of F_A, as in the motivating analysis.
- **S2.** Placebo: AUC of the predictors' floor-change count.
- **S3.** ΔAUC from the H3 baseline model to the baseline plus F_B (2,000 bootstrap refits).
- **S4.** AUC of each predictor alone under draw B.
- **S5.** Concordance between the two targets' change sets (Jaccard index; Haldane odds ratio).
- **S6.** AUC of F_B among QA items with G = 0, with interval.
- **S7.** Change counts by F_B, split by direction (correct→wrong, wrong→correct).
- **S8.** The primary analysis excluding questions with identical draw A and draw B exchanged contexts.

### 4.3 Interpretation limits (fixed in advance)

- **Scope.** The claim is limited to this exchange, BM25 at k = 10, the three included fresh-panel benchmarks (NQ, HotpotQA and FEVER), this prompt and these models. The historical motivating panel and Part A coding sample retain their original four-benchmark scope.
- **Same-family result only.** A supported H1 with H2 falsified or inconclusive is reported as within-family transfer only.
- **AUC without H3.** H1 or H2 supported without H3 is reported as transfer that may be explained by difficulty or content.
- **No pooling.** The motivating results (§1.2) are not pooled with these results.

---

## 5. Human coding (two research assistants)

**Ethics.** A written determination from the King Abdulaziz University research ethics committee was requested and is under review when this registration is filed. Coding starts only after a written determination permits it. The determination's reference is added by a dated amendment before coding begins. If no permission is obtained, Parts A and B are reported as not performed, and H1–H3 are unaffected.

**Coders.** Two research assistants, identified privately to the PI and named in the acknowledgements with their consent. They do not use AI tools or web search for coding.

Two research assistants code independently. Disagreements are resolved by discussion, and agreement before resolution is reported (Cohen's κ). The coding manual is frozen with this registration.

### 5.1 Part A — human relevance check (completes the human check planned in ms4w8)

**Sample.** 200 exchanged-in, grade-zero passages from the **frozen** panel (seed 20261014): 100 from questions whose Qwen3-8B correctness changed and 100 from questions whose correctness did not. One passage is drawn per question.

**Drawn before filing.** The sample was drawn from the frozen audit package with `build_partA_export.py` and `sample_partA.py`. SHA-256 of the coder sheet (CSV): a9ed8b6cb1210b71612e7e1021c54d1ee01d1df4450bde03e4ccd17b5374826f; of the sealed key: 75b0833b4eb35134646cf28443c5ad0031cc24364f23b0da512b14e2ce8e4d89. Both are also recorded in `LOCK.json`. The 200 items comprise 69 NQ, 54 HotpotQA, 36 FEVER and 41 SciFact passages. The key stays with the PI until both coders have submitted.

**Blinding.** Coders see only the question, the gold answer and the passage.

**Codes.**

- answers or decides the question (yes / partly / no);
- contains the gold string (yes / no);
- same topic (yes / no).

**Analysis.**

- Agreement with the AI-judge labels.
- Change rates where both coders code "no".

### 5.2 Part B — candidate mechanisms (fresh panel; exploratory)

**Sample.** After generation, 200 fresh-panel questions (seed 20261015): 100 with a Qwen3-32B change and 100 without, stratified by benchmark. Coders are blind to status.

**Codes.**

- more than one defensible answer;
- needs two or more passages;
- conflicting passages;
- underspecified question;
- debatable gold answer.

**Analysis.** Associations with F_B and with target change are described. No mechanism claim is made.

---

## 6. Execution and failure rules

These are identical to OSF whjbs §7:

- one job = one model × one benchmark × one draw;
- technical failures are re-run with an identical configuration, up to three attempts;
- failed outputs are kept but never analysed;
- re-runs are triggered only by failure.

**Locking.**

- `LOCK.json` freezes the runner, `models.json`, `FRESH_PANEL.json`, `analyze_predict.py`, `predict_config.json` (listing only the included benchmarks), the coding manual, the Part A coder sheet and its sealed key.
- The lock is published (GitHub commit and attached to this registration) before the first generation.
- A defect found before any output is inspected is handled by a dated public amendment. A defect found later is reported as a deviation.

## 7. Data and code

All per-question records, run metadata, hashes, human codes and analysis outputs will be deposited publicly with the resulting paper.

Code: github.com/adeebnoor/ridi (`experiments/predict_transfer/`).

---

## 8. Completed tokenizer-only preflight before registration

Preflight completed without loading model weights or generating model responses. The source archives and all 73 registered artifacts passed SHA-256 verification. The original exclusion filter was recovered byte-for-byte and matched the prespecified SHA-256; it was not rebuilt.

| Benchmark | Archive queries | Registered eligible | Frozen-panel exclusion | Additional known-source exclusion | Duplicate exclusion | Context-length exclusion | Fresh eligible | Selected n |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Natural Questions | 2255 | 2255 | 250 | 300 | 0 | 0 | 1705 | 250 |
| HotpotQA | 7405 | 7405 | 250 | 300 | 0 | 0 | 6855 | 250 |
| FEVER | 6656 | 6656 | 150 | 311 | 78 | 0 | 6117 | 300 |
| SciFact | 299 | 299 | 150 | 149 | 0 | 0 | 0 | 0 |

Included benchmarks: nq, hotpotqa, fever. Total selected n = 800; planned model-by-draw-by-benchmark units = 24.

Exclusions are sequential and mutually exclusive. Counts are bounded by the registered prepared-v4 input archives; the SciFact archive contains 299 queries. Eligibility uses the unchanged registered select_universal_panel with limit=len(queries). All three contexts were rendered with each of the five tokenizers, preserving the frozen runner’s chat-rendering and special-token handling. The context gate reserved 128 output tokens, with limits of 40,960 for each Qwen3 model and 4,096 for OLMo-2. Token sequences were never truncated.

Benchmarks below 75 fresh eligible questions are excluded. The prespecified SciFact-to-FEVER reallocation and sampling seed 20261012 were applied. Sampling preserves input query order. The optional pre-generation AI-judge covariate was not collected. Known limitations of unrecovered project input history remain unchanged.

OLMo-2-0325-32B-Instruct revision: `b96024342a77a69aa0dda815c3454a671f477463`. No thinking block was produced by its tokenizer-only template probe.

FRESH_PANEL.json SHA-256: `6bf4deffdf1c6b961f5f0762626edbef1a68ba5b49d3d26d23022b3c87f00b54`. This receipt is not a scientific lock; the runner, configuration and panel must be locked and published after registration and before generation.
