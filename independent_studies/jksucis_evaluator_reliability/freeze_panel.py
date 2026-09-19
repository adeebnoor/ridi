#!/usr/bin/env python3
import hashlib, json, pathlib, re
from datasets import load_dataset

STUDY="LLM-EVAL-RELIABILITY-JKSU-v1"
SEED="20260919"
ROOT=pathlib.Path(__file__).resolve().parent/"frozen"
ROOT.mkdir(parents=True,exist_ok=True)
REVS={
 "arc_challenge":"210d026faf9955653af8916fad021475a3f00453",
 "openbookqa":"388097ea7776314e93a529163e0fea805b8a6454",
 "commonsenseqa":"94630fe30dad47192a8546eb75f094926d47e155",
 "bbh":"982bb89fd79532a8ac676a61fc42eb1aeec63f99",
}
BBH_TASKS=[
 "date_understanding","disambiguation_qa","geometric_shapes",
 "logical_deduction_five_objects","movie_recommendation","ruin_names",
 "salient_translation_error_detection","temporal_sequences"
]

def h(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def stable(dataset,item_id): return h(f"{STUDY}|{dataset}|{item_id}|{SEED}")
def build_prompt(q, labels, texts):
    opts="\n".join(f"({a}) {b}" for a,b in zip(labels,texts))
    return (
      "Answer the following multiple-choice question. Give a short explanation. "
      "End with exactly: Final answer: <choice label>\n\n"
      f"Question: {q}\nOptions:\n{opts}"
    )

groups={}

ds=load_dataset("allenai/ai2_arc","ARC-Challenge",revision=REVS["arc_challenge"],split="test")
arr=[]
for i,r in enumerate(ds):
    item_id=str(r["id"])
    labels=[str(x) for x in r["choices"]["label"]]; texts=[str(x) for x in r["choices"]["text"]]
    arr.append((stable("arc_challenge",item_id),{"study":STUDY,"dataset":"arc_challenge","item_id":item_id,"source_index":i,
      "gold":str(r["answerKey"]),"valid_labels":labels,"choice_texts":dict(zip(labels,texts)),"prompt":build_prompt(r["question"],labels,texts)}))
groups["arc_challenge"]=arr

ds=load_dataset("allenai/openbookqa","main",revision=REVS["openbookqa"],split="test")
arr=[]
for i,r in enumerate(ds):
    item_id=str(r["id"])
    labels=[str(x) for x in r["choices"]["label"]]; texts=[str(x) for x in r["choices"]["text"]]
    arr.append((stable("openbookqa",item_id),{"study":STUDY,"dataset":"openbookqa","item_id":item_id,"source_index":i,
      "gold":str(r["answerKey"]),"valid_labels":labels,"choice_texts":dict(zip(labels,texts)),"prompt":build_prompt(r["question_stem"],labels,texts)}))
groups["openbookqa"]=arr

ds=load_dataset("tau/commonsense_qa",revision=REVS["commonsenseqa"],split="validation")
arr=[]
for i,r in enumerate(ds):
    item_id=str(r["id"])
    labels=[str(x) for x in r["choices"]["label"]]; texts=[str(x) for x in r["choices"]["text"]]
    arr.append((stable("commonsenseqa",item_id),{"study":STUDY,"dataset":"commonsenseqa","item_id":item_id,"source_index":i,
      "gold":str(r["answerKey"]),"valid_labels":labels,"choice_texts":dict(zip(labels,texts)),"prompt":build_prompt(r["question"],labels,texts)}))
groups["commonsenseqa"]=arr

arr=[]
for task in BBH_TASKS:
    ds=load_dataset("lukaemon/bbh",task,revision=REVS["bbh"],split="test")
    for i,r in enumerate(ds):
        labels=[]
        for lab in re.findall(r"^\(([A-Z])\)\s",r["input"],flags=re.M):
            if lab not in labels: labels.append(lab)
        gold=str(r["target"]).strip().strip("()")
        if not labels or gold not in labels: continue
        # Parse exact choice text from the source input.
        choices={}
        for lab,txt in re.findall(r"^\(([A-Z])\)\s(.+)$",r["input"],flags=re.M):
            choices[lab]=txt.strip()
        item_id=f"{task}:{i}"
        prompt=(
          "Answer the following multiple-choice question. Give a short explanation. "
          "End with exactly: Final answer: <choice label>\n\n"+r["input"]
        )
        arr.append((stable("bbh",item_id),{"study":STUDY,"dataset":"bbh","bbh_task":task,"item_id":item_id,"source_index":i,
          "gold":gold,"valid_labels":labels,"choice_texts":choices,"prompt":prompt}))
groups["bbh"]=arr

rows=[]
for d,arr in groups.items():
    arr.sort(key=lambda x:(x[0],x[1]["item_id"]))
    if len(arr)<250: raise RuntimeError((d,len(arr)))
    for rank,(_,r) in enumerate(arr[:250],1):
        r["selection_rank"]=rank; r["prompt_sha256"]=h(r["prompt"]); rows.append(r)

out=ROOT/"FROZEN_PANEL.jsonl"
with out.open("w",encoding="utf-8") as f:
    for r in rows: f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n")
b=out.read_bytes()
manifest={
 "study":STUDY,"seed":int(SEED),"created_pre_output":True,
 "dataset_revisions":REVS,"splits":{"arc_challenge":"test","openbookqa":"test","commonsenseqa":"validation","bbh":"test"},
 "bbh_tasks":BBH_TASKS,"targets":{d:250 for d in groups},"rows":len(rows),
 "panel_sha256":hashlib.sha256(b).hexdigest(),
 "prompt_sha256_by_dataset":{
   d:hashlib.sha256(("\n".join(r["prompt_sha256"] for r in rows if r["dataset"]==d)+"\n").encode()).hexdigest()
   for d in groups
 }
}
(ROOT/"FROZEN_PANEL_MANIFEST.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(manifest,sort_keys=True))
