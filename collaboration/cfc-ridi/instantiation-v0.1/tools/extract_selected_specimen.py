#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

CASE_ID = "RAG-nq-test1035"
EXPECTED = {
    ("source","A"): "60e19ea94ff13ded74e6ca19d6063909d374951f86218a9e3e68833b46126734",
    ("endpoint","A"): "e03c1c6433cd197f780537a90d1541744b314cf8eb196ca426f7dc4a41779c67",
    ("source","B"): "018f1de8876594e57a383b69a1fcd605e811cf062695cc2ab947c737a697e308",
    ("endpoint","B"): "e66408834f040464bb8146e4ed814a26f15bb871519db4194c7a764b4e8580c5",
}

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def extract(path: Path, kind: str, outdir: Path):
    hits = {}
    with path.open("rb") as f:
        for n, line in enumerate(f, start=1):
            if not line.endswith(b"\n"):
                raise SystemExit(f"{path}: line {n} is not LF-terminated")
            try:
                obj = json.loads(line)
            except Exception as e:
                raise SystemExit(f"{path}: invalid JSON on line {n}: {e}")
            if obj.get("case_id") != CASE_ID:
                continue
            arm = obj.get("arm")
            if arm not in {"A","B"}:
                raise SystemExit(f"{path}: selected row line {n} has invalid arm={arm!r}")
            if arm in hits:
                raise SystemExit(f"{path}: duplicate selected arm {arm}")
            got = sha256(line)
            want = EXPECTED[(kind, arm)]
            if got != want:
                raise SystemExit(f"{path}: hash mismatch for {kind} arm {arm}: got {got}, expected {want}")
            hits[arm] = (n, line, obj, got)
    if set(hits) != {"A","B"}:
        raise SystemExit(f"{path}: expected A/B for {CASE_ID}, found {sorted(hits)}")
    for arm,(n,line,obj,digest) in hits.items():
        out = outdir / f"{kind}_{arm}.jsonl"
        out.write_bytes(line)
        print(f"{kind}\t{arm}\tline={n}\tbytes={len(line)}\tsha256={digest}\tout={out}")
    return hits

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--sources", required=True, type=Path)
    ap.add_argument("--endpoints", required=True, type=Path)
    ap.add_argument("--outdir", required=True, type=Path)
    args=ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    src=extract(args.sources,"source",args.outdir)
    ep=extract(args.endpoints,"endpoint",args.outdir)
    manifest={"case_id":CASE_ID,"files":[]}
    for kind,hits in [("source",src),("endpoint",ep)]:
        for arm in ("A","B"):
            n,line,obj,digest=hits[arm]
            manifest["files"].append({
                "kind":kind,"arm":arm,"line_number":n,
                "bytes":len(line),"sha256":digest,
                "file":f"{kind}_{arm}.jsonl"
            })
    mbytes=(json.dumps(manifest,sort_keys=True,indent=2)+"\n").encode("utf-8")
    (args.outdir/"EXTRACTION_MANIFEST.json").write_bytes(mbytes)
    print(f"manifest_sha256={sha256(mbytes)}")
    print("PASS: exact selected A/B source and endpoint bytes match frozen hashes.")

if __name__ == "__main__":
    main()
