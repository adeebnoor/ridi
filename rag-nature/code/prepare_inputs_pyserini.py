"""Prepare immutable RIDI-RAG inputs from official/public sources.

This script performs retrieval and source-to-BEIR gold alignment only. It NEVER calls a
language model. It is intended to run before OSF registration.

Outputs per dataset:
  data/beir/<dataset>/{corpus.jsonl,queries.jsonl,qrels/test.tsv}
  data/gold/<dataset>.jsonl
  runs/<dataset>/{bm25,splade[,contriever]}.trec
  protocol/input_reports/<dataset>.json

Any ambiguous or incomplete gold mapping is a hard failure.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

DATASETS = {"nq", "hotpotqa", "fever", "scifact"}
TOPIC_KEYS = {d: f"beir-v1.0.0-{d}-test" for d in DATASETS}
INDEX_FLAT = {d: f"beir-v1.0.0-{d}.flat" for d in DATASETS}
INDEX_SPLADE = {d: f"beir-v1.0.0-{d}.splade-pp-ed" for d in DATASETS}
INDEX_CONTRIEVER = {"scifact": "beir-v1.0.0-scifact.contriever-msmarco"}
CONTRIEVER_ID = "facebook/contriever-msmarco"
CONTRIEVER_REV = "abe8c1493371369031bcb1e02acb754cf4e162fa"
SPLADE_ID = "naver/splade-cocondenser-ensembledistil"

SOURCE_URLS = {
    "nq": "https://dl.fbaipublicfiles.com/dpr/data/retriever/nq-test.qa.csv",
    "hotpotqa": "https://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_fullwiki_v1.json",
    "fever": "https://s3-eu-west-1.amazonaws.com/fever.public/shared_task_dev.jsonl",
    "scifact": "https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_text(s: str) -> str:
    s = str(s).strip()
    s = re.sub(r"\s+", " ", s)
    return s.casefold()


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "RIDI-RAG-preregistration-input-prep/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r, dest.open("wb") as f:
        shutil.copyfileobj(r, f)


def run_cmd(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def topic_text(v: Any) -> str:
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        for k in ("title", "query", "question", "text", "description"):
            x = v.get(k)
            if isinstance(x, str) and x.strip():
                return x
    raise ValueError(f"unrecognized topic record: {v!r}")


def pyserini_topics_qrels(dataset: str):
    from pyserini.search import get_topics, get_qrels
    key = TOPIC_KEYS[dataset]
    topics_raw = get_topics(key)
    qrels_raw = get_qrels(key)
    topics = {str(q): topic_text(v) for q, v in topics_raw.items()}
    qrels: dict[str, dict[str, int]] = {}
    for q, ds in qrels_raw.items():
        qrels[str(q)] = {str(d): int(v) for d, v in ds.items()}
    return topics, qrels


def make_runs(dataset: str, root: Path, include_dense: bool) -> dict[str, Path]:
    outdir = root / "runs" / dataset
    outdir.mkdir(parents=True, exist_ok=True)
    topic = TOPIC_KEYS[dataset]
    bm25 = outdir / "bm25.trec"
    splade = outdir / "splade.trec"
    run_cmd([sys.executable, "-m", "pyserini.search.lucene", "--threads", "16", "--batch-size", "128", "--index", INDEX_FLAT[dataset], "--topics", topic, "--output", str(bm25), "--output-format", "trec", "--hits", "100", "--bm25", "--remove-query"])
    run_cmd([sys.executable, "-m", "pyserini.search.lucene", "--threads", "16", "--batch-size", "128", "--index", INDEX_SPLADE[dataset], "--topics", topic, "--encoder", SPLADE_ID, "--output", str(splade), "--output-format", "trec", "--hits", "100", "--impact", "--pretokenized", "--remove-query"])
    runs = {"bm25": bm25, "splade": splade}
    if include_dense:
        dense = outdir / "contriever.trec"
        from huggingface_hub import snapshot_download
        snapshot = snapshot_download(repo_id=CONTRIEVER_ID, revision=CONTRIEVER_REV)
        run_cmd([sys.executable, "-m", "pyserini.search.faiss", "--index", INDEX_CONTRIEVER[dataset], "--topics", topic, "--encoder-class", "contriever", "--encoder", snapshot, "--output", str(dense), "--output-format", "trec", "--hits", "100", "--batch", "64", "--threads", "4"])
        runs["contriever"] = dense
    return runs


def parse_run(path: Path) -> dict[str, list[str]]:
    d: dict[str, list[tuple[int, str]]] = defaultdict(list)
    with path.open(encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            p = line.split()
            if len(p) < 6:
                raise ValueError(f"bad TREC run {path}:{ln}")
            d[str(p[0])].append((int(p[3]), str(p[2])))
    out = {}
    for q, xs in d.items():
        xs.sort()
        docs = [doc for _, doc in xs]
        if len(docs) != len(set(docs)):
            raise ValueError(f"duplicate doc in {path} qid={q}")
        out[q] = docs
    return out


def write_beir_compact(dataset: str, root: Path, topics: dict[str, str], qrels: dict[str, dict[str, int]], runs: dict[str, Path]) -> dict[str, Any]:
    dd = root / "data" / "beir" / dataset
    (dd / "qrels").mkdir(parents=True, exist_ok=True)
    with (dd / "queries.jsonl").open("w", encoding="utf-8") as f:
        for qid in sorted(topics):
            f.write(json.dumps({"_id": qid, "text": topics[qid]}, ensure_ascii=False) + "\n")
    with (dd / "qrels" / "test.tsv").open("w", encoding="utf-8") as f:
        f.write("query-id\tcorpus-id\tscore\n")
        for qid in sorted(qrels):
            for did, score in sorted(qrels[qid].items()):
                f.write(f"{qid}\t{did}\t{score}\n")
    run_maps = {k: parse_run(p) for k, p in runs.items()}
    missing_qids = {k: sorted(set(topics) - set(v)) for k, v in run_maps.items()}
    if any(missing_qids.values()):
        raise RuntimeError(f"retrieval omitted queries: { {k: len(v) for k,v in missing_qids.items()} }")
    short = {k: [q for q, docs in v.items() if len(docs) < 100] for k, v in run_maps.items()}
    if any(short.values()):
        raise RuntimeError(f"retrieval has <100 hits: { {k: len(v) for k,v in short.items()} }")
    candidate_ids: set[str] = set()
    for rm in run_maps.values():
        for q in topics:
            candidate_ids.update(rm[q][:100])
    from pyserini.search.lucene import LuceneSearcher
    searcher = LuceneSearcher.from_prebuilt_index(INDEX_FLAT[dataset])
    corpus_path = dd / "corpus.jsonl"
    not_found = []
    with corpus_path.open("w", encoding="utf-8") as f:
        for did in sorted(candidate_ids):
            doc = searcher.doc(did)
            if doc is None:
                not_found.append(did)
                continue
            raw = doc.raw()
            try:
                obj = json.loads(raw)
            except Exception:
                obj = {"contents": raw}
            title = str(obj.get("title", "") or "")
            text = str(obj.get("text", obj.get("contents", "")) or "")
            f.write(json.dumps({"_id": did, "title": title, "text": text}, ensure_ascii=False) + "\n")
    if not_found:
        raise RuntimeError(f"{dataset}: {len(not_found)} candidate docs absent from flat index, first={not_found[:5]}")
    return {"topics": len(topics), "qrels_queries": len(qrels), "candidate_docs": len(candidate_ids), "run_query_counts": {k: len(v) for k, v in run_maps.items()}}


def index_unique(records: Iterable[dict[str, Any]], text_key: str) -> tuple[dict[str, dict[str, Any]], set[str]]:
    one: dict[str, dict[str, Any]] = {}
    collisions: set[str] = set()
    for r in records:
        key = norm_text(r[text_key])
        if key in one:
            collisions.add(key)
        else:
            one[key] = r
    for k in collisions:
        one.pop(k, None)
    return one, collisions


def parse_answers_cell(s: str) -> list[str]:
    s = s.strip()
    for parser in (json.loads, ast.literal_eval):
        try:
            v = parser(s)
            if isinstance(v, (list, tuple)):
                return [str(x) for x in v]
        except Exception:
            pass
    return [s] if s else []


def gold_nq(source: Path, topics: dict[str, str]) -> tuple[dict[str, dict], dict]:
    recs = []
    with source.open(encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) < 2:
                continue
            recs.append({"question": row[0], "answers": parse_answers_cell(row[1])})
    by_text, collisions = index_unique(recs, "question")
    out, missing = {}, []
    for qid, q in topics.items():
        r = by_text.get(norm_text(q))
        if r is None:
            missing.append(qid)
        else:
            out[qid] = {"_id": qid, "answers": r["answers"]}
    return out, {"source_records": len(recs), "ambiguous_text_keys": len(collisions), "missing": missing}


def gold_hotpot(source: Path, topics: dict[str, str]) -> tuple[dict[str, dict], dict]:
    recs = json.loads(source.read_text(encoding="utf-8"))
    by_id = {str(r.get("_id")): r for r in recs if r.get("_id") is not None}
    by_text, collisions = index_unique(recs, "question")
    out, missing = {}, []
    for qid, q in topics.items():
        r = by_id.get(qid) or by_text.get(norm_text(q))
        if r is None:
            missing.append(qid)
        else:
            out[qid] = {"_id": qid, "answers": [str(r["answer"])]}
    return out, {"source_records": len(recs), "ambiguous_text_keys": len(collisions), "missing": missing}


def gold_fever(source: Path, topics: dict[str, str]) -> tuple[dict[str, dict], dict]:
    recs = [json.loads(x) for x in source.read_text(encoding="utf-8").splitlines() if x.strip()]
    by_id = {str(r.get("id")): r for r in recs if r.get("id") is not None}
    by_text, collisions = index_unique(recs, "claim")
    out, missing = {}, []
    allowed = {"SUPPORTS", "REFUTES", "NOT ENOUGH INFO", "NOT_ENOUGH_INFO"}
    for qid, q in topics.items():
        r = by_id.get(qid)
        if r is not None and norm_text(r.get("claim", "")) != norm_text(q):
            r = None
        r = r or by_text.get(norm_text(q))
        if r is None:
            missing.append(qid); continue
        lab = str(r.get("label", "")).upper().strip()
        if lab not in allowed:
            raise RuntimeError(f"FEVER unexpected label {lab!r} qid={qid}")
        lab = lab.replace(" ", "_")
        out[qid] = {"_id": qid, "labels": [lab]}
    return out, {"source_records": len(recs), "ambiguous_text_keys": len(collisions), "missing": missing}


def gold_scifact(tar_path: Path, topics: dict[str, str]) -> tuple[dict[str, dict], dict]:
    with tarfile.open(tar_path, "r:gz") as tf:
        cand = [n for n in tf.getnames() if n.endswith("claims_dev.jsonl")]
        if len(cand) != 1:
            raise RuntimeError(f"SciFact tar expected one claims_dev.jsonl, got {cand}")
        fh = tf.extractfile(cand[0])
        if fh is None:
            raise RuntimeError("could not extract SciFact claims_dev")
        recs = [json.loads(x) for x in io.TextIOWrapper(fh, encoding="utf-8") if x.strip()]
    by_id = {str(r.get("id")): r for r in recs if r.get("id") is not None}
    by_text, collisions = index_unique(recs, "claim")
    out, missing = {}, []
    for qid, q in topics.items():
        r = by_id.get(qid)
        if r is not None and norm_text(r.get("claim", "")) != norm_text(q):
            r = None
        r = r or by_text.get(norm_text(q))
        if r is None:
            missing.append(qid); continue
        ev = r.get("evidence") or {}
        labels = set()
        for rationales in ev.values():
            for rat in rationales:
                lab = str(rat.get("label", "")).upper()
                if lab == "SUPPORT": labels.add("SUPPORTS")
                elif lab == "CONTRADICT": labels.add("REFUTES")
                else: raise RuntimeError(f"SciFact unexpected rationale label {lab!r}")
        if len(labels) > 1:
            raise RuntimeError(f"SciFact mixed labels for qid={qid}: {labels}")
        label = next(iter(labels)) if labels else "NOT_ENOUGH_INFO"
        out[qid] = {"_id": qid, "labels": [label]}
    return out, {"source_records": len(recs), "ambiguous_text_keys": len(collisions), "missing": missing}


def prepare_gold(dataset: str, root: Path, topics: dict[str, str]) -> dict[str, Any]:
    cache = root / ".source_cache"
    cache.mkdir(parents=True, exist_ok=True)
    ext = {"nq": ".csv", "hotpotqa": ".json", "fever": ".jsonl", "scifact": ".tar.gz"}[dataset]
    source = cache / f"{dataset}{ext}"
    if not source.exists():
        download(SOURCE_URLS[dataset], source)
    if dataset == "nq": out, rep = gold_nq(source, topics)
    elif dataset == "hotpotqa": out, rep = gold_hotpot(source, topics)
    elif dataset == "fever": out, rep = gold_fever(source, topics)
    elif dataset == "scifact": out, rep = gold_scifact(source, topics)
    else: raise ValueError(dataset)
    if rep["missing"]:
        raise RuntimeError(f"{dataset}: gold source failed to map {len(rep['missing'])}/{len(topics)} BEIR queries; first={rep['missing'][:10]}")
    gp = root / "data" / "gold" / f"{dataset}.jsonl"
    gp.parent.mkdir(parents=True, exist_ok=True)
    with gp.open("w", encoding="utf-8") as f:
        for qid in sorted(out):
            f.write(json.dumps(out[qid], ensure_ascii=False) + "\n")
    rep.update({"mapped": len(out), "source_url": SOURCE_URLS[dataset], "source_sha256": sha256_file(source), "gold_sha256": sha256_file(gp)})
    return rep


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(DATASETS), required=True)
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--skip-retrieval", action="store_true")
    args = ap.parse_args()
    root = args.root.resolve(); root.mkdir(parents=True, exist_ok=True)
    dataset = args.dataset
    topics, qrels = pyserini_topics_qrels(dataset)
    if not topics or not qrels:
        raise RuntimeError(f"{dataset}: Pyserini topics/qrels unavailable")
    include_dense = dataset == "scifact"
    if args.skip_retrieval:
        rd = root / "runs" / dataset
        runs = {"bm25": rd / "bm25.trec", "splade": rd / "splade.trec"}
        if include_dense: runs["contriever"] = rd / "contriever.trec"
        missing = [str(x) for x in runs.values() if not x.exists()]
        if missing: raise RuntimeError(f"missing pre-existing runs: {missing}")
    else:
        runs = make_runs(dataset, root, include_dense)
    data_report = write_beir_compact(dataset, root, topics, qrels, runs)
    gold_report = prepare_gold(dataset, root, topics)
    report = {"dataset": dataset, "topic_key": TOPIC_KEYS[dataset], "flat_index": INDEX_FLAT[dataset], "splade_index": INDEX_SPLADE[dataset], "dense_index": INDEX_CONTRIEVER.get(dataset), "data": data_report, "gold": gold_report, "artifacts": {}}
    paths = [root / "data" / "beir" / dataset / "corpus.jsonl", root / "data" / "beir" / dataset / "queries.jsonl", root / "data" / "beir" / dataset / "qrels" / "test.tsv", root / "data" / "gold" / f"{dataset}.jsonl", *runs.values()]
    for p in paths:
        report["artifacts"][str(p.relative_to(root))] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    rp = root / "protocol" / "input_reports" / f"{dataset}.json"
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
