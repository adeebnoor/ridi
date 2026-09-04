# RIDI Audit Minimum Reporting Standard v1

RIDI denotes the **Reproducibility of Identity Decisions Index**.

A study may describe an analysis as a **representation-aware decision reproducibility audit** only when it reports all required elements below.

1. **Freeze source evidence (S).** Identify the exact evidence-bearing records used in both arms, with version and integrity hash where feasible.
2. **Define the representation intervention (R0 → R1).** State exactly what changes and what does not. Distinguish nominal relabelling, structural remapping, compression and learned representation changes.
3. **Freeze inference and decision context (F, C).** Keep the inference procedure, candidate identities, decision rule and pre-specified cutoffs fixed within the contrast, or explicitly model randomness Z.
4. **Report conventional performance.** Provide task-appropriate aggregate metrics so decision turnover is not confused with ordinary performance collapse.
5. **Report decision identity.** Report RIDI and changed slots at every pre-specified cutoff, with deterministic tie handling and the common candidate universe made explicit.
6. **Run a mechanism-matched invariance control.** Include a transformation expected to preserve the computation and verify zero turnover within the declared numerical tolerance.
7. **Check the margin certificate when score vectors are comparable.** Report `gamma_k`, `epsilon` and whether `gamma_k > 2*epsilon` certifies stability. Once paired score vectors are stored, certification requires no retraining or additional inference.
8. **Calibrate learned systems against stochasticity.** Compare R0→R1 turnover with same-representation retraining variability using pre-specified seeds or ensembles. Do not attribute turnover to representation when it is statistically indistinguishable from the retraining null.
9. **Test changed identities against independent outcomes when feasible.** Do not equate stability with correctness or change with harm.
10. **Declare the identity budget prospectively.** If turnover is constrained, justify the utility-regret tolerance from domain costs or governance requirements; do not tune it after inspecting the desired identities.
11. **Preserve adverse outcomes and protocol lineage.** Report failed gates, null results and implementation corrections without replacing the original confirmatory estimand post-outcome.

The minimum interpretive claim is: **decision identity is or is not invariant under the stated representation intervention**. The audit alone does not establish clinical harm, causal utility, fairness, or superiority of one representation.
