# Does scale close the gap between identical retrieval evaluations and the answers they produce? A preregistered scale curve within one model family

**Study ID:** RIDI-RAG-QWEN3-SCALE-CURVE-v1
**Author:** Adeeb Noor, King Abdulaziz University (arnoor@kau.edu.sa; ORCID 0000-0002-8251-1853)
**Parent registrations:** OSF txwdv (primary experiment); OSF ms4w8 (registered extensions P1–P5)
**Template:** OSF Preregistration (standard). Registered before any output of this study is generated.

---

## 1. Study information

### 1.1 Background
In the registered primary experiment (OSF txwdv), uncredited passages were exchanged at random inside frozen BM25 top-10 search results for 800 questions from four BEIR benchmarks, keeping every credited passage at its rank, so every grade-based retrieval score was identical by construction. With Qwen3-8B, answer correctness changed for 17.27% of questions (equal-benchmark mean) against a 1.03% execution floor. A post hoc run with Qwen3-32B gave 12.37%. Whether the effect persists, shrinks towards the execution floor, or vanishes as model size grows is unknown.

### 1.2 Research questions
- **RQ1.** Does the excess of answer-correctness change over the execution floor persist at the largest dense model in the Qwen3 family (32B)?
- **RQ2.** Does it persist at every size from 0.6B to 32B?
- **RQ3.** How does it change with model size within the tested range?

### 1.3 Hypotheses (directional where stated)
- **H1 (persistence at 32B).** For Qwen3-32B, the equal-benchmark excess E = I − F is at least 5 percentage points with a 95% lower bound above 2 points. I is the intervention change rate and F is the execution-floor change rate, both defined in section 4.
- **H2 (persistence at all sizes).** At every executed size, the 95% lower bound of E exceeds 2 points.
- **H3 (scale trend, two-sided).** The slope of E on log10(parameters) across executed sizes differs from zero. No direction is predicted.

### 1.4 Disclosure of prior knowledge
- The author knows two earlier results on this panel:
  - Qwen3-8B primary rates (17.27% intervention, 1.03% floor; registered).
  - The Qwen3-32B intervention rate (12.37%; post hoc, publicly locked before output, not OSF-registered).
- No result for 0.6B, 1.7B, 4B or 14B has been generated or seen.
- The 32B floor under this design has not been measured.
- This study re-runs 8B and 32B under one protocol. Earlier results are not pooled with new ones.
- The decision thresholds (5 points; lower bound 2 points) are inherited from the registered H2 of OSF txwdv. They were fixed before the earlier results were known.

---

## 2. Design

### 2.1 Overview
This is a within-question paired design. The same 800 questions, contexts and prompts are presented to each model.

### 2.2 Factors
- **Model size:** six dense Qwen3 models.
- **Condition:** three conditions per model.

### 2.3 Conditions (per model, per question)

| Condition | Context | Execution |
|---|---|---|
| reference_single | registered BM25 top-10 reference passages | one prompt per forward pass |
| random_single | registered grade-preserving random exchange (same document identities as the primary experiment) | one prompt per forward pass |
| reference_fixed16 | reference passages | consecutive blocks of 16 prompts in frozen panel order within each benchmark, left padding |

### 2.4 Blinding
- Per-question correctness is written to files and never printed to logs.
- No result file is opened, and no partial aggregate is computed, until all jobs have finished or been declared failed (section 7).

### 2.5 Randomization
There is no new randomization. The exchange is the registered random draw (seed 20260902), reproduced byte for byte. The runner verifies the frozen manifest, document identities and prompt-manifest SHA-256 for each benchmark before loading any model.

---

## 3. Sampling plan

### 3.1 Data
The frozen registered panel of 800 questions:

| Benchmark | Questions | Task |
|---|---:|---|
| Natural Questions | 250 | QA |
| HotpotQA | 250 | QA |
| FEVER | 150 | verdict |
| SciFact | 150 | verdict |

The panel, corpora, qrels, gold answers, prompts and scorer are the registered artifacts of OSF txwdv. Each is verified against its SHA-256 before use.

### 3.2 Models
Primary family: dense Qwen3 models with thinking disabled.

| Key | Model | Parameters (B) |
|---|---|---:|
| qwen3-0.6b | Qwen/Qwen3-0.6B | 0.6 |
| qwen3-1.7b | Qwen/Qwen3-1.7B | 1.7 |
| qwen3-4b | Qwen/Qwen3-4B | 4 |
| qwen3-8b | Qwen/Qwen3-8B | 8 |
| qwen3-14b | Qwen/Qwen3-14B | 14 |
| qwen3-32b | Qwen/Qwen3-32B | 32 |

- Exact Hugging Face commit SHAs are recorded in `models.json`. That file's SHA-256 is recorded in `LOCK.json`.
- `LOCK.json` is committed publicly and attached to this registration before generation.
- The 8B and 32B revisions are those used earlier: 8B `b968826d…`, 32B `9216db57…`.

Optional tier: Qwen/Qwen3-235B-A22B (mixture of experts, 22B active parameters).
- It is run only if it fits the same local, unquantized, deterministic regime on at least eight 80-GB GPUs.
- It is analysed separately (section 6.3) and never enters H1–H3.
- No API or quantized substitute is permitted for any model.

### 3.3 Generation settings (all models)
- Greedy decoding (do_sample=False).
- max_new_tokens = 128.
- Chat template with enable_thinking=False.
- Passages truncated to 1,200 characters.
- Seed 20260902.
- torch.use_deterministic_algorithms(True); TF32 disabled.
- Native unquantized weights (bfloat16).
- Environment, GPU type and loaded dtype are recorded for every job.

### 3.4 Sample size
Fixed at 800 paired questions by the registered panel. There is no stopping rule beyond completion.

As a precision guide: with a change rate near 12% and a floor near 1%, an equal-benchmark 95% interval for E is roughly ±2.5 points (the post hoc 32B intervention rate of 12.37% had an interval of 10.07–14.77%). This is enough to separate E from the 2-point boundary when E ≥ 5 points.

---

## 4. Variables

All outcomes are computed with the frozen registered scorer against gold answers.

| Variable | Definition |
|---|---|
| Intervention change (I) | Correctness differs between reference_single and random_single |
| Execution-floor change (F) | Correctness differs between reference_single and reference_fixed16 |
| Excess (E) | I − F, computed on the equal-benchmark scale (mean of the four benchmark rates) |
| Direction | correct→wrong and wrong→correct counts for the intervention contrast |
| Canonical change | Normalized answer differs between reference_single and random_single |
| Accuracy | Correctness in reference_single and random_single |

---

## 5. Pre-analysis checks (reported, not used to exclude)
- **C1. Determinism.** For each model and benchmark, the first 16 reference prompts are regenerated one at a time after the main run. The number of byte-identical answers is reported.
- **C2. Reproduction of the archived 8B run.** For Qwen3-8B, per-question correctness in reference_single and random_single is compared with the archived primary run (expected: full agreement). Any disagreement is reported. The new 8B values are analysed as generated.

---

## 6. Analysis plan

### 6.1 Estimation
For each model, the following are computed on the equal-benchmark scale, with pooled values also reported:
- I, F and E.
- Canonical change rate.
- Accuracy in each condition.

Uncertainty uses 100,000 bootstrap resamples (seed 20261010) of questions within benchmark.
- The resampled questions are shared across models (joint, paired bootstrap), so differences and trends between models respect the pairing.
- Intervals are 95% percentile intervals. The accuracy difference uses a 90% interval for two one-sided tests at ±5 points.

### 6.2 Confirmatory decisions
- **H1 (Qwen3-32B):**
  - *supported* if E ≥ 5 points and the 95% lower bound is > 2 points;
  - *falsified (vanishes)* if the 95% upper bound is < 2 points;
  - otherwise *inconclusive*.
- **H2:**
  - *supported* if the 95% lower bound of E exceeds 2 points at every executed primary size;
  - whether all six sizes were executed is reported alongside.
- **H3:**
  - Ordinary least-squares slope of E on log10(parameters, billions) across executed primary sizes (at least three required).
  - 95% interval from the joint bootstrap.
  - Classified as decreasing (upper bound < 0), increasing (lower bound > 0) or no detectable trend.

No α-adjustment is applied across H1–H3. Each hypothesis answers a distinct question, and all are reported regardless of outcome.

### 6.3 Secondary analyses (descriptive)
- **S1.** Canonical change rate by size.
- **S2.** Direction: correct→wrong versus wrong→correct, with an exact two-sided binomial test per size.
- **S3.** Accuracy by condition and size. Two one-sided tests at ±5 points on the paired accuracy difference.
- **S4.** Cross-scale overlap of changed questions:
  - Jaccard index and Haldane-corrected odds ratio for each pair of sizes.
  - Distribution of the number of sizes at which each question changes.
  - Permutation test of concentration (variance of that count; 10,000 within-benchmark permutations; seed 20261011).

  S4 asks whether the same questions change across scale.
- **S5.** Change rates by size within strata defined by the frozen P4 judge labels:
  - no exchanged passage flagged by either judge (93 questions);
  - judges never agreed (238);
  - strict registered clean rule (86);
  - QA items with no gold-answer string in any exchanged passage (282).

  Pooled rates are reported with Wilson 95% intervals. No stratum-specific floors are claimed.
- **S6.** The optional 235B tier, analysed with the H1 rule and reported separately.

### 6.4 Interpretation limits (fixed in advance)
- No extrapolation beyond the tested range. No claim of the form "the effect vanishes at size X" is permitted.
- Results concern one open-weight family, one retriever (BM25), k = 10, four benchmarks and this prompt.
- A decreasing trend with H1 supported is reported as "declines with scale but persists through 32B".
- A falsified H1 is reported as "vanishes at 32B in this family".

---

## 7. Execution and failure rules
- One job = one model × one benchmark. Jobs may run in any order and on any compatible hardware.
- **Infrastructure failure** means a crash, timeout or out-of-memory error, before or during generation.
  - The job is re-run from the start with an identical configuration, up to three attempts.
  - The attempt number is recorded.
  - Outputs of failed attempts are kept but never analysed.
  - Re-runs are triggered only by the failure itself, never by any outcome.
- A model that does not complete all four benchmarks within three attempts each is reported as not executed. No substitute model is used.
- Code, `models.json` and the analysis script are frozen by `LOCK.json`, and the runner refuses to start if any file differs.
- A defect found after the lock is handled by a dated, public pre-output amendment if no output has been inspected. Otherwise it is reported as a deviation.
- The analysis runs once, after all jobs end, with `aggregate_scale_curve.py` exactly as locked.

## 8. Data and code
- All per-question records, run metadata, hashes and the analysis output will be deposited publicly with the resulting paper.
- Code: https://github.com/adeebnoor/ridi (directory `experiments/qwen3_scale_curve/`).
