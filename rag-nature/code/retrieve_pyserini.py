"""Generate one frozen top-100 retrieval run from a Pyserini prebuilt BEIR index.
No language-model generation occurs here.
"""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

SPLADE_ID = "naver/splade-cocondenser-ensembledistil"
CONTRIEVER_ID = "facebook/contriever-msmarco"
CONTRIEVER_REV = "abe8c1493371369031bcb1e02acb754cf4e162fa"


def run(cmd):
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run([str(x) for x in cmd], check=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--dataset', choices=['nq','hotpotqa','fever','scifact'], required=True)
    ap.add_argument('--retriever', choices=['bm25','splade','contriever'], required=True)
    ap.add_argument('--root', type=Path, required=True)
    a=ap.parse_args(); d=a.dataset; r=a.retriever; root=a.root.resolve()
    if r=='contriever' and d!='scifact':
        raise SystemExit('Contriever is preregistered only for SciFact')
    out=root/'runs'/d/f'{r}.trec'; out.parent.mkdir(parents=True,exist_ok=True)
    topic=f'beir-v1.0.0-{d}-test'
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
