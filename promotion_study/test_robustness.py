#!/usr/bin/env python3
from robustness import classify_differences,score_width
r=classify_differences("A","B","X",{"E1":0.1,"E2":0.2,"E3":0.05})
assert r["robust_direction"]=="model1_over_model2" and not r["evaluator_specification_sensitive"] and not r["strict_ranking_reversal"]
r=classify_differences("A","B","X",{"E1":-0.1,"E2":-0.02,"E3":-0.2})
assert r["robust_direction"]=="model2_over_model1" and not r["evaluator_specification_sensitive"]
r=classify_differences("A","B","X",{"E1":0.1,"E2":0.0,"E3":0.2})
assert r["evaluator_specification_sensitive"] and not r["strict_ranking_reversal"] and r["robust_direction"] is None
r=classify_differences("A","B","X",{"E1":0.1,"E2":-0.01,"E3":0.2})
assert r["evaluator_specification_sensitive"] and r["strict_ranking_reversal"] and r["robust_direction"] is None
assert abs(score_width([0.5,0.55,0.48])-0.07)<1e-12
print("ESR_CERTIFICATE_TESTS_PASS")
