#!/usr/bin/env python3
from __future__ import annotations
import argparse, pathlib, subprocess, sys, time, urllib.request

DATASETS=("nq","hotpotqa","fever","scifact")
SPLADE_ID="naver/splade-cocondenser-ensembledistil"
TOPIC_BASE="https://raw.githubusercontent.com/castorini/eval/master/topics"

def download(url: str, dest: pathlib.Path):
    dest.parent.mkdir(parents=True,exist_ok=True)
    last=None
    for i in range(5):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"RIDI-frontier-downstream/1.0"})
            with urllib.request.urlopen(req,timeout=120) as r, dest.open("wb") as f:
                f.write(r.read())
            if dest.stat().st_size<20:
                raise RuntimeError("download too small")
            return
        except Exception as e:
            last=e
            time.sleep(2**i)
    raise RuntimeError(f"download failed {url}: {last}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dataset",choices=DATASETS,required=True)
    ap.add_argument("--retriever",choices=("bm25","splade"),required=True)
    ap.add_argument("--root",type=pathlib.Path,required=True)
    a=ap.parse_args(); d=a.dataset; r=a.retriever; root=a.root.resolve()

    topics=root/"sources"/f"topics.beir-v1.0.0-{d}.test.tsv.gz"
    download(f"{TOPIC_BASE}/topics.beir-v1.0.0-{d}.test.tsv.gz",topics)

    out=root/"runs"/d/f"{r}.trec"
    out.parent.mkdir(parents=True,exist_ok=True)

    if r=="bm25":
        cmd=[sys.executable,"-m","pyserini.search.lucene","--threads","16","--batch-size","128",
             "--index",f"beir-v1.0.0-{d}.flat","--topics",str(topics),"--output",str(out),
             "--output-format","trec","--hits","1000","--bm25","--remove-query"]
    else:
        cmd=[sys.executable,"-m","pyserini.search.lucene","--threads","16","--batch-size","128",
             "--index",f"beir-v1.0.0-{d}.splade-pp-ed","--topics",str(topics),
             "--encoder",SPLADE_ID,"--output",str(out),"--output-format","trec","--hits","1000",
             "--impact","--pretokenized","--remove-query"]

    print("+"," ".join(cmd),flush=True)
    subprocess.run(cmd,check=True)
    n=sum(1 for _ in out.open(encoding="utf-8"))
    if n<1000:
        raise RuntimeError(f"suspiciously short run: {n}")
    print(f"WROTE {out} lines={n}")

if __name__=="__main__":
    main()
