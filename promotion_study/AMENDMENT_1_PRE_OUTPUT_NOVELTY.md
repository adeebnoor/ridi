# AMENDMENT 1 — PRE-OUTPUT NOVELTY REFINEMENT

Date: 19 September 2026
Study: EVAL-RANK-JKSUCIS-v1
Timing: **before any model endpoint generation for this study.**

## Why this amendment exists

A pre-execution literature audit identified prior work showing that answer extraction can fail and that benchmark implementations can alter scores or rankings, including xFinder (2024) and public analyses of differing MMLU implementations.

A paper whose main claim is only "two parsers disagree" or "E1 versus E2 can reverse a ranking" would therefore be insufficiently differentiated.

## New formal primary estimand: evaluator-specification robustness

For each benchmark b, model pair (i,j), and frozen evaluator e in {E1,...,E5}, define:

d_e(i,j,b) = accuracy_e(i,b) - accuracy_e(j,b).

Define the **evaluator-specification difference interval**

I(i,j,b) = [ min_e d_e(i,j,b), max_e d_e(i,j,b) ].

Classification:
- robust i>j if the lower endpoint is >0;
- robust j>i if the upper endpoint is <0;
- evaluator-specification-sensitive if the interval contains 0;
- strict ranking reversal if the interval contains both a negative and a positive observed difference;
- a zero/tie can make an ordering non-robust but is not called a reversal by itself.

For each model m and benchmark b, also define **evaluator score width**:
W(m,b) = max_e accuracy_e(m,b) - min_e accuracy_e(m,b).

## Revised primary endpoints

1. Proportion of the 12 predeclared benchmark × model-pair comparisons whose evaluator-specification difference interval contains 0 (ordering not robust to the frozen evaluator specification set).
2. Strict ranking-reversal count/rate across the same 12 comparisons.

The original E1-versus-E2 reversal and item-level decision-disagreement endpoints remain mandatory reported special cases/secondary endpoints.

## Statistical reporting

For every evaluator-specific pairwise accuracy difference, retain the locked 100,000 item-bootstrap interval. Bootstrap resamples will also report the frequency with which the five-evaluator difference interval contains 0. This frequency is uncertainty support, not a posterior probability.

## What does not change

No model, benchmark, selected item, raw-generation prompt, model revision, evaluator implementation, generation setting, sample hash, Nature firewall or anti-selection rule changes.

The new estimand treats evaluator choice as a finite predeclared measurement-specification set; it does not claim that E1-E5 exhaust every possible evaluator.
