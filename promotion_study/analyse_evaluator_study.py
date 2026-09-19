#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
import numpy as np

SEED=20260919
DRAWS=100000
DATASETS=["commonsenseqa","openbookqa","hellaswag","boolq"]
EVALS=["E1","E2","E3","E4","E5"]

def rate(x):return float(np.mean(np.asarray(x,dtype=float))) if len(x) else float("nan")
def ci(x):return [float(np.quantile(x,.025)),float(np.quantile(x,.975))]
def sign(x):return 1 if x>0 else (-1 if x<0 else 0)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("raw",nargs="+");ap.add_argument("--out",type=Path,default=Path("JKSUCIS_AGGREGATE.json"));a=ap.parse_args()
    rows=[]
    for p in a.raw:rows += [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]
    models=sorted(set(r["model"] for r in rows))
    if len(models)!=3:raise RuntimeError(f"Expected 3 locked models, got {models}")
    bymd={(m,d):{r["id"]:r for r in rows if r["model"]==m and r["dataset"]==d} for m in models for d in DATASETS}
    cell={}
    for m in models:
        cell[m]={}
        for d in DATASETS:
            rr=list(bymd[(m,d)].values())
            if len(rr)!=250:raise RuntimeError(f"{m}/{d}: expected 250 rows, got {len(rr)}")
            evalstats={}
            for e in EVALS:
                evalstats[e]={
                  "accuracy":rate([r["correct"][e] for r in rr]),
                  "unresolved":sum(r["decisions"][e] is None for r in rr),
                  "unresolved_rate":rate([r["decisions"][e] is None for r in rr])
                }
            accs=[evalstats[e]["accuracy"] for e in EVALS]
            cell[m][d]={
              "n":len(rr),"evaluators":evalstats,
              "evaluator_score_width":max(accs)-min(accs),
              "E1_E2_disagreement":rate([r["decisions"]["E1"]!=r["decisions"]["E2"] for r in rr])
            }

    rng=np.random.default_rng(SEED)
    pairwise=[]
    for d in DATASETS:
        common=sorted(set.intersection(*(set(bymd[(m,d)]) for m in models)))
        if len(common)!=250:raise RuntimeError(f"{d}: models do not share same 250 frozen IDs")
        for m1,m2 in itertools.combinations(models,2):
            observed_diffs={}
            arrays={}
            for e in EVALS:
                a1=np.asarray([int(bymd[(m1,d)][i]["correct"][e]) for i in common],dtype=float)
                a2=np.asarray([int(bymd[(m2,d)][i]["correct"][e]) for i in common],dtype=float)
                arrays[e]=(a1,a2);observed_diffs[e]=float((a1-a2).mean())
            vals=list(observed_diffs.values());lo=min(vals);hi=max(vals)
            sensitive=(lo<=0<=hi);strict_reversal=(lo<0<hi)
            robust_direction=("m1_over_m2" if lo>0 else ("m2_over_m1" if hi<0 else None))
            boot={e:np.empty(DRAWS) for e in EVALS}
            b_sensitive=np.empty(DRAWS,dtype=float);b_reversal=np.empty(DRAWS,dtype=float)
            for start in range(0,DRAWS,1000):
                k=min(1000,DRAWS-start);idx=rng.integers(0,len(common),size=(k,len(common)))
                mat=np.empty((k,len(EVALS)),dtype=float)
                for j,e in enumerate(EVALS):
                    a1,a2=arrays[e];v=(a1[idx]-a2[idx]).mean(axis=1);mat[:,j]=v;boot[e][start:start+k]=v
                blo=mat.min(axis=1);bhi=mat.max(axis=1)
                b_sensitive[start:start+k]=(blo<=0)&(bhi>=0)
                b_reversal[start:start+k]=(blo<0)&(bhi>0)
            pairwise.append({
              "dataset":d,"model1":m1,"model2":m2,
              "evaluator_differences":observed_diffs,
              "evaluator_difference_ci95":{e:ci(boot[e]) for e in EVALS},
              "difference_interval":[lo,hi],
              "evaluator_specification_sensitive":sensitive,
              "strict_ranking_reversal":strict_reversal,
              "robust_direction":robust_direction,
              "bootstrap_sensitive_frequency":float(b_sensitive.mean()),
              "bootstrap_strict_reversal_frequency":float(b_reversal.mean()),
              "E1_vs_E2_special_case_reversal":sign(observed_diffs["E1"])*sign(observed_diffs["E2"])==-1
            })

    # Equal-cell E1-vs-E2 item-level disagreement, retained from original lock.
    cell_dis=[cell[m][d]["E1_E2_disagreement"] for m in models for d in DATASETS]
    bmacro=np.empty(DRAWS)
    for start in range(0,DRAWS,1000):
        k=min(1000,DRAWS-start);vals=np.zeros(k,dtype=float)
        for d in DATASETS:
            ids=sorted(set.intersection(*(set(bymd[(m,d)]) for m in models)))
            idx=rng.integers(0,len(ids),size=(k,len(ids)))
            for m in models:
                arr=np.asarray([bymd[(m,d)][i]["decisions"]["E1"]!=bymd[(m,d)][i]["decisions"]["E2"] for i in ids],dtype=float)
                vals += arr[idx].mean(axis=1)/12.0
        bmacro[start:start+k]=vals

    sensitive_n=sum(x["evaluator_specification_sensitive"] for x in pairwise)
    reversal_n=sum(x["strict_ranking_reversal"] for x in pairwise)
    widths=[cell[m][d]["evaluator_score_width"] for m in models for d in DATASETS]
    out={
      "study":"EVAL-RANK-JKSUCIS-v1",
      "amendment":"evaluator-specification robustness across frozen E1-E5 set",
      "bootstrap":{"draws":DRAWS,"seed":SEED,"unit":"frozen item within benchmark"},
      "models":models,"cells":cell,"pairwise":pairwise,
      "primary":{
        "specification_sensitive_comparisons":sensitive_n,
        "ranking_comparisons":len(pairwise),
        "specification_sensitive_rate":sensitive_n/len(pairwise),
        "strict_ranking_reversals":reversal_n,
        "strict_ranking_reversal_rate":reversal_n/len(pairwise)
      },
      "secondary":{
        "mean_evaluator_score_width":rate(widths),
        "equal_cell_E1_E2_decision_disagreement":rate(cell_dis),
        "equal_cell_E1_E2_disagreement_ci95":ci(bmacro),
        "E1_E2_special_case_reversals":sum(x["E1_vs_E2_special_case_reversal"] for x in pairwise)
      },
      "interpretation_hierarchy":"evaluator-specification robustness first; strict reversal subtype; E1-vs-E2 retained as predeclared special case"
    }
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
