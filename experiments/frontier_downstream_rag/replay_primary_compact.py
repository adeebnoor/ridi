#!/usr/bin/env python3
"""Compact deterministic replay of the already-generated primary frontier contrast.

This is not a new endpoint and does not alter RIDI-NATURE-FRONTIER-DOWNSTREAM-v1.
It regenerates only the frozen k=10 updated and eta=0.001 controlled states so the
per-query paired correctness/text-disagreement records can be recovered in a compact,
auditable log. Aggregate values must match the completed full 12-state execution.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, os, random, re, sys, unicodedata, urllib.request
from pathlib import Path

FROZEN_COMMIT="f98be71b4402d95a3337dac78f272c3aa55cbd62"
MODEL_ID="Qwen/Qwen3-8B"
REVISION="b968826d9c46dd6066d109eabc6255188de91218"
SEED=20260902
EXPECTED_GZ={
 "nq":"3f982bf2297d0f0b3d66fd4d8fa22a13513ad12ba4ead6c2ec6f63bcae0361d3",
 "hotpotqa":"43e65af6dc474b58f620344dea57476126d5ef5121e932b765a72bde6c489514",
 "fever":"27e92d6cd3c6de13bfad0c5ced65544bb037bcbe3010175c81665bdc57169011",
 "scifact":"7980a59a5e4af42d75af4f483007d3b95b8196d138962b523abf86fddfc24970",
}
BASE=f"https://raw.githubusercontent.com/adeebnoor/ridi/{FROZEN_COMMIT}/experiments/frontier_downstream_rag/frozen"
CITE_RE=re.compile(r"\[\s*\d+(?:\s*[,;\-]\s*\d+)*\s*\]")
STRICT=re.compile(r"\A\s*(SUPPORTS|REFUTES|NOT_ENOUGH_INFO)(?![A-Za-z0-9_])",re.I)

def get(u):
 r=urllib.request.Request(u,headers={"User-Agent":"RIDI-primary-replay/1.0"})
 return urllib.request.urlopen(r,timeout=180).read()
def sha(b): return hashlib.sha256(b).hexdigest()
def normqa(s):
 s=unicodedata.normalize("NFKC",CITE_RE.sub(" ",str(s))).casefold()
 s="".join(" " if unicodedata.category(ch).startswith("P") else ch for ch in s)
 return " ".join(x for x in s.split() if x not in {"a","an","the"})
def normtext(s):
 s=unicodedata.normalize("NFKC",CITE_RE.sub(" ",str(s))).casefold()
 return " ".join(s.split())
def correct(ans,row):
 if row["dataset"] in {"nq","hotpotqa"}:
  p=normqa(ans); return p in [normqa(x) for x in row["gold"].get("answers",[])]
 m=STRICT.match(str(ans)); p=m.group(1).upper() if m else "UNPARSEABLE"
 gold={str(x).upper().replace(" ","_").replace("-","_") for x in row["gold"].get("labels",[])}
 return p in gold
def messages(row,ids):
 ps=[]
 for i,did in enumerate(ids,1):
  d=row["documents"][did]; title=str(d.get("title","")).strip(); body=str(d.get("text","")).strip()
  ps.append(f"[{i}] {title}\n{body}" if title else f"[{i}] {body}")
 block="\n\n".join(ps)
 if row["dataset"] in {"nq","hotpotqa"}:
  return [{"role":"system","content":"Use the provided passages to answer the question. Return only the shortest answer that directly answers the question. Do not include citations or explanations."},
          {"role":"user","content":f"Passages:\n{block}\n\nQuestion: {row['query']}\nAnswer:"}]
 return [{"role":"system","content":"Use the provided passages to classify the claim. Return exactly one label: SUPPORTS, REFUTES, or NOT_ENOUGH_INFO."},
         {"role":"user","content":f"Passages:\n{block}\n\nClaim: {row['query']}\nLabel:"}]

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--dataset",choices=list(EXPECTED_GZ),required=True); ap.add_argument("--batch-size",type=int,default=8)
 a=ap.parse_args(); d=a.dataset
 raw=get(f"{BASE}/{d}_sample.jsonl.gz")
 assert sha(raw)==EXPECTED_GZ[d]
 rows=[json.loads(x) for x in gzip.decompress(raw).decode().splitlines() if x.strip()]
 assert len(rows)==100
 os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG",":4096:8")
 import torch, transformers, huggingface_hub, accelerate
 from transformers import AutoTokenizer,AutoModelForCausalLM
 print("RIDI_REPLAY_ENV\t"+json.dumps({"python":sys.version.split()[0],"torch":torch.__version__,"transformers":transformers.__version__,"huggingface_hub":huggingface_hub.__version__,"accelerate":accelerate.__version__,"gpu":torch.cuda.get_device_name(0)},sort_keys=True),flush=True)
 torch.manual_seed(SEED); random.seed(SEED); torch.use_deterministic_algorithms(True)
 torch.backends.cuda.matmul.allow_tf32=False; torch.backends.cudnn.allow_tf32=False
 tok=AutoTokenizer.from_pretrained(MODEL_ID,revision=REVISION)
 if tok.pad_token_id is None: tok.pad_token_id=tok.eos_token_id
 tok.padding_side="left"
 model=AutoModelForCausalLM.from_pretrained(MODEL_ID,revision=REVISION,torch_dtype=torch.bfloat16,device_map="auto"); model.eval()
 recs=[]
 for qi,row in enumerate(rows,1):
  names=["k10_updated","k10_eta_0_001"]
  prompts=[tok.apply_chat_template(messages(row,row["states"][n]),tokenize=False,add_generation_prompt=True,enable_thinking=False) for n in names]
  enc=tok(prompts,return_tensors="pt",padding=True).to(model.device)
  with torch.inference_mode():
   gen=model.generate(**enc,max_new_tokens=128,do_sample=False,pad_token_id=tok.pad_token_id)
  w=enc["input_ids"].shape[1]
  answers=[tok.decode(gen[j,w:],skip_special_tokens=True).strip() for j in range(2)]
  u,c=answers; cu=bool(correct(u,row)); cc=bool(correct(c,row))
  f=row["frontier"]["k10_eta_0_001"]
  rec={"dataset":d,"query_id":str(row["query_id"]),
       "updated_correct":cu,"controlled_correct":cc,
       "correctness_difference":int(cc)-int(cu),
       "correctness_status_disagreement":int(cu!=cc),
       "answer_text_disagreement":int(normtext(u)!=normtext(c)),
       "updated_answer_sha256":hashlib.sha256(u.encode()).hexdigest(),
       "controlled_answer_sha256":hashlib.sha256(c.encode()).hexdigest(),
       "delta_unconstrained":int(f["delta_unconstrained"]),
       "j_eta":int(f["j_eta"]),
       "utility_regret":float(f["utility_regret"]),
       "avoidable_turnover_fraction":f["avoidable_turnover_fraction"]}
  recs.append(rec)
  print("RIDI_PRIMARY_RECORD\t"+json.dumps(rec,sort_keys=True),flush=True)
 print("RIDI_PRIMARY_REPLAY_SUMMARY\t"+json.dumps({
   "dataset":d,"n":100,
   "updated_accuracy":sum(x["updated_correct"] for x in recs)/100,
   "controlled_accuracy":sum(x["controlled_correct"] for x in recs)/100,
   "paired_accuracy_difference":sum(x["correctness_difference"] for x in recs)/100,
   "correctness_status_disagreement":sum(x["correctness_status_disagreement"] for x in recs)/100,
   "answer_text_disagreement":sum(x["answer_text_disagreement"] for x in recs)/100,
   "mean_delta_unconstrained":sum(x["delta_unconstrained"] for x in recs)/100,
   "mean_j_eta":sum(x["j_eta"] for x in recs)/100,
   "mean_reduction":sum(x["delta_unconstrained"]-x["j_eta"] for x in recs)/100},sort_keys=True),flush=True)
if __name__=="__main__": main()
