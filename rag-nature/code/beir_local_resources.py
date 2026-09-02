"""Local, hashable BEIR topics/qrels for prospective RIDI-RAG preparation.

Pyserini/Anserini may resolve named evaluation resources through the JVM. For a
prospective preregistration we instead download the canonical Castorini evaluation files
with Python, parse them locally, and record exact SHA-256 hashes before any LLM call.
"""
from __future__ import annotations

import gzip
import hashlib
import shutil
import urllib.request
from pathlib import Path

DATASETS = {"nq", "hotpotqa", "fever", "scifact"}
TOPICS_BASE = "https://raw.githubusercontent.com/castorini/eval/master/topics"
QRELS_BASE = "https://raw.githubusercontent.com/castorini/eval/master/qrels"
USER_AGENT = "RIDI-RAG-Nature-prereg-input-prep/1.0"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resource_urls(dataset: str) -> tuple[str, str]:
    if dataset not in DATASETS:
        raise ValueError(dataset)
    stem = f"beir-v1.0.0-{dataset}.test"
    return (
        f"{TOPICS_BASE}/topics.{stem}.tsv.gz",
        f"{QRELS_BASE}/qrels.{stem}.txt",
    )


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    tmp = dest.with_suffix(dest.suffix + ".part")
    try:
        with urllib.request.urlopen(req, timeout=180) as r, tmp.open("wb") as f:
            shutil.copyfileobj(r, f)
        if tmp.stat().st_size == 0:
            raise RuntimeError(f"downloaded empty resource: {url}")
        tmp.replace(dest)
    finally:
        if tmp.exists():
            tmp.unlink()


def ensure_resources(dataset: str, cache_dir: Path) -> dict:
    topic_url, qrels_url = resource_urls(dataset)
    cache_dir.mkdir(parents=True, exist_ok=True)
    topic_path = cache_dir / f"topics.beir-v1.0.0-{dataset}.test.tsv.gz"
    qrels_path = cache_dir / f"qrels.beir-v1.0.0-{dataset}.test.txt"
    if not topic_path.exists():
        _download(topic_url, topic_path)
    if not qrels_path.exists():
        _download(qrels_url, qrels_path)
    return {
        "topics_path": topic_path,
        "qrels_path": qrels_path,
        "topics_url": topic_url,
        "qrels_url": qrels_url,
        "topics_sha256": sha256_file(topic_path),
        "qrels_sha256": sha256_file(qrels_path),
    }


def load_topics_qrels(dataset: str, cache_dir: Path) -> tuple[dict[str, str], dict[str, dict[str, int]], dict]:
    meta = ensure_resources(dataset, cache_dir)
    topics: dict[str, str] = {}
    with gzip.open(meta["topics_path"], "rt", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line:
                continue
            p = line.split("\t", 1)
            if len(p) != 2:
                raise RuntimeError(f"bad BEIR topics line {ln}: {line[:120]!r}")
            qid, text = p[0].strip(), p[1].strip()
            if not qid or not text or qid in topics:
                raise RuntimeError(f"invalid/duplicate BEIR topic qid={qid!r} line={ln}")
            topics[qid] = text

    qrels: dict[str, dict[str, int]] = {}
    with Path(meta["qrels_path"]).open("r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            p = line.split()
            if not p:
                continue
            if len(p) != 4:
                raise RuntimeError(f"bad BEIR qrels line {ln}: {line[:120]!r}")
            qid, _, did, score = p
            qrels.setdefault(str(qid), {})[str(did)] = int(score)

    if not topics or not qrels:
        raise RuntimeError(f"empty BEIR resources for {dataset}")
    unknown_qrels = sorted(set(qrels) - set(topics))
    if unknown_qrels:
        raise RuntimeError(f"qrels contain unknown topic ids for {dataset}: {unknown_qrels[:10]}")
    meta = dict(meta)
    meta.update({"topic_count": len(topics), "qrel_query_count": len(qrels), "qrel_pair_count": sum(len(v) for v in qrels.values())})
    return topics, qrels, meta
