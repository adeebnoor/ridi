# RIDI-24 domain-separated capture (post hoc)

Data and code for the domain-separated RIDI-24 rows of Extended Data Table 1, Supplementary Note 7 and Supplementary Table 19 (medicine and finance analysed separately). This analysis was made after the registered RIDI-24 outcomes were known; it is descriptive and does not replace the registered equal-domain primary.

| File | Content |
|---|---|
| `RIDI24_scores_registered.csv` | The frozen RIDI-24 score table: 126,000 rows (model_key, domain, qid, arm, regime, correct). SHA-256 `5531ef7da9328b71f6a046770ec19154eff0adc9f2c8ba02352ad87894ac98a3`. The raw outputs and registration are at https://osf.io/6b8fs/ and 10.17605/OSF.IO/7UZV5 |
| `RIDI24_replay_verification.json` | Earlier computational replay: the score table recomputed from the 27 raw record files is identical to the registered table |
| `analyze_v27_1.py` | The original v27.1 post hoc script. Section 4 (lines 138–179) is the domain-separated analysis; the other sections need historical archives that are not in this package |
| `reproduce_domain_bootstrap.py` | Section 4 of `analyze_v27_1.py` extracted to run on its own; the code is unchanged apart from the line that reads the CSV and the output file name |
| `ridi24_domain_separated_v27_1.json` | Saved output of the original script (values rounded to three decimals) |
| `rerun_receipt_v55.json` | Re-run of 13 November 2026: the regenerated output equals the saved file, with the unrounded interval bounds |

**Run.** From this folder, with Python 3, NumPy and pandas: `python reproduce_domain_bootstrap.py` (about one minute). It writes `ridi24_domain_separated_REGENERATED.json`, which should equal `ridi24_domain_separated_v27_1.json`. The script checks first that the two domains average to the registered equal-domain values (69.957% and 71.108%).

**Method.** Registered 300-case budget per update and domain with fractional ties; two-stage bootstrap (twelve update pairs with replacement within a domain, then one shared draw of the 1,500 questions); 20,000 draws; seed 2026102901.

**Result.** Combined minus difficulty capture: medicine 2.02 points (95% interval −0.25 to 4.23); finance 0.28 (−0.98 to 1.50). The unrounded finance lower bound is −0.98458, so −0.98 is the correct two-decimal value; the −0.985 in the saved JSON is the three-decimal rounding of the same number. In six of the twelve finance updates the budget covers every eligible case, so finance carries little information about policy differences.
