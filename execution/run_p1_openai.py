# /// script
# dependencies = ["requests>=2.32", "openai>=1.40", "numpy>=1.26", "scipy>=1.11"]
# ///
import hashlib, json, os, platform, requests, shutil, subprocess, sys, time, zipfile
from pathlib import Path
BASE="https://api.firestorage.ai/dev/file"; SHARE="OjZ4x0tKnOrV"; FID="01a0d33c0ce677c78d43bd0f6122ab96"
ASSET_SHA="4316136c29e27e8617c6031d79d0dcc7863e5b4f9c7e5619e16d2e916640ed58"
MODEL="gpt-5.6-sol"; OUT=Path(os.environ.get("RIDI_RESULTS_DIR","/results"))/"rerun_20260924"/"p1"; OUT.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
if not os.environ.get('OPENAI_API_KEY'): raise SystemExit('OPENAI_API_KEY missing')
m=requests.post(f"{BASE}/shares/{SHARE}/files/{FID}/download",timeout=60); m.raise_for_status(); data=requests.get(m.json()["downloadUrl"],timeout=600).content; assert hashlib.sha256(data).hexdigest()==ASSET_SHA
z=Path('/tmp/v954.zip'); z.write_bytes(data); d=Path('/tmp/v954'); shutil.rmtree(d,ignore_errors=True); d.mkdir(); zipfile.ZipFile(z).extractall(d)
roots=[p for p in d.rglob('08_New_Experiments') if (p/'p1_frontier_model.py').exists()]; assert len(roots)==1,roots; root=roots[0]
assert sha(root/'data/contexts_800.jsonl')=="1485c0ad114673d297c580080d11086d3ace8827f9b586b15ad3928c7d0b21a1"
assert sha(root/'frozen_registered/scoring.py')=="5b9f02f7a8bcd4df98f3bf28e66017e86e4cfa3e36d495acb6d1e2828488c7ee"
subprocess.run([sys.executable,'check_contexts.py','data/contexts_800.jsonl','--registered-panel','--require-prompt'],cwd=root,check=True)
subprocess.run([sys.executable,'p1_frontier_model.py','--contexts','data/contexts_800.jsonl','--out',str(OUT),'--backend','openai','--model',MODEL,'--repeats','3','--frozen-scorer','frozen_registered/scoring.py','--workers','8'],cwd=root,check=True)
manifest={"model":MODEL,"registration":"OSF ms4w8","protocol_commit":"440f72f3d4879b9c5320e34f0fa6afaa731f5fb2","code_freeze_commit":"fb29c4cdbaed7598412081b14a4b9183c0f78177","generations_sha256":sha(OUT/'generations.jsonl'),"summary_sha256":sha(OUT/'P1_summary.json'),"python":sys.version,"platform":platform.platform(),"status":"P1_COMPLETE","time":time.time()}
(OUT/'RERUN_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('RIDI_P1_PASS',json.dumps(manifest,sort_keys=True),flush=True); print('P1_SUMMARY',(OUT/'P1_summary.json').read_text(),flush=True)
