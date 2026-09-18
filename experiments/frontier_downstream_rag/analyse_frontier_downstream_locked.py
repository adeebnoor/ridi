#!/usr/bin/env python3
"""Locked aggregate analysis for RIDI-NATURE-FRONTIER-DOWNSTREAM-v1.

This analysis was committed after Qwen3 generation began but before any endpoint
result was inspected. It implements only the already locked endpoints.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,pathlib
import numpy as np

DATASETS=("nq","hotpotqa","fever","scifact")
SEED=20260918
DRAWS=100000

def read_jsonl(p):
    return [json.loads(x) for x in pathlib.Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

def pct(a,q): return float(np.quantile(np.asarray(a,float),q))

def bootstrap(rows_by_dataset, value_fn):
    rng=np.random.default_rng(SEED)
    vals=np.empty(DRAWS,float)
    for b in range(DRAWS):
        means=[]
        for d in DATASETS:
            rows=rows_by_dataset[d]
            idx=rng.integers(0,len(rows),size=len(rows))
            means.append(float(np.mean([value_fn(rows[i]) for i in idx])))
        vals[b]=float(np.mean(means))
    return [pct(vals,.025),pct(vals,.975)]

def cell_metrics(rows,k,eta):
    upd=f"k{k}_updated";ctl=f"k{k}_{eta}"
    n=len(rows)
    diffs=[];flips=[];texts=[];dirs={"updated_correct_controlled_wrong":0,"updated_wrong_controlled_correct":0}
    sens=[]
    for r in rows:
        u=bool(r["responses"][upd]["score"]["primary"])
        c=bool(r["responses"][ctl]["score"]["primary"])
        us=bool(r["responses"][upd]["score"]["sensitivity"])
        cs=bool(r["responses"][ctl]["score"]["sensitivity"])
        diffs.append(int(c)-int(u));sens.append(int(cs)-int(us))
        flips.append(int(u!=c))
        texts.append(int(r["responses"][upd]["normalized_text"]!=r["responses"][ctl]["normalized_text"]))
        if u and not c: dirs["updated_correct_controlled_wrong"]+=1
        if (not u) and c: dirs["updated_wrong_controlled_correct"]+=1
    return {
      "n":n,
      "updated_accuracy_primary":float(np.mean([r["responses"][upd]["score"]["primary"] for r in rows])),
      "controlled_accuracy_primary":float(np.mean([r["responses"][ctl]["score"]["primary"] for r in rows])),
      "paired_accuracy_difference_primary":float(np.mean(diffs)),
      "correctness_status_disagreement_primary":float(np.mean(flips)),
      "answer_text_disagreement":float(np.mean(texts)),
      "updated_accuracy_sensitivity":float(np.mean([r["responses"][upd]["score"]["sensitivity"] for r in rows])),
      "controlled_accuracy_sensitivity":float(np.mean([r["responses"][ctl]["score"]["sensitivity"] for r in rows])),
      "paired_accuracy_difference_sensitivity":float(np.mean(sens)),
      **dirs
    }

def main():
    ap=argparse.ArgumentParser()
    for d in DATASETS: ap.add_argument(f"--{d}",required=True)
    ap.add_argument("--frozen-manifest",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args();out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    rows_by={}
    for d in DATASETS:
        rows=read_jsonl(getattr(a,d))
        if len(rows)!=100 or any(r["dataset"]!=d for r in rows):raise RuntimeError(f"{d}: invalid result panel")
        qids=[str(r["query_id"]) for r in rows]
        if len(set(qids))!=100:raise RuntimeError(f"{d}: duplicate query id")
        rows_by[d]=rows
    fm=json.loads(pathlib.Path(a.frozen_manifest).read_text())
    if set(fm["datasets"])!=set(DATASETS):raise RuntimeError("frozen manifest datasets mismatch")

    summary={"protocol_id":"RIDI-NATURE-FRONTIER-DOWNSTREAM-v1",
             "analysis_locked_seed":SEED,"bootstrap_draws":DRAWS,
             "primary":{"k":10,"eta":0.001},"datasets":{},"sensitivity_surface":{}}
    per=[]
    for d,rows in rows_by.items():
        m=cell_metrics(rows,10,"eta_0_001")
        m["identity_control"]=fm["datasets"][d]["primary_identity_summary"]
        summary["datasets"][d]=m
        for r in rows:
            u=bool(r["responses"]["k10_updated"]["score"]["primary"])
            c=bool(r["responses"]["k10_eta_0_001"]["score"]["primary"])
            per.append({"dataset":d,"query_id":str(r["query_id"]),
                        "updated_correct":int(u),"controlled_correct":int(c),
                        "paired_correctness_difference":int(c)-int(u),
                        "correctness_status_changed":int(u!=c),
                        "answer_text_changed":int(r["responses"]["k10_updated"]["normalized_text"]!=r["responses"]["k10_eta_0_001"]["normalized_text"]),
                        "delta_unconstrained":int(r["primary_frontier"]["delta_unconstrained"]),
                        "j_eta":int(r["primary_frontier"]["j_eta"]),
                        "utility_regret":float(r["primary_frontier"]["utility_regret"])})

    macro_diff=float(np.mean([summary["datasets"][d]["paired_accuracy_difference_primary"] for d in DATASETS]))
    macro_text=float(np.mean([summary["datasets"][d]["answer_text_disagreement"] for d in DATASETS]))
    macro_flip=float(np.mean([summary["datasets"][d]["correctness_status_disagreement_primary"] for d in DATASETS]))
    macro_id=float(np.mean([fm["datasets"][d]["primary_identity_summary"]["mean_changed_slots_reduction"] for d in DATASETS]))
    macro_avoid=float(np.mean([fm["datasets"][d]["primary_identity_summary"]["mean_avoidable_turnover_fraction_among_changed"] for d in DATASETS]))
    summary["primary_macro"]={
      "mean_changed_slots_reduction_equal_dataset_weight":macro_id,
      "mean_avoidable_turnover_fraction_among_changed_equal_dataset_weight":macro_avoid,
      "paired_accuracy_difference_controlled_minus_updated":macro_diff,
      "paired_accuracy_difference_ci95":bootstrap(rows_by,lambda r:int(r["responses"]["k10_eta_0_001"]["score"]["primary"])-int(r["responses"]["k10_updated"]["score"]["primary"])),
      "correctness_status_disagreement":macro_flip,
      "correctness_status_disagreement_ci95":bootstrap(rows_by,lambda r:int(r["responses"]["k10_eta_0_001"]["score"]["primary"]!=r["responses"]["k10_updated"]["score"]["primary"])),
      "answer_text_disagreement":macro_text,
      "answer_text_disagreement_ci95":bootstrap(rows_by,lambda r:int(r["responses"]["k10_eta_0_001"]["normalized_text"]!=r["responses"]["k10_updated"]["normalized_text"])),
    }

    for k in (5,10,20):
        for eta in ("eta_0_0001","eta_0_001"):
            key=f"k{k}_{eta}"
            summary["sensitivity_surface"][key]={
              d:cell_metrics(rows_by[d],k,eta) for d in DATASETS
            }
            summary["sensitivity_surface"][key]["macro_paired_accuracy_difference"]=float(np.mean([
              summary["sensitivity_surface"][key][d]["paired_accuracy_difference_primary"] for d in DATASETS]))
            summary["sensitivity_surface"][key]["macro_answer_text_disagreement"]=float(np.mean([
              summary["sensitivity_surface"][key][d]["answer_text_disagreement"] for d in DATASETS]))

    with (out/"per_query_primary.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(per[0]));w.writeheader();w.writerows(per)
    (out/"frontier_downstream_final_summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print(json.dumps(summary["primary_macro"],indent=2,sort_keys=True))

if __name__=="__main__":main()
