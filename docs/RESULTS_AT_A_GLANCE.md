# Results at a glance

These values summarize the **current Nature manuscript lock, v65.1 (5 September 2026)**, and its locked supporting analyses. v65.1 is a formatting/cross-reference lock; its scientific content is unchanged from the v65 Final Scientific Lock. Historical exploratory analyses remain in repository provenance but are not used to support the present main claims.

| Analysis | Finding | Interpretation boundary |
|---|---|---|
| Preregistered RAG primary, Qwen3-8B/BM25/k=10 | Equal-dataset-weight macro correctness divergence **17.27%** (95% stratified-bootstrap CI **14.60–20.03%**); canonical-output divergence **32.87%** | Estimates behavioral non-equivalence inside an exactly audit-equivalent class; not universal fragility or net harm |
| RAG order-only control | **4.80%** macro correctness divergence with identical membership, RIDI=0 | Shows order/context effects exist; identity substitution is not the only source of variation |
| RAG identity-dose ladder | RIDI `0.446 → 0.655 → 0.953`; correctness divergence `6.97% → 11.07% → 17.27%` | Full substitution clearly exceeds order control; low-dose separation is modest and no clean causal decomposition is claimed |
| SciFact 275 | Same registered audit metrics and fixed positive passage; identity substitution changes `SUPPORTS → REFUTES`, RIDI=0.947; permutation retains `SUPPORTS` | Illustrative case, not a separate inferential endpoint |
| External SciFact 275 regeneration | **Two independent blind external regenerations** reproduced the substantive reference/permutation `SUPPORTS` versus identity-substitution `REFUTES` pattern | Hamdan used a disclosed Q4_K_M llama.cpp/Ollama serving path because the host could not run the pinned bf16 Hugging Face stack; Théophile used the pinned model on a distinct GPU/software stack but his reference began `Verdict: SUPPORTS`, exposing the preregistered strict-parser boundary. These are targeted robustness/reproducibility checks, not replacements for the 800-query endpoint or CODECHECK certification |
| Synthetic sufficient certificate | **33,958/168,000 = 20.2%** certified; zero false certificates | Sufficient condition only; unresolved cases are not predicted unstable |
| EPSS v2→v3 production update | **565/1,000** priorities changed; RIDI **0.722**; adjacent same-version controls changed **0** and **7** | Production turnover, not proof of harm or benefit |
| EPSS external reproduction | Sealed numerical workflow reproduced by **two independent external executors** in separate environments | Independent computational execution, not a CODECHECK certificate |
| EPSS identity control | `eta=0.0001` avoids **14.34%** of turnover while retaining **12/12** delayed KEV positives; `eta=0.001` avoids **40.88%** but retains **10/12** and fails the 95% retention gate | Utility-regret budget must be checked against application outcomes |
| GraphSAGE identity control | At `eta=0.001`, changed slots **31.1→13.3**; **78.8%** avoidable turnover (95% CI **76.0–81.4%**) | Conditional on declared utility and tolerance |
| Text-retrieval identity control | At `k=100`, changed documents **45.8→33.3**; **28.7%** avoidable (95% CI **27.6–29.7%**) | Domain-specific frontier geometry; no universal effect size |
| Registered failures | RxNorm primary criterion failed after cardinality correction; all three registered Open Targets hypotheses unsupported | Failures are retained as claim boundaries, not converted into positive evidence |

## Current figure map

- **Main Fig. 1:** preregistered RAG consequence.
- **Main Fig. 2:** EPSS production update.
- **Main Fig. 3:** exact identity–utility frontier.
- **Extended Data Figs. 1–4:** RAG controls, sufficient certificate, four EPSS transitions, and registered failures respectively.

## Verification status

The community CODECHECK request is registered at issue #208. Formal checking has not begun and **no CODECHECK certificate is claimed**. Independent external executions are reported according to their actual scope: exact numerical reproduction for EPSS and targeted substantive regeneration for SciFact 275.
