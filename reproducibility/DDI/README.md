# Drug-interaction application: source data

Two registered model-output experiments on the same 173 drug pairs and 519 prompts (three calls per pair: reference context B0, identical repeat R0, changed segmentation B1).

| File | Content |
|---|---|
| RIDI_DDI_v38_RESULTS_SUMMARY.json | Open-weight model (Qwen3-8B; registration https://osf.io/epk7v/): counts, tests, intervals and SHA-256 digests of the frozen inputs, generator and raw outputs |
| RIDI_DDI_v38_8_MAJOR_DOWNGRADES.csv | The eight Major pairs that Qwen3-8B labelled Moderate or Minor after the update |
| RIDI_DDI_v38_WARNING_RADIUS.csv | Exploratory keyword-distance restrictions (50 to 300 characters) for Qwen3-8B |
| RIDI_DDI_commercial_summary.json | Commercial model (GPT-5.4 mini; registration https://osf.io/t9wvh/): recomputed from the raw outputs by `../code/ddi_commercial_recompute.py` |
| RIDI_DDI_cross_model_comparison.csv | The registered, prespecified and post hoc contrasts for both models in one table |

**Reading the results.** The open-weight primary contrast was positive at pair level (8/91 versus 0/91) and inconclusive under a post hoc check that allows for shared drugs. Its repeat (R0) reproduced the reference exactly, because calls were generated one at a time with greedy decoding. The commercial replication was registered after that result was known; its primary criterion was not met (5/76 versus 4/76), and its interval overlaps that of the open-weight model. The correctness-change and label-change contrasts for the commercial model were not listed in the frozen pre-outcome manifest; they are post hoc and descriptive. P values from the two models are not pooled.

**Scope.** Reference classes are DDInter severity classes. The relevance record is a lexical co-mention score, not a relevance judgement. No clinical outcome, deployed alerting system or patient harm was measured.

**Case-level data.** The frozen inputs, raw outputs and per-case labels are not in this folder. They combine DDInter classes with DailyMed label text, are held by the author and can be provided to editors and reviewers on request. `ddi_commercial_recompute.py` runs on those files and reproduces `RIDI_DDI_commercial_summary.json`.

**Sources and licence.** DDInter (Xiong et al., Nucleic Acids Res. 50, D1200–D1207, 2022) is distributed under CC BY-NC-SA 4.0; the pair names and classes in this folder are derived from it and are shared under the same licence. Drug-label text is from DailyMed (US National Library of Medicine).

File names keep the version label of the run that produced them.

## Recovered pre-inference co-mention gate (v43)

The original author-side screening source is now supplied at `../code/pre_inference_bm25_gate_300.py`; it matches the author-workstation file byte for byte (SHA-256 `d4f4b8fe95465cb163130c3a7c5a61c09d3424714a63be94e6e2d55470fbe6e2`). The verified screen ran on 861 pairs: 685 had score equality before all other filters; 173 passed every criterion. The author-workstation frozen full-guard CSV (SHA-256 `1254c2bc6a6ec07ddf845e199b21a893dd46948a885ad3da72c1d42b75bde8e3`) was independently read on 10 November 2026: among 173 selected pairs, **0 failed the exact equality test**. See `PREINFERENCE_EQUALITY_GATE_AUDIT_v43.json` for the source-file hashes and the precise 1e-12 gate.

Caveat: the code references author-owned source material not redistributed in the package. The code and summary establish the selection rule and recheck it against the original frozen ledger; case-level independent reproduction still requires access to the retained source corpus and case-level records. This lexical score is not interchangeable with BEIR relevance grades or a medical relevance judgement.

## Reconciliation of 914 and 861 pairs, and reviewer reproducibility (v44.1)

The source-coverage ledger has 1,655 records for 914 unique drug pairs: 313 Major, 513 Moderate, 35 Minor and 53 Unknown in DDInter. The 53 Unknown pairs are outside the three-class outcome vocabulary and were excluded, which leaves 861 pairs for the retrieval gate. The separate pilot-exclusion file (42 pairs) does not overlap the 914 candidates. Of the 861 screened pairs, 685 had equal co-mention proxy scores and 173 passed all gates (103 Major, 68 Moderate, 2 Minor).

A confidential reviewer archive, retained on the author workstation, holds the source corpus, the coverage ledger, the full pre-inference ledger, the frozen script, the pilot-exclusion list and a SHA-256 manifest. A clean rerun from it reproduced 861/861 screening records and 173/173 selected pairs. This covers pre-inference selection only. It does not cover model inference, clinical severity or patient outcomes. The archive is available to editors and reviewers on request, subject to source licences. Receipt: `AUTHOR_REPRODUCIBILITY_RECEIPT_v44.json`.

| File | SHA-256 |
|---|---|
| evidence_corpus.jsonl | `06f3cc995c5eab205f41d3beed7d92785d15209813e6a3c30c985bb7c85017fb` |
| source_pair_coverage.jsonl | `13738a17ae18ad14749e7218e5042b850b59d7092e1020c62e7be86b492379b4` |
| FULL_GUARD.csv | `1254c2bc6a6ec07ddf845e199b21a893dd46948a885ad3da72c1d42b75bde8e3` |
| pre_inference_bm25_gate_300.py | `d4f4b8fe95465cb163130c3a7c5a61c09d3424714a63be94e6e2d55470fbe6e2` |
| private reviewer kit (ZIP) | `d54c4078f3375bb4365b52bb2d73165979b24792a6959b1bc70b6b8d0e2163cd` |

The Mistral D runtime disclosure is public at https://osf.io/bjuwe/files/osfstorage/6af35b48fb5d24ac130032c3 (1,801 bytes; SHA-256 `c481ce4d5f14437f88753499b2e1a04c0081bf8a410a1f37f37b2f880ade641b`, identical to `../holdout/RIDI_CONFIRM_H3_RUNTIME_DISCLOSURE_20261109.md`).
