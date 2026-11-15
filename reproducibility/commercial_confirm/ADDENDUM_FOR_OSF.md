# RIDI-CONFIRM-C: Commercial-model replication of the RIDI-CONFIRM held-out test (preregistration addendum)

**Status: written before any outcome data.** Version 1.3-draft, 12 November 2026 (UTC+3); supersedes the 1.0-draft of 10 November 2026 and the 1.1- and 1.2-drafts of the same day (settings below were decided from the technical access checks described in the next paragraphs and in §10, before registration and before any confirmatory call). This addendum extends the RIDI-CONFIRM registration https://osf.io/794p5/ (project https://osf.io/bjuwe/), and it does not modify that registration. With the single exception of the technical checks described below, no commercial-model output on any RIDI-CONFIRM prompt has been generated, viewed or scored.

A technical access check was run on 12 November 2026 on five questions per model, using the bm25_whole arm only (plus a few further calls on three of those questions to test Gemini reasoning settings; see §10). The outputs were inspected only for non-emptiness, finish reason, token usage and answer format. The check is excluded from every analysis, and no correctness, change or agreement metric was or is to be computed from it. A second technical check, on the same 30 frozen prompts sampled across arms and datasets, was run for each of the three models (§10); it was a format-only inspection (emptiness, finish reason, token usage), with no scoring and no correctness computed, and it is excluded from every analysis. Because it used frozen confirmatory-cohort prompts (no other prompts exist), the author saw only these counts and no scores. The settings in §4 and §7 are pre-registration settings decided from these checks. No confirmatory call has been made.

## 1. Background and prior observation (disclosure)
- The open-weight RIDI-CONFIRM results are known to the author:
  - H1 excess for W of 3.33 points (Qwen3-8B) and 6.80 points (Mistral-7B-Instruct-v0.3);
  - H3 excess for D of 7.67 and 13.22 points.
- A separate commercial replication of the drug-interaction study (https://osf.io/t9wvh/, GPT-5.4 mini) did not meet its registered criterion.
- This study is therefore **not a blind confirmation**. It tests whether the held-out RIDI-CONFIRM effect transfers to commercial models. The question IDs, prompts, eligibility flags, scorer and analysis are those frozen before the open-weight outcomes, and none was changed after them.

## 2. Hypotheses (registered criterion form, applied per commercial model *m*)
- **H1c (primary).** Among E1_win questions (identical released top-10 relevance-grade vectors under W), the answer-correctness change between BM25 whole-document and BM25 150-word-window prompts exceeds the same-context re-execution change by more than 2 percentage points. This is tested with the frozen one-sided within-benchmark bootstrap: equal benchmark weights, 20,000 draws, seed 20261102, P(excess ≤ 0.02), Holm correction across the three commercial models at one-sided α = 0.025.
- **H2c.** As for H1c, within strict E3_win. It is descriptive if fewer than 100 questions are eligible.
- **H3c (secondary, nominal).** Change for full-corpus Contriever versus BM25 whole-document within E1_dense, minus the re-execution change, overall and by benchmark.
- **H4c (descriptive).** Overlap of changed E1_win questions across the commercial models; the either-model rate with an exact 95% interval.

## 3. Pass/fail criteria (fixed now)
- **Per model:** H1c is met for model *m* if its Holm-adjusted test passes under the frozen scorer.
- **Study-level replication criterion:** met if H1c passes for at least two of the three models. Otherwise it is reported as not met.
- **Partial pattern:** if exactly one model passes, the result is reported as "not met; supported in one model".
- All results are published whatever their direction.
- The format-scorer variant is a sensitivity analysis only.

## 4. Models and decoding (pinned)
| Key | Vendor | Exact model ID | Decoding |
|---|---|---|---|
| gpt-5.4-mini | OpenAI | `gpt-5.4-mini-2026-03-17` (same snapshot as t9wvh) | Chat Completions; temperature 0; reasoning_effort "none"; max_completion_tokens 128; seed 20261110 |
| claude-sonnet-5.5 | Anthropic | `claude-sonnet-5-5` (the model identifier returned by the API is recorded per call) | Messages API; **no temperature parameter** (the vendor rejects it for this model, so the vendor default applies); thinking `{"type":"between_tools"}`; no tools supplied; max_tokens 128 |
| gemini-3.8-flash | Google, via OpenRouter | OpenRouter slug `google/gemini-3.8-flash` (the model and provider returned are recorded per call) | OpenRouter chat completions (`https://openrouter.ai/api/v1/chat/completions`); temperature 0; `reasoning: {"effort":"minimal"}`; **max_tokens 640** (reasoning tokens count toward it); seed 20261110; provider preferences `only: ["google-ai-studio"]`, `allow_fallbacks: false`, `data_collection: "deny"` (no prompt retention or training, as declared by the provider; no fallback to other providers) |

**Gemini via OpenRouter.** The lowest reasoning setting the endpoint accepts is "minimal": "none" and `enabled: false` are rejected (HTTP 400, reasoning is mandatory). "minimal", "low" and "low" with reasoning excluded gave identical, non-empty answers in the access check, so "minimal" is pinned. Calls are pinned to the Google AI Studio standard-tier endpoint (USD 0.75 per million input tokens and USD 3.75 per million output tokens; this endpoint was used for all access-check calls); costs are taken from the usage reported by OpenRouter, or from tokens at these prices if higher. OpenRouter forwards requests to Google, which is a third-party processor; the no-retention/no-training setting rests on the provider's declared policy and OpenRouter's routing filter. Reasoning is billed as output and counts toward max_tokens. In a 30-item technical check at max_tokens 128, 2 of 30 answers ended with finish_reason "length" (reasoning of 118–122 tokens left the answer cut off; none was empty). Rerunning the same 30 items at 256, 384 and 640 gave 30/30 finish_reason "stop" and no empty answers; reasoning appeared on 4 of 30 items, with a maximum of 346 tokens. max_tokens 640 is therefore pinned, with margin above the largest observed reasoning use. The answer itself stays short (mean 36 output tokens including reasoning); the instruction in the prompt, not the limit, controls answer length.

For GPT-5.4 mini and Claude Sonnet 5.5 the 128-token output limit matches the registered greedy 128-token generation, and it stays: neither model spends tokens on reasoning here (GPT reasoning_effort "none": 0 reasoning tokens; Claude with no tools: 0 thinking tokens), and in the 30-item technical check at 128 tokens (§10.2) all 30 answers of each model ended naturally (finish reasons stop and end_turn respectively; none empty; at most 28 and 79 output tokens, respectively; 0 reasoning or thinking tokens). Gemini differs only because its endpoint forces a reasoning phase whose tokens share the limit; its 640 is a reasoning-plus-answer budget, and the answer is still limited to a short span by the prompt. Each call sends the frozen prompt text byte-for-byte as a single user message (or the frozen message list, if the file stores one). The model identifier and usage reported by each vendor are stored with every output.

## 5. Cohort and arms
- **Cohort:** the locked RIDI-CONFIRM cohort of 1,500 questions (500 each from Natural Questions, HotpotQA and FEVER; ID list SHA-256 da06e5c9…3d4d5b).
- **Eligibility flags:** frozen before generation (`flags_W_AND_H3_D_FROZEN.csv`).
- **Arms per model:**
  - bm25_whole, bm25_window and contriever;
  - two further independent calls of the bm25_whole prompt, which give the re-execution floor.
- **Total:** 7,500 calls per model.
- **Re-execution floor:** the control indicator is 1 if any of the three bm25_whole calls disagree in scored correctness, as in the registered conservative floor.
  - The two repeat calls are labelled whole_rep_b1 and whole_rep_b16, so the frozen script runs unmodified.
  - For commercial APIs these labels denote *independent repeat calls*, not batch sizes. This is a declared adaptation, because vendor batching cannot be controlled.
- **Call order:**
  - Pass 0: all three primary arms, shuffled with seed 20261110.
  - Then pass 1 (first repeat) and pass 2 (second repeat), each started only after the previous pass has finished.

## 6. Scoring and primary analysis
- **Scorer:** the frozen scorer `scoring.py` (SHA-256 5b9f02f7…c7ee), called through the registered adapter logic for the frozen and format variants.
- **Gold:** the frozen file (SHA-256 f899b972…e89203).
- **Exclusions:** questions without a reference answer are excluded from reference-dependent scoring, as registered. No replacements are made.
- **Analysis:** the unmodified `holdout_analysis.py` (SHA-256 09fe6ee3…1b3c), run with `--models gpt-5.4-mini claude-sonnet-5.5 gemini-3.8-flash`. Holm is therefore applied across three models.
- **Equal weighting:** rates use equal benchmark weights, as registered.

## 7. Budget, stopping rules and deviations
- **Total cap:** USD 200 including the access check, enforced by a file-locked ledger. Before every call, the runner reserves a pessimistic worst-case cost and aborts rather than exceed the cap.
- **Per-model caps:** USD 30 (gpt-5.4-mini), USD 75 (claude-sonnet-5.5) and USD 18 (gemini-3.8-flash). Gemini is funded by a prepaid OpenRouter balance of USD 20 (about USD 19.83 remaining after the checks), which is also a hard limit. If it is reached, the Gemini run stops and is reported as incomplete.
- **Projected costs** (computed from the character counts of all 7,500 frozen prompts per model, input-token ratios and answer lengths observed in the access check, standard tier, no discounts; ranges span answer lengths 0.8–1.5 times those observed up to the worst case of 128 output tokens on every call):
  - gpt-5.4-mini about USD 9–13;
  - claude-sonnet-5.5 about USD 38–46;
  - gemini-3.8-flash (via OpenRouter, Google AI Studio standard tier, max_tokens 640) about USD 10–12 (input about USD 9.2; output including reasoning about USD 1.0–2.0, from a mean of 36 output tokens per call in the 30-item check and a doubling allowance). The theoretical worst case of 640 output tokens on every call would be about USD 27 and would hit the USD 18 cap; it is not expected. Any OpenRouter credit-purchase fee is additional and outside this estimate;
  - total about USD 57–71 (central estimate about USD 58), against the **hard cap of USD 200** for the whole study including the access check. The technical checks cost USD 0.46 in total (§10); scaling the 30-item check to 7,500 calls gives about USD 8.8 (gpt-5.4-mini), 39.4 (claude-sonnet-5.5) and 10.0 (gemini-3.8-flash), which lie inside the ranges above. Caps are unchanged.
- **If a cap is reached:** the model stops. Its missing arms are counted and its questions excluded under the registered missing-arm rule. The result is reported as incomplete.
- **API errors:**
  - a transport-level retry wrapper retries HTTP 429, 500, 502, 503, 504 and 529 up to six times (waits of 5 s doubling to a maximum of 60 s), and the runner makes up to six attempts per call with exponential backoff; failed responses are not billed and not charged to the ledger;
  - a persistent failure is a missing arm;
  - authentication or model-not-found errors stop the model.
- **Refusals, empty answers and truncated answers** are scored as returned. No prompt is edited, truncated or regenerated.
- **Model unavailable before the run:** if a pinned model ID is unavailable, the vendor's nearest successor may be substituted only before any confirmatory call, with a dated amendment.
- **Deprecation mid-run:** the run for that model stops and is reported as incomplete.
- **Gemini max_tokens (decided before registration):** the rule "raise max_tokens if any answer is empty or truncated in a technical check" was applied on 12 November 2026 and settled at 640 (§4, §10). No setting is changed after the first confirmatory call. Empty or truncated answers are then scored as returned.
- **Other deviations** are listed in the results with their timing relative to outcome data.

## 8. Frozen inputs (SHA-256)
| File | SHA-256 |
|---|---|
| H3_D_1500_PROMPTS_PRE_GENERATION.jsonl | e5962184bb97ae4557304b65d03ee5277bc2315e61fcde3a2d9db9c5ba786a74 |
| W_3000_PROMPTS_PRE_GENERATION.jsonl | c981f2847d41b2c46bbef198e538f56e5f445611d01602f2ad2a0893018d5186 |
| prompt template | 381cd2f539fc0216a07a3d72a955a6f5590d8779548b99371180f723b550ab9a |
| gold | f899b9727dd6612fca12bc6f0b6d42bb4ef15e3807815714a973cb5585e89203 |
| flags_W_AND_H3_D_FROZEN.csv | 9b8c8d9f7eae36712a98e7ba919610ed5ca68e00c8ce9e0906eeb7ea5cbd33f0 |
| scoring.py (frozen scorer) | 5b9f02f7a8bcd4df98f3bf28e66017e86e4cfa3e36d495acb6d1e2828488c7ee |
| holdout_analysis.py (frozen H1–H4) | 09fe6ee38e535205bc117aa6e212e7d31158cc3686cee776f38c2d7b24d11b3c |
| H3_D_FLAGS_PROMPTS_PREGEN_LOCK.json | 4148e1ca04cc0eb036ba97a5a824dc187175c569d367a763e1ab1ac320d90b13 |
| code/run_commercial.py (includes the OpenRouter vendor) | see MANIFEST_SHA256.txt |
| code/models_pinned.json | see MANIFEST_SHA256.txt |
| code/score_and_analyze.py | see MANIFEST_SHA256.txt |
| code/tech_check.py (format-only technical check) | see MANIFEST_SHA256.txt |

## 9. Data and reporting
- **Deposit:** all raw outputs, per-call usage, the spend ledger and hashes will be deposited in project bjuwe.
- **Benchmark text:** handled under the original licences.
- **In the manuscript:** the results will be reported as a registered replication with its timing disclosed, together with the t9wvh result.

## 10. Technical-check record (excluded from all analyses)
### 10.1 Access check (5 questions per model)
- **Date:** 12 November 2026. Five questions per model, bm25_whole arm only, outputs in `smoke/` (not in `runs/`).
- **Result:** all three models returned non-empty answers on 5/5 calls (finish reasons stop/end_turn), in the expected answer format. No correctness was computed.
- **Earlier Gemini attempt:** before OpenRouter was available, access attempts through Google's own API (thinkingLevel "low") produced no retained output: six failed calls (not billed) and one billed call (USD 0.0022) whose output was not kept. They are recorded in the ledger, and the empty folder is kept as `smoke/_gemini-3.8-flash_direct_google_attempt_no_output/`.
- **Other models:** the GPT and Claude access checks were run with exactly the settings in §4 (Claude with no temperature parameter).

### 10.2 Thirty-item technical check, all three models (format only)
- **Date and design:** 12 November 2026. The exact pinned settings of §4 for each model, at the max_tokens stated in the tables. Thirty frozen prompts (10 per arm: bm25_whole, bm25_window, contriever; 3–4 per dataset within each arm; sampled with seed 20261112; the five access-check questions excluded), the same 30 for all three models. All prompts of the study are frozen confirmatory-cohort prompts, so no non-cohort prompts were available. The check records only emptiness, finish reason and token counts (`code/tech_check.py`, outputs in `smoke/tech_check_30/<model>/mt<max_tokens>/`). No scoring was done and no correctness, change or agreement metric was computed. "Truncated" means finish_reason "length" (OpenAI, OpenRouter) or "max_tokens" (Anthropic).
- **Decision rule (fixed before the runs):** if any answer is empty or truncated, raise that model's max_tokens to the smallest tested value that gives 30/30 complete answers, with margin, and rerun the same 30.

**Gemini 3.8 Flash (via OpenRouter)**

| max_tokens | empty | truncated | complete | items with reasoning | reasoning tokens (max) | mean output tokens | cost (USD) |
|---|---|---|---|---|---|---|---|
| 128 | 0 | 2 | 28 | 4 | 415 (122) | 26.7 | 0.0390 |
| 256 | 0 | 0 | 30 | 4 | 578 (245) | 32.4 | 0.0396 |
| 384 | 0 | 0 | 30 | 4 | 679 (346) | 35.8 | 0.0400 |
| 640 | 0 | 0 | 30 | 4 | 679 (346) | 35.8 | 0.0400 |

**GPT-5.4 mini and Claude Sonnet 5.5 (max_tokens 128 only, because no answer was empty or truncated)**

| Model | max_tokens | empty | truncated | complete | items with reasoning/thinking | mean output tokens (max) | cost (USD) |
|---|---|---|---|---|---|---|---|
| gpt-5.4-mini | 128 | 0 | 0 | 30 (stop) | 0 | 11.2 (28) | 0.0351 |
| claude-sonnet-5.5 | 128 | 0 | 0 | 30 (end_turn) | 0 | 29.7 (79) | 0.1576 |

- **Decision (before registration):** Gemini is raised to max_tokens 640, because 2 of 30 answers were truncated at 128; 256 was the smallest tested value giving 30/30 complete answers, but the observed maximum reasoning use was 346 tokens, so 640 is pinned for margin. GPT-5.4 mini and Claude Sonnet 5.5 stay at 128 because none of their 30 answers was empty or truncated and neither used reasoning or thinking tokens (largest answers 28 and 79 tokens). The models differ only because Gemini's endpoint forces a reasoning phase that shares the output limit. All values were fixed on this evidence before any confirmatory call.
- **Run notes:** the first GPT run stopped after one billed call because of a logging error in the check script (no output was saved for that call); the script was fixed and the GPT check was rerun in full. That one call is in the ledger.

### 10.3 Spend recorded in `SPEND_LEDGER.json`
- Access check (10.1): gpt-5.4-mini USD 0.0083; claude-sonnet-5.5 USD 0.0716; gemini-3.8-flash USD 0.0264 (five final calls through OpenRouter, the reasoning-setting probe and the earlier direct call).
- 30-item check (10.2): gemini-3.8-flash (four runs) USD 0.1585; gpt-5.4-mini USD 0.0367 (including the one lost call); claude-sonnet-5.5 USD 0.1576.
- Total of all technical checks: USD 0.4591. No confirmatory call has been made.
