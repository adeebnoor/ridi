# /// script
# dependencies = [
#   "requests>=2.32", "torch>=2.4", "transformers>=4.51", "accelerate>=0.33",
#   "numpy>=1.26", "scipy>=1.11"
# ]
# ///
import hashlib, json, os, platform, requests, shutil, subprocess, sys, time, zipfile
from pathlib import Path

BASE="https://api.firestorage.ai/dev/file"
SHARE="OjZ4x0tKnOrV"
FID="01a0d33b991472e4ba11a81ae1646a5c"
ASSET_SHA="509af2d85d0c305bb729b055a78e5c43670b871969d70b5cd66c64ae63cc4081"
MODEL="Qwen/Qwen3-8B"
REV="b968826d9c46dd6066d109eabc6255188de91218"
EXPECTED_P2="d5bbeaceacec4a1366af199cc58cabac834bd7e432d3207e0b6e4fb4398e1ab8"
EXPECTED_P3="f8d10c277f151387c34b555d86676ee0375973506abde815fa7ce96516e0737a"
OUT=Path(os.environ.get("RIDI_RESULTS_DIR","/results"))/"rerun_20260924"/"p2_p3"
OUT.mkdir(parents=True, exist_ok=True)

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dl():
    m=requests.post(f"{BASE}/shares/{SHARE}/files/{FID}/download",timeout=60); m.raise_for_status()
    data=requests.get(m.json()["downloadUrl"],timeout=600).content
    assert hashlib.sha256(data).hexdigest()==ASSET_SHA
    p=Path("/tmp/ridi_exec.zip"); p.write_bytes(data)
    d=Path("/tmp/ridi_exec"); shutil.rmtree(d,ignore_errors=True); d.mkdir()
    with zipfile.ZipFile(p) as z: z.extractall(d)
    roots=list(d.rglob("p2_p3")); assert len(roots)==1, roots
    return roots[0]
root=dl()
subprocess.run([sys.executable,"check_contexts.py","data/contexts_800.jsonl","--registered-panel","--require-prompt"],cwd=root,check=True)
assert sha(root/"data/contexts_800.jsonl")=="1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1"
assert sha(root/"frozen_registered/scoring.py")=="5b9f02f7a8bcd4df98f3bf28e66017e86e4cfa3e36d495acb6d1e2828488c7ee"
p2=OUT/"P2"; p3=OUT/"P3"
subprocess.run([sys.executable,"p2_noise_floor.py","--contexts","data/contexts_800.jsonl","--out",str(p2),"--backend","hf","--model",MODEL,"--revision",REV,"--frozen-scorer","frozen_registered/scoring.py","--archived","data/registered_generations_primary_800.jsonl","--regimes","single","fixed:16","shuffled:16:1","shuffled:16:2"],cwd=root,check=True)
assert sha(p2/"generations.jsonl")==EXPECTED_P2,(sha(p2/"generations.jsonl"),EXPECTED_P2)
subprocess.run([sys.executable,"p3_multi_draw.py","--contexts","data/draws.jsonl","--out",str(p3),"--backend","hf","--model",MODEL,"--revision",REV,"--frozen-scorer","frozen_registered/scoring.py","--regime","fixed:16"],cwd=root,check=True)
assert sha(p3/"generations.jsonl")==EXPECTED_P3,(sha(p3/"generations.jsonl"),EXPECTED_P3)
manifest={"asset_sha256":ASSET_SHA,"model":MODEL,"revision":REV,"p2_generations_sha256":EXPECTED_P2,"p3_generations_sha256":EXPECTED_P3,"python":sys.version,"platform":platform.platform(),"time":time.time(),"status":"PASS_EXACT_SHA_MATCH"}
(OUT/"RERUN_MANIFEST.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print("RIDI_P2_P3_RERUN_PASS",json.dumps(manifest,sort_keys=True),flush=True)
