# Source data and reproducibility
This folder is the Source Data accompanying the manuscript (data release of 16 November 2026). Paths below are relative to this folder. Figure numbering follows the manuscript; tables and figures cited as Extended Data here appear as Online Appendix Tables A1–A6 and Figures A1–A4 in the current version. Archived input names can carry an older figure or version number.

## Replay the held-out study
Use Python 3 with NumPy and pandas. Figure generation also requires SciPy, Matplotlib and scikit-learn. From this directory:

```bash
python code/check_holdout.py > replay.json
mkdir -p rendered
python code/make_figures.py --out rendered
python code/make_figure_2.py --out rendered   # the figure carries no embedded title
```

`make_figures.py` also writes an earlier two-panel `Figure_1`. Run `python code/make_figure_1_v42.py --out rendered` after it to obtain the three-panel Figure 1 of the Article (see "Added in v42" below).

`check_holdout.py` verifies the registered script and the receipt hashes, recovers the original 21,216 W score rows by byte prefix, and compares identifiers and all W eligibility flags for the 1,500 questions. It verifies that the other 5,304 rows belong to D and runs the untouched registered analysis twice. The script compares the resulting W-only and W/D reports with the respective frozen originals after accounting for the archived line-ending convention. The four paired net-accuracy intervals at the end of the output are a separate post hoc analysis. The saved output is `holdout/paired_accuracy_and_replay.json`. For a portable JSON comparison, decode both JSON files and compare the resulting objects.

| Finding | Data used for verification |
|---|---|
| Figure 1 and primary example | Figure_1_historical.json (plotted six-size rates), Scale_4800_paired_correctness.csv (case outcomes), Primary_800_paired_outcomes.csv and claim275_SOURCE.txt |
| Figure 2, controlled study and re-execution | Primary_800_paired_outcomes.csv, archived point and interval estimates in make_figure_2.py, and SCALE_REGISTERED_REPLAY_COMPACT_VERIFIED.json for the registered scale panels |
| Figure 3a–e | Figure5_factorial_cells_v28.csv, Figure5_factorial_components_v28.csv and Figure5_natural_transitions_v28.csv for panels a–c. Natural_segmentation_561_summary.json gives the archived Table 1 counts for panels d and e. The intersection and mutually exclusive categories follow by inclusion–exclusion. |
| Figure 3f and Extended Data Table 3 | holdout/flags_W_AND_H3_D_FROZEN.csv, scores_W_AND_H3_D_REAL.csv, Holdout_Frozen_Analysis.json, and code/holdout_analysis.py. The four plotted rows are tabulated in figure_data/Figure_3f_source_data.csv |
| Figure 4 and Supplementary Figure 1 | Scale_4800_paired_correctness.csv, Transfer_800_paired_correctness.csv and Source_Reconciliation.json (post hoc markers/classification aggregates) |
| Held-out methodological sensitivity | H3_D_E3_SECONDARY_AUDIT_20261109.json, the original Mistral preflight receipts and project disclosure, and W_H5m_v1_1_POSTHOC_ONLY_20261107.json |

**Interpretation.** H1 is the only two-model Holm decision implemented in the recovered confirmatory script. The paired two-sided percentile intervals in Figure 3f are nominal. H3 is a nominal registered contrast. Figure 3f uses the combined W/D run consistently. H4's frozen and complete-case denominators answer different questions. Human H5 case ratings are pending. No unblinding key or private adjudicator files are included.

**Mistral D.** The public-facing text is `holdout/RIDI_CONFIRM_H3_RUNTIME_DISCLOSURE_20261109.md`. Two original preflights and their contemporaneous change note document the change from 8,192 to 16,384 before successful generation. The separate OSF_H5_V2 receipt refers only to the earlier decision about submission timing.

**Data scope and licensing.** This directory provides scored case tables, historical figure aggregates and the released holdout receipts. Some historical panels can be replotted from published aggregates. Their upstream full model-output archives are not duplicated in this ZIP. For historical raw files, access limitations, licensing and restricted human coding, consult Data availability in the manuscript, Supplementary Notes 8 and 13 and Supplementary Table 6. The registered holdout is https://osf.io/794p5/ and its project is https://osf.io/bjuwe/.

## RIDI-24 domain-separated capture (added in v55)
`posthoc_v27_1_domain/` holds the frozen RIDI-24 score table (126,000 rows), the original post hoc script `analyze_v27_1.py`, a standalone extraction of its domain section, the saved output and a re-run receipt. It supports the domain-separated rows of Extended Data Table 1, Supplementary Note 7 and Supplementary Table 19 (finance: combined minus difficulty 0.28 points, 95% interval −0.98 to 1.50). Run `python reproduce_domain_bootstrap.py` inside that folder; see its README.

## Drug-interaction application
`DDI/` holds the aggregate results of the two registered drug-interaction experiments (https://osf.io/epk7v/ and https://osf.io/t9wvh/), the eight pairs downgraded in the first experiment and a cross-model comparison; see `DDI/README.md`. `code/ddi_commercial_recompute.py` recomputes the commercial-model results from the raw outputs (it needs SciPy). The case-level inputs and outputs are held by the author and can be provided to editors and reviewers on request.

## Primary archive files (added in v48.1)
`primary_archive/registered_generations_primary_800.jsonl` (1,600 records; SHA-256 `e7d1c8c06eece5482f632d628f933741ebbfc379ae01a99a293abdd9debf929c`) is the two-arm primary record named in Supplementary Note 2. `primary_archive/Primary_registered_outputs_original.zip` (SHA-256 `c19942d0eb4a0087195c46a45831a1cf864676b813485dcf4e5565a2a676f231`) holds the original registered Qwen3-8B outputs for the four benchmarks against which that record was bound. `contexts_800.jsonl` (25 MB; SHA-256 `1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1`) is not in this package; it is held in the reviewer archive.

## Files named in the Supplementary Information that are not distributed in this package
These files are retained by the author, are not deposited in any public repository, and are provided to editors and reviewers on request. Their file names keep the version label of the run that produced them. The file marked * is part of the confidential drug-interaction reviewer archive described in `DDI/README.md` and in Data availability.

| File | Named in | Content |
|---|---|---|
| Archived_controls_inventory_v27_1.csv | Supplementary Note 2 | Inventory of the archived dose, near-cutoff and reorder controls |
| source_provenance_v27_1.json | Supplementary Notes 1 and 8 | Hashes of retained primary files and the two-arm source binding |
| execution_floor_calibration_v27_1.csv | Supplementary Note 2; Extended Data | Per-execution floors for the 44 measured executions |
| transition_classes_4800_v27_1.csv | Supplementary Note 1 | Per-item transition classes for the 4,800 scale-study pairs |
| corrected_sensitivities_v27_1.json and .py | Extended Data; Supplementary Note 17 | Post hoc conditional sensitivities, masks, seeds and denominators |
| LEGACY_PRESENT_AND_MISSING.json | Supplementary Note 8 | Full list of recovered and missing historical archive entries |
| factorial_analysis.json | Supplementary Note 9 | Signed-coefficient intervals for the execution factorial |
| unambiguous_change.py (v1.0) and unambiguous_change_v1_1.py (v1.1) | Methods; Supplementary Notes 12 and 17 | Mechanical classifiers used for the exploratory H5m analysis |
| FULL_GUARD.csv *; evidence_corpus.jsonl *; source_pair_coverage.jsonl * | Supplementary Note 14; `DDI/README.md` | Pre-inference ledgers and source corpus; SHA-256 values are listed in `DDI/README.md` |

`replay.json` in the commands above is the output of `check_holdout.py`, written locally by the reader; the saved output is `holdout/paired_accuracy_and_replay.json`.

## Added in v40 (post hoc, exploratory)
| Finding | Data and code |
|---|---|
| Supplementary Fig. 2 and Supplementary Note 16 (hidden turnover: changes cancelled in the mean) | `code/hidden_turnover_v40.py` reads only the existing paired files listed in its header and writes `posthoc_v40/Hidden_turnover_by_comparison_v40.csv` and `posthoc_v40/Hidden_turnover_summary_v40.json`; `code/make_supp_figure_2_v40.py --out rendered` draws the figure. No new model output; no reported number changes. |

```bash
python code/hidden_turnover_v40.py
python code/make_supp_figure_2_v40.py --out rendered
```

## Added in v42 (theory and Figure 1b)
| Finding | Data and code |
|---|---|
| Proposition 1 (Box 1) and its proof (Methods) | `code/theory_checks_v42.py` checks part (b) exhaustively for n ≤ 14, part (c) exhaustively for n ≤ 6, part (a) for the five measures on 20,000 random exchanges, and computes the primary-study witness from `Primary_800_paired_outcomes.csv` and `Scale_4800_paired_correctness.csv`. Output: `code/theory_checks_v42_output.json` (`ALL_CHECKS_PASS: true`). `figure_data/BEIR_qrels_grade_census_v42.json` records that every released BEIR test judgement for the four benchmarks has grade 1 (URLs and SHA-256 of the files read on 10 November 2026). |
| Figure 1 (panels a–c; panel b new) | `code/make_figure_1_v42.py --out rendered` writes the figure and `figure_data/Figure1b_v42_source.csv`. Panels a and c are unchanged in content from earlier versions. |

**v43 addition:** `code/pre_inference_bm25_gate_300.py` and `DDI/PREINFERENCE_EQUALITY_GATE_AUDIT_v43.json` provide the original DDI eligibility implementation and its verified source-file fingerprints; no model outputs were changed.


**v44:** content unchanged from v43 except `DDI/README.md` (spelling). Methods now states that each DDI window carries its label's drug-name prefix, which the frozen gate script includes when scoring co-mention.

**Note on `OSF_PUBLIC_STATUS_READBACK_v43.json`.** This file records an earlier check made on 10 November 2026. Its field `public_note_found_at_checked_time: false` and its caution describe the state at the time of that check. The Mistral runtime disclosure (`RIDI_CONFIRM_H3_RUNTIME_DISCLOSURE_20261109.md`) was uploaded to OSF later that day (OSF activity record, 17:58 UTC) and is cited in Data availability. The readback file is kept unchanged as the record of the earlier check.

## Added in v49: RIDI-CONFIRM-C (commercial-model replication)
`commercial_confirm/` holds the raw outputs, scores, frozen H1c–H4c report, spend ledger, run and supervisor logs, code and the registered addendum for the replication reported in Results ("The size of the gap depends on the model"), Methods, Extended Data Table 4 and Supplementary Note 18. See `commercial_confirm/README.md`. No file of earlier versions changed.

## Added in v51 and v52: RIDI-CONFIRM-C reference-answer exclusion (post-outcome rerun)
`commercial_confirm/posthoc_reference_exclusion_v51/` holds a script and its outputs. The registered addendum (section 6) excludes questions without a reference answer, but `commercial_confirm/scores_commercial.csv` contains the 174 Natural Questions items that are absent from the open-weight score table (`holdout/scores_W_AND_H3_D_REAL.csv`, 1,326 questions), each scored 0 in every arm, model and scorer variant. The script documents this, removes those questions and runs the unmodified `code/holdout_analysis.py` (same model order as the saved report). It first reproduces the saved report `commercial_confirm/H1_H4_commercial.json` byte for byte.

| File | Content |
|---|---|
| `reference_exclusion_sensitivity.py` | The script. Run from this folder: `python commercial_confirm/posthoc_reference_exclusion_v51/reference_exclusion_sensitivity.py` (needs SciPy and NumPy) |
| `scores_commercial_reference_available.csv` | The commercial scores restricted to the 1,326 questions with a reference |
| `H1_H4_commercial_reference_available.json` | Output of the frozen analysis script on that table |
| `reference_exclusion_summary.json` | Audit counts and the estimates quoted in Results, Methods, Extended Data Table 4 (second part) and Supplementary Note 18 |

This rerun was made after the outcomes were known and is not a registered analysis. The registered-script estimates are reported as run. The reference file (`holdout_1500_gold.jsonl`, SHA-256 `f899b9727dd6612fca12bc6f0b6d42bb4ef15e3807815714a973cb5585e89203`) is a frozen RIDI-CONFIRM input and is not distributed in this package. In v53 it was checked directly: it marks exactly 174 Natural Questions items `has_reference = false`; this set equals the set absent from the open-weight score table and the set scored 0 in all 5,220 commercial cells. `commercial_confirm/posthoc_reference_exclusion_v51/reference_flag_check.py` (run from this directory with the path of the reference file) writes the receipt `reference_flag_check.json`.

**v52, Figure 1.** In `code/make_figure_1_v42.py` the label in panel b now reads "Relevance record identical for 800/800 questions"; the longer label ran outside its box. `01_Article/Figures/Figure_1.pdf` was regenerated with the script. No plotted value and no source file changed (`figure_data/Figure1b_v42_source.csv` is byte-identical).

