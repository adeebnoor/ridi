# Nature main firewall for independent promotion studies

**Locked before any model generation for the two independent studies below.**

This directory is intentionally separated from the Nature-main scientific programme. The two studies may be submitted before the Nature manuscript only if this firewall remains intact.

## Prohibited reuse from Nature main

Neither independent study may use, reanalyse, reproduce as a study result, or promote as a headline result any of the following:

- the allocation-identity theorem or audit-equivalence theorem;
- RIDI or the identity–utility frontier as an estimand, method, analysis or framing device;
- EPSS, CISA KEV, CMS HVBP, CMS Table 16B, or any operational result from the Nature manuscript;
- the Nature RAG panels: Natural Questions, HotpotQA, FEVER or SciFact;
- any Qwen3-8B or Qwen3-32B result reported in the Nature manuscript;
- the Nature frontier-to-downstream SPLADE++ experiment;
- any figure, table, query-level record, bootstrap output, paragraph or primary claim from the Nature manuscript.

The Nature observation that motivated the general research questions may be acknowledged only as internal hypothesis generation. It is not study data for either independent paper.

## Allowed common infrastructure

Generic open-source libraries, GPU hardware, public model families, statistical routines and standard reproducibility practices may be shared. Any code copied from the Nature repository must be generic infrastructure only and must be identified; study-specific Nature analysis code is prohibited.

## Paper A — AJSE

Study ID: `LLM-EXEC-REPRO-AJSE-v1`

Question: whether nominally deterministic greedy LLM inference is invariant to execution configuration when the semantic target prompt and model are unchanged.

New datasets only: MMLU-Pro and GSM8K.

## Paper B — JKSUCIS

Study ID: `LLM-EVAL-RELIABILITY-JKSU-v1`

Question: whether alternative predeclared evaluator/parsing rules applied to the same newly generated model outputs change benchmark scores, model ordering or statistical conclusions.

New datasets only: ARC-Challenge, OpenBookQA, CommonsenseQA and selected BIG-Bench Hard tasks.

## Submission disclosure

If either independent paper is submitted or published before Nature main, the Nature cover letter must disclose it as a related manuscript and explicitly state the firewall: no shared Nature datasets, primary results, theorem, RIDI/frontier analysis, EPSS/CMS evidence, figures or tables.

Any future change that would breach this firewall requires stopping the independent submission plan rather than weakening Nature main.
