"""Assembly entry point that removes JVM topic/qrel downloads from the prereg pipeline.

It monkey-patches only the BEIR topic/qrel loader in the already-audited assembly logic.
Retrieval runs and language-model generation are untouched. After assembly it records the
canonical Anserini topic/qrel URLs and SHA-256 hashes in the per-dataset provenance report.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import prepare_inputs_pyserini as base
from beir_local_resources import load_topics_qrels

_RESOURCE_META: dict[str, dict] = {}


def _root_from_argv() -> Path:
    try:
        i = sys.argv.index("--root")
        return Path(sys.argv[i + 1]).resolve()
    except Exception as e:
        raise RuntimeError("--root is required before local BEIR resource loading") from e


def local_topics_qrels(dataset: str):
    root = _root_from_argv()
    topics, qrels, meta = load_topics_qrels(dataset, root / ".beir_resources")
    _RESOURCE_META[dataset] = meta
    return topics, qrels


def _dataset_from_argv() -> str:
    try:
        i = sys.argv.index("--dataset")
        return sys.argv[i + 1]
    except Exception as e:
        raise RuntimeError("--dataset is required") from e


def main() -> int:
    base.pyserini_topics_qrels = local_topics_qrels
    rc = base.main()
    if rc:
        return rc
    root = _root_from_argv()
    dataset = _dataset_from_argv()
    rp = root / "protocol" / "input_reports" / f"{dataset}.json"
    report = json.loads(rp.read_text(encoding="utf-8"))
    meta = _RESOURCE_META[dataset]
    report["beir_benchmark_resources"] = {
        "topics_url": meta["topics_url"],
        "topics_sha256": meta["topics_sha256"],
        "qrels_url": meta["qrels_url"],
        "qrels_sha256": meta["qrels_sha256"],
        "topic_count": meta["topic_count"],
        "qrel_query_count": meta["qrel_query_count"],
        "qrel_pair_count": meta["qrel_pair_count"],
    }
    rp.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PROVENANCE-HARDENED REPORT")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
