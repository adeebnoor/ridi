#!/usr/bin/env python3
"""Locked analysis engine for RIDI-NATURE-FRONTIER-DOWNSTREAM-v1.

This script intentionally requires frozen inputs. It does not download datasets,
retrieve passages or call a language model. Those steps must create the input
files defined in PROTOCOL_LOCK.md before endpoint analysis.

Input CSV columns:
query_id,dataset,doc_id,baseline_score,updated_score,relevance_grade,
reference_answer,updated_answer,frontier_eta_0_0001_answer,frontier_eta_0_001_answer,
reference_correct,updated_correct,frontier_eta_0_0001_correct,frontier_eta_0_001_correct

One row per query-document candidate. Answers/correctness repeat within query.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib
import numpy as np
import pandas as pd
from ridi_audit.selector import identity_utility_frontier, select_identity_control, ridi_from_changed_slots

KS=(5,10,20)
ETAS=(0.0001,0.001)
SEED=20260918
DRAWS=100000

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def norm_text(x):
    return " ".join(str(x).strip().lower().split())

def boot_paired(vals, strata, draws=DRAWS, seed=SEED):
    rng=np.random.default_rng(seed)
    vals=np.asarray(vals,float); strata=np.asarray(strata,str)
    groups={s:np.flatnonzero(strata==s) for s in sorted(set(strata))}
    out=np.empty(draws,float)
    for d in range(draws):
        pieces=[]
        for idx in groups.values():
            pieces.append(vals[rng.choice(idx,size=len(idx),replace=True)])
        out[d]=np.mean(np.concatenate(pieces))
    return [float(np.quantile(out,.025)),float(np.quantile(out,.975))]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    out=pathlib.Path(args.out); out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(args.input,dtype={"query_id":str,"doc_id":str})
    req={"query_id","dataset","doc_id","baseline_score","updated_score","relevance_grade",
         "reference_answer","updated_answer","frontier_eta_0_0001_answer","frontier_eta_0_001_answer",
         "reference_correct","updated_correct","frontier_eta_0_0001_correct","frontier_eta_0_001_correct"}
    miss=req-set(df.columns)
    if miss: raise SystemExit(f"missing columns: {sorted(miss)}")
    rows=[]
    for (qid,ds),g in df.groupby(["query_id","dataset"],sort=True):
        g=g.copy()
        if g.doc_id.duplicated().any(): raise ValueError(f"duplicate doc_id in {qid}")
        g["baseline_score"]=pd.to_numeric(g.baseline_score,errors="raise")
        g["updated_score"]=pd.to_numeric(g.updated_score,errors="raise")
        ids=g.doc_id.astype(str).tolist()
        s0=g.baseline_score.astype(float).tolist()
        s1=g.updated_score.astype(float).tolist()
        for k in KS:
            if len(g)<2*k:
                rows.append({"query_id":qid,"dataset":ds,"k":k,"status":"unavailable_candidate_union"})
                continue
            fr=identity_utility_frontier(ids,s0,s1,k)
            base=set(np.asarray(ids,dtype=object)[fr.baseline_order[:k]].tolist())
            upd_order=np.lexsort((np.asarray(ids,dtype=str),-np.asarray(s1,float)))
            updated=set(np.asarray(ids,dtype=object)[upd_order[:k]].tolist())
            delta=k-len(base&updated)
            for eta in ETAS:
                sel=select_identity_control(fr,eta)
                state="frontier_eta_0_0001" if eta==0.0001 else "frontier_eta_0_001"
                ans_ref=str(g.reference_answer.iloc[0]); ans_upd=str(g.updated_answer.iloc[0]); ans_ctl=str(g[f"{state}_answer"].iloc[0])
                c_upd=int(g.updated_correct.iloc[0]); c_ctl=int(g[f"{state}_correct"].iloc[0])
                rows.append({
                    "query_id":qid,"dataset":ds,"k":k,"eta":eta,"status":"ok",
                    "changed_unconstrained":delta,"changed_controlled":int(sel["j_eta"]),
                    "changed_slots_reduction":delta-int(sel["j_eta"]),
                    "ridi_unconstrained":ridi_from_changed_slots(k,delta),
                    "ridi_controlled":float(sel["ridi_controlled"]),
                    "utility_regret":float(sel["utility_regret"]),
                    "avoidable_turnover_fraction":sel["avoidable_turnover_fraction"],
                    "updated_correct":c_upd,"controlled_correct":c_ctl,
                    "paired_correctness_difference":c_ctl-c_upd,
                    "answer_text_changed_updated_vs_controlled":int(norm_text(ans_upd)!=norm_text(ans_ctl)),
                    "answer_text_changed_reference_vs_updated":int(norm_text(ans_ref)!=norm_text(ans_upd)),
                    "answer_text_changed_reference_vs_controlled":int(norm_text(ans_ref)!=norm_text(ans_ctl)),
                })
    res=pd.DataFrame(rows)
    res.to_csv(out/"per_query_results.csv",index=False)
    primary=res[(res.status=="ok")&(res.k==10)&(res.eta==0.001)].copy()
    if primary.empty: raise RuntimeError("no primary cells")
    summary={
      "protocol_id":"RIDI-NATURE-FRONTIER-DOWNSTREAM-v1",
      "input_sha256":sha256(args.input),
      "n_primary_queries":int(len(primary)),
      "datasets":primary.dataset.value_counts().sort_index().to_dict(),
      "mean_changed_slots_unconstrained":float(primary.changed_unconstrained.mean()),
      "mean_changed_slots_controlled":float(primary.changed_controlled.mean()),
      "mean_changed_slots_reduction":float(primary.changed_slots_reduction.mean()),
      "mean_avoidable_turnover_fraction_among_changed":float(primary.loc[primary.changed_unconstrained>0,"avoidable_turnover_fraction"].mean()),
      "updated_accuracy":float(primary.updated_correct.mean()),
      "controlled_accuracy":float(primary.controlled_correct.mean()),
      "paired_correctness_difference":float(primary.paired_correctness_difference.mean()),
      "paired_correctness_difference_ci95":boot_paired(primary.paired_correctness_difference,primary.dataset),
      "updated_vs_controlled_answer_disagreement":float(primary.answer_text_changed_updated_vs_controlled.mean()),
      "mean_realized_utility_regret":float(primary.utility_regret.mean()),
      "max_realized_utility_regret":float(primary.utility_regret.max()),
    }
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    # full sensitivity surface
    agg=(res[res.status=="ok"].groupby(["dataset","k","eta"],as_index=False)
         .agg(n=("query_id","size"),
              changed_unconstrained=("changed_unconstrained","mean"),
              changed_controlled=("changed_controlled","mean"),
              avoidable_fraction=("avoidable_turnover_fraction","mean"),
              updated_accuracy=("updated_correct","mean"),
              controlled_accuracy=("controlled_correct","mean"),
              correctness_difference=("paired_correctness_difference","mean"),
              answer_disagreement=("answer_text_changed_updated_vs_controlled","mean"),
              utility_regret=("utility_regret","mean")))
    agg.to_csv(out/"sensitivity_surface.csv",index=False)
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
