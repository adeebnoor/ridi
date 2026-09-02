"""Assemble prospectively frozen RIDI-RAG benchmark inputs without any LLM calls.

Scientific invariants:
- benchmark topics/qrels come from hashable Castorini BEIR resources;
- retrieval runs are never modified;
- a query is pre-generation ineligible if any preregistered retriever has <100 hits or
  any top-100 candidate cannot be materialized from the same frozen BEIR flat index;
- source-derived gold must map every original BEIR test query exactly (ID or unique
  normalized-text match); no fuzzy matching is allowed;
- all source files and produced artifacts are SHA-256 hashed in the provenance report.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import shutil
import tarfile
import time
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from beir_local_resources import load_topics_qrels

DATASETS = {"nq", "hotpotqa", "fever", "scifact"}
INDEX_FLAT = {d: f"beir-v1.0.0-{d}.flat" for d in DATASETS}

NQ_COMMIT = "fb26a3073b1fe636c97302890a27b491d6530130"
HOTPOT_COMMIT = "a8af52d40ca73810f304ad1aa28b0cbb518f37de"
HOTPOT_SHA256 = "78933c0a31a5f7b420d4effdf4cd4eed573b28c6a3da6179dcf7a02b39e51d03"

SOURCE_URLS = {
    "nq": f"https://raw.githubusercontent.com/google-research-datasets/natural-questions/{NQ_COMMIT}/nq_open/NQ-open.dev.jsonl",
    "hotpotqa": f"https://huggingface.co/datasets/hotpotqa/hotpot_qa/resolve/{HOTPOT_COMMIT}/fullwiki/validation-00000-of-00001.parquet?download=true",
    "fever": "https://s3-eu-west-1.amazonaws.com/fever.public/shared_task_dev.jsonl",
    "scifact": "https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz",
}
SOURCE_EXT = {"nq": ".jsonl", "hotpotqa": ".parquet", "fever": ".jsonl", "scifact": ".tar.gz"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_text(s: str) -> str:
    return re.sub(r"\s+", " ", str(s).strip()).casefold()


def download(url: str, dest: Path, attempts: int = 5) -> None:
    """Atomic retrying download. Content identity is enforced separately by hash."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "RIDI-RAG-Nature-prereg-input-prep/2.0"})
            with urllib.request.urlopen(req, timeout=240) as r, tmp.open("wb") as f:
                shutil.copyfileobj(r, f)
            if tmp.stat().st_size <= 0:
                raise RuntimeError(f"empty download: {url}")
            tmp.replace(dest)
            return
        except Exception as e:
            last = e
            if tmp.exists():
                tmp.unlink()
            if attempt < attempts:
                time.sleep(min(30, 2 ** attempt))
    raise RuntimeError(f"download failed after {attempts} attempts: {url}") from last


def parse_run(path: Path) -> dict[str, list[str]]:
    by_q: dict[str, list[tuple[int, str]]] = defaultdict(list)
    with path.open(encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            p = line.split()
            if len(p) < 6:
                raise RuntimeError(f"bad TREC row {path}:{ln}")
            by_q[str(p[0])].append((int(p[3]), str(p[2])))
    out: dict[str, list[str]] = {}
    for qid, rows in by_q.items():
        rows.sort()
        docs = [d for _, d in rows]
        if len(docs) != len(set(docs)):
            raise RuntimeError(f"duplicate retrieved document: {path} qid={qid}")
        out[qid] = docs
    return out


def find_runs(root: Path, dataset: str) -> dict[str, Path]:
    rd = root / "runs" / dataset
    names = ["bm25", "splade"] + (["contriever"] if dataset == "scifact" else [])
    runs = {name: rd / f"{name}.trec" for name in names}
    missing = [str(p) for p in runs.values() if not p.exists()]
    if missing:
        raise RuntimeError(f"missing frozen retrieval runs: {missing}")
    return runs


def materialize_compact(dataset: str, root: Path, topics: dict[str, str], qrels: dict[str, dict[str, int]], runs: dict[str, Path]) -> dict[str, Any]:
    run_maps = {name: parse_run(path) for name, path in runs.items()}
    missing_qids = {name: sorted(set(topics) - set(rm)) for name, rm in run_maps.items()}
    if any(missing_qids.values()):
        raise RuntimeError(f"retrieval omitted entire queries: { {k: len(v) for k,v in missing_qids.items()} }")

    short_by_retriever = {name: sorted(q for q in topics if len(rm[q]) < 100) for name, rm in run_maps.items()}
    short_qids = set().union(*(set(v) for v in short_by_retriever.values())) if short_by_retriever else set()
    stage1 = sorted(set(topics) - short_qids)

    # Materialize every top-100 candidate for otherwise eligible queries from the same
    # Lucene flat index used for the lexical BEIR snapshot. Missing documents cause the
    # entire affected query to be excluded before panel selection, never a within-query drop.
    candidate_to_qids: dict[str, set[str]] = defaultdict(set)
    for qid in stage1:
        for rm in run_maps.values():
            for did in rm[qid][:100]:
                candidate_to_qids[did].add(qid)

    from pyserini.search.lucene import LuceneSearcher
    searcher = LuceneSearcher.from_prebuilt_index(INDEX_FLAT[dataset])
    docs: dict[str, dict[str, str]] = {}
    missing_docs: list[str] = []
    for did in sorted(candidate_to_qids):
        doc = searcher.doc(did)
        if doc is None:
            missing_docs.append(did)
            continue
        raw = doc.raw()
        try:
            obj = json.loads(raw)
        except Exception:
            obj = {"contents": raw}
        docs[did] = {
            "_id": did,
            "title": str(obj.get("title", "") or ""),
            "text": str(obj.get("text", obj.get("contents", "")) or ""),
        }

    materialization_bad_qids: set[str] = set()
    for did in missing_docs:
        materialization_bad_qids.update(candidate_to_qids[did])
    eligible_qids = sorted(set(stage1) - materialization_bad_qids)
    if not eligible_qids:
        raise RuntimeError(f"{dataset}: no eligible queries after pre-generation input integrity checks")

    # Retain only documents that can actually occur in an eligible query.
    needed: set[str] = set()
    for qid in eligible_qids:
        for rm in run_maps.values():
            needed.update(rm[qid][:100])
    unresolved = sorted(needed - set(docs))
    if unresolved:
        raise RuntimeError(f"internal materialization error: eligible queries still reference {len(unresolved)} missing docs")

    dd = root / "data" / "beir" / dataset
    (dd / "qrels").mkdir(parents=True, exist_ok=True)
    with (dd / "queries.jsonl").open("w", encoding="utf-8") as f:
        for qid in eligible_qids:
            f.write(json.dumps({"_id": qid, "text": topics[qid]}, ensure_ascii=False) + "\n")
    with (dd / "qrels" / "test.tsv").open("w", encoding="utf-8") as f:
        f.write("query-id\tcorpus-id\tscore\n")
        for qid in eligible_qids:
            for did, score in sorted(qrels.get(qid, {}).items()):
                f.write(f"{qid}\t{did}\t{score}\n")
    with (dd / "corpus.jsonl").open("w", encoding="utf-8") as f:
        for did in sorted(needed):
            f.write(json.dumps(docs[did], ensure_ascii=False) + "\n")

    exclusion_rows = []
    for qid in sorted(short_qids):
        exclusion_rows.append({"qid": qid, "reason": "retriever_depth_lt_100", "retrievers": sorted(k for k,v in short_by_retriever.items() if qid in set(v))})
    for qid in sorted(materialization_bad_qids):
        exclusion_rows.append({"qid": qid, "reason": "top100_candidate_absent_from_frozen_flat_index", "missing_doc_ids": sorted(d for d in missing_docs if qid in candidate_to_qids[d])})
    ex_path = root / "protocol" / "input_reports" / f"{dataset}_prepanel_exclusions.json"
    ex_path.parent.mkdir(parents=True, exist_ok=True)
    ex_path.write_text(json.dumps(exclusion_rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return {
        "original_topic_count": len(topics),
        "eligible_topic_count": len(eligible_qids),
        "excluded_topic_count": len(topics) - len(eligible_qids),
        "short_run_counts": {k: len(v) for k,v in short_by_retriever.items()},
        "short_run_qids": short_by_retriever,
        "flat_index_missing_doc_count": len(missing_docs),
        "flat_index_missing_doc_ids": missing_docs,
        "materialization_excluded_qids": sorted(materialization_bad_qids),
        "candidate_docs_materialized": len(needed),
        "run_query_counts": {k: len(v) for k,v in run_maps.items()},
        "prepanel_exclusions_file": str(ex_path.relative_to(root)),
        "prepanel_exclusions_sha256": sha256_file(ex_path),
    }


def index_unique(records: Iterable[dict[str, Any]], text_key: str) -> tuple[dict[str, dict[str, Any]], set[str]]:
    one: dict[str, dict[str, Any]] = {}
    collisions: set[str] = set()
    for r in records:
        key = norm_text(r[text_key])
        if key in one:
            collisions.add(key)
        else:
            one[key] = r
    for key in collisions:
        one.pop(key, None)
    return one, collisions


def map_nq(source: Path, topics: dict[str, str]):
    recs = [json.loads(x) for x in source.read_text(encoding="utf-8").splitlines() if x.strip()]
    by_text, collisions = index_unique(recs, "question")
    out, missing = {}, []
    for qid, q in topics.items():
        r = by_text.get(norm_text(q))
        if r is None:
            missing.append(qid)
        else:
            answers = [str(x) for x in (r.get("answer") or [])]
            if not answers:
                raise RuntimeError(f"NQ empty answer list qid={qid}")
            out[qid] = {"_id": qid, "answers": answers}
    return out, {"source_records": len(recs), "ambiguous_text_keys": len(collisions), "missing": missing, "mapping_rule": "unique normalized question text"}


def map_hotpot(source: Path, topics: dict[str, str]):
    import pyarrow.parquet as pq
    recs = pq.read_table(source).to_pylist()
    by_id = {str(r.get("id")): r for r in recs if r.get("id") is not None}
    by_text, collisions = index_unique(recs, "question")
    out, missing, id_text_mismatch = {}, [], []
    for qid, q in topics.items():
        r = by_id.get(qid)
        if r is not None and norm_text(r.get("question", "")) != norm_text(q):
            id_text_mismatch.append(qid)
            r = None
        r = r or by_text.get(norm_text(q))
        if r is None:
            missing.append(qid)
        else:
            out[qid] = {"_id": qid, "answers": [str(r["answer"])]}
    return out, {"source_records": len(recs), "ambiguous_text_keys": len(collisions), "id_text_mismatch": id_text_mismatch, "missing": missing, "mapping_rule": "exact id with normalized-text verification, else unique normalized question text"}


def map_fever(source: Path, topics: dict[str, str]):
    recs = [json.loads(x) for x in source.read_text(encoding="utf-8").splitlines() if x.strip()]
    by_id = {str(r.get("id")): r for r in recs if r.get("id") is not None}
    by_text, collisions = index_unique(recs, "claim")
    allowed = {"SUPPORTS", "REFUTES", "NOT ENOUGH INFO", "NOT_ENOUGH_INFO"}
    out, missing, id_text_mismatch = {}, [], []
    for qid, q in topics.items():
        r = by_id.get(qid)
        if r is not None and norm_text(r.get("claim", "")) != norm_text(q):
            id_text_mismatch.append(qid)
            r = None
        r = r or by_text.get(norm_text(q))
        if r is None:
            missing.append(qid); continue
        label = str(r.get("label", "")).upper().strip()
        if label not in allowed:
            raise RuntimeError(f"FEVER unexpected label {label!r} qid={qid}")
        out[qid] = {"_id": qid, "labels": [label.replace(" ", "_")]}
    return out, {"source_records": len(recs), "ambiguous_text_keys": len(collisions), "id_text_mismatch": id_text_mismatch, "missing": missing, "mapping_rule": "exact id with normalized-text verification, else unique normalized claim text"}


def map_scifact(source: Path, topics: dict[str, str]):
    with tarfile.open(source, "r:gz") as tf:
        names = [n for n in tf.getnames() if n.endswith("claims_dev.jsonl")]
        if len(names) != 1:
            raise RuntimeError(f"SciFact tar expected one claims_dev.jsonl, got {names}")
        fh = tf.extractfile(names[0])
        if fh is None:
            raise RuntimeError("SciFact claims_dev extraction failed")
        recs = [json.loads(x) for x in io.TextIOWrapper(fh, encoding="utf-8") if x.strip()]
    by_id = {str(r.get("id")): r for r in recs if r.get("id") is not None}
    by_text, collisions = index_unique(recs, "claim")
    out, missing, id_text_mismatch = {}, [], []
    for qid, q in topics.items():
        r = by_id.get(qid)
        if r is not None and norm_text(r.get("claim", "")) != norm_text(q):
            id_text_mismatch.append(qid)
            r = None
        r = r or by_text.get(norm_text(q))
        if r is None:
            missing.append(qid); continue
        labels = set()
        for rationales in (r.get("evidence") or {}).values():
            for rat in rationales:
                lab = str(rat.get("label", "")).upper()
                if lab == "SUPPORT": labels.add("SUPPORTS")
                elif lab == "CONTRADICT": labels.add("REFUTES")
                else: raise RuntimeError(f"SciFact unexpected evidence label {lab!r} qid={qid}")
        if len(labels) > 1:
            raise RuntimeError(f"SciFact mixed labels qid={qid}: {sorted(labels)}")
        out[qid] = {"_id": qid, "labels": [next(iter(labels)) if labels else "NOT_ENOUGH_INFO"]}
    return out, {"source_records": len(recs), "ambiguous_text_keys": len(collisions), "id_text_mismatch": id_text_mismatch, "missing": missing, "mapping_rule": "exact id with normalized-text verification, else unique normalized claim text"}


def prepare_gold(dataset: str, root: Path, topics: dict[str, str]) -> dict[str, Any]:
    cache = root / ".source_cache"
    source = cache / f"{dataset}{SOURCE_EXT[dataset]}"
    if not source.exists():
        download(SOURCE_URLS[dataset], source)
    actual_sha = sha256_file(source)
    if dataset == "hotpotqa" and actual_sha != HOTPOT_SHA256:
        raise RuntimeError(f"HotpotQA frozen parquet SHA-256 mismatch: {actual_sha} != {HOTPOT_SHA256}")

    if dataset == "nq": out, rep = map_nq(source, topics)
    elif dataset == "hotpotqa": out, rep = map_hotpot(source, topics)
    elif dataset == "fever": out, rep = map_fever(source, topics)
    elif dataset == "scifact": out, rep = map_scifact(source, topics)
    else: raise ValueError(dataset)

    # Hard preregistration gate: gold provenance must cover the original benchmark test
    # set, not merely the later selected panel.
    if rep["missing"]:
        raise RuntimeError(f"{dataset}: source gold failed to map {len(rep['missing'])}/{len(topics)} original BEIR queries; first={rep['missing'][:10]}")
    if len(out) != len(topics):
        raise RuntimeError(f"{dataset}: mapped gold cardinality mismatch {len(out)} != {len(topics)}")

    gp = root / "data" / "gold" / f"{dataset}.jsonl"
    gp.parent.mkdir(parents=True, exist_ok=True)
    with gp.open("w", encoding="utf-8") as f:
        for qid in sorted(out):
            f.write(json.dumps(out[qid], ensure_ascii=False) + "\n")
    rep.update({
        "mapped": len(out),
        "source_url": SOURCE_URLS[dataset],
        "source_sha256": actual_sha,
        "source_expected_sha256": HOTPOT_SHA256 if dataset == "hotpotqa" else None,
        "source_revision": NQ_COMMIT if dataset == "nq" else HOTPOT_COMMIT if dataset == "hotpotqa" else None,
        "gold_sha256": sha256_file(gp),
    })
    return rep


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(DATASETS), required=True)
    ap.add_argument("--root", type=Path, required=True)
    args = ap.parse_args()
    dataset = args.dataset
    root = args.root.resolve(); root.mkdir(parents=True, exist_ok=True)

    topics, qrels, beir_meta = load_topics_qrels(dataset, root / ".beir_resources")
    runs = find_runs(root, dataset)
    data_report = materialize_compact(dataset, root, topics, qrels, runs)
    gold_report = prepare_gold(dataset, root, topics)

    report = {
        "schema_version": "ridi-rag-prereg-input-provenance-v2",
        "dataset": dataset,
        "prospective_status": "NO_LLM_GENERATION_PERFORMED",
        "beir_benchmark_resources": {
            "topics_url": beir_meta["topics_url"], "topics_sha256": beir_meta["topics_sha256"],
            "qrels_url": beir_meta["qrels_url"], "qrels_sha256": beir_meta["qrels_sha256"],
            "topic_count": beir_meta["topic_count"], "qrel_query_count": beir_meta["qrel_query_count"],
            "qrel_pair_count": beir_meta["qrel_pair_count"],
        },
        "flat_index": INDEX_FLAT[dataset],
        "data": data_report,
        "gold": gold_report,
        "artifacts": {},
    }
    paths = [
        root / "data" / "beir" / dataset / "corpus.jsonl",
        root / "data" / "beir" / dataset / "queries.jsonl",
        root / "data" / "beir" / dataset / "qrels" / "test.tsv",
        root / "data" / "gold" / f"{dataset}.jsonl",
        *runs.values(),
    ]
    for p in paths:
        report["artifacts"][str(p.relative_to(root))] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    rp = root / "protocol" / "input_reports" / f"{dataset}.json"
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
