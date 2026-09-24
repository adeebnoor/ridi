# /// script
# dependencies = [
#   "requests>=2.32",
#   "torch>=2.4",
#   "transformers>=4.51",
#   "accelerate>=0.33",
#   "numpy>=1.26",
#   "scipy>=1.11"
# ]
# ///
import base64,gzip,hashlib,io,json,os,platform,subprocess,sys,time,zipfile
from pathlib import Path
import requests

BASE="https://api.firestorage.ai/dev/file"
SHARE="kWqytsrfwEpe"
FID="01a0d059ff00774ebefcc097f1f715a2"
ASSET_SHA="d0fd425973965c33e6a4e9bc53e4ec65382dbc6ca946aac48f70496a571a01ea"
P2_SHA="d5bbeaceacec4a1366af199cc58cabac834bd7e432d3207e0b6e4fb4398e1ab8"
P3_SHA="f8d10c277f151387c34b555d86676ee0375973506abde815fa7ce96516e0737a"
MODEL="Qwen/Qwen3-8B"
REV="b968826d9c46dd6066d109eabc6255188de91218"

work=Path("/tmp/ridi_p2p3_raw"); work.mkdir(parents=True,exist_ok=True)
m=requests.post(f"{BASE}/shares/{SHARE}/files/{FID}/download",timeout=60); m.raise_for_status()
data=requests.get(m.json()["downloadUrl"],timeout=300).content
got=hashlib.sha256(data).hexdigest()
print("ASSET_SHA256",got,flush=True); assert got==ASSET_SHA
with zipfile.ZipFile(io.BytesIO(data)) as z:z.extractall(work)
hits=list(work.rglob("p2_noise_floor.py")); assert len(hits)==1,hits
root=hits[0].parent
subprocess.run([sys.executable,"check_contexts.py","data/contexts_800.jsonl","--registered-panel","--require-prompt"],cwd=root,check=True)
print("ENV",json.dumps({"python":sys.version,"platform":platform.platform()}),flush=True)
subprocess.run([sys.executable,"-c","import torch,transformers,numpy,scipy; print('VERSIONS',torch.__version__,transformers.__version__,numpy.__version__,scipy.__version__); print('GPU',torch.cuda.get_device_name(0),torch.cuda.get_device_properties(0).total_memory)"],check=True)

p2=root/"results"/"p2_raw_rerun"
cmd=[sys.executable,"p2_noise_floor.py","--contexts","data/contexts_800.jsonl","--out",str(p2),"--backend","hf","--model",MODEL,"--revision",REV,
     "--frozen-scorer","frozen_registered/scoring.py","--archived","data/registered_generations_primary_800.jsonl",
     "--regimes","single","fixed:16","shuffled:16:1","shuffled:16:2"]
print("START_P2",time.time(),flush=True); subprocess.run(cmd,cwd=root,check=True)
p2g=p2/"generations.jsonl"; h2=hashlib.sha256(p2g.read_bytes()).hexdigest()
print("P2_GENERATIONS_SHA256",h2,"MATCH",h2==P2_SHA,flush=True); assert h2==P2_SHA

p3=root/"results"/"p3_raw_rerun"
cmd=[sys.executable,"p3_multi_draw.py","--contexts","data/draws.jsonl","--out",str(p3),"--backend","hf","--model",MODEL,"--revision",REV,
     "--frozen-scorer","frozen_registered/scoring.py","--regime","fixed:16"]
print("START_P3",time.time(),flush=True); subprocess.run(cmd,cwd=root,check=True)
p3g=p3/"generations.jsonl"; h3=hashlib.sha256(p3g.read_bytes()).hexdigest()
print("P3_GENERATIONS_SHA256",h3,"MATCH",h3==P3_SHA,flush=True); assert h3==P3_SHA

def emit(label,paths):
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p,arc in paths: z.write(p,arc)
    raw=buf.getvalue(); sha=hashlib.sha256(raw).hexdigest(); b64=base64.b64encode(raw).decode()
    chunk=30000; n=(len(b64)+chunk-1)//chunk
    print(f"RAW_BEGIN {label} bytes={len(raw)} sha256={sha} chunks={n}",flush=True)
    for i in range(n):
        print(f"RAW_CHUNK {label} {i+1}/{n} {b64[i*chunk:(i+1)*chunk]}",flush=True)
    print(f"RAW_END {label}",flush=True)

emit("P2",[(p2g,"generations.jsonl"),(p2/"P2_summary.json","P2_summary.json")])
emit("P3",[(p3g,"generations.jsonl"),(p3/"P3_summary.json","P3_summary.json")])
print("RERUN_STATUS=PASS",flush=True)
