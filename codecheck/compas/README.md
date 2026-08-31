# CODECHECK submission — protected-attribute audit-equivalence (COMPAS)

**Manuscript:** *Performance and group-fairness audits leave AI allocations unidentified*  
**Author:** Adeeb Noor, King Abdulaziz University · ORCID 0000-0002-8251-1853  
**What is checked:** **Main Fig. 2** and the protected-attribute equivalence paragraph in the main text.

## In one line

```bash
python3 prepare_inputs.py && python3 layered_audit.py && python3 verify_layers.py && python3 figure_compas.py && sha256sum -c MANIFEST.sha256
```

Runtime after dependencies are installed is under one minute on a laptop. Network access is used only once by `prepare_inputs.py` to fetch the public ProPublica CSV at a pinned Git commit. The source human-data file is **not redistributed** by this package.

## What the code does

An audit that reports only per-cell counts — how many selected people fall in each combination of outcome, protected group and risk band — cannot distinguish any two selections with the same counts. This package computes, on the public ProPublica COMPAS two-year cohort, how large that indistinguishable class is and how far the composition of the supervised cohort can move inside it, for four cumulative audit definitions.

`verify_layers.py` is the falsification test: it explicitly constructs all 32 extremal allocations and checks that every audited statistic is identical to the deployed allocation. If any statistic differs, the claim is wrong and the script reports the mismatch.

## Requirements

Python ≥3.9 with pandas, numpy and matplotlib.

```bash
python3 -m pip install -r requirements.txt
```

## Expected values

`VALUE_KEY.json` holds the canonical values. A successful check reproduces them exactly.

| Quantity | Expected |
|---|---|
| Cohort size | 6,172 |
| Two-year positives | 2,809 (45.5%) |
| African-American | 3,175 (51.4%) · Female 1,175 (19.0%) |
| Deployed top-1,000 | precision@1,000 = 0.745, recall = 0.2652, African-American share 74.7% |
| Layer *outcome* | log10 class 1094.4; mean age 21.75–50.89 |
| Layer *+ race* | log10 class 1048.2; mean age 21.88–48.63; female share 0.0–63.7% |
| Layer *+ risk decile* | log10 class 112.7; mean age 27.81–30.46; female share 9.5–15.1% |
| Layer *+ sex* | log10 class 109.2; mean age 27.86–30.45; female share fixed at 13.1% |
| Verification | 0 mismatches across 32 extremal constructions |

## Data provenance and privacy

`prepare_inputs.py` fetches `compas-scores-two-years.csv` from ProPublica's public `compas-analysis` repository at commit `bafff5da3f2e45eca6c2d5055faad269defd135a`. It applies ProPublica's published filters and retains only `id, sex, age, race, decile_score, priors_count, two_year_recid`. Direct identifiers in the upstream file are never used by the analysis and are not included in this repository. The derived seven-column file must hash to `8fe0a122e7bd08d79b217d92bab1d111c0b3192dad2f11832d49a6591a0a5d6e`.

## Scope and limits

- The analysis is retrospective, not prospective.
- The reported ranges are constructive extrema: bounds on what the audit cannot exclude, not predictions about a particular alternative model.
- The cohort is the public research cohort, not an operational pretrial population.
- COMPAS is used as a public benchmark with protected attributes, a deployed score and an observed outcome; no claim is made about any vendor's current product.

## License

The analysis code is MIT licensed; documentation/results are CC BY 4.0. The upstream ProPublica dataset is fetched from its original public repository and is not redistributed here.
