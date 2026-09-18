# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "torch==2.11.0",
#   "transformers==4.57.6",
#   "accelerate==1.14.0",
#   "huggingface_hub==0.36.2",
#   "requests>=2.32",
# ]
# ///
from __future__ import annotations
import csv, hashlib, io, json, os, sys, tempfile, time, urllib.request, zipfile
from pathlib import Path
import requests

SHARE="l5ppqdrXbxy_"
API=f"https://api.firestorage.ai/dev/file/shares/{SHARE}"
PROMPT_BUNDLE_SHA="f12394567a0dde9e1e4b2aa34452770b47e3e8e0891ea0001c295e060a3dfe62"
PROMPT_JSONL_SHA="ce1da238040e9c2e74744c9e5de4867975acc7fc5ced485cfff80393097a7033"
REG_BUNDLE_SHA="1a3c4909fa9c351826a7b9a861173b8d64df534ae095c96dd15d2d6281eed31b"
MODEL="Qwen/Qwen3-32B"
REVISION="9216db5781bf21249d130ec9da846c4624c16137"
SEED=20260902
DATASETS=["nq","hotpotqa","fever","scifact"]
EXPECTED_N={"nq":250,"hotpotqa":250,"fever":150,"scifact":150}
WORK=Path("/tmp/ridi_qwen32b")
WORK.mkdir(parents=True,exist_ok=True)

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for x in iter(lambda:f.read(1<<20),b""): h.update(x)
    return h.hexdigest()

def share_download(substr):
    listing=json.load(urllib.request.urlopen(API+"/files?maxResults=1000",timeout=30))
    hits=[x for x in listing["files"] if substr in x["fileName"]]
    if len(hits)!=1: raise RuntimeError((substr,[(x["fileName"],x["fileId"]) for x in hits]))
    req=urllib.request.Request(API+f"/files/{hits[0]['fileId']}/download",method="POST")
    meta=json.load(urllib.request.urlopen(req,timeout=30))
    return urllib.request.urlopen(meta["downloadUrl"],timeout=180).read()

def main():
    print("DOWNLOADING_FROZEN_INPUTS",flush=True)
    prompt_zip=share_download("PROMPT_BUNDLE_EXPORT")
    reg_zip=share_download("OSF_COMPACT_REGISTRATION")
    if sha_bytes(prompt_zip)!=PROMPT_BUNDLE_SHA: raise RuntimeError("prompt bundle hash mismatch")
    if sha_bytes(reg_zip)!=REG_BUNDLE_SHA: raise RuntimeError("registration bundle hash mismatch")
    with tempfile.TemporaryDirectory(prefix="ridi32b_reg_") as td:
        root=Path(td)
        with zipfile.ZipFile(io.BytesIO(reg_zip)) as z:z.extractall(root/"reg")
        with zipfile.ZipFile(io.BytesIO(prompt_zip)) as z:
            raw=z.read("RIDI_RAG_512_PROMPTS.jsonl")
            manifest=json.loads(z.read("RIDI_RAG_512_PROMPTS.manifest.json"))
        if sha_bytes(raw)!=PROMPT_JSONL_SHA: raise RuntimeError("prompt JSONL hash mismatch")
        rows=[json.loads(x) for x in raw.decode().splitlines() if x.strip()]
        if len(rows)!=800: raise RuntimeError(f"expected 800 rows, got {len(rows)}")
        counts={d:sum(r["dataset"]==d for r in rows) for d in DATASETS}
        if counts!=EXPECTED_N: raise RuntimeError(f"dataset panel mismatch {counts}")
        sys.path.insert(0,str(root/"reg"/"code"))
        from backend import HFBackend
        import scoring
        print("LOADING_MODEL",MODEL,REVISION,flush=True)
        backend=HFBackend(MODEL,REVISION,128,SEED,{"enable_thinking":False})
        env=backend.environment
        print("ENV",json.dumps(env,sort_keys=True),flush=True)
        out=[]; raw_path=WORK/"qwen3_32b_primary_raw.jsonl"
        started=time.time()
        with raw_path.open("w",encoding="utf-8") as h:
            for i,row in enumerate(rows,1):
                ar=backend.generate(row["prompts"]["reference"])
                ax=backend.generate(row["prompts"]["random"])
                cr=bool(scoring.is_correct(ar,row["gold"],row["task"],row.get("labels")))
                cx=bool(scoring.is_correct(ax,row["gold"],row["task"],row.get("labels")))
                rec={"dataset":row["dataset"],"query_id":str(row["query_id"]),"task":row["task"],
                     "reference_answer":ar,"random_answer":ax,"reference_correct":cr,
                     "random_correct":cx,"correctness_changed":cr!=cx,
                     "reference_answer_sha256":sha_bytes(ar.encode()),"random_answer_sha256":sha_bytes(ax.encode())}
                out.append(rec); h.write(json.dumps(rec,ensure_ascii=False,sort_keys=True)+"\n"); h.flush()
                if i%20==0: print("PROGRESS",i,"/800 elapsed_s",round(time.time()-started,1),flush=True)
        by={}
        for d in DATASETS:
            rr=[x for x in out if x["dataset"]==d]
            flips=sum(x["correctness_changed"] for x in rr)
            ctw=sum(x["reference_correct"] and not x["random_correct"] for x in rr)
            wtc=sum((not x["reference_correct"]) and x["random_correct"] for x in rr)
            by[d]={"n":len(rr),"flips":flips,"rate":flips/len(rr),"correct_to_wrong":ctw,"wrong_to_correct":wtc}
        macro=sum(by[d]["rate"] for d in DATASETS)/4
        pooled=sum(by[d]["flips"] for d in DATASETS)
        summary={"study":"RIDI-RAG-QWEN3-32B-SCALE-SENSITIVITY-v1","status":"completed","post_hoc":True,
                 "model_id":MODEL,"revision":REVISION,"n_queries":800,"generation_calls":1600,
                 "max_new_tokens":128,"seed":SEED,"enable_thinking":False,
                 "prompt_bundle_sha256":PROMPT_BUNDLE_SHA,"prompt_jsonl_sha256":PROMPT_JSONL_SHA,
                 "registered_bundle_sha256":REG_BUNDLE_SHA,"environment":env,
                 "dataset_results":by,"macro_rate":macro,"pooled_flips":pooled,
                 "elapsed_generation_seconds":time.time()-started,
                 "raw_outputs_sha256":sha_file(raw_path),
                 "claim_boundary":"Post-hoc scale robustness only; preregistered Qwen3-8B remains primary."}
        sp=WORK/"qwen3_32b_scale_sensitivity_summary.json"
        sp.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        vp=WORK/"qwen3_32b_flip_vector.csv"
        fields=["dataset","query_id","reference_correct","random_correct","correctness_changed","reference_answer_sha256","random_answer_sha256"]
        with vp.open("w",newline="",encoding="utf-8") as h:
            w=csv.DictWriter(h,fieldnames=fields);w.writeheader()
            for r in out:w.writerow({k:r[k] for k in fields})
        meta={"prompt_bundle_sha256":sha_bytes(prompt_zip),"registered_bundle_sha256":sha_bytes(reg_zip),
              "raw_outputs_sha256":sha_file(raw_path),"summary_sha256":sha_file(sp),"vector_sha256":sha_file(vp)}
        mp=WORK/"qwen3_32b_execution_manifest.json"; mp.write_text(json.dumps(meta,indent=2,sort_keys=True)+"\n")
        zp=WORK/"RIDI_Qwen3_32B_Scale_Sensitivity_RESULTS.zip"
        with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
            for p in (raw_path,sp,vp,mp): z.write(p,p.name)
        print("FINAL_SUMMARY",json.dumps(summary,sort_keys=True),flush=True)
        print("FINAL_ZIP_SHA256",sha_file(zp),"BYTES",zp.stat().st_size,flush=True)
        with zp.open("rb") as h:
            resp=requests.post("https://tmpfiles.org/api/v1/upload",files={"file":(zp.name,h,"application/zip")},timeout=240)
        resp.raise_for_status()
        u=resp.json()["data"]["url"].replace("https://tmpfiles.org/","https://tmpfiles.org/dl/")
        print("FINAL_DOWNLOAD_URL",u,flush=True)
if __name__=="__main__": main()
