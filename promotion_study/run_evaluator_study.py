#!/usr/bin/env python3
from __future__ import annotations
import argparse,base64,hashlib,json,os,random,sys,time,zipfile
from pathlib import Path
import numpy as np
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG",":4096:8")
import torch,transformers,accelerate,huggingface_hub,datasets
from transformers import AutoModelForCausalLM,AutoTokenizer
from freeze_inputs import reconstruct
from evaluators import EVALUATORS

SEED=20260919
MAX_NEW=96
MODELS={
 "qwen25_3b":("Qwen/Qwen2.5-3B-Instruct","aa8e72537993ba99e69dfaafa59ed015b17504d1"),
 "phi35_mini":("microsoft/Phi-3.5-mini-instruct","2fe192450127e6a83f7441aef6e3ca586c338b77"),
 "smollm2_17b":("HuggingFaceTB/SmolLM2-1.7B-Instruct","31b70e2e869a7173562077fd711b654946d38674")
}
LETTERS="ABCDE"
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha_text(s):return sha_bytes(s.encode("utf-8"))

def item(key,row):
    head="Answer the question. You may explain briefly. End with exactly one line beginning FINAL:. "
    if key=="commonsenseqa":
        labels=row["choices"]["label"];opts=row["choices"]["text"];q=row["question"];gold=row["answerKey"];task="mc"
    elif key=="openbookqa":
        labels=row["choices"]["label"];opts=row["choices"]["text"];q=row["question_stem"];gold=row["answerKey"];task="mc"
    elif key=="hellaswag":
        labels=list(LETTERS[:len(row["endings"])]);opts=row["endings"];q=row["ctx"];gold=labels[int(row["label"])];task="mc"
    elif key=="boolq":
        task="bool";labels=["yes","no"];opts=["yes","no"];q="Passage:\n"+row["passage"]+"\n\nQuestion: "+row["question"];gold="yes" if bool(row["answer"]) else "no"
    else:raise KeyError(key)
    if task=="mc":
        body="\n".join(f"{a}. {b}" for a,b in zip(labels,opts))
        prompt=head+"On the FINAL line give only the option letter.\n\nQuestion/context:\n"+q+"\n\nOptions:\n"+body
    else:
        prompt=head+"On the FINAL line give only yes or no.\n\n"+q
    return {"prompt":prompt,"task":task,"labels":labels,"options":opts,"gold":gold}

def set_det():
    random.seed(SEED);np.random.seed(SEED);torch.manual_seed(SEED)
    if torch.cuda.is_available():torch.cuda.manual_seed_all(SEED)
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model",choices=MODELS,required=True)
    ap.add_argument("--out",type=Path,default=Path("/tmp/jks_eval"))
    ap.add_argument("--emit-zip-base64",action="store_true")
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    panels,freeze_summary=reconstruct();mid,rev=MODELS[a.model]
    print("FROZEN_PANEL_VERIFIED",json.dumps(freeze_summary,sort_keys=True),flush=True)
    tok=AutoTokenizer.from_pretrained(mid,revision=rev,use_fast=True,trust_remote_code=False)
    if tok.pad_token_id is None:tok.pad_token=tok.eos_token
    set_det()
    if not torch.cuda.is_available():raise RuntimeError("CUDA GPU required for locked execution; do not silently substitute CPU/quantization")
    model=AutoModelForCausalLM.from_pretrained(mid,revision=rev,torch_dtype=torch.bfloat16,device_map="auto",trust_remote_code=False)
    model.eval()
    env={
      "python":sys.version.split()[0],"torch":torch.__version__,"transformers":transformers.__version__,
      "accelerate":accelerate.__version__,"huggingface_hub":huggingface_hub.__version__,
      "datasets":datasets.__version__,"cuda":torch.version.cuda,
      "gpu":[torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
      "dtype":str(next(model.parameters()).dtype),"batch_size":1,"seed":SEED,
      "max_new_tokens":MAX_NEW,"deterministic_algorithms":True,"tf32":False,
      "model_id":mid,"revision":rev
    }
    print("ENV",json.dumps(env,sort_keys=True),flush=True)
    raw=a.out/f"{a.model}_raw.jsonl";n=0;t0=time.time()
    with raw.open("w",encoding="utf-8") as f:
      for key,panel in panels.items():
        for rid,row in panel:
          it=item(key,row)
          chat=[{"role":"user","content":it["prompt"]}]
          text=tok.apply_chat_template(chat,tokenize=False,add_generation_prompt=True)
          enc=tok(text,return_tensors="pt",add_special_tokens=False).to(model.device)
          with torch.inference_mode():
            out=model.generate(**enc,do_sample=False,max_new_tokens=MAX_NEW,pad_token_id=tok.pad_token_id)
          ans=tok.decode(out[0,enc["input_ids"].shape[1]:],skip_special_tokens=True).strip()
          decisions={name:fn(ans,it["task"],it["labels"],it["options"]) for name,fn in EVALUATORS.items()}
          correct={name:(d==it["gold"]) for name,d in decisions.items()}
          rec={
            "study":"EVAL-RANK-JKSUCIS-v1","model":a.model,"model_id":mid,"revision":rev,
            "dataset":key,"id":rid,"task":it["task"],"gold":it["gold"],
            "labels":it["labels"],"options":it["options"],
            "prompt_sha256":sha_text(it["prompt"]),"raw_output":ans,
            "raw_output_sha256":sha_text(ans),"decisions":decisions,"correct":correct
          }
          f.write(json.dumps(rec,ensure_ascii=False,sort_keys=True)+"\n");f.flush()
          print("JKS_RECORD\t"+json.dumps({"dataset":key,"id":rid,"raw_sha256":rec["raw_output_sha256"],"decisions":decisions,"correct":correct},sort_keys=True),flush=True)
          n+=1
          if n%50==0:print("PROGRESS",n,"/1000",round(time.time()-t0,1),flush=True)
    manifest={"study":"EVAL-RANK-JKSUCIS-v1","model":a.model,"environment":env,"frozen_panel":freeze_summary,"raw_sha256":sha_bytes(raw.read_bytes()),"records":n}
    mp=a.out/f"{a.model}_execution_manifest.json"
    mp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    zp=a.out/f"JKSUCIS_{a.model}_RESULTS.zip"
    with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
        z.write(raw,raw.name);z.write(mp,mp.name)
    print("FINAL_ZIP_SHA256",sha_bytes(zp.read_bytes()),"BYTES",zp.stat().st_size,flush=True)
    if a.emit_zip_base64:
      b64=base64.b64encode(zp.read_bytes()).decode();chunk=16000;total=(len(b64)+chunk-1)//chunk
      for i in range(total):print(f"ZIP_CHUNK\t{i}\t{total}\t{b64[i*chunk:(i+1)*chunk]}",flush=True)
if __name__=="__main__":main()
