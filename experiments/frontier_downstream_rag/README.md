# Frontier → downstream RAG extension

This directory contains the public protocol lock and deterministic analysis engine for the next Nature-strengthening experiment.

**Protocol:** `RIDI-NATURE-FRONTIER-DOWNSTREAM-v1`

The experiment is designed to answer a question not resolved by the current manuscript: after an updated retriever changes the evidence set, can the exact identity–utility frontier retain substantially more baseline evidence while remaining inside a declared updated-rank-utility budget, and what happens to downstream LLM answers?

## State

The protocol and analysis engine are public before endpoint execution. No endpoint result is claimed in this directory until frozen BM25/SPLADE++ candidate files and the pinned Qwen3-8B generations have been produced under the protocol.

## Primary design

- 400 frozen queries: 100 each NQ, HotpotQA, FEVER, SciFact
- baseline BM25 vs updated SPLADE++
- k=10 primary; k={5,20} sensitivity
- eta=0.001 primary; eta=0.0001 secondary
- four generator states: reference, updated-unconstrained, frontier 0.01%, frontier 0.1%
- same pinned Qwen3-8B generator/scoring family as the registered RAG study
- paired downstream correctness and answer disagreement
- all results reported regardless of direction

See `PROTOCOL_LOCK.md` for the complete failure rules and interpretation boundary.
