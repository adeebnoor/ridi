#!/usr/bin/env python3
from __future__ import annotations

import argparse, gzip, hashlib, io, json, os, random, re, string, sys, time, unicodedata, urllib.request, zipfile
from pathlib import Path

FROZEN_COMMIT="f98be71b4402d95a3337dac78f272c3aa55cbd62"
MODEL_ID="Qwen/Qwen3-8B"
REVISION="b968826d9c46dd6066d109eabc6255188de91218"
SEED=20260902
MAX_NEW_TOKENS=128
KS=(5,10,20)
STATE_SUFFIXES=("reference","updated","eta_0_0001","eta_0_001")
EXPECTED_GZ={
 "nq":"3f982bf2297d0f0b3d66fd4d8fa22a13513ad12ba4ead6c2ec6f63bcae0361d3",
 "hotpotqa":"43e65af6dc474b58f620344dea57476126d5ef5121e932b765a72bde6c489514",
 "fever":"27e92d6cd3c6de13bfad0c5ced65544bb037bcbe3010175c81665bdc57169011",
 "scifact":"7980a59a5e4af42d75af4f483007d3b95b8196d138962b523abf86fddfc24970",
}
BASE=f"https://raw.githubusercontent.com/adeebnoor/ridi/{FROZEN_COMMIT}/experiments/frontier_downstream_rag/frozen"

CITE_RE=re.compile(r"\[\s*\d+(?:\s*[,;\-]\s*\d+)*\s*\]")
STRICT_CLASS_RE=re.compile(r"\A\s*(SUPPORTS|REFUTES|NOT_ENOUGH_INFO)(?![A-Za-z0-9_])",re.I)
WRAPPER_CLASS_RE=re.compile(
 r"\A\s*(?:[>#*_\x60]+\s*)*"
 r"(?:(?:verdict|answer|label|classification)\s*:\s*(?:[*_\x60]+\s*)*)?"
 r"(NOT_ENOUGH_INFO|SUPPORTS|REFUTES)(?![A-Za-z0-9_])",re.I
)

def sha_bytes(b:bytes)->str:return hashlib.sha256(b).hexdigest()

def get(url:str)->bytes:
 req=urllib.request.Request(url,headers={"User-Agent":"RIDI-frontier-downstream-generation/1.0"})
 with urllib.request.urlopen(req,timeout=180) as r:return r.read()

def strip_citations(s:str)->str:return CITE_RE.sub(" ",str(s))

def normalize_qa(s:str)->str:
 s=unicodedata.normalize("NFKC",strip_citations(s)).casefold()
 s="".join(" " if unicodedata.category(ch).startswith("P") else ch for ch in s)
 toks=[x for x in s.split() if x not in {"a","an","the"}]
 return " ".join(toks)

def normalize_text(s:str)->str:
 s=unicodedata.normalize("NFKC",strip_citations(s)).casefold()
 return " ".join(s.split())

def qa_correct(answer:str,gold:dict,substring:bool=False)->bool:
 pred=normalize_qa(answer)
 vals=[normalize_qa(x) for x in gold.get("answers",[]) if str(x).strip()]
 if substring:return any(v and v in pred for v in vals)
 return pred in vals

def class_pred(answer:str,wrapper:bool=False)->str:
 m=(WRAPPER_CLASS_RE if wrapper else STRICT_CLASS_RE).match(str(answer))
 return m.group(1).upper() if m else "UNPARSEABLE"

def class_correct(answer:str,gold:dict,wrapper:bool=False)->bool:
 accepted={str(x).upper().replace(" ","_").replace("-","_") for x in gold.get("labels",[])}
 return class_pred(answer,wrapper) in accepted

def make_messages(row:dict,docids:list[str])->list[dict]:
 parts=[]
 for i,did in enumerate(docids,1):
  d=row["documents"][did]
  title=str(d.get("title","")).strip()
  body=str(d.get("text","")).strip()
  if title: parts.append(f"[{i}] {title}\n{body}")
  else: parts.append(f"[{i}] {body}")
 passages="\n\n".join(parts)
 if row["dataset"] in {"nq","hotpotqa"}:
  system="Use the provided passages to answer the question. Return only the shortest answer that directly answers the question. Do not include citations or explanations."
  user=f"Passages:\n{passages}\n\nQuestion: {row['query']}\nAnswer:"
 else:
  system="Use the provided passages to classify the claim. Return exactly one label: SUPPORTS, REFUTES, or NOT_ENOUGH_INFO."
  user=f"Passages:\n{passages}\n\nClaim: {row['query']}\nLabel:"
 return [{"role":"system","content":system},{"role":"user","content":user}]

def score(answer:str,row:dict)->dict:
 if row["dataset"] in {"nq","hotpotqa"}:
  return {"primary":qa_correct(answer,row["gold"],False),
          "sensitivity":qa_correct(answer,row["gold"],True),
          "parsed":None}
 return {"primary":class_correct(answer,row["gold"],False),
         "sensitivity":class_correct(answer,row["gold"],True),
         "parsed":class_pred(answer,False),
         "parsed_sensitivity":class_pred(answer,True)}

def aggregate(records:list[dict])->dict:
 out={"dataset":records[0]["dataset"],"n":len(records),"cells":{}}
 for k in KS:
  upd=f"k{k}_updated"
  for eta in ("eta_0_0001","eta_0_001"):
   ctl=f"k{k}_{eta}"
   key=f"k{k}_{eta}"
   n=len(records)
   au=sum(r["responses"][upd]["score"]["primary"] for r in records)/n
   ac=sum(r["responses"][ctl]["score"]["primary"] for r in records)/n
   au2=sum(r["responses"][upd]["score"]["sensitivity"] for r in records)/n
   ac2=sum(r["responses"][ctl]["score"]["sensitivity"] for r in records)/n
   flips=sum(r["responses"][upd]["score"]["primary"]!=r["responses"][ctl]["score"]["primary"] for r in records)
   txt=sum(r["responses"][upd]["normalized_text"]!=r["responses"][ctl]["normalized_text"] for r in records)
   out["cells"][key]={
    "updated_accuracy_primary":au,"controlled_accuracy_primary":ac,
    "paired_accuracy_difference_primary":ac-au,
    "correctness_status_disagreement_primary":flips/n,
    "answer_text_disagreement":txt/n,
    "updated_accuracy_sensitivity":au2,"controlled_accuracy_sensitivity":ac2,
    "paired_accuracy_difference_sensitivity":ac2-au2,
   }
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--dataset",choices=list(EXPECTED_GZ),required=True)
 ap.add_argument("--out",type=Path,default=Path("/tmp/ridi_frontier_generation"))
 ap.add_argument("--batch-size",type=int,default=4)
 ap.add_argument("--emit-archive-b64",action="store_true")
 a=ap.parse_args();d=a.dataset;a.out.mkdir(parents=True,exist_ok=True)
 raw=get(f"{BASE}/{d}_sample.jsonl.gz")
 if sha_bytes(raw)!=EXPECTED_GZ[d]:raise RuntimeError("frozen sample gzip SHA-256 mismatch")
 rows=[json.loads(x) for x in gzip.decompress(raw).decode().splitlines() if x.strip()]
 if len(rows)!=100:raise RuntimeError(f"expected 100 rows, got {len(rows)}")
 print("RIDI_RECOVERY_MODE\\texact-original-12-state-batch-composition",flush=True)

 os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG",":4096:8")
 import torch, transformers, huggingface_hub, accelerate
 from transformers import AutoTokenizer, AutoModelForCausalLM
 versions={"python":sys.version.split()[0],"torch":torch.__version__,"transformers":transformers.__version__,
           "huggingface_hub":huggingface_hub.__version__,"accelerate":accelerate.__version__,
           "cuda":torch.version.cuda,"gpu":torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}
 print("RIDI_ENV\t"+json.dumps(versions,sort_keys=True),flush=True)
 if not torch.cuda.is_available():raise RuntimeError("CUDA GPU required")
 torch.manual_seed(SEED);random.seed(SEED)
 torch.use_deterministic_algorithms(True)
 torch.backends.cuda.matmul.allow_tf32=False
 torch.backends.cudnn.allow_tf32=False

 tok=AutoTokenizer.from_pretrained(MODEL_ID,revision=REVISION)
 if tok.pad_token_id is None:tok.pad_token_id=tok.eos_token_id
 tok.padding_side="left"
 model=AutoModelForCausalLM.from_pretrained(MODEL_ID,revision=REVISION,torch_dtype=torch.bfloat16,device_map="auto")
 model.eval()

 result_path=a.out/f"{d}_frontier_downstream_raw.jsonl"
 records=[];calls=0;t0=time.time()
 with result_path.open("w",encoding="utf-8") as fh:
  for qi,row in enumerate(rows,1):
   prompts=[];names=[]
   for k in KS:
    for suffix in STATE_SUFFIXES:
     name=f"k{k}_{suffix}";names.append(name)
     messages=make_messages(row,row["states"][name])
     p=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
     prompts.append(p)
   answers={}
   for st in range(0,len(prompts),a.batch_size):
    batch=prompts[st:st+a.batch_size];bnames=names[st:st+a.batch_size]
    enc=tok(batch,return_tensors="pt",padding=True).to(model.device)
    with torch.inference_mode():
     gen=model.generate(**enc,max_new_tokens=MAX_NEW_TOKENS,do_sample=False,pad_token_id=tok.pad_token_id)
    lens=enc["attention_mask"].sum(dim=1).tolist()
    # left padding: generated tokens begin at common padded input width
    input_width=enc["input_ids"].shape[1]
    for j,nm in enumerate(bnames):
     ans=tok.decode(gen[j,input_width:],skip_special_tokens=True).strip()
     answers[nm]=ans
     calls+=1
   responses={}
   for nm,ans in answers.items():
    responses[nm]={"answer":ans,"answer_sha256":hashlib.sha256(ans.encode()).hexdigest(),
                   "normalized_text":normalize_text(ans),"score":score(ans,row)}
   rec={"dataset":d,"query_id":str(row["query_id"]),"gold":row["gold"],
        "responses":responses,
        "primary_frontier":row["frontier"]["k10_eta_0_001"],
        "sample_sha256":EXPECTED_GZ[d]}
   u=responses["k10_updated"]; c=responses["k10_eta_0_001"]; pf=rec["primary_frontier"]
   compact={"dataset":d,"query_id":str(row["query_id"]),
            "updated_correct":bool(u["score"]["primary"]),"controlled_correct":bool(c["score"]["primary"]),
            "correctness_difference":int(bool(c["score"]["primary"]))-int(bool(u["score"]["primary"])),
            "correctness_status_disagreement":int(bool(u["score"]["primary"])!=bool(c["score"]["primary"])),
            "answer_text_disagreement":int(u["normalized_text"]!=c["normalized_text"]),
            "updated_answer_sha256":u["answer_sha256"],"controlled_answer_sha256":c["answer_sha256"],
            "delta_unconstrained":int(pf["delta_unconstrained"]),"j_eta":int(pf["j_eta"]),
            "utility_regret":float(pf["utility_regret"]),"avoidable_turnover_fraction":pf["avoidable_turnover_fraction"]}
   print("RIDI_PRIMARY_RECORD\\t"+json.dumps(compact,sort_keys=True),flush=True)
   records.append(rec);fh.write(json.dumps(rec,ensure_ascii=False,sort_keys=True)+"\n");fh.flush()
   if qi%10==0:print(f"RIDI_PROGRESS\t{d}\t{qi}/100\tcalls={calls}\telapsed={time.time()-t0:.1f}",flush=True)

 summary=aggregate(records)
 summary.update({"study":"RIDI-NATURE-FRONTIER-DOWNSTREAM-v1","model_id":MODEL_ID,"revision":REVISION,
                 "seed":SEED,"max_new_tokens":MAX_NEW_TOKENS,"enable_thinking":False,
                 "generation_calls":calls,"environment":versions,"frozen_panel_commit":FROZEN_COMMIT,
                 "raw_sha256":sha_bytes(result_path.read_bytes()),"elapsed_seconds":time.time()-t0})
 summary_path=a.out/f"{d}_summary.json";summary_path.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
 env_path=a.out/f"{d}_environment.json";env_path.write_text(json.dumps(versions,indent=2,sort_keys=True)+"\n")
 zip_path=a.out/f"RIDI_FRONTIER_DOWNSTREAM_{d.upper()}_RESULTS.zip"
 with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as z:
  z.write(result_path,result_path.name);z.write(summary_path,summary_path.name);z.write(env_path,env_path.name)
 print("RIDI_SUMMARY\t"+json.dumps(summary,sort_keys=True),flush=True)
 print("RIDI_ZIP_SHA256\t"+sha_bytes(zip_path.read_bytes()),flush=True)
 try:
  import requests
  with zip_path.open("rb") as f:
   resp=requests.post("https://tmpfiles.org/api/v1/upload",files={"file":(zip_path.name,f,"application/zip")},timeout=180)
  resp.raise_for_status()
  url=resp.json()["data"]["url"].replace("https://tmpfiles.org/","https://tmpfiles.org/dl/")
  print("RIDI_DOWNLOAD_URL\t"+url,flush=True)
 except Exception as e:
  print("RIDI_UPLOAD_ERROR\t"+repr(e),flush=True)
 return 0

if __name__=="__main__":
 raise SystemExit(main())
