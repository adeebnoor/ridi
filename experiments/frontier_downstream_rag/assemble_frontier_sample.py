#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import pathlib
import sys
import time
import urllib.request
from collections import defaultdict

import numpy as np

TOPIC_BASE="https://raw.githubusercontent.com/castorini/eval/master/topics"
QREL_BASE="https://raw.githubusercontent.com/castorini/eval/master/qrels"
INDEX_FLAT={d:f"beir-v1.0.0-{d}.flat" for d in ("nq","hotpotqa","fever","scifact")}
SEED=20260918
KS=(5,10,20)
ETAS=(0.0001,0.001)

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
            with urllib.request.urlopen(req,timeout=180) as r, dest.open("wb") as f:
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
            p=line.rstrip("\n").split("\t",1)
            if len(p)!=2:
                raise ValueError(f"bad topic line {ln}")
            out[str(p[0])]=p[1]
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
        raise RuntimeError("cannot load registered gold-mapping helper")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def build_gold_map(helper, dataset: str, root: pathlib.Path, topics: dict[str,str]):
    cache=root/".source_cache"
    cache.mkdir(parents=True,exist_ok=True)
    ext={"nq":".csv","hotpotqa":".json","fever":".jsonl","scifact":".tar.gz"}[dataset]
    source=cache/f"{dataset}{ext}"
    if not source.exists():
        helper.download(helper.SOURCE_URLS[dataset],source)
    if dataset=="nq":
        gold,report=helper.gold_nq(source,topics)
    elif dataset=="hotpotqa":
        gold,report=helper.gold_hotpot(source,topics)
    elif dataset=="fever":
        gold,report=helper.gold_fever(source,topics)
    elif dataset=="scifact":
        gold,report=helper.gold_scifact(source,topics)
    else:
        raise ValueError(dataset)
    report=dict(report)
    report["mapped"]=len(gold)
    report["source_url"]=helper.SOURCE_URLS[dataset]
    report["source_sha256"]=sha256_file(source)
    return gold,report,source

def ordered_ids(ids, scores, k):
    pairs=sorted(zip(ids,scores),key=lambda z:(-float(z[1]),str(z[0])))
    return [str(doc) for doc,_ in pairs[:k]]

def eta_key(eta: float) -> str:
    return "eta_0_0001" if eta==0.0001 else "eta_0_001"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dataset",choices=["nq","hotpotqa","fever","scifact"],required=True)
    ap.add_argument("--root",type=pathlib.Path,required=True)
    ap.add_argument("--repo-root",type=pathlib.Path,default=pathlib.Path("."))
    args=ap.parse_args()

    d=args.dataset
    root=args.root.resolve()
    repo=args.repo_root.resolve()
    sys.path.insert(0,str(repo/"src"))
    from ridi_audit.selector import identity_utility_frontier, select_identity_control

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

    helper=load_old_gold_helper(repo)
    gold,gold_report,gold_source=build_gold_map(helper,d,root,topics)

    eligibility={}
    common_by_q={}
    for qid in sorted(topics):
        if qid not in gold:
            eligibility[qid]="gold_unmapped"
            continue
        if qid not in bm25 or qid not in splade or len(bm25[qid])<1000 or len(splade[qid])<1000:
            eligibility[qid]="missing_depth"
            continue
        bmap={doc:(rank,score) for rank,doc,score in bm25[qid][:1000]}
        smap={doc:(rank,score) for rank,doc,score in splade[qid][:1000]}
        common=sorted(set(bmap).intersection(smap))
        if len(common)<40:
            eligibility[qid]="common_lt_40"
            continue
        eligibility[qid]="eligible"
        common_by_q[qid]=common

    eligible=sorted(common_by_q)
    if len(eligible)<100:
        counts={s:list(eligibility.values()).count(s) for s in sorted(set(eligibility.values()))}
        raise RuntimeError(f"{d}: only {len(eligible)} amended-eligible queries; counts={counts}")

    rng=np.random.default_rng(SEED)
    chosen=sorted(rng.choice(np.array(eligible,dtype=object),size=100,replace=False).tolist())

    from pyserini.search.lucene import LuceneSearcher
    searcher=LuceneSearcher.from_prebuilt_index(INDEX_FLAT[d])

    frozen_dir=root/"frozen"
    frozen_dir.mkdir(parents=True,exist_ok=True)
    output_path=frozen_dir/f"{d}_sample.jsonl"

    identity_summary=[]
    with output_path.open("w",encoding="utf-8") as out:
        for qid in chosen:
            bmap={doc:(rank,score) for rank,doc,score in bm25[qid][:1000]}
            smap={doc:(rank,score) for rank,doc,score in splade[qid][:1000]}
            ids=common_by_q[qid]
            s0=[float(bmap[x][1]) for x in ids]
            s1=[float(smap[x][1]) for x in ids]

            states={}
            frontiers={}
            text_needed=set()

            for k in KS:
                reference=ordered_ids(ids,s0,k)
                updated=ordered_ids(ids,s1,k)
                states[f"k{k}_reference"]=reference
                states[f"k{k}_updated"]=updated
                text_needed.update(reference)
                text_needed.update(updated)

                frontier=identity_utility_frontier(ids,s0,s1,k)
                for eta in ETAS:
                    sel=select_identity_control(frontier,eta)
                    raw_selected=[ids[int(i)] for i in sel["selected_indices"]]
                    # Controlled contexts use the updated retriever ordering.
                    controlled=ordered_ids(raw_selected,[s1[ids.index(x)] for x in raw_selected],k)
                    ek=eta_key(eta)
                    states[f"k{k}_{ek}"]=controlled
                    text_needed.update(controlled)
                    frontiers[f"k{k}_{ek}"]={
                        "j_eta":int(sel["j_eta"]),
                        "delta_unconstrained":int(sel["delta_unconstrained"]),
                        "avoidable_turnover_fraction":sel["avoidable_turnover_fraction"],
                        "utility_regret":float(sel["utility_regret"]),
                        "ridi_unconstrained":float(sel["ridi_unconstrained"]),
                        "ridi_controlled":float(sel["ridi_controlled"])
                    }

            documents={}
            for docid in sorted(text_needed):
                doc=searcher.doc(docid)
                if doc is None:
                    raise RuntimeError(f"{d}/{qid}: selected candidate {docid} missing from flat index")
                raw=doc.raw()
                try:
                    obj=json.loads(raw)
                except Exception:
                    obj={"contents":raw}
                documents[docid]={
                    "title":str(obj.get("title","") or ""),
                    "text":str(obj.get("text",obj.get("contents","")) or "")[:1200],
                    "qrel":int(qrels.get(qid,{}).get(docid,0)),
                    "bm25_rank":int(bmap[docid][0]),
                    "bm25_score":float(bmap[docid][1]),
                    "splade_rank":int(smap[docid][0]),
                    "splade_score":float(smap[docid][1])
                }

            candidate_scores=[
                {
                    "doc_id":docid,
                    "bm25_rank":int(bmap[docid][0]),
                    "bm25_score":float(bmap[docid][1]),
                    "splade_rank":int(smap[docid][0]),
                    "splade_score":float(smap[docid][1]),
                    "qrel":int(qrels.get(qid,{}).get(docid,0))
                }
                for docid in ids
            ]

            primary=frontiers["k10_eta_0_001"]
            identity_summary.append({
                "query_id":qid,
                "common_n":len(ids),
                **primary
            })

            rec={
                "query_id":qid,
                "dataset":d,
                "query":topics[qid],
                "gold":gold[qid],
                "common_candidate_count":len(ids),
                "candidate_scores":candidate_scores,
                "states":states,
                "frontier":frontiers,
                "documents":documents
            }
            out.write(json.dumps(rec,ensure_ascii=False)+"\n")

    rows=sum(1 for _ in output_path.open(encoding="utf-8"))
    if rows!=100:
        raise RuntimeError(f"{d}: expected 100 frozen queries, got {rows}")

    counts={s:list(eligibility.values()).count(s) for s in sorted(set(eligibility.values()))}
    primary_delta=np.array([x["delta_unconstrained"] for x in identity_summary],dtype=float)
    primary_j=np.array([x["j_eta"] for x in identity_summary],dtype=float)
    primary_avoid=[x["avoidable_turnover_fraction"] for x in identity_summary if x["avoidable_turnover_fraction"] is not None]

    manifest={
        "protocol_id":"RIDI-NATURE-FRONTIER-DOWNSTREAM-v1",
        "amendment":"AMENDMENT_1_PRE_GENERATION.md",
        "dataset":d,
        "seed":SEED,
        "candidate_universe":"intersection of BM25 top1000 and SPLADE++ top1000",
        "eligible_queries":len(eligible),
        "selected_queries":100,
        "eligibility_counts":counts,
        "selected_query_ids":chosen,
        "primary_identity_summary":{
            "k":10,
            "eta":0.001,
            "mean_unconstrained_changed_slots":float(primary_delta.mean()),
            "mean_controlled_changed_slots":float(primary_j.mean()),
            "mean_changed_slots_reduction":float((primary_delta-primary_j).mean()),
            "mean_avoidable_turnover_fraction_among_changed":float(np.mean(primary_avoid)) if primary_avoid else None
        },
        "artifacts":{
            "topics":{"sha256":sha256_file(topics_path),"bytes":topics_path.stat().st_size},
            "qrels":{"sha256":sha256_file(qrels_path),"bytes":qrels_path.stat().st_size},
            "bm25_top1000":{"sha256":sha256_file(root/"runs"/d/"bm25.trec")},
            "splade_top1000":{"sha256":sha256_file(root/"runs"/d/"splade.trec")},
            "gold_source":{"sha256":sha256_file(gold_source),"bytes":gold_source.stat().st_size},
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
        "primary_identity_summary":manifest["primary_identity_summary"],
        "frozen_sample_sha256":manifest["artifacts"]["frozen_sample"]["sha256"]
    },indent=2))

if __name__=="__main__":
    main()
