"""Prospective v4 assembly: v3 plus immutable FEVER labelled-dev provenance.

No language-model calls. FEVER source is a pinned Hugging Face dataset snapshot of
FEVER v1.0 labelled_dev. Evidence-level duplicate rows are deterministically collapsed
by (id, normalized claim, label) before mapping BEIR queries. Any contradictory duplicate
or incomplete BEIR-query mapping is a hard failure.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import assemble_prereg_inputs as v2
import assemble_prereg_inputs_v3 as v3

FEVER_COMMIT = "55e20b98b435ba817a6c9b4e05871932bd164645"
FEVER_SHA256 = "1e9522968f5aec3702dc7c838c1a2297bb536ff96a36d3147b157838eb74ae33"
FEVER_URL = (
    "https://huggingface.co/datasets/fever/fever/resolve/"
    f"{FEVER_COMMIT}/v1.0/fever-labelled_dev.parquet?download=true"
)
_ORIGINAL_PREPARE_GOLD = v2.prepare_gold


def map_fever_parquet(source: Path, topics: dict[str, str]):
    import pyarrow.parquet as pq

    raw = pq.read_table(source, columns=["id", "claim", "label"]).to_pylist()
    # The parquet has one row per evidence annotation/evidence item. Collapse exact
    # duplicate claim-level gold, but reject contradictions rather than choosing one.
    by_id_candidates: dict[str, set[tuple[str, str]]] = {}
    for r in raw:
        qid = str(r["id"])
        claim = str(r["claim"])
        label = str(r["label"]).upper().strip().replace(" ", "_")
        if label == "NOTENOUGHINFO":
            label = "NOT_ENOUGH_INFO"
        if label not in {"SUPPORTS", "REFUTES", "NOT_ENOUGH_INFO"}:
            raise RuntimeError(f"FEVER unexpected label {label!r} id={qid}")
        by_id_candidates.setdefault(qid, set()).add((claim, label))

    contradictory_ids = sorted(qid for qid, vals in by_id_candidates.items() if len(vals) != 1)
    if contradictory_ids:
        raise RuntimeError(
            f"FEVER contradictory claim/label rows for {len(contradictory_ids)} ids; "
            f"first={contradictory_ids[:10]}"
        )

    canonical = {qid: next(iter(vals)) for qid, vals in by_id_candidates.items()}
    # Text index is used only as deterministic fallback when BEIR IDs differ. Repeated
    # normalized claims are deliberately non-matchable by text.
    text_to_ids: dict[str, list[str]] = {}
    for qid, (claim, _label) in canonical.items():
        text_to_ids.setdefault(v2.norm_text(claim), []).append(qid)

    out: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    id_text_mismatch: list[str] = []
    text_fallback_count = 0
    ambiguous_text_keys = sum(1 for ids in text_to_ids.values() if len(ids) != 1)

    for qid, query in topics.items():
        rec = canonical.get(str(qid))
        if rec is not None and v2.norm_text(rec[0]) != v2.norm_text(query):
            id_text_mismatch.append(str(qid))
            rec = None
        if rec is None:
            ids = text_to_ids.get(v2.norm_text(query), [])
            if len(ids) == 1:
                rec = canonical[ids[0]]
                text_fallback_count += 1
        if rec is None:
            missing.append(str(qid))
            continue
        claim, label = rec
        out[str(qid)] = {"_id": str(qid), "labels": [label]}

    return out, {
        "source_rows": len(raw),
        "unique_source_claim_ids": len(canonical),
        "ambiguous_text_keys": ambiguous_text_keys,
        "id_text_mismatch": id_text_mismatch,
        "text_fallback_count": text_fallback_count,
        "missing": missing,
        "mapping_rule": "exact id with normalized-claim verification, else unique exact normalized claim text; evidence rows collapsed only when claim and label agree",
    }


def prepare_gold_patched(dataset: str, root: Path, topics: dict[str, str]):
    if dataset != "fever":
        return _ORIGINAL_PREPARE_GOLD(dataset, root, topics)

    cache = root / ".source_cache"
    source = cache / "fever.parquet"
    if not source.exists():
        v2.download(FEVER_URL, source)
    actual_sha = v2.sha256_file(source)
    if actual_sha != FEVER_SHA256:
        raise RuntimeError(f"FEVER frozen parquet SHA-256 mismatch: {actual_sha} != {FEVER_SHA256}")

    out, rep = map_fever_parquet(source, topics)
    if rep["missing"]:
        raise RuntimeError(
            f"fever: pinned source gold failed to map {len(rep['missing'])}/{len(topics)} "
            f"original BEIR queries; first={rep['missing'][:10]}"
        )
    if len(out) != len(topics):
        raise RuntimeError(f"fever: mapped gold cardinality mismatch {len(out)} != {len(topics)}")

    gp = root / "data" / "gold" / "fever.jsonl"
    gp.parent.mkdir(parents=True, exist_ok=True)
    with gp.open("w", encoding="utf-8") as f:
        for qid in sorted(out):
            f.write(json.dumps(out[qid], ensure_ascii=False) + "\n")

    rep.update({
        "mapped": len(out),
        "source_url": FEVER_URL,
        "source_sha256": actual_sha,
        "source_expected_sha256": FEVER_SHA256,
        "source_revision": FEVER_COMMIT,
        "gold_sha256": v2.sha256_file(gp),
        "fuzzy_matching": False,
        "human_adjudication": False,
        "generated_gold": False,
    })
    return rep


# Patch the dependency used inside v3.main before dispatching its unchanged prospective logic.
v2.prepare_gold = prepare_gold_patched

if __name__ == "__main__":
    raise SystemExit(v3.main())
