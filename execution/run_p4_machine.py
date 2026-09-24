# /// script
# dependencies = [
#   "requests>=2.32", "torch>=2.4", "transformers>=4.51", "accelerate>=0.33",
#   "numpy>=1.26", "scipy>=1.11"
# ]
# ///
import hashlib, json, os, requests, shutil, subprocess, sys, time, zipfile
from pathlib import Path
BASE="https://api.firestorage.ai/dev/file"; SHARE="OjZ4x0tKnOrV"; FID="01a0d33b991472e4ba11a81ae1646a5c"
ASSET_SHA="509af2d85d0c305bb729b055a78e5c43670b871969d70b5cd66c64ae63cc4081"
PATCH_URL="https://raw.githubusercontent.com/adeebnoor/ridi/166dc2e38de19bf34c2d2b37190c9d67f8c28986/execution/p4_semantic_audit_operational_v1.py"
J1="mistralai/Mistral-7B-Instruct-v0.3"; J1R="c170c708c41dac9275d15a8fff4eca08d52bab71"
J2="allenai/OLMo-2-1124-7B-Instruct"; J2R="470b1fba1ae01581f270116362ee4aa1b97f4c84"
OUT=Path(os.environ.get("RIDI_RESULTS_DIR","/results"))/"rerun_20260924"/"p4"; OUT.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
m=requests.post(f"{BASE}/shares/{SHARE}/files/{FID}/download",timeout=60); m.raise_for_status(); data=requests.get(m.json()["downloadUrl"],timeout=600).content; assert hashlib.sha256(data).hexdigest()==ASSET_SHA
z=Path('/tmp/ridi.zip'); z.write_bytes(data); d=Path('/tmp/ridi'); shutil.rmtree(d,ignore_errors=True); d.mkdir(); zipfile.ZipFile(z).extractall(d)
roots=[p for p in d.rglob('p2_p3') if (p/'data/contexts_800.jsonl').exists()]; assert len(roots)==1,roots; root=roots[0]
patch=requests.get(PATCH_URL,timeout=60); patch.raise_for_status(); (root/'p4_semantic_audit_operational_v1.py').write_bytes(patch.content)
print('P4_OPERATIONAL_SCRIPT_SHA256',hashlib.sha256(patch.content).hexdigest(),flush=True)
p2=Path(os.environ.get("RIDI_RESULTS_DIR","/results"))/"rerun_20260924"/"p2_p3"/"P2"/"generations.jsonl"
if not p2.exists(): raise SystemExit(f'Missing deterministic P2 raw file: {p2}')
assert sha(p2)=="d5bbeaceacec4a1366af199cc58cabac834bd7e432d3207e0b6e4fb4398e1ab8"
subprocess.run([sys.executable,'p4_semantic_audit_operational_v1.py','--stage','judge','--contexts','data/contexts_800.jsonl','--out',str(OUT),'--judge1',f'hf:{J1}','--judge1-revision',J1R,'--judge2',f'hf:{J2}','--judge2-revision',J2R,'--chunk-size','24'],cwd=root,check=True)
subprocess.run([sys.executable,'p4_semantic_audit_operational_v1.py','--stage','analyze','--contexts','data/contexts_800.jsonl','--out',str(OUT),'--generations',str(p2),'--regime','fixed:16'],cwd=root,check=True)
labels=OUT/'passage_labels.jsonl'; summary=OUT/'P4_summary.json'
manifest={"clarification_commit":"0ce7426d1b67cb5ee12bab848e3c2904a95d9ab5","judge1":J1,"judge1_revision":J1R,"judge2":J2,"judge2_revision":J2R,"labels_sha256":sha(labels),"summary_sha256":sha(summary),"p2_generations_sha256":sha(p2),"status":"P4_MACHINE_COMPLETE","time":time.time()}
(OUT/'RERUN_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('RIDI_P4_MACHINE_PASS',json.dumps(manifest,sort_keys=True),flush=True); print('P4_SUMMARY',summary.read_text(),flush=True)
