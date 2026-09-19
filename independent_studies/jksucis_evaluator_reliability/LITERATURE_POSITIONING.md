# Literature positioning — JKSUCIS evaluator reliability

This note is for manuscript positioning and was drafted while the locked experiment was still running. It does not alter the protocol.

## Closest work

1. Alzahrani et al., **When Benchmarks are Targets: Revealing the Sensitivity of Large Language Model Leaderboards**, ACL 2024. The study shows that benchmark perturbations such as answer-choice order and answer-selection method can change leaderboard rankings by multiple positions.
2. Hua et al., **Flaw or Artifact? Rethinking Prompt Sensitivity in Evaluating LLMs**, EMNLP 2025. The study shows that some apparent prompt sensitivity is induced by heuristic evaluation and rigid answer matching, and compares heuristic scoring with LLM-as-a-judge.
3. Kostić et al., **Same Meaning, Different Scores: Lexical and Syntactic Sensitivity in LLM Evaluation**, LREC 2026. The study holds meaning approximately constant while perturbing lexical/syntactic form and observes changes in scores and rankings.

## Narrow contribution of the present study

The present study isolates the **evaluator software** after model inference.

Every model produces one saved response per item. Those response bytes are then frozen. Five predeclared parsers are applied to the **same output bytes**.

No prompt, option order, model state or generation output changes between evaluators.

Primary questions:

- Can parser choice alone strictly reverse the ordering of two models?
- Can parser choice alone change whether a paired bootstrap comparison excludes zero?
- How wide is the evaluator-induced score range for a fixed model × benchmark cell?
- How much of the effect is explained by the evaluator's unparsed-output policy?

The contribution is therefore not generic prompt sensitivity. It is a controlled measurement-reliability study in which the experimental object (the generated answer) is byte-identical and only the scoring implementation changes.

The Nature manuscript's datasets, RIDI/frontier methods and conclusions are excluded by the public firewall.
