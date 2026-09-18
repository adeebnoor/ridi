# Public systems change what they prioritise without recording it

**Adeeb Noor**  
Department of Information Technology, Faculty of Computing and Information Technology, King Abdulaziz University, Jeddah, Saudi Arabia  
ORCID: 0000-0002-8251-1853

> **Status — 18 September 2026:** public synopsis of the current frontier-led working manuscript. It is not peer reviewed, accepted or published. The public repository records the evidence and software; the manuscript remains subject to further robustness work and author finalization.

## Central contribution

Ranking systems act on finite selections: passages a model reads, vulnerabilities a security team reviews, documents in a shortlist, or biomedical relationships proposed for follow-up. When a system is updated, aggregate metrics do not tell us how much the selected membership changed or how much of that churn was actually required by the updated scoring objective.

This work separates those questions:

1. **Measurement:** record selected-set overlap, changed slots and RIDI (Jaccard distance on the selected identities).
2. **Control:** compute the **identity–utility frontier**, the exact minimum replacement count compatible with a declared rank-utility budget.

For a baseline top-k set and updated scores, the utility-maximizing selection with exactly `j` outsiders retains the highest-ranked incumbents and adds the highest-ranked outsiders. Sorted prefix sums evaluate every `j` in `O(n log n)` time, yielding the full frontier without retraining or access to training data.

An avoidable-turnover fraction is meaningful only relative to the stated objective and tolerance.

## Why exact audit equality is not enough

The supporting prospective RAG experiment was publicly preregistered before any registered language-model outcome was generated.

- **800 frozen queries:** Natural Questions 250, HotpotQA 250, FEVER 150, SciFact 150.
- Positive-qrel passages remained at the exact same ranks.
- Precision@k, recall@k, nDCG@k, MRR@k, MAP@k and the complete relevance-grade-by-position vector were identical by construction.
- Primary equal-dataset-weight benchmark-defined correctness change: **17.27%** (95% stratified-bootstrap interval **14.60–20.03%**).
- Normalized answer-text change: **32.87%**.
- Directional counts: **60 correct→incorrect**, **74 incorrect→correct**.
- Order-only control with identical membership: **4.80%**.
- No primary query had uniquely identified passage membership; the median number of compatible passage sets exceeded **10¹²**.

The novelty claim is deliberately narrow. Prior work already shows that irrelevant/distracting context and passage position can change language-model answers and that conventional retrieval measures correlate imperfectly with downstream accuracy. Here the complete assessed grade sequence is held exactly fixed, every registered retrieval metric is numerically identical, and the remaining membership ambiguity is quantified directly.

## Parser sensitivity

A post hoc formatting analysis rescored all 300 FEVER/SciFact primary queries under two declared prefix-tolerant rules. Both rules returned the same labels:

- registered classification correctness changes: **58 / 300** (two-dataset mean **19.33%**)
- prefix-tolerant result: **53 changes** — 52 persisted, six resolved, one new change appeared (two-dataset mean **17.67%**)

This classification-only sensitivity is **not** the four-dataset primary endpoint and is not human semantic adjudication. The registered result remains unchanged. A separate post hoc 512-token generation-length sensitivity reran the same frozen 800-query Qwen3-8B/BM25/k=10 reference-versus-random comparison and reproduced **all 134 registered correctness-change indicators with zero query-level discordance**; the equal-dataset-weight macro remained **17.27%**.

## Illustrative SciFact case

SciFact claim 275 retains its positive passage at rank 1 and the relevance-grade vector:

```text
[1,0,0,0,0,0,0,0,0,0]
```

with identical registered metrics:

```text
precision@10 = 0.10
recall@10    = 0.3333
nDCG@10      = 0.4693
MRR@10       = 1.00
MAP@10       = 0.3333
```

Replacing nine metric-zero passages in the primary random-replacement condition changes the model verdict `SUPPORTS → REFUTES` while the audit remains identical. The same-query permutation control retains the original membership and remains `SUPPORTS`.

### Targeted external regeneration

Two external executors returned blind regenerations of this example.

- **Mohammed Hamdan:** hardware limits required a disclosed Q4_K_M llama.cpp/Ollama serving path. The reference/identity/permutation outputs were `SUPPORTS` and the random-replacement output was `REFUTES`, reproducing a strict-scored correctness change.
- **Théophile Ossard:** used the pinned Qwen3-8B revision in a distinct GPU/software environment. His reference began `Verdict: SUPPORTS`, which the frozen strict first-token parser labelled `UNPARSEABLE`; the random-replacement output was `REFUTES`. Thus his run reproduced the substantive support-to-refutation contrast, but not a correctness-status change under the registered parser.

These are targeted robustness checks, not independent replication of the aggregate 800-query endpoint.

## Production application: EPSS

For the EPSS v2→v3 update, after the documented outcome-window exclusions:

- candidate universe: **195,886** vulnerabilities
- top-1,000 changed slots: **565** (`RIDI=0.722`)
- adjacent same-version controls: **0** and **7** changes
- later KEV hits: **8 → 12**
- full-universe AUROC: **0.665 → 0.610**

The identity–utility frontier shows:

- `eta=0.0001` (0.01% relative rank-utility loss): **14.34%** of replacements avoided (95% descriptive changed-slot bootstrap interval **11.50–17.35%**), **12/12** later KEV hits retained
- `eta=0.001` (0.1%): **40.88%** avoided (95% descriptive changed-slot bootstrap interval **36.81–44.96%**), **10/12** retained

With only twelve delayed outcome events at the primary cutoff, these retrospective counts do not establish a consistent benefit or causal effect. A post hoc extension using the same pinned inputs reproduced the 365-day **8→12** headline first, then yielded **20→21** at two years and **32→33** at three years. Full-universe AUROC remained lower for v3 at both longer windows (**0.683 vs 0.715** at two years; **0.695 vs 0.720** at three years), as did average precision. The primary window remains 365 days.

## Production application: CMS Hospital Value-Based Purchasing

Two locked annual Total Performance Score comparisons changed **195/500** selected hospitals in FY2024→FY2025 and **202/500** in FY2025→FY2026. At a **0.1%** updated rank-utility budget, the exact identity–utility frontier required **174** and **181** replacements, respectively: **10.77%** avoidable turnover (95% descriptive changed-slot bootstrap interval **6.67–15.38%**) and **10.40%** (**6.44–14.85%**).

Because the same-fiscal-year archive files originally labelled as controls were later shown to be byte-identical republications, they are retained only as provenance checks. A separate outcome linkage to actual IPPS Table 16B Hospital VBP payment adjustment factors was publicly preregistered at **OSF 9guc5 before outcome-file access**.

- Exactly unchanged published TPS: factor changed in **14/15** FY2024→FY2025 matched transitions and **5/5** FY2025→FY2026, or **19/20 pooled**.
- Frontier-displaceable identities: **84** transition identities total, mean absolute factor change **0.006525**.
- Stable comparison transitions: **4,642**, mean absolute factor change **0.005505**.
- Transition-stratified mean difference: **0.001020**, 100,000-resample 95% interval **0.000077–0.002008**, seed 20260916.
- Seven FY2026 TPS-only CCNs were unmatched to Table 16B and remained unimputed.

The linkage is descriptive. It does not estimate dollar revenue, attribute factor movement causally to RIDI or score turnover, assess patient outcomes or hospital quality, label policy as harmful/beneficial, or treat top-500 as a statutory CMS threshold.

Before acquiring any pre-COVID hospital-level TPS values, official CMS programme/final-rule records were screened for consecutive FY2017–FY2021 pairs under a strict like-for-like rule requiring the same measure set, domain structure/weights and material performance-period/scoring definitions. **No pair qualified** under that strict methodology screen. A separate historical extension was then **publicly locked before historical hospital-level TPS acquisition** as `RIDI-CMS-HVBP-HISTORICAL-EXTENSION-v1` (protocol/code commit `5f151cbe3e2c2dfbe06fdb901289c32314472eb4`). The lock prespecified the official CMS archive endpoint, deterministic fiscal-year snapshot rule, `k={100,500,1000}`, `eta={0,0.0001,0.001}`, tie breaking, all-ties sensitivity and failure rules. Its first automated execution (GitHub Actions run `35339908821`) recovered FY2021 TPS but **no adjacent pre-pause TPS pair** under the locked source rule: FY2017 and FY2018 had no theme-level archive snapshot in the prespecified fiscal-year windows, and the selected FY2019/FY2020 archives contained no `hvbp_tps.csv`. The protocol forbade switching archive dates or substitute sources after execution, so no historical turnover estimate was generated. The execution record/results are archived at commit `2d69ba1aa063da229a10a6dc9c7d241cc7ee7a12` (artifact SHA-256 `26ddf7a0feb32d5fb3ccc871b3c298a7a97dc7d9405683591707a2106fe19072`). This is a timestamped public outcome-naive lock, **not** an OSF preregistration and not a retroactive registration of the original FY2024–FY2026 TPS/frontier analysis. CMS also did not calculate a TPS for FY2022 or FY2023 after measure suppressions/pauses, and Table 16B was not necessary in either year. The manuscript therefore treats the two analysed post-pause transitions as finite descriptive observations, not a long-run annual turnover rate.

## Prospective frontier-to-downstream control

A separate public lock tested the frontier as an end-to-end intervention after a real retriever update. Before Qwen3-8B generation, 400 queries (100 each Natural Questions, HotpotQA, FEVER and SciFact) were frozen from a **common-retrievable** candidate universe: the intersection of BM25 and SPLADE++ top-1,000 candidates. The primary cell was `k=10, eta=0.001`.

- Mean changed slots: **5.7275 → 5.3850**, absolute reduction **0.3425** (100,000-draw stratified-bootstrap 95% interval **0.2950–0.3925**).
- Mean query-level avoidable-turnover fraction among changed queries: **7.00%** (95% interval **5.84–8.25%**).
- Benchmark accuracy: **57.25% → 57.00%**; paired difference **−0.25 percentage points** (95% interval **−1.25 to +0.75**).
- Correctness status changed in **5/400 (1.25%)** queries; normalized answer text changed in **11/400 (2.75%)**.
- Directional correctness changes were **2 improved / 3 worsened** after identity control.

The result is deliberately not presented as non-inferiority or downstream benefit. It shows the realized finite-panel trade-off under a tight rank-utility budget. The extension was publicly locked before generation, but it is **not an OSF preregistration**. Protocol lock: `383830dbd7c67f1898e88422bab8a49e5e91e9de`; frozen panel: `f98be71b4402d95a3337dac78f272c3aa55cbd62`; exact per-query replay archive: `d2162d26754917d6b635d23d7d80163d7a00ef2d`; locked aggregate: `a13864d63198fce111651090dcc0924dce644a01`.

A compact recovery that changed tensor/batch composition produced a few different greedy outputs and was excluded. An exact replay preserving all twelve original states per query, their order and batches of four reproduced the original aggregate summaries and raw-output SHA-256 values. The executed path is therefore reported explicitly rather than claiming batch-shape-independent determinism.

## Generality of the frontier

At the locked 0.1% rank-utility budget:

- **GraphSAGE / RTX-KG2pre:** mean changed slots **31.1 → 13.3**; mean avoidable turnover **78.8%** (95% query-bootstrap interval **76.0–81.4%**); mean RIDI **0.116 → 0.043**.
- **20 Newsgroups retrieval, k=100:** mean changed documents **45.8 → 33.3**; mean avoidable turnover **28.7%** (95% interval **27.6–29.7%**) with small label-based nDCG/recall changes.

The differing avoidable fractions are substantive: the frontier measures how much churn the score landscape requires rather than assuming a universal tolerance.

## Exploratory boundaries

Drug-interaction catalogue, human-study, NHANES/MIMIC medication-context and pair-event annotation analyses are retained as exploratory secondary work. In the severity-matched catalogue construction, the severity sequence is identical by design while selected identity can change. In the TWOSIDES-linked NHANES subset, the **primary complete-linkage result is 16/32 changed annotation profiles**; the strict-boundary sensitivity is **15/31**.

These are database/selection annotations, not observed patient adverse events, delivered alerts or evidence of clinical interchangeability. The supplied TWOSIDES derivative has unresolved release identity and p-value adjustment provenance, so it is not described as independent clinical validation.

Registered RxNorm and Open Targets failures remain visible as boundaries of the evidence.

## Verification status

- The sealed EPSS workflow was reproduced by **two external executors** in separate environments.
- Targeted SciFact 275 runs are described above with their actual differences.
- Author-side replays and deterministic computational checks are separate from external execution.
- **No formal CODECHECK certificate has been issued.** Community register issue #208 was closed with an invitation to return once a public preprint is available or the manuscript is under journal review.

## Current figure architecture

- **Main Fig. 1:** exact retrieval-evaluation equality and answer changes.
- **Main Fig. 2:** EPSS production update and frontier/outcome trade-off.
- **Main Fig. 3:** identity–utility frontier across applications.
- **Extended Data Fig. 1:** passage-set ambiguity, capacity and order controls.
- **Extended Data Fig. 2:** sufficient stability certificate.
- **Extended Data Fig. 3:** four EPSS version transitions.
- **Extended Data Fig. 4:** registered failures (RxNorm / Open Targets).
- **Extended Data Fig. 5:** exploratory drug-interaction catalogue replay.

## Reproducibility

- **RAG preregistration:** https://osf.io/txwdv/
- **CMS Table 16B linkage preregistration:** https://osf.io/9guc5/
- **CMS historical public lock:** `experiments/cms_historical/PROTOCOL_LOCK.md` at commit `5f151cbe3e2c2dfbe06fdb901289c32314472eb4`
- **CMS historical first-run record/results:** `experiments/cms_historical/` at commit `2d69ba1aa063da229a10a6dc9c7d241cc7ee7a12`
- **Repository:** https://github.com/adeebnoor/ridi
- **PyPI:** https://pypi.org/project/ridi-audit/
- **CODECHECK register issue #208:** https://github.com/codecheckers/register/issues/208

## Scientific boundaries

RIDI measures and controls selected membership under a declared objective. It does not by itself establish correctness, fairness, harm, benefit, clinical utility or model superiority. Correctness changes in the RAG study are bidirectional. Benchmark qrels are incomplete, so zero-grade passages are called **metric-zero**, not semantically irrelevant. The registered RAG generators are open-weight 7–8B models under a fixed 128-token regime; the completed 512-token rerun is post hoc and does not replace that registered regime. A larger-model scale sensitivity and independent aggregate 800-query execution remain pending and are not claimed. EPSS outcome evidence is sparse and retrospective. A sufficiently identity-aware audit can remove the membership ambiguity by recording selected identities directly.

## Use or test the method

- [Install `ridi-audit`](https://pypi.org/project/ridi-audit/)
- [60-second notebook](https://colab.research.google.com/github/adeebnoor/ridi/blob/main/notebooks/RIDI_60_Second_Experiment.ipynb)
- [Quick Start](../docs/QUICKSTART.md)
- [Python API](../docs/API.md)
- [Use cases](../docs/USE_CASES.md)
- [Reporting checklist](../docs/REPORTING_CHECKLIST.md)
- [Repository home](../README.md)
