# NOVELTY AUDIT — JKSUCIS STUDY

Audit date: 19 September 2026
Timing: before model endpoint generation.

## Closest work found

1. Yu et al. **xFinder: Robust and Pinpoint Answer Extraction for Large Language Models** (arXiv:2405.11874, 2024).
   - Shows regex answer-extraction errors can compromise LLM evaluation and proposes a learned extractor.
   - Consequence: do not claim discovery that answer extraction can be wrong.

2. Hugging Face Open LLM Leaderboard analysis of alternative MMLU implementations.
   - Publicly demonstrates that benchmark implementation choices can yield different scores and model ordering.
   - Consequence: do not make "implementations can change rankings" the sole novelty claim.

3. Benchmark^2 (2026) and Train-before-Test (2025) study model-ranking quality/consistency across benchmarks.
   - Consequence: distinguish evaluator-specification robustness from cross-benchmark ranking consistency.

4. Recent work on evaluator/rubric or calibration sensitivity can also yield ranking changes.
   - Consequence: the paper is specifically about deterministic answer-extraction specifications applied to the **same frozen raw outputs**, not LLM judges, calibration metrics or benchmark selection.

## Remaining target gap

The amended contribution treats the evaluator as a finite measurement specification set.

For each benchmark/model pair, compute the five evaluator-specific accuracy differences and their interval:
I = [min_e d_e, max_e d_e].

A model ordering is evaluator-robust only if this interval stays strictly above or below zero. An interval containing zero marks specification sensitivity; observed differences of both signs constitute strict reversal.

This separates:
- score width for a single model;
- ordering robustness for a model pair;
- strict ranking reversal as a stronger subtype;
- item-level parser disagreement as a mechanistic diagnostic.

## Safe novelty language

Preferred:
- "We formalize evaluator-specification robustness over a predeclared finite parser set..."
- "We hold raw generations fixed and quantify whether pairwise model ordering survives plausible deterministic extraction rules..."

Avoid:
- "first paper showing parsers matter"
- "first ranking reversals in LLM evaluation"
- "our evaluator is universally correct"

## Submission-time novelty check

Repeat the literature search immediately before submission.
