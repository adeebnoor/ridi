# RIDI repository/product lock — v65.1 final formatting state

Date: 2026-09-05

This note records the current public repository state after the v65 Final Scientific Lock and the v65.1 formatting/cross-reference audit.

## Public-facing scientific state

- Manuscript title: **Identical audits can yield different AI decisions**.
- Current article lock: **v65.1**, a formatting-only lock; scientific content is unchanged from v65.
- Main narrative is aligned to three displays: preregistered RAG consequence, EPSS production update, exact identity–utility frontier.
- Current figure architecture is exactly **Main Figs. 1–3** and **Extended Data Figs. 1–4**.
- The sealed EPSS numerical workflow was independently reproduced by **two external executors** in separate environments.
- SciFact query 275 was independently regenerated **twice, blind**, with the substantive reference/permutation `SUPPORTS` versus audit-equivalent identity-substitution `REFUTES` pattern reproduced in both runs.
- Mohammed Hamdan's run is explicitly bounded as a cross-serving/quantization robustness regeneration because hardware limitations required a disclosed Q4_K_M llama.cpp/Ollama serving path rather than the frozen bf16 Hugging Face runtime.
- Théophile Ossard's run used the pinned Qwen3-8B revision on a distinct GPU/software stack and exposed a strict first-token parser boundary through a `Verdict: SUPPORTS` prefix; the discrepancy is retained transparently.
- Community CODECHECK request #208 is registered; formal checking has not begun and no certificate is claimed.
- Public software release: **`ridi-audit==1.1.1`**, published through PyPI Trusted Publishing with attestations and verified by reinstalling from the public PyPI index.

## Product goals

The public repository presents, in order:

1. the scientific object (allocation identity),
2. the decisive preregistered result,
3. the production stress test,
4. the constructive identity–utility frontier,
5. a one-entry-point Python API and CLI,
6. transparent reproducibility status and scientific boundaries.

Historical submission/version records are provenance, not the primary researcher experience.
