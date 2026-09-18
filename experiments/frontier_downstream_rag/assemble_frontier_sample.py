#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import pathlib
import time
import urllib.request
from collections import defaultdict

import numpy as np

TOPIC_BASE="https://raw.githubusercontent.com/castorini/eval/master/topics"
QREL_BASE="https://raw.githubusercontent.com/castorini/eval/master/qrels"
INDEX_FLAT={d:f"beir-v1.0.0-{d}.flat" for d in ("nq","hotpotqa","fever","scifact")}
SEED=20260918

def sha256_file(path: pathlib.Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()

def download(url: str, dest: pathlib.Path) -> None:
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

def read_topics(path: pathlib.Path) -> dict[str,str]:
    out={}
    with gzip.open(path,"rt",encoding="utf-8") as f:
        for ln,line in enumerate(f,1):
            if not line.strip():
                continue
            parts=line.rstrip("\n").split("\t",1)
            if len(parts)!=2:
                raise ValueError(f"bad topic line {ln}")
            out[str(parts[0])]=parts[1]
    return out

def read_qrels(path: pathlib.Path) -> dict[str,dict[str,int]]:
    out=defaultdict(dict)
    with path.open(encoding="utf-8") as f:
        for ln,line in enumerate(f,1):
            if not line.strip():
                continue
            p=line.split()
            if len(p)<4:
                raise ValueError(f"bad qrel line {ln}")
            out[str(p[0])][str(p[2])]=int(float(p[3]))
    return dict(out)

def read_run(path: pathlib.Path) -> dict[str,list[tuple[int,str,float]]]:
    out=defaultdict(list)
    with path.open(encoding="utf-8") as f:
        for ln,line in enumerate(f,1):
            p=line.split()
            if len(p)<6:
                raise ValueError(f"bad TREC run {path}:{ln}")
            out[str(p[0])].append((int(p[3]),str(p[2]),float(p[4])))
    final={}
    for qid,xs in out.items():
        xs.sort(key=lambda z:z[0])
        if len({x[1] for x in xs})!=len(xs):
            raise ValueError(f"duplicate doc IDs for {qid} in {path}")
        final[qid]=xs
    return final

def load_old_gold_helper(repo_root: pathlib.Path):
    path=repo_root/"rag-nature"/"code"/"prepare_inputs_pyserini.py"
    spec=importlib.util.spec_from_file_location("oldprep",path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load gold helper")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dataset",choices=["nq","hotpotqa","fever","scifact"],required=True)
    ap.add_argument("--root",type=pathlib.Path,required=True)
    ap.add_argument("--repo-root",type=pathlib.Path,default=pathlib.Path("."))
    args=ap.parse_args()

    d=args.dataset
    root=args.root.resolve()
    repo=args.repo_root.resolve()
    src=root/"sources"
    src.mkdir(parents=True,exist_ok=True)

    topics_path=src/f"topics.beir-v1.0.0-{d}.test.tsv.gz"
    qrels_path=src/f"qrels.beir-v1.0.0-{d}.test.txt"
    if not topics_path.exists():
        download(f"{TOPIC_BASE}/topics.beir-v1.0.0-{d}.test.tsv.gz",topics_path)
    download(f"{QREL_BASE}/qrels.beir-v1.0.0-{d}.test.txt",qrels_path)

    topics=read_topics(topics_path)
    qrels=read_qrels(qrels_path)
    bm25=read_run(root/"runs"/d/"bm25.trec")
    splade=read_run(root/"runs"/d/"splade.trec")

    eligible=[]
    eligibility={}
    for qid in sorted(topics):
        if qid not in bm25 or qid not in splade or len(bm25[qid])<1000 or len(splade[qid])<1000:
            eligibility[qid]="missing_depth"
            continue

        b100={doc for _,doc,_ in bm25[qid][:100]}
        s100={doc for _,doc,_ in splade[qid][:100]}
        union=b100|s100

        b1000={doc for _,doc,_ in bm25[qid][:1000]}
        s1000={doc for _,doc,_ in splade[qid][:1000]}

        if len(union)<40:
            eligibility[qid]="union_lt_40"
            continue
        if not union<=b1000 or not union<=s1000:
            eligibility[qid]="cross_score_missing"
            continue

        eligibility[qid]="eligible"
        eligible.append(qid)

    if len(eligible)<100:
        raise RuntimeError(f"{d}: only {len(eligible)} eligible queries")

    rng=np.random.default_rng(SEED)
    arr=np.array(sorted(eligible),dtype=object)
    chosen=sorted(rng.choice(arr,size=100,replace=False).tolist())

    helper=load_old_gold_helper(repo)
    gold_report=helper.prepare_gold(d,root,topics)
    gold_path=root/"data"/"gold"/f"{d}.jsonl"
    gold={}
    for line in gold_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            obj=json.loads(line)
            gold[str(obj["_id"])]=obj

    from pyserini.search.lucene import LuceneSearcher
    searcher=LuceneSearcher.from_prebuilt_index(INDEX_FLAT[d])

    frozen_dir=root/"frozen"
    frozen_dir.mkdir(parents=True,exist_ok=True)
    output_path=frozen_dir/f"{d}_sample.jsonl"

    with output_path.open("w",encoding="utf-8") as out:
        for qid in chosen:
            bmap={doc:(rank,score) for rank,doc,score in bm25[qid][:1000]}
            smap={doc:(rank,score) for rank,doc,score in splade[qid][:1000]}
            union=sorted({doc for _,doc,_ in bm25[qid][:100]} | {doc for _,doc,_ in splade[qid][:100]})

            candidates=[]
            for docid in union:
                doc=searcher.doc(docid)
                if doc is None:
                    raise RuntimeError(f"{d}/{qid}: candidate {docid} missing from flat index")

                raw=doc.raw()
                try:
                    obj=json.loads(raw)
                except Exception:
                    obj={"contents":raw}

                title=str(obj.get("title","") or "")
                text=str(obj.get("text",obj.get("contents","")) or "")[:1200]
                br,bs=bmap[docid]
                sr,ss=smap[docid]

                candidates.append({
                    "doc_id":docid,
                    "bm25_rank":int(br),
                    "bm25_score":float(bs),
                    "splade_rank":int(sr),
                    "splade_score":float(ss),
                    "qrel":int(qrels.get(qid,{}).get(docid,0)),
                    "title":title,
                    "text":text
                })

            rec={
                "query_id":qid,
                "dataset":d,
                "query":topics[qid],
                "gold":gold[qid],
                "candidates":candidates
            }
            out.write(json.dumps(rec,ensure_ascii=False)+"\n")

    rows=sum(1 for _ in output_path.open(encoding="utf-8"))
    if rows!=100:
        raise RuntimeError(f"{d}: expected 100 frozen queries, got {rows}")

    counts={}
    for status in eligibility.values():
        counts[status]=counts.get(status,0)+1

    manifest={
        "protocol_id":"RIDI-NATURE-FRONTIER-DOWNSTREAM-v1",
        "technical_clarification":"TECHNICAL_CLARIFICATION_v1.md",
        "dataset":d,
        "seed":SEED,
        "eligible_queries":len(eligible),
        "selected_queries":100,
        "eligibility_counts":counts,
        "selected_query_ids":chosen,
        "artifacts":{
            "topics":{"sha256":sha256_file(topics_path),"bytes":topics_path.stat().st_size},
            "qrels":{"sha256":sha256_file(qrels_path),"bytes":qrels_path.stat().st_size},
            "bm25_top1000":{"sha256":sha256_file(root/"runs"/d/"bm25.trec")},
            "splade_top1000":{"sha256":sha256_file(root/"runs"/d/"splade.trec")},
            "gold":{"sha256":sha256_file(gold_path)},
            "frozen_sample":{"sha256":sha256_file(output_path),"bytes":output_path.stat().st_size}
        },
        "gold_report":gold_report
    }

    manifest_path=frozen_dir/f"{d}_manifest.json"
    manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

    print(json.dumps({
        "dataset":d,
        "eligible_queries":len(eligible),
        "selected_queries":100,
        "eligibility_counts":counts,
        "frozen_sample_sha256":manifest["artifacts"]["frozen_sample"]["sha256"]
    },indent=2))

if __name__=="__main__":
    main()
