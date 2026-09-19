#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
import numpy as np

SEED=20260919
DRAWS=100000
DATASETS=["commonsenseqa","openbookqa","hellaswag","boolq"]
EVALS=["E1","E2","E3","E4","E5"]

def rate(x):
    return float(np.mean(np.asarray(x,dtype=float))) if len(x) else float("nan")
def sign(x):
    return 1 if x>0 else (-1 if x<0 else 0)
def ci(a):
    return [float(np.quantile(a,.025)),float(np.quantile(a,.975))]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("raw",nargs="+")
    ap.add_argument("--out",type=Path,default=Path("JKSUCIS_AGGREGATE.json"))
    a=ap.parse_args()
    rows=[]
    for p in a.raw:
        rows += [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]
    models=sorted(set(r["model"] for r in rows))
    if len(models)!=3:raise RuntimeError(f"Expected 3 locked models, got {models}")

    bymd={(m,d):{r["id"]:r for r in rows if r["model"]==m and r["dataset"]==d} for m in models for d in DATASETS}
    cell={}
    for m in models:
        cell[m]={}
        for d in DATASETS:
            rr=list(bymd[(m,d)].values())
            if len(rr)!=250:raise RuntimeError(f"{m}/{d}: expected 250 rows, got {len(rr)}")
            cell[m][d]={"n":len(rr)}
            for e in EVALS:
                cell[m][d][e]={
                    "accuracy":rate([r["correct"][e] for r in rr]),
                    "unresolved":sum(r["decisions"][e] is None for r in rr),
                    "unresolved_rate":rate([r["decisions"][e] is None for r in rr])
                }
            cell[m][d]["E1_E2_disagreement"]=rate([r["decisions"]["E1"]!=r["decisions"]["E2"] for r in rr])

    rng=np.random.default_rng(SEED)
    pairwise=[]
    for d in DATASETS:
        common=sorted(set.intersection(*(set(bymd[(m,d)]) for m in models)))
        if len(common)!=250:raise RuntimeError(f"{d}: models do not share same 250 frozen IDs")
        for m1,m2 in itertools.combinations(models,2):
            e1a=np.asarray([int(bymd[(m1,d)][i]["correct"]["E1"]) for i in common],dtype=float)
            e1b=np.asarray([int(bymd[(m2,d)][i]["correct"]["E1"]) for i in common],dtype=float)
            e2a=np.asarray([int(bymd[(m1,d)][i]["correct"]["E2"]) for i in common],dtype=float)
            e2b=np.asarray([int(bymd[(m2,d)][i]["correct"]["E2"]) for i in common],dtype=float)
            diff1=float((e1a-e1b).mean());diff2=float((e2a-e2b).mean())
            observed_reversal=(sign(diff1)*sign(diff2)==-1)
            bd1=np.empty(DRAWS);bd2=np.empty(DRAWS)
            chunk=1000
            for start in range(0,DRAWS,chunk):
                k=min(chunk,DRAWS-start)
                idx=rng.integers(0,len(common),size=(k,len(common)))
                bd1[start:start+k]=(e1a[idx]-e1b[idx]).mean(axis=1)
                bd2[start:start+k]=(e2a[idx]-e2b[idx]).mean(axis=1)
            bsign=np.asarray([sign(x)*sign(y)==-1 for x,y in zip(bd1,bd2)],dtype=float)
            pairwise.append({
              "dataset":d,"model1":m1,"model2":m2,
              "E1_accuracy_difference":diff1,"E1_diff_ci95":ci(bd1),
              "E2_accuracy_difference":diff2,"E2_diff_ci95":ci(bd2),
              "observed_ranking_reversal":observed_reversal,
              "bootstrap_sign_disagreement_frequency":float(bsign.mean())
            })

    # Equal-cell primary decision-disagreement macro: same frozen item resampling within each benchmark.
    bmacro=np.empty(DRAWS)
    cell_disagreement=[cell[m][d]["E1_E2_disagreement"] for m in models for d in DATASETS]
    for start in range(0,DRAWS,1000):
        k=min(1000,DRAWS-start)
        vals=np.zeros(k,dtype=float)
        for d in DATASETS:
            ids=sorted(set.intersection(*(set(bymd[(m,d)]) for m in models)))
            idx=rng.integers(0,len(ids),size=(k,len(ids)))
            for m in models:
                arr=np.asarray([bymd[(m,d)][i]["decisions"]["E1"]!=bymd[(m,d)][i]["decisions"]["E2"] for i in ids],dtype=float)
                vals += arr[idx].mean(axis=1)/12.0
        bmacro[start:start+k]=vals

    reversals=sum(x["observed_ranking_reversal"] for x in pairwise)
    out={
      "study":"EVAL-RANK-JKSUCIS-v1",
      "bootstrap":{"draws":DRAWS,"seed":SEED,"unit":"frozen item within benchmark"},
      "models":models,"cells":cell,"pairwise":pairwise,
      "primary":{
        "ranking_reversals":reversals,
        "ranking_comparisons":len(pairwise),
        "ranking_reversal_rate":reversals/len(pairwise),
        "equal_cell_E1_E2_decision_disagreement":rate(cell_disagreement),
        "equal_cell_E1_E2_disagreement_ci95":ci(bmacro)
      },
      "interpretation_hierarchy":"ranking reversal if observed; otherwise score instability; otherwise bounded evaluator robustness"
    }
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
