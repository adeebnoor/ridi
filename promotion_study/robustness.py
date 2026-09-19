#!/usr/bin/env python3
"""Evaluator-Specification Robustness (ESR) certificate utilities."""
from __future__ import annotations
import hashlib,json

CERTIFICATE_VERSION="ESR-v1"

def canonical_json(x):
    return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)

def score_width(accuracies):
    vals=[float(x) for x in accuracies]
    if not vals: raise ValueError("empty accuracy set")
    return max(vals)-min(vals)

def classify_differences(model1,model2,benchmark,differences):
    if not differences: raise ValueError("empty evaluator-difference set")
    vals={str(k):float(v) for k,v in differences.items()}
    lo=min(vals.values());hi=max(vals.values())
    sensitive=(lo<=0<=hi)
    reversal=(lo<0<hi)
    direction=("model1_over_model2" if lo>0 else ("model2_over_model1" if hi<0 else None))
    core={
      "certificate_version":CERTIFICATE_VERSION,
      "model1":model1,"model2":model2,"benchmark":benchmark,
      "evaluator_differences":vals,
      "difference_interval":[lo,hi],
      "evaluator_specification_sensitive":sensitive,
      "strict_ranking_reversal":reversal,
      "robust_direction":direction
    }
    core["certificate_sha256"]=hashlib.sha256(canonical_json(core).encode("utf-8")).hexdigest()
    return core
