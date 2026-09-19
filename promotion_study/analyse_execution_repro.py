#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np

SEED=20260919
DRAWS=100000
DATASETS=["mmlu_pro","gsm8k","arc_challenge","truthfulqa_mc"]
PRIMARY=("B","C")
SECONDARY=[("A","C"),("A","B"),("C","D")]

def load(paths):
    rows=[]
    for p in paths:
        rows += [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]
    return rows

def flags(r,a,b):
    ca=r["conditions"][a];cb=r["conditions"][b]
    stable_a=ca["repeat_text_sha256"][0]==ca["repeat_text_sha256"][1]
    stable_b=cb["repeat_text_sha256"][0]==cb["repeat_text_sha256"][1]
    exact=stable_a and stable_b and ca["repeat_text_sha256"][0]!=cb["repeat_text_sha256"][0]
    normalized=stable_a and stable_b and ca["repeat_normalized_sha256"][0]!=cb["repeat_normalized_sha256"][0]
    stable_dec=(ca["repeat_decision"][0]==ca["repeat_decision"][1] and cb["repeat_decision"][0]==cb["repeat_decision"][1])
    decision=stable_dec and ca["repeat_decision"][0]!=cb["repeat_decision"][0]
    ctw=stable_dec and ca["repeat_correct"][0] and not cb["repeat_correct"][0]
    wtc=stable_dec and (not ca["repeat_correct"][0]) and cb["repeat_correct"][0]
    return stable_a,stable_b,exact,normalized,decision,ctw,wtc

def rate(xs):return float(np.mean(np.asarray(xs,dtype=float))) if xs else float("nan")
def ci(a):return [float(np.quantile(a,.025)),float(np.quantile(a,.975))]

def summarize(rr,a,b):
    ff=[flags(r,a,b) for r in rr]
    return {
      "n":len(rr),
      f"{a}_repeat_failure":sum(not x[0] for x in ff),
      f"{b}_repeat_failure":sum(not x[1] for x in ff),
      "exact_divergence":sum(x[2] for x in ff),"exact_rate":rate([x[2] for x in ff]),
      "normalized_divergence":sum(x[3] for x in ff),"normalized_rate":rate([x[3] for x in ff]),
      "decision_divergence":sum(x[4] for x in ff),"decision_rate":rate([x[4] for x in ff]),
      "correct_to_wrong":sum(x[5] for x in ff),"wrong_to_correct":sum(x[6] for x in ff)
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument("raw",nargs="+");ap.add_argument("--out",type=Path,default=Path("AJSE_AGGREGATE.json"));a=ap.parse_args()
    rows=load(a.raw);models=sorted(set(r["model"] for r in rows))
    results={"study":"LLM-EXEC-REPRO-AJSE-v1","amendment":"fixed-batch co-tenant-composition primary contrast","primary_contrast":"B_vs_C_batch8","models":{},"bootstrap":{"draws":DRAWS,"seed":SEED}}
    for model in models:
        mr=[r for r in rows if r["model"]==model];groups={d:[r for r in mr if r["dataset"]==d] for d in DATASETS}
        for d,g in groups.items():
            if len(g)!=150:raise RuntimeError(f"{model}/{d}: expected 150 rows, got {len(g)}")
        by={}
        for d,rr in groups.items():
            by[d]={"primary_B_vs_C":summarize(rr,"B","C")}
            for x,y in SECONDARY:by[d][f"secondary_{x}_vs_{y}"]=summarize(rr,x,y)
        macro_exact=rate([by[d]["primary_B_vs_C"]["exact_rate"] for d in DATASETS])
        macro_dec=rate([by[d]["primary_B_vs_C"]["decision_rate"] for d in DATASETS])
        rng=np.random.default_rng(SEED);be=np.empty(DRAWS);bd=np.empty(DRAWS)
        for i in range(DRAWS):
            ers=[];drs=[]
            for d in DATASETS:
                g=groups[d];idx=rng.integers(0,len(g),size=len(g));sample=[g[int(j)] for j in idx]
                ff=[flags(r,"B","C") for r in sample];ers.append(rate([x[2] for x in ff]));drs.append(rate([x[4] for x in ff]))
            be[i]=rate(ers);bd[i]=rate(drs)
        results["models"][model]={
          "datasets":by,
          "primary_macro_exact_rate":macro_exact,"primary_macro_exact_ci95":ci(be),
          "primary_macro_decision_rate":macro_dec,"primary_macro_decision_ci95":ci(bd)
        }
    a.out.write_text(json.dumps(results,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(results,sort_keys=True))
if __name__=="__main__":main()
