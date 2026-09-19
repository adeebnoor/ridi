#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from dataclasses import dataclass
import numpy as np
from datasets import load_dataset
SEED=20260919
N=250
@dataclass(frozen=True)
class Spec:
    key:str;repo:str;revision:str;config:str;split:str;expected_population:int;expected_sha:str
SPECS=[
Spec("commonsenseqa","tau/commonsense_qa","94630fe30dad47192a8546eb75f094926d47e155","default","validation",1221,"1c03091e297f8b046bc00a9d9b038a51336df0ee9295fd33cb3b84ed2168cbc7"),
Spec("openbookqa","allenai/openbookqa","388097ea7776314e93a529163e0fea805b8a6454","main","validation",500,"362801e4353ac9a4cc911a5cca9f8bb9fff8a61bbf57fd4a5b400c04aaf1bb43"),
Spec("hellaswag","Rowan/hellaswag","218ec52e09a7e7462a5400043bb9a69a41d06b76","default","validation",10042,"00ef02b156210ce9201508e7d77e28c97774f5d54388e32f11423673e554d816"),
Spec("boolq","google/boolq","35b264d03638db9f4ce671b711558bf7ff0f80d5","default","validation",3270,"e08437f808e9a8fe9c9f8c5aca6cea30875c5560ba3500c2c5529183608b440c"),
]
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def sha(s):return hashlib.sha256(s.encode("utf-8")).hexdigest()
def stable_id(key,row):
    if key in ("commonsenseqa","openbookqa"):return str(row["id"])
    if key=="hellaswag":return str(row["ind"])
    if key=="boolq":return sha(str(row["question"])+"\n"+str(row["passage"]))
    raise KeyError(key)
def reconstruct():
    rng=np.random.default_rng(SEED);panels={};summary={}
    for s in SPECS:
        ds=load_dataset(s.repo,s.config,split=s.split,revision=s.revision)
        if len(ds)!=s.expected_population:raise RuntimeError(f"{s.key}: population mismatch {len(ds)}")
        entries=[];rowmap={}
        for row in ds:
            rid=stable_id(s.key,row);rh=sha(canon(row));entries.append({"id":rid,"row_sha256":rh});rowmap[rid]=row
        entries.sort(key=lambda z:z["id"])
        idx=np.sort(rng.choice(len(entries),size=N,replace=False));selected=[entries[int(i)] for i in idx]
        got=sha(canon(selected))
        if got!=s.expected_sha:raise RuntimeError(f"{s.key}: sample SHA mismatch {got} != {s.expected_sha}")
        panels[s.key]=[(x["id"],rowmap[x["id"]]) for x in selected]
        summary[s.key]={"n":N,"sha256":got}
    return panels,summary
if __name__=="__main__":
    _,s=reconstruct();print(json.dumps(s,indent=2,sort_keys=True))
