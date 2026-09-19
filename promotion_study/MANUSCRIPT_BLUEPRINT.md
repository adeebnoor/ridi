# MANUSCRIPT BLUEPRINT — AJSE

Working title (result-neutral):
**Execution-path reproducibility of deterministic large language model inference**

Target length: approximately 5,000–6,000 words plus references.

## Abstract
Purpose → controlled execution-path design → primary exact-text and final-decision endpoints → strongest predeclared result → engineering implication. No Nature result or cross-manuscript comparison.

## 1. Introduction
Problem: deterministic decoding is commonly treated as synonymous with reproducible output.
Gap: reproducibility claims often specify seed/decoding but not surrounding batch geometry.
Contribution: controlled, pre-output-locked test of execution-path invariance.

## 2. Related work
Deterministic numerical computing; GPU kernel reproducibility; LLM inference reproducibility; batching/padding serving systems. Do not cite unpublished Nature results as evidence.

## 3. Experimental design
2 models × 4 non-Nature benchmarks.
600 frozen targets/model.
Conditions A isolated; B length-matched batch; C mixed-length batch; D same mixed batch reversed.
Every condition executed twice.
Exact immutable revisions and hashes.

## 4. Endpoints and analysis
Primary:
1. exact-text divergence A vs C with duplicate stability;
2. final-decision divergence A vs C with duplicate stability.
Secondary: normalized divergence, other condition contrasts, repeatability failure, task/model heterogeneity, length dispersion.
100,000 stratified bootstrap.

## 5. Results
5.1 Integrity and within-path repeatability.
5.2 Primary exact-text divergence.
5.3 Primary decision divergence.
5.4 Which execution changes matter.
5.5 Benchmark/model heterogeneity.
No condition becomes primary because it looks larger.

## 6. Engineering implications
What must be recorded for reproducible LLM deployment/evaluation: model revision, runtime stack, accelerator, batching policy, padding side, batch composition/order and exact execution path.

## 7. Limitations
Two open model families; specified GPU/runtime; no proprietary API claim; no universal nondeterminism claim.

## 8. Conclusion
Use only conclusions supported by locked endpoints.

### Preplanned displays
Fig. 1 study design and execution paths.
Fig. 2 exact-text divergence by model/benchmark with CIs.
Fig. 3 final-decision divergence by model/benchmark with CIs.
Fig. 4 divergence versus target length / companion-length dispersion.
Table 1 frozen models, data and runtime.
Table 2 primary/secondary endpoint summary.
