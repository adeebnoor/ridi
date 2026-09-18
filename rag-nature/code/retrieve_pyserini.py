"""Generate one frozen top-100 retrieval run from a Pyserini prebuilt BEIR index.
No language-model generation occurs here.

Technical note (2026-09-18): Pyserini/Anserini's Java topic downloader failed on
GitHub-hosted topic files before any retrieval endpoint was produced. To avoid
changing the scientific design, queries are now read from the official BEIR
dataset archive and written to a local TSV before retrieval. Dataset, queries,
retrievers, indexes, and top-100 rule are unchanged.
"""
from __future__ import annotations
import argparse, csv, io, json, shutil, subprocess, sys, urllib.request, zipfile
from pathlib import Path

SPLADE_ID = "naver/splade-cocondenser-ensembledistil"
CONTRIEVER_ID = "facebook/contriever-msmarco"
CONTRIEVER_REV = "abe8c1493371369031bcb1e02acb754cf4e162fa"
BEIR_BASE = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets"


def run(cmd):
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run([str(x) for x in cmd], check=True)


def download(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    req=urllib.request.Request(url,headers={"User-Agent":"RIDI-frontier-downstream/1.0"})
    with urllib.request.urlopen(req,timeout=300) as r, dest.open("wb") as f:
        shutil.copyfileobj(r,f)


def find_member(z: zipfile.ZipFile, suffix: str) -> str:
    hits=[n for n in z.namelist() if n.endswith(suffix)]
    if len(hits)!=1:
        raise RuntimeError(f"expected one {suffix}, got {hits[:10]}")
    return hits[0]


def local_topics(dataset: str, root: Path) -> Path:
    cache=root/"source"/f"{dataset}.zip"
    if not cache.exists():
        download(f"{BEIR_BASE}/{dataset}.zip",cache)
    out=root/"source"/f"{dataset}.topics.tsv"
    with zipfile.ZipFile(cache) as z:
        qname=find_member(z,"/queries.jsonl")
        rows=[]
        with z.open(qname) as fh:
            for raw in io.TextIOWrapper(fh,encoding="utf-8"):
                if not raw.strip(): continue
                o=json.loads(raw)
                qid=str(o.get("_id"))
                txt=str(o.get("text","")).replace("\t"," ").replace("\n"," ").strip()
                if not qid or not txt: raise RuntimeError("bad BEIR query record")
                rows.append((qid,txt))
    with out.open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,delimiter="\t",lineterminator="\n")
        w.writerows(rows)
    print(f"LOCAL_TOPICS {dataset} n={len(rows)} path={out}")
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--dataset', choices=['nq','hotpotqa','fever','scifact'], required=True)
    ap.add_argument('--retriever', choices=['bm25','splade','contriever'], required=True)
    ap.add_argument('--root', type=Path, required=True)
    a=ap.parse_args(); d=a.dataset; r=a.retriever; root=a.root.resolve()
    if r=='contriever' and d!='scifact':
        raise SystemExit('Contriever is preregistered only for SciFact')
    out=root/'runs'/d/f'{r}.trec'; out.parent.mkdir(parents=True,exist_ok=True)
    topic=local_topics(d,root)
    if r=='bm25':
        cmd=[sys.executable,'-m','pyserini.search.lucene','--threads','16','--batch-size','128',
             '--index',f'beir-v1.0.0-{d}.flat','--topics',topic,'--output',out,
             '--output-format','trec','--hits','100','--bm25','--remove-query']
    elif r=='splade':
        cmd=[sys.executable,'-m','pyserini.search.lucene','--threads','16','--batch-size','128',
             '--index',f'beir-v1.0.0-{d}.splade-pp-ed','--topics',topic,'--encoder',SPLADE_ID,
             '--output',out,'--output-format','trec','--hits','100','--impact','--pretokenized','--remove-query']
    else:
        from huggingface_hub import snapshot_download
        snapshot=snapshot_download(repo_id=CONTRIEVER_ID,revision=CONTRIEVER_REV)
        cmd=[sys.executable,'-m','pyserini.search.faiss','--encoder-class','contriever','--encoder',snapshot,
             '--index','beir-v1.0.0-scifact.contriever-msmarco','--topics',topic,
             '--output',out,'--output-format','trec','--hits','100','--batch','64','--threads','4']
    run(cmd)
    lines=sum(1 for _ in out.open(encoding='utf-8'))
    if lines < 100:
        raise RuntimeError(f'suspiciously short run: {lines} lines')
    print(f'WROTE {out} lines={lines}')

if __name__=='__main__': main()
