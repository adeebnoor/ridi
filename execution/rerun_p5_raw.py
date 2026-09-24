# /// script
# dependencies = [
#   "requests>=2.32", "torch>=2.4", "sentence-transformers>=5.0", "transformers>=4.51",
#   "accelerate>=0.33", "numpy>=1.26", "scipy>=1.11", "pyyaml>=6.0"
# ]
# ///
import hashlib, json, math, os, requests, shutil, statistics as st, subprocess, sys, time, zipfile
from collections import defaultdict
from pathlib import Path
BASE="https://api.firestorage.ai/dev/file"; SHARE="OjZ4x0tKnOrV"; FID="01a0d33b991472e4ba11a81ae1646a5c"
ASSET_SHA="509af2d85d0c305bb729b055a78e5c43670b871969d70b5cd66c64ae63cc4081"
EXPECTED_RANK="43050f9a720130658ca54b199c90a06c10a2ac3e7a5648390db85a56275531b6"
EXPECTED_PAIRS="a643980275110e3585486eda51b66263622246ed046f8e45fe4b2ea5f44bf3eb"
OUT=Path(os.environ.get("RIDI_RESULTS_DIR","/results"))/"rerun_20260924"/"p5"; OUT.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
m=requests.post(f"{BASE}/shares/{SHARE}/files/{FID}/download",timeout=60); m.raise_for_status(); data=requests.get(m.json()["downloadUrl"],timeout=600).content; assert hashlib.sha256(data).hexdigest()==ASSET_SHA
z=Path("/tmp/ridi.zip"); z.write_bytes(data); d=Path("/tmp/ridi"); shutil.rmtree(d,ignore_errors=True); d.mkdir(); zipfile.ZipFile(z).extractall(d)
roots=list(d.rglob("p5")); roots=[p for p in roots if (p/"p5_natural_prevalence.py").exists()]; assert len(roots)==1,roots; root=roots[0]
work=root/"work"
for f in ("rankings.jsonl","pairs.json","roster_manifest.json"):
    p=work/f
    if p.exists(): p.unlink()
subprocess.run([sys.executable,"p5_natural_prevalence.py","rerank","--work","work","--roster","p5_roster_template.yaml"],cwd=root,check=True)
assert sha(work/"rankings.jsonl")==EXPECTED_RANK,(sha(work/"rankings.jsonl"),EXPECTED_RANK)
subprocess.run([sys.executable,"p5_natural_prevalence.py","qualify","--work","work","--margin","0.01","--alpha","0.05"],cwd=root,check=True)
assert sha(work/"pairs.json")==EXPECTED_PAIRS,(sha(work/"pairs.json"),EXPECTED_PAIRS)
pairs=json.load(open(work/"pairs.json"))["all_pairs"]; by=defaultdict(list)
for p in pairs:
    hwn=(p["ndcg_ci90"][1]-p["ndcg_ci90"][0])/2; hwr=(p["recall_ci90"][1]-p["recall_ci90"][0])/2
    margin=max(abs(p["ndcg_ci90"][0]),abs(p["ndcg_ci90"][1]),abs(p["recall_ci90"][0]),abs(p["recall_ci90"][1]))
    sdn=hwn*math.sqrt(p["n"])/1.645; sdr=hwr*math.sqrt(p["n"])/1.645
    by[p["dataset"]].append({"pair":f'{p["a"]}|{p["b"]}',"n":p["n"],"hw_ndcg":hwn,"hw_recall":hwr,"min_margin":margin,"n_needed_0.01_at_zero_difference":math.ceil(max((1.645*sdn/.01)**2,(1.645*sdr/.01)**2))})
out={"status":"post hoc descriptive diagnostic; does not alter the registered P5 decision","datasets":{}}
for ds,rows in sorted(by.items()):
    mm=[r["min_margin"] for r in rows]
    out["datasets"][ds]={"n_pairs":len(rows),"qualification_n":rows[0]["n"],"median_halfwidth_ndcg":st.median(r["hw_ndcg"] for r in rows),"median_halfwidth_recall":st.median(r["hw_recall"] for r in rows),"smallest_min_margin":min(mm),"median_min_margin":st.median(mm),"pairs_within_0.01":sum(x<=.01 for x in mm),"pairs_within_0.02":sum(x<=.02 for x in mm),"pairs_within_0.05":sum(x<=.05 for x in mm),"median_n_needed_for_0.01_at_zero_difference":st.median(r["n_needed_0.01_at_zero_difference"] for r in rows),"closest_pairs":sorted(rows,key=lambda r:r["min_margin"])[:5]}
(OUT/"p5_margin_diagnostic.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
for name in ["rankings.jsonl","pairs.json","roster_manifest.json"]: shutil.copy2(work/name,OUT/name)
for name in ["selected_queries.jsonl","pools.jsonl","registered_qids.txt","P5_POOL_MANIFEST.json"]: shutil.copy2(work/name,OUT/name)
manifest={"asset_sha256":ASSET_SHA,"rankings_sha256":EXPECTED_RANK,"pairs_sha256":EXPECTED_PAIRS,"n_pairs":len(pairs),"n_qualified":sum(bool(p.get("qualified")) for p in pairs),"status":"PASS_EXACT_SHA_MATCH","time":time.time()}
(OUT/"RERUN_MANIFEST.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print("RIDI_P5_RERUN_PASS",json.dumps(manifest,sort_keys=True),flush=True); print("P5_MARGIN_DIAGNOSTIC",json.dumps(out,sort_keys=True),flush=True)
