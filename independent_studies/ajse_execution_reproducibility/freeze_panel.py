#!/usr/bin/env python3
import hashlib, json, pathlib, re
from datasets import load_dataset

STUDY="LLM-EXEC-REPRO-AJSE-v1"
SEED="20260919"
ROOT=pathlib.Path(__file__).resolve().parent/"frozen"
ROOT.mkdir(parents=True,exist_ok=True)

REVS={
 "mmlu_pro":"b189ec765aa7ed75c8acfea42df31fdae71f97be",
 "gsm8k":"740312add88f781978c0658806c59bc2815b9866",
}

def h(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def stable(dataset,item_id): return h(f"{STUDY}|{dataset}|{item_id}|{SEED}")

def mmlu_prompt(r):
    opts="\n".join(f"({chr(65+i)}) {x}" for i,x in enumerate(r["options"]))
    return (
      "Answer the multiple-choice question. Give a concise explanation, then end with exactly "
      "'Final answer: <letter>'.\n\n"
      f"Question: {r['question']}\nOptions:\n{opts}"
    )

def gsm_prompt(r):
    return (
      "Solve the following math problem. Give concise step-by-step reasoning, then end with exactly "
      "'Final answer: <number>'.\n\n"
      f"Problem: {r['question']}"
    )

rows=[]
m=load_dataset("TIGER-Lab/MMLU-Pro",revision=REVS["mmlu_pro"],split="test")
cand=[]
for i,r in enumerate(m):
    item_id=str(r["question_id"])
    cand.append((stable("mmlu_pro",item_id),{
      "study":STUDY,"dataset":"mmlu_pro","item_id":item_id,"source_index":i,
      "gold":str(r["answer"]).strip(),"prompt":mmlu_prompt(r)
    }))
cand.sort(key=lambda x:(x[0],x[1]["item_id"]))
for j,(_,r) in enumerate(cand[:152]):
    r["role"]="target" if j<150 else "support_anchor"; r["selection_rank"]=j+1
    r["prompt_sha256"]=h(r["prompt"]); rows.append(r)

g=load_dataset("openai/gsm8k","main",revision=REVS["gsm8k"],split="test")
cand=[]
for i,r in enumerate(g):
    qhash=h(r["question"])[:16]
    item_id=f"test-{i}-{qhash}"
    gold=r["answer"].rsplit("####",1)[-1].strip().replace(",","")
    cand.append((stable("gsm8k",item_id),{
      "study":STUDY,"dataset":"gsm8k","item_id":item_id,"source_index":i,
      "gold":gold,"prompt":gsm_prompt(r)
    }))
cand.sort(key=lambda x:(x[0],x[1]["item_id"]))
for j,(_,r) in enumerate(cand[:152]):
    r["role"]="target" if j<150 else "support_anchor"; r["selection_rank"]=j+1
    r["prompt_sha256"]=h(r["prompt"]); rows.append(r)

out=ROOT/"FROZEN_PANEL.jsonl"
with out.open("w",encoding="utf-8") as f:
    for r in rows: f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n")
b=out.read_bytes()
templates={
 "mmlu_pro":h("Answer the multiple-choice question. Give a concise explanation, then end with exactly 'Final answer: <letter>'."),
 "gsm8k":h("Solve the following math problem. Give concise step-by-step reasoning, then end with exactly 'Final answer: <number>'."),
}
manifest={
 "study":STUDY,"seed":int(SEED),"created_pre_output":True,
 "dataset_revisions":REVS,
 "targets":{"mmlu_pro":150,"gsm8k":150},
 "support_anchors":{"mmlu_pro":2,"gsm8k":2},
 "rows":len(rows),"panel_sha256":hashlib.sha256(b).hexdigest(),
 "prompt_template_component_sha256":templates,
 "prompt_sha256_by_dataset":{
   d:hashlib.sha256(("\n".join(r["prompt_sha256"] for r in rows if r["dataset"]==d)+"\n").encode()).hexdigest()
   for d in ["mmlu_pro","gsm8k"]
 }
}
(ROOT/"FROZEN_PANEL_MANIFEST.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(manifest,sort_keys=True))
