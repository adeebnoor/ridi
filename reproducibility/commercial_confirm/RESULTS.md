# RIDI-CONFIRM-C: confirmatory results (commercial-model replication)
Registration: https://osf.io/anbjd/ (DOI 10.17605/OSF.IO/ANBJD). Generated 2026-11-13T07:52:47.884203+03:00 (Asia/Riyadh) by code/make_results.py from the frozen analysis script (unmodified). Analysis report: analysis/H1_H4_commercial.json (SHA-256 692a8318af1e667f2aafe9ffdb2ba9be3f110be213c708ea3928c53dc19ef553), scores: analysis/scores_commercial.csv.

## Verdict
**Replication criterion NOT MET; supported in one model (gemini-3.8-flash).**
Study-level criterion: H1c must pass (Holm-adjusted, one-sided alpha 0.025) for at least two of three models. Passing models: gemini-3.8-flash.
All three runs completed all 7,500 calls.

## Completion, empty and truncated answers, spend
| Model | calls recorded | completed | errors (missing arms) | empty | truncated | spend (USD) | restarts |
|---|---|---|---|---|---|---|---|
| gpt-5.4-mini | 7500 | 100.0% | 0 | 0 (0.0%) | 0 (0.0%) | 8.8207 | 0 |
| claude-sonnet-5.5 | 7500 | 100.0% | 0 | 0 (0.0%) | 21 (0.28%) | 40.4973 | 0 |
| gemini-3.8-flash | 7500 | 100.0% | 2 | 0 (0.0%) | 4 (0.053%) | 10.3435 | 0 |

Total ledger spend including technical checks: USD 60.1206 (hard cap 200; Gemini cap 18).

## H1c (primary), E1_win, frozen scorer
### H1c: bm25_whole vs bm25_window, excess over re-execution
| Model | n eligible | excluded (missing arm) | change rate (eq. wt) | re-execution rate (eq. wt) | excess (eq. wt) | 95% CI of excess | one-sided P(excess ≤ 0.02) | Holm-supported |
|---|---|---|---|---|---|---|---|---|
| gpt-5.4-mini | 1264 | 0 | 0.0454 | 0.0356 | 0.0098 | [-0.0024, 0.0221] | 0.9488 | False |
| claude-sonnet-5.5 | 1264 | 0 | 0.0313 | 0.0239 | 0.0074 | [-0.0023, 0.0174] | 0.9929 | False |
| gemini-3.8-flash | 1262 | 2 | 0.0347 | 0.0000 | 0.0347 | [0.0247, 0.0452] | 0.0011 | True |

## H2c, strict E3_win (descriptive if fewer than 100 questions)
### H2c
| Model | n eligible | excluded (missing arm) | change rate (eq. wt) | re-execution rate (eq. wt) | excess (eq. wt) | 95% CI of excess | one-sided P(excess ≤ 0.02) | Holm-supported |
|---|---|---|---|---|---|---|---|---|
| gpt-5.4-mini | 197 | 0 | 0.0290 | 0.0200 | 0.0090 | [-0.0141, 0.0337] | 0.8512 | n/a |
| claude-sonnet-5.5 | 197 | 0 | 0.0507 | 0.0351 | 0.0156 | [-0.0148, 0.0465] | 0.6004 | n/a |
| gemini-3.8-flash | 197 | 0 | 0.0243 | 0.0000 | 0.0243 | [0.0050, 0.0483] | 0.4353 | n/a |

Descriptive only: gpt-5.4-mini=False, claude-sonnet-5.5=False, gemini-3.8-flash=False.

## H3c, contriever vs bm25_whole, E1_dense (nominal)
| Model | stratum | n | change rate (eq. wt) | re-execution rate (eq. wt) | excess | 95% CI | one-sided P(excess ≤ 0.02) |
|---|---|---|---|---|---|---|---|
| gpt-5.4-mini | all | 590 | 0.0540 | 0.0329 | 0.0211 | [0.0008, 0.0418] | 0.4583 |
| gpt-5.4-mini | fever | 231 | 0.0303 | 0.0303 | 0.0000 | [-0.0173, 0.0173] | 0.9876 |
| gpt-5.4-mini | hotpotqa | 206 | 0.0728 | 0.0291 | 0.0437 | [0.0097, 0.0825] | 0.1131 |
| gpt-5.4-mini | nq | 153 | 0.0588 | 0.0392 | 0.0196 | [-0.0261, 0.0654] | 0.5587 |
| claude-sonnet-5.5 | all | 590 | 0.0658 | 0.0195 | 0.0462 | [0.0262, 0.0674] | 0.0053 |
| claude-sonnet-5.5 | fever | 231 | 0.0346 | 0.0130 | 0.0216 | [-0.0043, 0.0519] | 0.4546 |
| claude-sonnet-5.5 | hotpotqa | 206 | 0.0777 | 0.0194 | 0.0583 | [0.0243, 0.0971] | 0.0226 |
| claude-sonnet-5.5 | nq | 153 | 0.0850 | 0.0261 | 0.0588 | [0.0196, 0.1046] | 0.0364 |
| gemini-3.8-flash | all | 590 | 0.0616 | 0.0000 | 0.0616 | [0.0422, 0.0822] | 0.0000 |
| gemini-3.8-flash | fever | 231 | 0.0433 | 0.0000 | 0.0433 | [0.0173, 0.0693] | 0.0277 |
| gemini-3.8-flash | hotpotqa | 206 | 0.0631 | 0.0000 | 0.0631 | [0.0340, 0.0971] | 0.0029 |
| gemini-3.8-flash | nq | 153 | 0.0784 | 0.0000 | 0.0784 | [0.0392, 0.1242] | 0.0018 |

## H4c (descriptive): overlap of changed E1_win questions
n E1_win = 1264; changed in either model = 118 (exact 95% CI [0.0779, 0.1107]); in all three = 1; only in one model: {"claude-sonnet-5.5": 29, "gemini-3.8-flash": 25, "gpt-5.4-mini": 46}.

## Sensitivity: format-scorer variant (not confirmatory)
### H1c with the format scorer
| Model | n eligible | excluded (missing arm) | change rate (eq. wt) | re-execution rate (eq. wt) | excess (eq. wt) | 95% CI of excess | one-sided P(excess ≤ 0.02) | Holm-supported |
|---|---|---|---|---|---|---|---|---|
| gpt-5.4-mini | 1264 | 0 | 0.0454 | 0.0356 | 0.0098 | [-0.0024, 0.0221] | 0.9488 | n/a |
| claude-sonnet-5.5 | 1264 | 0 | 0.0313 | 0.0239 | 0.0074 | [-0.0023, 0.0174] | 0.9929 | n/a |
| gemini-3.8-flash | 1262 | 2 | 0.0347 | 0.0000 | 0.0347 | [0.0247, 0.0452] | 0.0011 | n/a |

## Deviations and operational notes
- Settings, prompts, scorer, call order and analysis are exactly those of addendum v1.3 (osf.io/anbjd); runner and analysis code are unmodified (hashes in MANIFEST_SHA256.txt).
- Operational interruptions (see runs/RUN_LOG.md): a runner crash caused by the runner's ledger file being read while another process was writing it, and two hung HTTP calls; the runner was resumed from its saved outputs, and an in-flight call may have been repeated (possible extra billed calls not in the ledger). The runner was supervised by code/supervisor.py (restart after a crash or a 10-minute stall; stop rules for >2% empty answers, repeated failures and near-cap spend).
- Missing arms (errors) are excluded under the registered rule and counted in the tables above.
- The 'whole_rep_b1' / 'whole_rep_b16' labels denote independent repeat calls (declared in the addendum).
- Gemini max_tokens 640 and GPT/Claude 128 as pre-registered.
