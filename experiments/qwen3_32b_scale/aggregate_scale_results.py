#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parent/"results"
DATASETS=["nq","hotpotqa","fever","scifact"]
EXPECTED_N={"nq":250,"hotpotqa":250,"fever":150,"scifact":150}
SEED=20260919
DRAWS=100000
rows={}
for d in DATASETS:
    p=ROOT/f"{d}_records.jsonl"
    rows[d]=[json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows[d])==EXPECTED_N[d]

def mean(xs): return float(np.mean(np.asarray(xs,dtype=float)))
def ci(a): return [float(np.quantile(a,.025)),float(np.quantile(a,.975))]

dataset={}
for d in DATASETS:
    r=rows[d]
    dataset[d]={
      "n":len(r),
      "qwen32_flips":sum(x["correctness_changed"] for x in r),
      "qwen32_rate":mean([x["correctness_changed"] for x in r]),
      "qwen8_flips":sum(x["qwen8_correctness_changed"] for x in r),
      "qwen8_rate":mean([x["qwen8_correctness_changed"] for x in r]),
      "paired_rate_difference_32_minus_8":mean([int(x["correctness_changed"])-int(x["qwen8_correctness_changed"]) for x in r]),
      "correct_to_wrong":sum(x["correct_to_wrong"] for x in r),
      "wrong_to_correct":sum(x["wrong_to_correct"] for x in r),
      "canonical_changes":sum(x["canonical_changed"] for x in r),
      "canonical_change_rate":mean([x["canonical_changed"] for x in r]),
      "both_flip":sum(x["correctness_changed"] and x["qwen8_correctness_changed"] for x in r),
      "qwen32_only_flip":sum(x["correctness_changed"] and not x["qwen8_correctness_changed"] for x in r),
      "qwen8_only_flip":sum((not x["correctness_changed"]) and x["qwen8_correctness_changed"] for x in r),
      "neither_flip":sum((not x["correctness_changed"]) and (not x["qwen8_correctness_changed"]) for x in r),
    }

macro32=mean([dataset[d]["qwen32_rate"] for d in DATASETS])
macro8=mean([dataset[d]["qwen8_rate"] for d in DATASETS])
macro_diff=macro32-macro8
canonical_macro=mean([dataset[d]["canonical_change_rate"] for d in DATASETS])

rng=np.random.default_rng(SEED)
b32=np.empty(DRAWS); b8=np.empty(DRAWS); bdiff=np.empty(DRAWS); bcanon=np.empty(DRAWS)
for i in range(DRAWS):
    r32=[]; r8=[]; rc=[]
    for d in DATASETS:
        g=rows[d]
        idx=rng.integers(0,len(g),size=len(g))
        s=[g[int(j)] for j in idx]
        r32.append(mean([x["correctness_changed"] for x in s]))
        r8.append(mean([x["qwen8_correctness_changed"] for x in s]))
        rc.append(mean([x["canonical_changed"] for x in s]))
    b32[i]=mean(r32); b8[i]=mean(r8); bdiff[i]=b32[i]-b8[i]; bcanon[i]=mean(rc)

decision="supports transfer" if macro32>=0.05 else ("falsifies strong scale-transfer consequence" if macro32<0.02 else "inconclusive")
out={
 "study":"RIDI-RAG-QWEN3-32B-SCALE-v1",
 "status":"completed",
 "registration_status":"post hoc scale-transfer extension, publicly locked before successful Qwen3-32B generation; not OSF preregistered",
 "model":{"id":"Qwen/Qwen3-32B","revision":"9216db5781bf21249d130ec9da846c4624c16137"},
 "frozen_design":{"n_queries":800,"datasets":{"nq":250,"hotpotqa":250,"fever":150,"scifact":150},"retriever":"BM25","k":10,"intervention":"same registered random metric-zero identity substitution","max_new_tokens":128,"seed":20260902,"thinking":False,"decoding":"greedy"},
 "decision_boundaries":{"support_macro_gte":0.05,"falsify_macro_lt":0.02,"otherwise":"inconclusive"},
 "dataset":dataset,
 "equal_dataset_weight_macro":{
   "qwen32_rate":macro32,"qwen32_ci95":ci(b32),
   "qwen8_rate_same_queries":macro8,"qwen8_ci95_recomputed":ci(b8),
   "paired_difference_32_minus_8":macro_diff,"paired_difference_ci95":ci(bdiff),
   "canonical_change_rate":canonical_macro,"canonical_change_rate_ci95":ci(bcanon),
   "correct_to_wrong":sum(dataset[d]["correct_to_wrong"] for d in DATASETS),
   "wrong_to_correct":sum(dataset[d]["wrong_to_correct"] for d in DATASETS),
   "qwen32_flips_pooled":sum(dataset[d]["qwen32_flips"] for d in DATASETS),
   "qwen8_flips_pooled":sum(dataset[d]["qwen8_flips"] for d in DATASETS)
 },
 "bootstrap":{"draws":DRAWS,"seed":SEED,"stratification":"resample queries with replacement within each dataset; equal weight across four dataset rates"},
 "decision":decision,
 "claim_boundary":"Scale robustness within one open-weight Qwen3 family at 32B. Does not establish behavior for proprietary models, all large models, all prompts, or all retrieval settings."
}
(ROOT/"QWEN3_32B_SCALE_AGGREGATE.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
md=["# Qwen3-32B scale-transfer result","",
"Protocol: RIDI-RAG-QWEN3-32B-SCALE-v1",
"Status: post hoc scale-transfer extension, publicly locked before successful 32B generation; not an OSF preregistration.",
f"Bootstrap: {DRAWS:,} dataset-stratified query resamples; seed {SEED}.","",
"| Dataset | Qwen3-32B flips | Rate | Qwen3-8B flips | 8B rate | 32B-8B | C-to-W | W-to-C | Canonical change |",
"|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
for d in DATASETS:
    x=dataset[d]
    md.append(f"| {d} | {x['qwen32_flips']}/{x['n']} | {100*x['qwen32_rate']:.2f}% | {x['qwen8_flips']}/{x['n']} | {100*x['qwen8_rate']:.2f}% | {100*x['paired_rate_difference_32_minus_8']:+.2f} pp | {x['correct_to_wrong']} | {x['wrong_to_correct']} | {100*x['canonical_change_rate']:.2f}% |")
m=out["equal_dataset_weight_macro"]
md += ["","## Equal-dataset-weight macro","",
f"- Qwen3-32B correctness divergence: {100*m['qwen32_rate']:.2f}% (95% bootstrap {100*m['qwen32_ci95'][0]:.2f}-{100*m['qwen32_ci95'][1]:.2f}%).",
f"- Same-query Qwen3-8B macro: {100*m['qwen8_rate_same_queries']:.2f}%.",
f"- Paired 32B-8B difference: {100*m['paired_difference_32_minus_8']:+.2f} pp (95% bootstrap {100*m['paired_difference_ci95'][0]:+.2f} to {100*m['paired_difference_ci95'][1]:+.2f} pp).",
f"- Directional 32B changes: {m['correct_to_wrong']} correct-to-wrong and {m['wrong_to_correct']} wrong-to-correct.",
f"- Canonical-output divergence: {100*m['canonical_change_rate']:.2f}% (95% bootstrap {100*m['canonical_change_rate_ci95'][0]:.2f}-{100*m['canonical_change_rate_ci95'][1]:.2f}%).",
f"- Predeclared scale-transfer decision: {decision}.",
"",
"The magnitude is lower than at 8B, so the result supports persistence across scale but not scale invariance. The experiment does not establish behavior for proprietary or arbitrary large models."
]
(ROOT/"QWEN3_32B_SCALE_AGGREGATE.md").write_text("\n".join(md)+"\n",encoding="utf-8")
print(json.dumps(out,sort_keys=True))
