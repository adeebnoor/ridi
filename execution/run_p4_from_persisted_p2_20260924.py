# /// script
# dependencies = ["requests>=2.32","torch>=2.4","transformers>=4.51","accelerate>=0.33","numpy>=1.26","scipy>=1.11"]
# ///
import os, requests, hashlib, pathlib, zipfile, urllib.request

base=os.environ["SUPA_BASE"]
key=os.environ["SUPA_KEY"]
bucket=os.environ["SUPA_BUCKET"]
prefix=os.environ["SUPA_PREFIX"]
headers={"apikey":key,"Authorization":"Bearer "+key}

src_url=f"{base}/storage/v1/object/{bucket}/{prefix}/p2_p3_raw.zip"
r=requests.get(src_url,headers=headers,timeout=600)
r.raise_for_status()
arc=pathlib.Path("/tmp/p2_p3_raw.zip")
arc.write_bytes(r.content)

root=pathlib.Path("/tmp/results/rerun_20260924/p2_p3")
root.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(arc) as z:
    z.extractall(root)

p2=root/"P2"/"generations.jsonl"
expected="d5bbeaceacec4a1366af199cc58cabac834bd7e432d3207e0b6e4fb4398e1ab8"
got=hashlib.sha256(p2.read_bytes()).hexdigest()
print("P2_RAW_SHA256",got,flush=True)
assert got==expected,(got,expected)

p4_url="https://raw.githubusercontent.com/adeebnoor/ridi/844f6d7a0a4299912cbcea33eb1280ddafbcca59/execution/run_p4_machine.py"
code=urllib.request.urlopen(p4_url,timeout=60).read().decode("utf-8")
os.environ["RIDI_RESULTS_DIR"]="/tmp/results"
exec(compile(code,p4_url,"exec"),{"__name__":"__main__"})

src=pathlib.Path("/tmp/results/rerun_20260924/p4")
out=pathlib.Path("/tmp/p4_raw.zip")
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(src.rglob("*")):
        if p.is_file():
            z.write(p,p.relative_to(src))
sha=hashlib.sha256(out.read_bytes()).hexdigest()

dst_url=f"{base}/storage/v1/object/{bucket}/{prefix}/p4_raw.zip"
up_headers={**headers,"Content-Type":"application/zip","x-upsert":"false"}
u=requests.post(dst_url,headers=up_headers,data=out.read_bytes(),timeout=600)
print("P4_UPLOAD",u.status_code,u.text[:300],flush=True)
assert u.status_code in (200,201),u.text
v=requests.get(dst_url,headers=headers,timeout=600)
v.raise_for_status()
verify=hashlib.sha256(v.content).hexdigest()
print("P4_PERSISTED_SHA256",sha,"VERIFY",verify,"BYTES",out.stat().st_size,flush=True)
assert verify==sha
print("RIDI_P4_PERSISTENCE_PASS",sha,flush=True)
