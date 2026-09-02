"""Prospective v3 input assembly.

NQ is explicitly defined as the exact intersection of BEIR-NQ test queries and the
Google NQ-Open original-dev short-answer set. This is an eligibility definition, not a
post-outcome exclusion: it is applied before panel selection and before any LLM call.
No fuzzy matching, answer generation, or human adjudication is permitted.

Other datasets retain the v2 rule requiring complete source-gold coverage.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import assemble_prereg_inputs as v2
from beir_local_resources import load_topics_qrels


def prepare_nq_exact_subset(root: Path, topics: dict[str, str]):
    cache = root / ".source_cache"
    source = cache / f"nq{v2.SOURCE_EXT['nq']}"
    if not source.exists():
        v2.download(v2.SOURCE_URLS["nq"], source)
    mapped, rep = v2.map_nq(source, topics)
    if not mapped:
        raise RuntimeError("NQ exact-gold intersection is empty")
    gp = root / "data" / "gold" / "nq.jsonl"
    gp.parent.mkdir(parents=True, exist_ok=True)
    with gp.open("w", encoding="utf-8") as f:
        for qid in sorted(mapped):
            f.write(json.dumps(mapped[qid], ensure_ascii=False) + "\n")
    rep.update({
        "mapped": len(mapped),
        "source_url": v2.SOURCE_URLS["nq"],
        "source_sha256": v2.sha256_file(source),
        "source_revision": v2.NQ_COMMIT,
        "gold_sha256": v2.sha256_file(gp),
        "eligibility_definition": "BEIR-NQ test query must have a unique exact normalized-question match in Google NQ-Open original-dev with a nonempty official short-answer list",
        "subset_status": "PROSPECTIVELY_DEFINED_BEFORE_PANEL_SELECTION_AND_BEFORE_LLM_GENERATION",
        "excluded_for_no_exact_short_answer_gold": len(rep["missing"]),
        "fuzzy_matching": False,
        "human_adjudication": False,
        "generated_gold": False,
    })
    return mapped, rep


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(v2.DATASETS), required=True)
    ap.add_argument("--root", type=Path, required=True)
    args = ap.parse_args()
    dataset = args.dataset
    root = args.root.resolve(); root.mkdir(parents=True, exist_ok=True)

    all_topics, all_qrels, beir_meta = load_topics_qrels(dataset, root / ".beir_resources")
    runs = v2.find_runs(root, dataset)

    if dataset == "nq":
        mapped_gold, gold_report = prepare_nq_exact_subset(root, all_topics)
        eligible_ids = set(mapped_gold)
        topics = {q: all_topics[q] for q in all_topics if q in eligible_ids}
        qrels = {q: all_qrels.get(q, {}) for q in topics}
        if len(topics) < 250:
            raise RuntimeError(f"NQ exact-gold intersection too small for preregistered panel target: {len(topics)} < 250")
    else:
        gold_report = v2.prepare_gold(dataset, root, all_topics)
        topics, qrels = all_topics, all_qrels

    data_report = v2.materialize_compact(dataset, root, topics, qrels, runs)
    if dataset == "nq":
        data_report["beir_original_topic_count"] = len(all_topics)
        data_report["exact_short_answer_gold_eligible_before_technical_checks"] = len(topics)
        data_report["gold_ineligible_qids_count"] = len(all_topics) - len(topics)
        data_report["gold_ineligible_qids"] = sorted(set(all_topics) - set(topics))

    report = {
        "schema_version": "ridi-rag-prereg-input-provenance-v3",
        "dataset": dataset,
        "prospective_status": "NO_LLM_GENERATION_PERFORMED",
        "beir_benchmark_resources": {
            "topics_url": beir_meta["topics_url"], "topics_sha256": beir_meta["topics_sha256"],
            "qrels_url": beir_meta["qrels_url"], "qrels_sha256": beir_meta["qrels_sha256"],
            "topic_count": beir_meta["topic_count"], "qrel_query_count": beir_meta["qrel_query_count"],
            "qrel_pair_count": beir_meta["qrel_pair_count"],
        },
        "flat_index": v2.INDEX_FLAT[dataset],
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
        report["artifacts"][str(p.relative_to(root))] = {"sha256": v2.sha256_file(p), "bytes": p.stat().st_size}
    rp = root / "protocol" / "input_reports" / f"{dataset}.json"
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
