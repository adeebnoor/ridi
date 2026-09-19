#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, hashlib, json, os, random, re, sys, time, zipfile
from pathlib import Path
import numpy as np

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG",":4096:8")

import torch
import transformers, accelerate, huggingface_hub, datasets
from transformers import AutoModelForCausalLM, AutoTokenizer
from freeze_inputs import reconstruct

SEED=20260919
MAX_NEW=96
MODELS={
 "qwen25_7b":("Qwen/Qwen2.5-7B-Instruct","a09a35458c702b33eeacc393d103063234e8bc28"),
 "mistral7b_v03":("mistralai/Mistral-7B-Instruct-v0.3","c170c708c41dac9275d15a8fff4eca08d52bab71"),
}
LETTERS="ABCDEFGHIJ"

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_text(s): return sha_bytes(s.encode("utf-8"))
def canonical_text(s): return " ".join(s.casefold().split())

def task_prompt(key,row):
    head="Answer the problem. You may reason briefly. End with exactly one line beginning FINAL:. "
    if key=="gsm8k":
        q=row["question"]
        return head+"On the FINAL line give only the numeric answer.\n\nQuestion: "+q
    if key=="mmlu_pro":
        opts=row["options"]
        body="\n".join(f"{LETTERS[i]}. {x}" for i,x in enumerate(opts))
        return head+"On the FINAL line give only the option letter.\n\nQuestion: "+row["question"]+"\n\nOptions:\n"+body
    if key=="arc_challenge":
        labels=row["choices"]["label"]; texts=row["choices"]["text"]
        body="\n".join(f"{a}. {b}" for a,b in zip(labels,texts))
        return head+"On the FINAL line give only the option letter.\n\nQuestion: "+row["question"]+"\n\nOptions:\n"+body
    if key=="truthfulqa_mc":
        opts=row["mc1_targets"]["choices"]
        body="\n".join(f"{LETTERS[i]}. {x}" for i,x in enumerate(opts))
        return head+"On the FINAL line give only the option letter.\n\nQuestion: "+row["question"]+"\n\nOptions:\n"+body
    raise KeyError(key)

def gold_answer(key,row):
    if key=="gsm8k":
        m=re.search(r"####\s*([-+]?(?:\d[\d,]*)(?:\.\d+)?)",row["answer"])
        if not m: raise RuntimeError("GSM8K gold parse failure")
        return m.group(1).replace(",","")
    if key=="mmlu_pro": return str(row["answer"]).strip().upper()
    if key=="arc_challenge": return str(row["answerKey"]).strip().upper()
    if key=="truthfulqa_mc":
        labs=row["mc1_targets"]["labels"]
        idx=[i for i,x in enumerate(labs) if int(x)==1]
        if len(idx)!=1: raise RuntimeError("TruthfulQA mc1 gold not unique")
        return LETTERS[idx[0]]
    raise KeyError(key)

def final_decision(key,text):
    lines=[x.strip() for x in text.strip().splitlines() if x.strip()]
    cand=None
    for line in lines:
        m=re.fullmatch(r"FINAL\s*:\s*(.+?)\s*",line,re.I)
        if m: cand=m.group(1).strip()
    if cand is None: return None
    if key=="gsm8k":
        m=re.fullmatch(r"[-+]?(?:\d[\d,]*)(?:\.\d+)?",cand.replace("$","").strip())
        return m.group(0).replace(",","") if m else None
    m=re.fullmatch(r"[\(\[\{]?\s*([A-J])\s*[\)\]\}\.\!\?]?",cand,re.I)
    return m.group(1).upper() if m else None

def build_plans(ids,prompts,tok):
    lengths={}
    for rid in ids:
        text=tok.apply_chat_template([{"role":"user","content":prompts[rid]}],tokenize=False,add_generation_prompt=True)
        lengths[rid]=len(tok(text,add_special_tokens=False)["input_ids"])
    ordered=sorted(ids,key=lambda x:(lengths[x],x))
    vals=np.asarray([lengths[x] for x in ordered],dtype=float)
    qtargets=np.quantile(vals,[.05,.20,.35,.50,.65,.80,.95],method="nearest")
    plans={}
    for rid in ids:
        others=[x for x in ids if x!=rid]
        matched=sorted(others,key=lambda x:(abs(lengths[x]-lengths[rid]),x))[:7]
        used=set(); mixed=[]
        for q in qtargets:
            candidates=[x for x in others if x not in used]
            pick=min(candidates,key=lambda x:(abs(lengths[x]-float(q)),x))
            used.add(pick); mixed.append(pick)
        plans[rid]={
          "A":[rid],
          "B":[rid]+matched,
          "C":[rid]+mixed,
          "D":list(reversed([rid]+mixed)),
        }
    payload=json.dumps({"lengths":lengths,"plans":plans},sort_keys=True,separators=(",",":"))
    return lengths,plans,sha_text(payload)

def set_determinism():
    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(SEED)
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False

def generate_batch(model,tok,prompt_map,batch_ids):
    chats=[[{"role":"user","content":prompt_map[x]}] for x in batch_ids]
    texts=[tok.apply_chat_template(c,tokenize=False,add_generation_prompt=True) for c in chats]
    indiv=[tok(t,add_special_tokens=False)["input_ids"] for t in texts]
    enc=tok(texts,return_tensors="pt",padding=True,add_special_tokens=False)
    mask=enc["attention_mask"]
    for i,ids in enumerate(indiv):
        got=enc["input_ids"][i][mask[i].bool()].tolist()
        if got!=ids: raise RuntimeError("Target token IDs changed under batching")
    enc={k:v.to(model.device) for k,v in enc.items()}
    with torch.inference_mode():
        out=model.generate(**enc,do_sample=False,max_new_tokens=MAX_NEW,pad_token_id=tok.pad_token_id)
    inlen=enc["input_ids"].shape[1]
    return [tok.decode(out[i,inlen:],skip_special_tokens=True).strip() for i in range(len(batch_ids))]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model",choices=MODELS,required=True)
    ap.add_argument("--out",type=Path,default=Path("/tmp/ajse_repro"))
    ap.add_argument("--emit-zip-base64",action="store_true")
    a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    panels,freeze_summary=reconstruct()
    model_id,rev=MODELS[a.model]
    print("FROZEN_PANEL_VERIFIED",json.dumps(freeze_summary,sort_keys=True),flush=True)

    tok=AutoTokenizer.from_pretrained(model_id,revision=rev,use_fast=True)
    tok.padding_side="left"
    if tok.pad_token_id is None: tok.pad_token=tok.eos_token

    prepared={}
    plan_hashes={}
    for key,panel in panels.items():
        ids=[rid for rid,_ in panel]
        prompt_map={rid:task_prompt(key,row) for rid,row in panel}
        row_map={rid:row for rid,row in panel}
        lengths,plans,ph=build_plans(ids,prompt_map,tok)
        prepared[key]=(ids,prompt_map,row_map,lengths,plans)
        plan_hashes[key]=ph
    plan_manifest_sha=sha_text(json.dumps(plan_hashes,sort_keys=True,separators=(",",":")))
    print("COMPANION_PLAN_SHA256",plan_manifest_sha,json.dumps(plan_hashes,sort_keys=True),flush=True)

    set_determinism()
    if not torch.cuda.is_available(): raise RuntimeError("CUDA GPU required; CPU/quantized fallback is prohibited by protocol")
    model=AutoModelForCausalLM.from_pretrained(model_id,revision=rev,torch_dtype=torch.bfloat16,device_map="auto")
    model.eval()
    env={
      "python":sys.version.split()[0],"torch":torch.__version__,"transformers":transformers.__version__,
      "accelerate":accelerate.__version__,"huggingface_hub":huggingface_hub.__version__,
      "datasets":datasets.__version__,"cuda":torch.version.cuda,
      "gpu":[torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
      "dtype":str(next(model.parameters()).dtype),"seed":SEED,"max_new_tokens":MAX_NEW,
      "deterministic_algorithms":True,"tf32":False,"cublas_workspace_config":os.environ.get("CUBLAS_WORKSPACE_CONFIG"),
      "model_id":model_id,"revision":rev,"companion_plan_sha256":plan_manifest_sha,
    }
    print("ENV",json.dumps(env,sort_keys=True),flush=True)

    raw=a.out/f"{a.model}_raw.jsonl"
    t0=time.time(); n=0
    with raw.open("w",encoding="utf-8") as f:
      for key,(ids,prompt_map,row_map,lengths,plans) in prepared.items():
        for rid in ids:
          rec={"model":a.model,"model_id":model_id,"revision":rev,"dataset":key,"id":rid,
               "prompt_sha256":sha_text(prompt_map[rid]),"prompt_tokens":lengths[rid],
               "gold":gold_answer(key,row_map[rid]),"conditions":{}}
          for condition in ["A","B","C","D"]:
            batch_ids=plans[rid][condition]
            target_index=batch_ids.index(rid)
            outs=[]
            for repeat in [1,2]:
              texts=generate_batch(model,tok,prompt_map,batch_ids)
              target=texts[target_index]
              outs.append(target)
            rec["conditions"][condition]={
              "batch_ids":batch_ids,"batch_size":len(batch_ids),"target_index":target_index,
              "repeat_text_sha256":[sha_text(x) for x in outs],
              "repeat_normalized_sha256":[sha_text(canonical_text(x)) for x in outs],
              "repeat_decision":[final_decision(key,x) for x in outs],
              "repeat_correct":[final_decision(key,x)==rec["gold"] for x in outs],
              "repeat_output":outs,
            }
          f.write(json.dumps(rec,ensure_ascii=False,sort_keys=True)+"\n"); f.flush()
          compact={"dataset":key,"id":rid,
                   "A_sha":rec["conditions"]["A"]["repeat_text_sha256"],
                   "C_sha":rec["conditions"]["C"]["repeat_text_sha256"],
                   "A_dec":rec["conditions"]["A"]["repeat_decision"],
                   "C_dec":rec["conditions"]["C"]["repeat_decision"]}
          print("AJSE_RECORD\t"+json.dumps(compact,sort_keys=True),flush=True)
          n+=1
          if n%25==0: print("PROGRESS",n,"/",sum(len(x[0]) for x in prepared.values()),round(time.time()-t0,1),flush=True)

    manifest={"study":"LLM-EXEC-REPRO-AJSE-v1","model":a.model,"environment":env,
              "frozen_panel":freeze_summary,"raw_sha256":sha_bytes(raw.read_bytes()),"records":n}
    mp=a.out/f"{a.model}_execution_manifest.json";mp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    zp=a.out/f"AJSE_{a.model}_RESULTS.zip"
    with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
        z.write(raw,raw.name); z.write(mp,mp.name)
    print("FINAL_ZIP_SHA256",sha_bytes(zp.read_bytes()),"BYTES",zp.stat().st_size,flush=True)
    if a.emit_zip_base64:
        b64=base64.b64encode(zp.read_bytes()).decode(); chunk=16000
        total=(len(b64)+chunk-1)//chunk
        for i in range(total): print(f"ZIP_CHUNK\t{i}\t{total}\t{b64[i*chunk:(i+1)*chunk]}",flush=True)

if __name__=="__main__": main()
