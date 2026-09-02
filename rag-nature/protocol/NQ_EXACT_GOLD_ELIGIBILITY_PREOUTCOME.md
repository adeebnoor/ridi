# Pre-outcome NQ exact-gold eligibility decision

**Decision time:** before panel selection, before OSF registration, and before any real language-model generation.

## Why this amendment is necessary

BEIR-NQ is a retrieval benchmark derived from the original Natural Questions development data after BEIR-specific filtering. It contains 3,452 test queries but does not provide answer strings as part of the BEIR retrieval release. Google NQ-Open original-dev provides official short-answer aliases for 3,610 questions, but its query population is not identical to the BEIR-NQ population.

A direct deterministic comparison established that not every BEIR-NQ query has an exact NQ-Open short-answer record. Therefore, treating NQ-Open as if it were the answer key for all BEIR-NQ would be incorrect.

## Prospective definition used in this study

The QA cell is defined as the **NQ-Open–aligned subset of BEIR-NQ**:

1. start with the frozen BEIR-NQ test topics;
2. normalize only Unicode/string whitespace and case for matching;
3. retain a BEIR query only if it has a **unique exact normalized-question match** in the frozen Google NQ-Open original-dev source;
4. require a non-empty official answer list;
5. apply the preregistered retrieval-depth, document-materialization, and substitutability gates;
6. choose the panel deterministically from the remaining eligible IDs before any model generation.

The study will not use fuzzy matching, semantic similarity matching, manually supplied answers, LLM-generated answers, or post-generation adjudication to recover unmatched NQ queries.

## Interpretation

Results from this cell must be described as applying to the **NQ-Open–aligned BEIR-NQ subset**, not to all 3,452 BEIR-NQ test queries.

The purpose of this cell is single-hop factual short-answer QA transport. HotpotQA supplies a separate multi-hop QA transport test, while FEVER and SciFact supply fact-verification transport tests.

## Retention rule

The NQ cell is retained only if the exact-gold subset still supports the preregistered universal-panel target after all technical and substitutability gates. If it does not, the NQ cell is removed or replaced **before OSF registration**; its target size will not be reduced after observing any language-model output.

## Provenance rule

The frozen registration bundle must include:

- the exact Google NQ-Open source revision and SHA-256;
- the BEIR topic/qrels URLs and SHA-256 values;
- the exact matched and unmatched query IDs;
- the deterministic pre-panel exclusion report;
- the final panel IDs and panel hash.

This document itself is part of the pre-registration manifest so the eligibility decision is auditable as pre-outcome.
