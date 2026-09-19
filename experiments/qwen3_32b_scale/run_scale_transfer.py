#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, csv, hashlib, io, json, os, random, shutil, sys, tempfile, time, urllib.request, zipfile
from pathlib import Path

MODEL_ID="Qwen/Qwen3-32B"
REVISION="9216db5781bf21249d130ec9da846c4624c16137"
SEED=20260902
REGISTERED_BUNDLE_SHA="1a3c4909fa9c351826a7b9a861173b8d64df534ae095c96dd15d2d6281eed31b"
FROZEN_MANIFEST_SHA="0dd99d3737b9fe4d92ce2228d4227e42d3b15b52b9f204be11dc5b53d03d2885"
CONTROL_SHA="4b5bc603fcbd5165766beabc05d17ec7e0cefa6e0d8c9c47fd65b06eca61c864"
PRIMARY_RESULTS_SHA="c19942d0eb4a0087195c46a45831a1cf864676b813485dcf4e5565a2a676f231"
DATA_SHA={
 "nq":"5b1e813b5e486f9c588c0a73a3d04a1402f4959d991a1c1631fa007f8559bc13",
 "hotpotqa":"783f1f41db0f22e9ca59ce8ddb9520d06105dd7a817746d8032295cd57025bfb",
 "fever":"b2cc0868918569047ba7b44f193e26a759a4e268d964cf8f20141c7d15eecd63",
 "scifact":"fcc9483c65b06df889c34267a358c79bc7720d507f2d03c0419a8d1d772be5dc",
}
PROMPT_DATASET_SHA={
 "nq":"78f32c89197c3f46fa405000a0d99664c975e9b52d0136c239407ac7a4b75330",
 "hotpotqa":"dcc66ff3c27bb3f0693e34cff68fd45771b081356ccaa031714e3f1f31866b49",
 "fever":"54231e17d0f367d617df6615ea8869c79952ba1057923c7b238776354ad9b4df",
 "scifact":"76842af60eabbeacec99bef62b619bb643b6f00d08bf8d03503ea940b0c7a7fa",
}
EXPECTED_N={"nq":250,"hotpotqa":250,"fever":150,"scifact":150}
FIRE_API="https://api.firestorage.ai/dev/file/shares"

def sha_bytes(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def sha_file(p:Path)->str:
 h=hashlib.sha256()
 with p.open("rb") as f:
  for x in iter(lambda:f.read(1<<20),b""):h.update(x)
 return h.hexdigest()

def fire_bytes(slug:str)->bytes:
 u=f"{FIRE_API}/{slug}"
 req=urllib.request.Request(u+"/files?maxResults=1000",headers={"User-Agent":"RIDI-Qwen32-scale/1.0"})
 listing=json.load(urllib.request.urlopen(req,timeout=60))
 files=listing.get("files",[])
 if len(files)!=1: raise RuntimeError(f"share {slug}: expected one file, got {[x.get('fileName') for x in files]}")
 fid=files[0]["fileId"]
 req=urllib.request.Request(u+f"/files/{fid}/download",data=b"",method="POST",headers={"User-Agent":"RIDI-Qwen32-scale/1.0"})
 meta=json.load(urllib.request.urlopen(req,timeout=60))
 return urllib.request.urlopen(meta["downloadUrl"],timeout=600).read()

def download_join(slugs:list[str])->bytes:
 return b"".join(fire_bytes(s) for s in slugs)

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--dataset",choices=list(EXPECTED_N),required=True)
 ap.add_argument("--control-share",required=True)
 ap.add_argument("--data-share",action="append",required=True)
 ap.add_argument("--primary-results-share",required=True)
 ap.add_argument("--out",type=Path,default=Path("/tmp/ridi_qwen32"))
 a=ap.parse_args(); dname=a.dataset
 a.out.mkdir(parents=True,exist_ok=True)
 print("SOURCE_TRANSFER_START",dname,flush=True)
 control=fire_bytes(a.control_share)
 data_zip=download_join(a.data_share)
 primary_zip=fire_bytes(a.primary_results_share)
 assert sha_bytes(control)==CONTROL_SHA,(sha_bytes(control),CONTROL_SHA)
 assert sha_bytes(data_zip)==DATA_SHA[dname],(sha_bytes(data_zip),DATA_SHA[dname])
 assert sha_bytes(primary_zip)==PRIMARY_RESULTS_SHA,(sha_bytes(primary_zip),PRIMARY_RESULTS_SHA)
 print("SOURCE_ZIPS_VERIFIED",dname,flush=True)

 with tempfile.TemporaryDirectory(prefix=f"ridi32_{dname}_") as td:
  td=Path(td); stage=td/"stage"; root=td/"root"; stage.mkdir(); root.mkdir()
  with zipfile.ZipFile(io.BytesIO(control)) as z:z.extractall(stage)
  reg=stage/"RIDI_RAG_NATURE_OSF_COMPACT_REGISTRATION_V2_20260902.zip"
  receipts=stage/"RIDI_RAG_POST_REGISTRATION_RECEIPTS_20260902.zip"
  assert sha_file(reg)==REGISTERED_BUNDLE_SHA
  with zipfile.ZipFile(reg) as z:z.extractall(root)
  with zipfile.ZipFile(receipts) as z:z.extractall(root)
  with zipfile.ZipFile(io.BytesIO(data_zip)) as z:z.extractall(root)
  shutil.copy2(reg,root/"protocol"/"REGISTRATION_BUNDLE.zip")
  assert sha_file(root/"protocol"/"FROZEN_MANIFEST.json")==FROZEN_MANIFEST_SHA
  manifest=json.loads((root/"protocol"/"FROZEN_MANIFEST.json").read_text())
  amap=manifest["artifact_sha256"]
  # Verify every available registered artifact and require all current-dataset artifacts.
  bad=[]
  for rel,exp in amap.items():
   p=root/rel
   if p.exists() and sha_file(p)!=exp: bad.append(rel)
  if bad: raise RuntimeError(f"registered artifact hash mismatch: {bad[:10]}")
  required=[x for x in amap if (
    not x.startswith(("data/beir/","runs/","data/gold/")) or
    x.startswith(f"data/beir/{dname}/") or x.startswith(f"runs/{dname}/") or x==f"data/gold/{dname}.jsonl"
  )]
  missing=[x for x in required if not (root/x).exists()]
  if missing: raise RuntimeError(f"missing required frozen artifacts: {missing[:10]}")
  print("REGISTERED_ARTIFACTS_VERIFIED",dname,len(required),flush=True)

  sys.path.insert(0,str(root/"code"))
  from equivalence import build_equivalent
  from io_utils import load_beir,load_gold,load_run,sha256_text
  from panels import select_universal_panel
  from prompts import get_prompt
  from scoring import canonical_answer,is_correct,is_correct_sensitivity
  from study import by_id

  c=manifest["resolved_config"]
  assert c["study_id"]=="RIDI-RAG-NATURE-v2-PROSPECTIVE"
  assert c["max_new_tokens"]==128 and c["seed"]==SEED and c["passage_chars"]==1200
  assert c["primary_retriever"]=="bm25" and c["primary_k"]==10 and c["primary_variant"]=="random"
  ds=by_id(c["datasets"],dname)
  corpus,queries,qrels,_=load_beir(root/ds["data_dir"])
  gold=load_gold(root/ds["gold_file"])
  all_runs={rid:load_run(root,rp,"trec") for rid,rp in ds["runs"].items()}
  panel=select_universal_panel(all_runs,queries,qrels,c["panel_ks"],c["pool_depth"],ds["panel_n"])
  assert len(panel)==EXPECTED_N[dname]
  pz=zipfile.ZipFile(io.BytesIO(primary_zip))
  rname=[n for n in pz.namelist() if n.endswith(f"{dname}__bm25__qwen3-8b__k10__primary.jsonl")][0]
  old=[json.loads(x) for x in pz.read(rname).decode().splitlines() if x.strip()]
  assert [str(x["query_id"]) for x in old]==[str(x) for x in panel]
  oldmap={str(x["query_id"]):x for x in old}
  prompt_t=get_prompt(ds["task"])
  pkey="qa" if ds["task"]=="qa" else "classification"
  assert sha256_text(prompt_t)==manifest["prompt_sha256"][pkey]
  ranked=all_runs["bm25"]

  prepared=[]; pm=[]
  for qid in panel:
   qid=str(qid); row=oldmap[qid]
   ref=list(ranked[qid][:10])
   alt=build_equivalent(qid,ranked[qid],qrels[qid],10,c["pool_depth"],"random",SEED,f"{dname}:bm25")
   rnd=list(alt.doc_ids)
   assert ref==row["doc_ids__reference"],f"reference IDs differ {qid}"
   assert rnd==row["doc_ids__random"],f"random IDs differ {qid}"
   prompts={}
   rec={"dataset":dname,"query_id":qid,"task":ds["task"]}
   for cond,docs in [("reference",ref),("random",rnd)]:
    passages="\n\n".join(f"[{j+1}] {corpus[x][:c['passage_chars']]}" for j,x in enumerate(docs))
    prompt=prompt_t.format(passages=passages,query=queries[qid])
    prompts[cond]=prompt
    rec[f"{cond}_prompt_sha256"]=sha_bytes(prompt.encode())
    rec[f"{cond}_doc_ids_sha256"]=sha_bytes(("\n".join(docs)+"\n").encode())
   pm.append(rec); prepared.append((qid,row,prompts))

  pm_bytes="".join(json.dumps(x,sort_keys=True,separators=(",",":"))+"\n" for x in pm).encode()
  assert sha_bytes(pm_bytes)==PROMPT_DATASET_SHA[dname],(sha_bytes(pm_bytes),PROMPT_DATASET_SHA[dname])
  print("PROMPT_MANIFEST_VERIFIED",dname,PROMPT_DATASET_SHA[dname],flush=True)

  os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG",":4096:8")
  import torch, transformers, huggingface_hub, accelerate
  from transformers import AutoModelForCausalLM,AutoTokenizer
  random.seed(SEED);torch.manual_seed(SEED)
  if torch.cuda.is_available():torch.cuda.manual_seed_all(SEED)
  torch.use_deterministic_algorithms(True)
  torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
  if not torch.cuda.is_available():raise RuntimeError("CUDA required")
  tok=AutoTokenizer.from_pretrained(MODEL_ID,revision=REVISION)
  model=AutoModelForCausalLM.from_pretrained(MODEL_ID,revision=REVISION,torch_dtype="auto",device_map="auto")
  model.eval()
  dtype=str(next(model.parameters()).dtype)
  env={"python":sys.version.split()[0],"torch":torch.__version__,"transformers":transformers.__version__,
       "huggingface_hub":huggingface_hub.__version__,"accelerate":accelerate.__version__,
       "cuda":torch.version.cuda,"gpu":[torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
       "parameter_dtype":dtype,"deterministic_algorithms":True,"do_sample":False,"tf32":False,
       "cublas_workspace_config":os.environ.get("CUBLAS_WORKSPACE_CONFIG")}
  print("QWEN32_ENV",json.dumps(env,sort_keys=True),flush=True)
  rows=[];t0=time.time()
  for i,(qid,oldrow,prompts) in enumerate(prepared,1):
   ans={}
   for cond in ["reference","random"]:
    messages=[{"role":"user","content":prompts[cond]}]
    text=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
    ids=tok(text,return_tensors="pt").to(model.device)
    with torch.inference_mode():
     out=model.generate(**ids,do_sample=False,max_new_tokens=128,pad_token_id=tok.eos_token_id)
    ans[cond]=tok.decode(out[0][ids["input_ids"].shape[1]:],skip_special_tokens=True).strip()
   cr=bool(is_correct(ans["reference"],gold[qid],ds["task"],ds.get("labels")))
   cx=bool(is_correct(ans["random"],gold[qid],ds["task"],ds.get("labels")))
   rec={"dataset":dname,"query_id":qid,"task":ds["task"],
        "reference_answer":ans["reference"],"random_answer":ans["random"],
        "reference_correct":cr,"random_correct":cx,"correctness_changed":cr!=cx,
        "correct_to_wrong":cr and not cx,"wrong_to_correct":(not cr) and cx,
        "canonical_reference":canonical_answer(ans["reference"],ds["task"],ds.get("labels")),
        "canonical_random":canonical_answer(ans["random"],ds["task"],ds.get("labels")),
        "canonical_changed":canonical_answer(ans["reference"],ds["task"],ds.get("labels"))!=canonical_answer(ans["random"],ds["task"],ds.get("labels")),
        "reference_answer_sha256":sha_bytes(ans["reference"].encode()),
        "random_answer_sha256":sha_bytes(ans["random"].encode()),
        "qwen8_correctness_changed":bool(oldrow["correct__reference"]!=oldrow["correct__random"])}
   rows.append(rec)
   compact={k:rec[k] for k in ["dataset","query_id","reference_correct","random_correct","correctness_changed","correct_to_wrong","wrong_to_correct","canonical_changed","qwen8_correctness_changed","reference_answer_sha256","random_answer_sha256"]}
   print("RIDI32_RECORD\t"+json.dumps(compact,sort_keys=True),flush=True)
   if i%10==0:print("RIDI32_PROGRESS",dname,i,len(prepared),round(time.time()-t0,1),flush=True)

  flips=sum(x["correctness_changed"] for x in rows)
  ctw=sum(x["correct_to_wrong"] for x in rows);wtc=sum(x["wrong_to_correct"] for x in rows)
  canon=sum(x["canonical_changed"] for x in rows)
  flip8=sum(x["qwen8_correctness_changed"] for x in rows)
  summary={"study":"RIDI-RAG-QWEN3-32B-SCALE-v1","dataset":dname,"n":len(rows),
    "model_id":MODEL_ID,"revision":REVISION,"max_new_tokens":128,"seed":SEED,"enable_thinking":False,
    "flips":flips,"rate":flips/len(rows),"correct_to_wrong":ctw,"wrong_to_correct":wtc,
    "canonical_changes":canon,"canonical_change_rate":canon/len(rows),
    "qwen8_flips_same_queries":flip8,"qwen8_rate_same_queries":flip8/len(rows),
    "environment":env,"prompt_manifest_sha256":PROMPT_DATASET_SHA[dname],
    "source_data_zip_sha256":DATA_SHA[dname],"control_zip_sha256":CONTROL_SHA,
    "primary_results_zip_sha256":PRIMARY_RESULTS_SHA,"elapsed_seconds":time.time()-t0}
  raw=a.out/f"{dname}_qwen3_32b_raw.jsonl"
  with raw.open("w",encoding="utf-8") as f:
   for x in rows:f.write(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n")
  summary["raw_sha256"]=sha_file(raw)
  sp=a.out/f"{dname}_summary.json";sp.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
  ep=a.out/f"{dname}_environment.json";ep.write_text(json.dumps(env,indent=2,sort_keys=True)+"\n")
  zp=a.out/f"RIDI_QWEN3_32B_{dname.upper()}_RESULTS.zip"
  with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
   z.write(raw,raw.name);z.write(sp,sp.name);z.write(ep,ep.name)
  zbytes=zp.read_bytes();zsha=sha_bytes(zbytes)
  print("RIDI32_SUMMARY\t"+json.dumps(summary,sort_keys=True),flush=True)
  print("RIDI32_ZIP_SHA256\t"+zsha,flush=True)
  b64=base64.b64encode(zbytes).decode();chunk=16000
  total=(len(b64)+chunk-1)//chunk
  for i in range(total):print(f"RIDI32_ZIP_CHUNK\t{i}\t{total}\t{b64[i*chunk:(i+1)*chunk]}",flush=True)
  print("RIDI32_DONE",dname,total,flush=True)

if __name__=="__main__":main()
