#!/usr/bin/env python3
"""Reconstruct and verify the pre-output AJSE frozen panel."""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass
import numpy as np
from datasets import load_dataset

SEED=20260919
N=150

@dataclass(frozen=True)
class Spec:
    key:str; repo:str; revision:str; config:str; split:str; expected_population:int; expected_sha:str

SPECS=[
Spec("mmlu_pro","TIGER-Lab/MMLU-Pro","b189ec765aa7ed75c8acfea42df31fdae71f97be","default","test",12032,"8507196db29ea8a1f470245d65ae71a7a917ec95cb45db3eaed77427619afd77"),
Spec("gsm8k","openai/gsm8k","740312add88f781978c0658806c59bc2815b9866","main","test",1319,"d1326d2138bd189f90d9966497373e1a9da9c001e8f536af167393c779d66f11"),
Spec("arc_challenge","allenai/ai2_arc","210d026faf9955653af8916fad021475a3f00453","ARC-Challenge","test",1172,"65ea6957753ff6f9a83a5ccda41bad7b70540eee449e77f5a7f2fa4b069e46db"),
Spec("truthfulqa_mc","truthfulqa/truthful_qa","741b8276f2d1982aa3d5b832d3ee81ed3b896490","multiple_choice","validation",817,"55a5578ac2b64e2ffaa3932d30062030c1c22d9d9b731ac59ff9302dded221e1"),
]

def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()

def stable_id(key,row):
    if key=="mmlu_pro": return str(row["question_id"])
    if key=="arc_challenge": return str(row["id"])
    if key=="gsm8k": return sha(str(row["question"]))
    if key=="truthfulqa_mc": return sha(str(row["question"]))
    raise KeyError(key)

def reconstruct():
    rng=np.random.default_rng(SEED)
    panels={}
    summary={}
    for s in SPECS:
        ds=load_dataset(s.repo,s.config,split=s.split,revision=s.revision)
        if len(ds)!=s.expected_population: raise RuntimeError(f"{s.key}: population {len(ds)} != {s.expected_population}")
        entries=[]
        rowmap={}
        for row in ds:
            rid=stable_id(s.key,row)
            rh=sha(canon(row))
            entries.append({"id":rid,"row_sha256":rh})
            rowmap[rid]=row
        entries.sort(key=lambda z:z["id"])
        idx=np.sort(rng.choice(len(entries),size=N,replace=False))
        selected=[entries[int(i)] for i in idx]
        got=sha(canon(selected))
        if got!=s.expected_sha: raise RuntimeError(f"{s.key}: frozen sample SHA mismatch {got} != {s.expected_sha}")
        panels[s.key]=[(x["id"],rowmap[x["id"]]) for x in selected]
        summary[s.key]={"n":N,"sha256":got}
    return panels,summary

if __name__=="__main__":
    _,s=reconstruct()
    print(json.dumps(s,indent=2,sort_keys=True))
