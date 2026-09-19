#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, random, re, sys, time, unicodedata, zipfile
from pathlib import Path
import requests

STUDY="LLM-EVAL-RELIABILITY-JKSU-v1"
MODELS={
 "qwen25":{"id":"Qwen/Qwen2.5-7B-Instruct","revision":"a09a35458c702b33eeacc393d103063234e8bc28"},
 "mistral":{"id":"mistralai/Mistral-7B-Instruct-v0.3","revision":"c170c708c41dac9275d15a8fff4eca08d52bab71"},
 "olmo2":{"id":"allenai/OLMo-2-1124-7B-Instruct","revision":"470b1fba1ae01581f270116362ee4aa1b97f4c84"},
 "phi35":{"id":"microsoft/Phi-3.5-mini-instruct","revision":"2fe192450127e6a83f7441aef6e3ca586c338b77"},
}
SEED=20260919

def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for x in iter(lambda:f.read(1<<20),b""):h.update(x)
    return h.hexdigest()
def nk(s):return unicodedata.normalize("NFKC",s)
def norm_choice(s):
    s=nk(s).casefold()
    s=re.sub(r"[\*_\~]","",s)
    s=re.sub(r"[^\w\s]"," ",s)
    return " ".join(s.split())

def e1(text,labels,choices):
    lines=[nk(x).strip() for x in text.splitlines() if nk(x).strip()]
    if not lines:return None
    m=re.fullmatch(r"Final answer:\s*([A-Z])",lines[-1])
    return m.group(1) if m and m.group(1) in labels else None
def e2(text,labels,choices):
    lines=[nk(x).strip() for x in text.splitlines() if nk(x).strip()]
    if not lines:return None
    line=lines[-1]
    m=re.search(r"(?i)final\s*answer\s*[:\-]?\s*[\*_\(\[]*\s*([A-Z])\s*[\)\]\*_\.\!]*\s*$",line)
    if m and m.group(1).upper() in labels:return m.group(1).upper()
    return None
def e3(text,labels,choices):
    hits=[x for x in re.findall(r"(?<![A-Za-z])([A-Z])(?![A-Za-z])",nk(text)) if x in labels]
    return hits[-1] if hits else None
def e4(text,labels,choices):
    lines=[x.strip() for x in nk(text).splitlines() if x.strip()]
    if not lines:return None
    q=norm_choice(lines[-1])
    hits=[lab for lab,txt in choices.items() if q==norm_choice(txt) or q==norm_choice("Final answer: "+txt)]
    return hits[0] if len(hits)==1 else None
def e5(text,labels,choices):
    return e2(text,labels,choices) or e4(text,labels,choices)
EVALS={"E1":e1,"E2":e2,"E3":e3,"E4":e4,"E5":e5}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-key",choices=MODELS,required=True)
    ap.add_argument("--panel-commit",required=True)
    ap.add_argument("--out",default="/tmp/jksu_eval")
    a=ap.parse_args()
    outdir=Path(a.out);outdir.mkdir(parents=True,exist_ok=True)
    url=f"https://raw.githubusercontent.com/adeebnoor/ridi/{a.panel_commit}/independent_studies/jksucis_evaluator_reliability/frozen/FROZEN_PANEL.jsonl"
    raw=requests.get(url,timeout=120);raw.raise_for_status()
    panel_bytes=raw.content
    rows=[json.loads(x) for x in raw.text.splitlines() if x.strip()]
    assert len(rows)==1000
    print("PANEL_SHA256",sha_bytes(panel_bytes),flush=True)

    os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG",":4096:8")
    import torch, transformers, accelerate, huggingface_hub
    from transformers import AutoTokenizer,AutoModelForCausalLM
    mcfg=MODELS[a.model_key]
    random.seed(SEED);torch.manual_seed(SEED)
    if torch.cuda.is_available():torch.cuda.manual_seed_all(SEED)
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    if not torch.cuda.is_available():raise RuntimeError("CUDA required")
    trc = False if a.model_key=="phi35" else True
    tok=AutoTokenizer.from_pretrained(mcfg["id"],revision=mcfg["revision"],trust_remote_code=trc)
    tok.padding_side="left"
    if tok.pad_token_id is None:tok.pad_token=tok.eos_token
    model=AutoModelForCausalLM.from_pretrained(
      mcfg["id"],revision=mcfg["revision"],torch_dtype=torch.bfloat16,
      device_map="auto",trust_remote_code=trc)
    model.eval()
    env={"python":sys.version.split()[0],"torch":torch.__version__,"transformers":transformers.__version__,
         "accelerate":accelerate.__version__,"huggingface_hub":huggingface_hub.__version__,
         "cuda":torch.version.cuda,"gpu":[torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
         "dtype":str(next(model.parameters()).dtype),"model_id":mcfg["id"],"revision":mcfg["revision"],
         "deterministic_algorithms":True,"tf32":False,"padding_side":tok.padding_side,"execution_batch_size":8}
    print("ENV",json.dumps(env,sort_keys=True),flush=True)

    def chat_text(prompt):
        msgs=[{"role":"user","content":prompt}]
        try:return tok.apply_chat_template(msgs,tokenize=False,add_generation_prompt=True)
        except Exception:return prompt
    recs=[];t0=time.time();batch_size=8
    for start in range(0,len(rows),batch_size):
        batch=rows[start:start+batch_size]
        texts=[chat_text(r["prompt"]) for r in batch]
        enc=tok(texts,return_tensors="pt",padding=True,add_special_tokens=False)
        enc={k:v.to(model.device) for k,v in enc.items()}
        with torch.inference_mode():
            gen=model.generate(**enc,do_sample=False,max_new_tokens=128,pad_token_id=tok.pad_token_id,use_cache=True)
        plen=enc["input_ids"].shape[1]
        for bi,r in enumerate(batch):
            tids=gen[bi,plen:].tolist()
            ans=tok.decode(tids,skip_special_tokens=True).strip()
            labels=[str(x) for x in r["valid_labels"]]; choices={str(k):str(v) for k,v in r["choice_texts"].items()}
            parsed={name:fn(ans,labels,choices) for name,fn in EVALS.items()}
            corr={name:(v==r["gold"]) if v is not None else False for name,v in parsed.items()}
            rec={"study":STUDY,"model_key":a.model_key,"model_id":mcfg["id"],"dataset":r["dataset"],
                 "item_id":r["item_id"],"bbh_task":r.get("bbh_task"),"gold":r["gold"],
                 "valid_labels":labels,"output":ans,"output_sha256":sha_bytes(ans.encode()),
                 "output_token_sha256":sha_bytes(json.dumps(tids,separators=(",",":")).encode()),
                 "parsed":parsed,"correct":corr,"output_tokens":len(tids),
                 "execution_batch_size":batch_size,"execution_batch_index":start//batch_size}
            recs.append(rec)
        done=min(start+batch_size,len(rows))
        if done%200==0 or done==len(rows):print("PROGRESS",a.model_key,done,len(rows),round(time.time()-t0,1),flush=True)

    rawp=outdir/f"{a.model_key}_records.jsonl"
    with rawp.open("w",encoding="utf-8") as f:
        for x in recs:f.write(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n")
    cells={}
    for d in ["arc_challenge","openbookqa","commonsenseqa","bbh"]:
        rr=[x for x in recs if x["dataset"]==d]
        cells[d]={}
        for e in EVALS:
            cells[d][e]={"n":len(rr),"correct":sum(x["correct"][e] for x in rr),
                         "unparsed":sum(x["parsed"][e] is None for x in rr)}
    summary={"study":STUDY,"model_key":a.model_key,"model":mcfg,"panel_commit":a.panel_commit,
             "panel_sha256":sha_bytes(panel_bytes),"environment":env,"cells":cells,
             "raw_sha256":sha_file(rawp),"elapsed_seconds":time.time()-t0}
    sp=outdir/f"{a.model_key}_summary.json";sp.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    zp=outdir/f"JKSU_EVAL_{a.model_key}.zip"
    with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
        for p in [rawp,sp]:z.write(p,p.name)
    print("FINAL_SUMMARY",json.dumps(summary,sort_keys=True),flush=True)
    print("FINAL_ZIP_SHA256",sha_file(zp),flush=True)
    try:
        with zp.open("rb") as f:
            resp=requests.post("https://tmpfiles.org/api/v1/upload",files={"file":(zp.name,f,"application/zip")},timeout=240)
        resp.raise_for_status()
        u=resp.json()["data"]["url"].replace("https://tmpfiles.org/","https://tmpfiles.org/dl/")
        print("FINAL_DOWNLOAD_URL",u,flush=True)
    except Exception as e:print("UPLOAD_ERROR",repr(e),flush=True)
if __name__=="__main__":main()
