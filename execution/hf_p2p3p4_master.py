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
import base64,hashlib,io,os,subprocess,sys,zipfile
from pathlib import Path
import requests

P2P3_URL="https://raw.githubusercontent.com/adeebnoor/ridi/97bd6206c7f69a9f4f30fa342e1b47beb5f287d2/execution/hf_p2p3_raw_rerun.py"
P4_URL="https://raw.githubusercontent.com/adeebnoor/ridi/d3c188be36fde874238013461b41d5c8cb0b857a/execution/p4_semantic_audit_operational.py"

tmp=Path("/tmp/ridi_master"); tmp.mkdir(parents=True,exist_ok=True)
p2p3=tmp/"hf_p2p3_raw_rerun.py"
r=requests.get(P2P3_URL,timeout=60); r.raise_for_status(); p2p3.write_bytes(r.content)
print("P2P3_RUNNER_SHA256",hashlib.sha256(r.content).hexdigest(),flush=True)
subprocess.run([sys.executable,str(p2p3)],check=True)

roots=list(Path("/tmp/ridi_p2p3_raw").rglob("p2_noise_floor.py"))
assert len(roots)==1,roots
root=roots[0].parent
p2g=root/"results"/"p2_raw_rerun"/"generations.jsonl"
assert p2g.exists()
p4s=root/"p4_semantic_audit_operational.py"
r=requests.get(P4_URL,timeout=60); r.raise_for_status(); p4s.write_bytes(r.content)
print("P4_RUNNER_SHA256",hashlib.sha256(r.content).hexdigest(),flush=True)

prompt=("You are auditing evidence for a {kind}.\n{label}: {question}\n\nPassage:\n{passage}\n\n"
        "Does this passage contain any information that would help {goal}, including partial, indirect or misleading "
        "evidence that a reader could use? Reply with exactly one word: YES or NO.")
assert hashlib.sha256(prompt.encode()).hexdigest()=="e7d4f75fad480666101c1dbd1b185f1990b1aa9107644185e7e8ece6e05fdd47"

out=root/"results"/"p4_machine_raw"
subprocess.run([sys.executable,str(p4s),"--stage","judge","--contexts","data/contexts_800.jsonl","--out",str(out),
 "--judge1","hf:mistralai/Mistral-7B-Instruct-v0.3","--judge1-revision","c170c708c41dac9275d15a8fff4eca08d52bab71",
 "--judge2","hf:allenai/OLMo-2-1124-7B-Instruct","--judge2-revision","470b1fba1ae01581f270116362ee4aa1b97f4c84",
 "--chunk-size","32"],cwd=root,check=True)
labels=out/"passage_labels.jsonl"
print("P4_LABEL_ROWS",sum(1 for _ in labels.open(encoding="utf-8")),flush=True)
print("P4_LABELS_SHA256",hashlib.sha256(labels.read_bytes()).hexdigest(),flush=True)
subprocess.run([sys.executable,str(p4s),"--stage","analyze","--contexts","data/contexts_800.jsonl","--out",str(out),
 "--generations",str(p2g),"--regime","fixed:16"],cwd=root,check=True)
print("P4_SUMMARY_JSON",(out/"P4_summary.json").read_text(encoding="utf-8"),flush=True)

buf=io.BytesIO()
with zipfile.ZipFile(buf,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    z.write(labels,"passage_labels.jsonl")
    z.write(out/"P4_summary.json","P4_summary.json")
    z.write(p4s,"p4_semantic_audit_operational.py")
raw=buf.getvalue(); b64=base64.b64encode(raw).decode(); chunk=30000
n=(len(b64)+chunk-1)//chunk
print(f"RAW_BEGIN P4 bytes={len(raw)} sha256={hashlib.sha256(raw).hexdigest()} chunks={n}",flush=True)
for i in range(n): print(f"RAW_CHUNK P4 {i+1}/{n} {b64[i*chunk:(i+1)*chunk]}",flush=True)
print("RAW_END P4",flush=True)
print("MASTER_STATUS=PASS",flush=True)
