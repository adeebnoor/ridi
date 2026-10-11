# RIDI-PREDICT-v1 post-run analysis recovery amendment
Date: 11 October 2026
Registration: https://osf.io/xrzp5/
Status: POST-RUN amendment, recorded after generation and the failed original analysis, before the recovery analysis. This is not a new preregistration.

## Authorization and prior execution
The PI authorized continuation on 11 October 2026 at 18:11:29 Asia/Riyadh (15:11:29 UTC), after being told that all 24 units had completed but the frozen analysis failed. The original analysis was invoked once at 13:25:21 UTC and failed at 13:25:23 UTC with no PREDICT_RESULTS files or hypothesis decisions. Its code and failed execution receipt remain unchanged.

Frozen analysis SHA256: 3c47b58d90b60fd35a331ce4db3ac873687860cf200202ecd4c48874cc6bc5d9
Original verified data ZIP SHA256: 3597aa0c608b591099693890e567b30801261ceacb5f11abb48dec7258526bd6

## Knowledge at the time of this amendment
All 24 final units succeeded; their archives and logs were authenticated. No generation is repeated. Diagnostic work at 15:13:53 UTC used the registered design matrices and outcome indicators, without computing AUCs, hypothesis decisions or bootstrap results. The two Qwen3-32B design matrices have full column rank, but a linear-programming certificate demonstrates quasi-complete separation: the direction minus the predictor-floor-change covariate has nonnegative signed margins for all 800 observations, strictly positive for 16, and zero for the rest. The registered Newton iteration does not converge; increasing the iteration cap does not create a finite maximum-likelihood estimate. Both OLMo matrices have overlap and the registered solver converges.

## Recovery rule fixed before its results
1. Preserve all raw records, labels, samples, exchange seeds, models, generation settings, covariates and frozen scientific files.
2. Run a separately named derivative recovery script once on a verified working copy. Verify the original nine locked files, the frozen analysis hash, and the derivative hash. Keep the original failed invocation visible.
3. Preserve the original H1/H2 prerequisites, AUC definitions, thresholds, 100000 stratified bootstrap draws, random seed and paired resampling. Preserve the registered calculations for S1, S2, S4, S5, S6 and S7.
4. Confine an unavailable regression to H3 and regression-dependent S3 for that target. Report H3 as not estimable under the registered finite-MLE/Wald procedure and S3 as unavailable when either registered full or baseline fit fails. Preserve null numerical fields and the reason. Do not call it falsified, inconclusive, supported, or a zero effect.
5. Do not drop the separating covariate, drop observations, increase the iteration cap, alter the convergence tolerance, penalize the regression, or substitute Firth, ridge or another estimator to obtain a decision. For a target whose registered fits converge, retain the original MLE, Wald interval, decision rule and 2000 S3 bootstrap refits, reporting the number that converge.
6. Complete the preregistered descriptive S8 that the original script did not emit. Exclude identical draw-A/draw-B contexts; report the excluded count. If it is zero, S8 is exactly the primary result and no second fit/bootstrap is run. Otherwise calculate the same primary estimands on the retained within-benchmark sample with the same registered seed and draw count, disclose subset regression failures, and label this as code added after the run to implement the registered descriptive analysis.
7. Output filenames and report explicitly identify this post-run recovery and the original failure. Do not imply the original frozen script completed successfully, or that this amendment predates data collection.
8. Human coding remains unperformed pending the written ethics determination. No PI-only annotation key is opened. No new GPU jobs, emails or manuscript submission are authorized by this computational recovery.

## Methodological basis
Albert A and Anderson JA (1984). On the existence of maximum likelihood estimates in logistic regression models. Biometrika 71(1):1-10. DOI: 10.1093/biomet/71.1.1.
Statsmodels documentation, Pitfalls, incomplete convergence / separation: https://www.statsmodels.org/dev/pitfalls.html
The separation diagnosis is established here by an explicit design-matrix certificate, not by treating a software convergence flag alone as proof.

## Disclosure
This amendment is published as a dated GitHub record before recovery execution. The OSF registration remains the original frozen record; this GitHub posting does not itself amend the OSF registry entry. The report must disclose that an OSF cross-reference remains to be added if no OSF update is completed.
