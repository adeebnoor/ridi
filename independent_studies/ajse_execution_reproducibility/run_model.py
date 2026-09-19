#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, random, re, sys, time, unicodedata, zipfile
from pathlib import Path
import requests

STUDY="LLM-EXEC-REPRO-AJSE-v1"
MODELS={
 "qwen25":{"id":"Qwen/Qwen2.5-7B-Instruct","revision":"a09a35458c702b33eeacc393d103063234e8bc28"},
 "mistral":{"id":"mistralai/Mistral-7B-Instruct-v0.3","revision":"c170c708c41dac9275d15a8fff4eca08d52bab71"},
 "olmo2":{"id":"allenai/OLMo-2-1124-7B-Instruct","revision":"470b1fba1ae01581f270116362ee4aa1b97f4c84"},
 "phi35":{"id":"microsoft/Phi-3.5-mini-instruct","revision":"2fe192450127e6a83f7441aef6e3ca586c338b77"},
}
SEED=20260919
MAX_NEW={"mmlu_pro":96,"gsm8k":192}

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for x in iter(lambda:f.read(1<<20),b""):h.update(x)
    return h.hexdigest()
def norm_text(s):
    return " ".join(unicodedata.normalize("NFKC",s).casefold().split())
def extract_decision(dataset,text):
    if dataset=="mmlu_pro":
        ms=re.findall(r"(?i)final\s*answer\s*:\s*[\(\[]?\s*([A-J])\b",text)
        return ms[-1].upper() if ms else None
    ms=re.findall(r"(?i)final\s*answer\s*:\s*\$?\s*([-+]?\d[\d,]*(?:\.\d+)?)",text)
    if not ms:return None
    v=ms[-1].replace(",","")
    try:
        if "." in v:
            x=float(v)
            return str(int(x)) if x.is_integer() else str(x)
        return str(int(v))
    except:return v
def correct(dataset,decision,gold):
    if decision is None:return False
    if dataset=="mmlu_pro":return decision==gold
    try:return float(decision)==float(gold.replace(",",""))
    except:return decision==gold.replace(",","")
def first_diff(a,b):
    n=min(len(a),len(b))
    for i in range(n):
        if a[i]!=b[i]:return i
    return None if len(a)==len(b) else n

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model-key",choices=MODELS,required=True)
    ap.add_argument("--panel-commit",required=True)
    ap.add_argument("--out",default="/tmp/ajse_exec")
    a=ap.parse_args()
    outdir=Path(a.out);outdir.mkdir(parents=True,exist_ok=True)
    url=f"https://raw.githubusercontent.com/adeebnoor/ridi/{a.panel_commit}/independent_studies/ajse_execution_reproducibility/frozen/FROZEN_PANEL.jsonl"
    raw=requests.get(url,timeout=120);raw.raise_for_status()
    panel_bytes=raw.content
    rows=[json.loads(x) for x in raw.text.splitlines() if x.strip()]
    assert len(rows)==304 and sum(r["role"]=="target" for r in rows)==300
    print("PANEL_SHA256",sha_bytes(panel_bytes),flush=True)

    os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG",":4096:8")
    import torch, transformers, accelerate, huggingface_hub
    from transformers import AutoTokenizer,AutoModelForCausalLM
    mcfg=MODELS[a.model_key]
    random.seed(SEED);torch.manual_seed(SEED)
    if torch.cuda.is_available():torch.cuda.manual_seed_all(SEED)
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False
    if not torch.cuda.is_available():raise RuntimeError("CUDA required")
    trc = False if a.model_key=="phi35" else True
    tok=AutoTokenizer.from_pretrained(mcfg["id"],revision=mcfg["revision"],trust_remote_code=trc)
    tok.padding_side="left"
    if tok.pad_token_id is None: tok.pad_token=tok.eos_token
    model=AutoModelForCausalLM.from_pretrained(
        mcfg["id"],revision=mcfg["revision"],torch_dtype=torch.bfloat16,
        device_map="auto",trust_remote_code=trc
    )
    model.eval()
    env={"python":sys.version.split()[0],"torch":torch.__version__,"transformers":transformers.__version__,
         "accelerate":accelerate.__version__,"huggingface_hub":huggingface_hub.__version__,
         "cuda":torch.version.cuda,"gpu":[torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
         "dtype":str(next(model.parameters()).dtype),"model_id":mcfg["id"],"revision":mcfg["revision"],
         "deterministic_algorithms":True,"tf32":False,"padding_side":tok.padding_side}
    print("ENV",json.dumps(env,sort_keys=True),flush=True)

    def chat_text(prompt):
        msgs=[{"role":"user","content":prompt}]
        try:return tok.apply_chat_template(msgs,tokenize=False,add_generation_prompt=True)
        except Exception:return prompt
    for r in rows:
        r["_chat"]=chat_text(r["prompt"])
        ids=tok(r["_chat"],add_special_tokens=False)["input_ids"]
        r["_input_len"]=len(ids)
        r["_input_sha"]=sha_bytes(json.dumps(ids,separators=(",",":")).encode())

    groups={}
    for d in ["mmlu_pro","gsm8k"]:
        rr=[r for r in rows if r["dataset"]==d]
        ss=sorted(rr,key=lambda r:(r["_input_len"],r["item_id"]))
        groups[(d,"batch4-near")]=[ss[i:i+4] for i in range(0,152,4)]
        strata=[ss[i*38:(i+1)*38] for i in range(4)]
        groups[(d,"batch4-mixed")]=[[strata[j][i] for j in range(4)] for i in range(38)]
    grouping_path=outdir/f"{a.model_key}_grouping.json"
    grouping_path.write_text(json.dumps({
      f"{d}:{cond}":[[x["item_id"] for x in g] for g in gg]
      for (d,cond),gg in groups.items()
    },indent=2,sort_keys=True)+"\n",encoding="utf-8")

    outputs={r["item_id"]:{} for r in rows if r["role"]=="target"}
    tokens={r["item_id"]:{} for r in rows if r["role"]=="target"}

    def generate_batch(batch,dataset):
        texts=[r["_chat"] for r in batch]
        enc=tok(texts,return_tensors="pt",padding=True,add_special_tokens=False)
        enc={k:v.to(model.device) for k,v in enc.items()}
        with torch.inference_mode():
            gen=model.generate(**enc,do_sample=False,max_new_tokens=MAX_NEW[dataset],
                               pad_token_id=tok.pad_token_id,use_cache=True)
        plen=enc["input_ids"].shape[1]
        ans=[]
        for i in range(len(batch)):
            tids=gen[i,plen:].tolist()
            ans.append((tok.decode(tids,skip_special_tokens=True).strip(),tids))
        return ans

    t0=time.time()
    targets=[r for r in rows if r["role"]=="target"]
    for rep in ["solo-1","solo-2"]:
        for n,r in enumerate(targets,1):
            ans,tids=generate_batch([r],r["dataset"])[0]
            outputs[r["item_id"]][rep]=ans;tokens[r["item_id"]][rep]=tids
            if n%50==0:print("PROGRESS",a.model_key,rep,n,len(targets),round(time.time()-t0,1),flush=True)

    for cond in ["batch4-near","batch4-mixed"]:
        for d in ["mmlu_pro","gsm8k"]:
            for gi,g in enumerate(groups[(d,cond)],1):
                ans=generate_batch(g,d)
                for r,(txt,tids) in zip(g,ans):
                    if r["role"]=="target":
                        outputs[r["item_id"]][cond]=txt;tokens[r["item_id"]][cond]=tids
                if gi%10==0:print("PROGRESS",a.model_key,cond,d,gi,38,round(time.time()-t0,1),flush=True)

    recs=[]
    for r in targets:
        iid=r["item_id"];base=outputs[iid]["solo-1"];bt=tokens[iid]["solo-1"]
        br=extract_decision(r["dataset"],base)
        row={"study":STUDY,"model_key":a.model_key,"model_id":mcfg["id"],"dataset":r["dataset"],
             "item_id":iid,"gold":r["gold"],"input_len":r["_input_len"],"input_token_sha256":r["_input_sha"],
             "solo1_correct":correct(r["dataset"],br,r["gold"])}
        row["outputs"]=outputs[iid]
        row["decisions"]={c:extract_decision(r["dataset"],outputs[iid][c]) for c in outputs[iid]}
        row["output_sha256"]={c:sha_bytes(outputs[iid][c].encode()) for c in outputs[iid]}
        row["token_sha256"]={c:sha_bytes(json.dumps(tokens[iid][c],separators=(",",":")).encode()) for c in tokens[iid]}
        row["comparisons"]={}
        for c in ["solo-2","batch4-near","batch4-mixed"]:
            dec=row["decisions"][c]
            row["comparisons"][c]={
              "exact_text_changed":outputs[iid][c]!=base,
              "normalized_text_changed":norm_text(outputs[iid][c])!=norm_text(base),
              "decision_changed":dec!=br,
              "correctness_changed":correct(r["dataset"],dec,r["gold"])!=row["solo1_correct"],
              "first_token_diff":first_diff(bt,tokens[iid][c])
            }
        recs.append(row)

    rawp=outdir/f"{a.model_key}_records.jsonl"
    with rawp.open("w",encoding="utf-8") as f:
        for x in recs:f.write(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n")
    cells={}
    for d in ["mmlu_pro","gsm8k"]:
        rr=[x for x in recs if x["dataset"]==d]
        for c in ["solo-2","batch4-near","batch4-mixed"]:
            cc=[x["comparisons"][c] for x in rr]
            cells[f"{d}:{c}"]={
              "n":len(rr),
              "exact_text_changed":sum(x["exact_text_changed"] for x in cc),
              "normalized_text_changed":sum(x["normalized_text_changed"] for x in cc),
              "decision_changed":sum(x["decision_changed"] for x in cc),
              "correctness_changed":sum(x["correctness_changed"] for x in cc)
            }
    summary={"study":STUDY,"model_key":a.model_key,"model":mcfg,"panel_commit":a.panel_commit,
             "panel_sha256":sha_bytes(panel_bytes),"environment":env,"cells":cells,
             "raw_sha256":sha_file(rawp),"grouping_sha256":sha_file(grouping_path),
             "elapsed_seconds":time.time()-t0}
    sp=outdir/f"{a.model_key}_summary.json";sp.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    zp=outdir/f"AJSE_EXEC_{a.model_key}.zip"
    with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
        for p in [rawp,sp,grouping_path]:z.write(p,p.name)
    print("FINAL_SUMMARY",json.dumps(summary,sort_keys=True),flush=True)
    print("FINAL_ZIP_SHA256",sha_file(zp),flush=True)
    try:
        with zp.open("rb") as f:
            resp=requests.post("https://tmpfiles.org/api/v1/upload",files={"file":(zp.name,f,"application/zip")},timeout=240)
        resp.raise_for_status()
        u=resp.json()["data"]["url"].replace("https://tmpfiles.org/","https://tmpfiles.org/dl/")
        print("FINAL_DOWNLOAD_URL",u,flush=True)
    except Exception as e: print("UPLOAD_ERROR",repr(e),flush=True)

if __name__=="__main__":main()
