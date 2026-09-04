# Numerical provenance

This page prevents headline values from drifting across the manuscript, Source Data, preregistered outputs and public repository. The current manuscript is **“Identical audits can yield different AI decisions.”** The current public manuscript lock is **v65.1 (formatting lock), 5 September 2026**. Its scientific content is unchanged from the v65 Final Scientific Lock; v65.1 corrects figure and Extended Data cross-references only.

## Preregistered RAG — decisive prospective result

Protocol: `RIDI-RAG-NATURE-v2-PROSPECTIVE`  
Registration: https://osf.io/txwdv/

| Endpoint | Preregistered result |
|---|---:|
| Frozen queries | 800 |
| Equal-dataset-weight macro canonical-output change | 32.87% |
| 95% stratified-bootstrap CI | 29.77–36.00% |
| Equal-dataset-weight macro benchmark-defined correctness divergence | 17.27% |
| 95% stratified-bootstrap CI | 14.60–20.03% |
| Order-only macro correctness divergence | 4.80% |
| Audit-equivalence checks | 24,500 real-data + 72,000 synthetic; 0 mismatches |

Registered identity-dose series at k=10:
- ~25% substitution: realized RIDI 0.446; correctness divergence 6.97%.
- ~50% substitution: realized RIDI 0.655; correctness divergence 11.07%.
- ~100% substitution: realized RIDI 0.953; correctness divergence 17.27%.

Capacity series:
- k=5: 12.90%
- k=10: 17.27%
- k=20: 13.23%

No monotonic capacity claim is made.

## SciFact 275 — illustrative preregistered case

- Gold label: `SUPPORTS`.
- Positive passage ID `4961038` remains fixed at rank 1.
- Relevance-grade vector: `[1,0,0,0,0,0,0,0,0,0]`.
- precision@10 = 0.10
- recall@10 = 0.3333333333
- nDCG@10 = 0.4692787260
- MRR@10 = 1.0
- MAP@10 = 0.3333333333
- Nine metric-zero identities are replaced in the random identity-substitution context.
- RIDI = 0.9473684211.
- Registered author run: reference `SUPPORTS`; order-only permutation `SUPPORTS`; identity substitution `REFUTES`.

### Independent blind regenerations

**Mohammed Hamdan:** audit checks were exactly equivalent with no mismatches; reference `SUPPORTS`; identity control `SUPPORTS` and byte-identical to reference; order-only permutation `SUPPORTS`; random identity substitution `REFUTES`. His disclosed hardware limitation required a Q4_K_M `qwen3:8b` llama.cpp/Ollama serving path rather than the pinned bf16 Hugging Face runtime; frozen inputs and prompt conditioning were retained. This is a cross-serving/quantization robustness regeneration, not an exact backend reproduction.

Hamdan output SHA-256:
- `scifact275_blind_output.json`: `1175da3aa65e7a5cd57eb82992904ec69e3e01038cb7b5cc8c65b3842743d19d`
- `scifact275_prepare_only.json`: `d31257c34080206e9cf37c040e2af2326d33660554a237bbd4abeb7ecd200913`

**Théophile Ossard:** separately reproduced the substantive reference/permutation `SUPPORTS` versus identity-substitution `REFUTES` pattern on a distinct GPU/software stack. His reference output began `Verdict: SUPPORTS`, which the preregistered strict first-token parser labelled unparseable. This parser boundary is reported rather than silently normalized.

These targeted runs are robustness/reproducibility evidence for the SciFact 275 phenomenon, not replacements for the registered 800-query aggregate endpoint and not CODECHECK certification.

## EPSS deterministic operational stress test

Protocol: `RIDI-CYBER-NATURAL-UPDATE-v1`.

- universe: 195,886 CVEs.
- v2→v3 top-1,000 changed slots: 565; RIDI ≈ 0.722.
- adjacent same-version top-1,000 controls: 0 and 7 changed slots.
- across four production transitions, 565–709 top-1,000 identities changed.
- delayed KEV evidence is sparse and cutoff-dependent; no uniform-benefit claim is made.
- exact identity control at eta=0.0001 avoids 14.34% of turnover while retaining 12/12 delayed KEV positives in the primary top-1,000 window.
- eta=0.001 avoids 40.88% but retains 10/12 and fails the registered 95% retention gate.

The sealed deterministic numerical workflow has been reproduced by **two independent external executors** in separate environments. These are independent computational executions, not CODECHECK certification.

## Current figure map

The v65.1 manuscript contains **three Main Figures** and **four Extended Data Figures**:

- **Main Fig. 1:** preregistered RAG consequence.
- **Main Fig. 2:** EPSS production update.
- **Main Fig. 3:** exact identity–utility frontier.
- **Extended Data Fig. 1:** RAG structural ambiguity / capacity / order controls.
- **Extended Data Fig. 2:** sufficient stability certificate.
- **Extended Data Fig. 3:** four EPSS production transitions.
- **Extended Data Fig. 4:** registered failures (RxNorm / Open Targets).

The v65.1 formatting lock was created specifically to re-audit and correct all figure and Extended Data cross-references without altering scientific content.

## Constructive solution — Main Fig. 3

The current manuscript places the exact identity–utility frontier in **Main Fig. 3**. It computes the minimum membership change compatible with a declared updated-score utility-regret budget using stored scores; no retraining is required.

- GraphSAGE at eta=0.001: mean changed slots 31.1→13.3; 78.8% avoidable turnover, 95% query-bootstrap interval 76.0–81.4%.
- Text retrieval at k=100: mean changed documents 45.8→33.3; 28.7% avoidable, 95% interval 27.6–29.7%; small label-based nDCG/recall changes.
- EPSS at eta=0.0001: 14.34% avoidable turnover while retaining all 12 delayed KEV positives in the primary top-1,000 window.

These are constructive control results, not a claim that identity preservation is always beneficial.

## Sufficient stability certificate

Synthetic margin-certificate sweep:
- 33,958 certified cases among 168,000 = 20.2%.
- zero false certificates.
- the remaining 79.8% are unresolved by this sufficient condition, not predicted unstable.

## Registered failures and archived exploratory analyses

- RxNorm failed its registered primary criterion; turnover largely collapsed after the post-registration cardinality correction.
- Open Targets: all three registered hypotheses were unsupported.
- Earlier exploratory COMPAS and crude CVE-year analyses remain archived but do not support the current main manuscript claims.

## Current submission Source Data

Current science-lock workbook: `RIDI_Nature_Source_Data_v65_FINAL_SCIENCE_LOCK.xlsx`, covering Main Figs. 1–3 and Extended Data Figs. 1–4. The v65.1 article-only formatting correction does not change the Source Data workbook.

## Software release

`ridi-audit==1.1.1` is published at https://pypi.org/project/ridi-audit/ using GitHub OIDC Trusted Publishing with PyPI/Sigstore attestations and a successful clean reinstall from the public PyPI index.

SHA-256:
- wheel: `b91dcf6cf227a3a579d88318029c02d78e378d16510a2223d17223acbf7bb6f7`
- sdist: `a2af6f98171cb5b5a307911eeca2824dd401e014d595c6af69c94ddcf3d5440e`

Software release is distinct from manuscript peer review and from independent scientific verification.

## CODECHECK status

Community request: https://github.com/codecheckers/register/issues/208  
Status as of **5 September 2026**: request registered; formal checking has not begun; **no certificate is claimed**. The CODECHECK team invited renewed contact when a public preprint exists or when the manuscript is undergoing journal review.

## Interpretation boundary

Allocation identity measures who or what receives finite action. It does not by itself establish harm, benefit, individual fairness, causal fairness or model superiority. RAG qrel-zero passages are therefore described as **metric-zero**, not semantically irrelevant; correctness divergences are bidirectional; KEV addition is delayed federal curation rather than exploitation onset or complete ground truth.
