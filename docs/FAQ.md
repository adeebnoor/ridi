# Frequently asked questions

## What does RIDI stand for?

RIDI is the **Reproducibility of Identity Decisions Index**. It asks whether the same identities receive a finite set of decision slots after a controlled computational change.

## Is RIDI just Jaccard distance?

The numerical set-distance primitive is Jaccard distance. The contribution is the decision-reproducibility estimand and protocol around it: a controlled representation intervention, mechanism-matched controls, retraining calibration, a score-margin certificate, independent outcome testing and exact identity-constrained selection. The claim is therefore not that a new set-similarity formula was invented, but that finite decision identity can be measured, attributed, certified, controlled and validated as a distinct reproducibility axis.

## Why not use Spearman or Kendall correlation?

Global rank statistics average over the full candidate universe. Finite decisions depend on membership near a cutoff. Two rankings can have correlation arbitrarily close to one while their top-*k* sets are disjoint as the universe grows.

## Is change necessarily bad?

No. A new representation can surface better candidates. Independent outcomes should determine whether changed identity is progress. RIDI makes the turnover visible and constrains only the portion that is unnecessary for a declared utility target.

## How should eta be chosen?

Prospectively, from domain costs, review capacity, safety requirements and stakeholder policy. `eta = 0.001` is a demonstration choice representing 0.1% normalized utility regret, not a universal standard.

## Does a non-zero RIDI prove that representation caused the change?

Only when the intervention design freezes source evidence, inference, candidate universe and decision rules, and when stochasticity is removed or calibrated. Otherwise it is a diagnostic difference, not causal attribution.
