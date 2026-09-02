"""Generate one frozen top-100 retrieval run from a Pyserini prebuilt BEIR index.
No language-model generation occurs here.
"""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

from beir_local_resources import ensure_resources

SPLADE_ID = "naver/splade-cocondenser-ensembledistil"
SPLADE_REV = "49cf4c7b0db5b870a401ddf5e2669993ef3699c7"
CONTRIEVER_ID = "facebook/contriever-msmarco"
CONTRIEVER_REV = "abe8c1493371369031bcb1e02acb754cf4e162fa"


def run(cmd):
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run([str(x) for x in cmd], check=True)


def frozen_snapshot(repo_id: str, revision: str) -> str:
    from huggingface_hub import snapshot_download
    snapshot=snapshot_download(repo_id=repo_id,revision=revision)
    print(f"HF snapshot {repo_id}@{revision}: {snapshot}", flush=True)
    return snapshot


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--dataset', choices=['nq','hotpotqa','fever','scifact'], required=True)
    ap.add_argument('--retriever', choices=['bm25','splade','contriever'], required=True)
    ap.add_argument('--root', type=Path, required=True)
    a=ap.parse_args(); d=a.dataset; r=a.retriever; root=a.root.resolve()
    if r=='contriever' and d!='scifact':
        raise SystemExit('Contriever is preregistered only for the additional SciFact dense-retrieval check')

    resources=ensure_resources(d, root/'.beir_resources')
    topic=resources['topics_path']
    print(f"BEIR topics: {topic} sha256={resources['topics_sha256']}", flush=True)

    out=root/'runs'/d/f'{r}.trec'; out.parent.mkdir(parents=True,exist_ok=True)
    if r=='bm25':
        cmd=[sys.executable,'-m','pyserini.search.lucene','--threads','16','--batch-size','128',
             '--index',f'beir-v1.0.0-{d}.flat','--topics',topic,'--output',out,
             '--output-format','trec','--hits','100','--bm25','--remove-query']
    elif r=='splade':
        snapshot=frozen_snapshot(SPLADE_ID,SPLADE_REV)
        cmd=[sys.executable,'-m','pyserini.search.lucene','--threads','16','--batch-size','128',
             '--index',f'beir-v1.0.0-{d}.splade-pp-ed','--topics',topic,'--encoder',snapshot,
             '--output',out,'--output-format','trec','--hits','100','--impact','--pretokenized','--remove-query']
    else:
        snapshot=frozen_snapshot(CONTRIEVER_ID,CONTRIEVER_REV)
        cmd=[sys.executable,'-m','pyserini.search.faiss','--encoder-class','contriever','--encoder',snapshot,
             '--index','beir-v1.0.0-scifact.contriever-msmarco','--topics',topic,
             '--output',out,'--output-format','trec','--hits','100','--batch','64','--threads','4']
    run(cmd)
    lines=sum(1 for _ in out.open(encoding='utf-8'))
    if lines < 100:
        raise RuntimeError(f'suspiciously short run: {lines} lines')
    print(f'WROTE {out} lines={lines}')

if __name__=='__main__': main()
