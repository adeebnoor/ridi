#!/usr/bin/env python3
"""Execute the locked RIDI cybersecurity natural-update analysis."""

from __future__ import annotations

import argparse
import csv
from datetime import date, timedelta
import gzip
import json
from pathlib import Path
import sys

import numpy as np
from scipy.stats import rankdata, spearmanr

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ridi_audit import (  # noqa: E402
    changed_slots,
    deterministic_topk,
    identity_utility_frontier,
    ridi,
    select_identity_control,
)


DATES = ["2023_03_05", "2023_03_06", "2023_03_07", "2023_03_08"]
KS = [100, 500, 1000, 5000]
PRIMARY_K = 1000
UPDATE_DATE = date(2023, 3, 7)
PRIMARY_END = date(2024, 3, 7)
ETA_LADDER = [0.0, 0.0001, 0.001, 0.005, 0.01]


def load_epss(path: Path) -> dict[str, float]:
    scores: dict[str, float] = {}
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        rows = (line for line in handle if not line.startswith("#"))
        for row in csv.DictReader(rows):
            scores[row["cve"].strip()] = float(row["epss"])
    return scores


def load_kev(path: Path) -> dict[str, date]:
    output: dict[str, date] = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            output[row["cveID"].strip()] = date.fromisoformat(row["dateAdded"].strip())
    return output


def topk(ids: np.ndarray, scores: np.ndarray, k: int) -> list[str]:
    return deterministic_topk(ids, scores, k)


def audit_pair(ids: np.ndarray, left: np.ndarray, right: np.ndarray) -> dict:
    rho = float(spearmanr(left, right).statistic)
    result = {"global_spearman": rho, "cutoffs": {}}
    for k in KS:
        a, b = topk(ids, left, k), topk(ids, right, k)
        result["cutoffs"][str(k)] = {
            "ridi": ridi(a, b),
            "changed_slots": changed_slots(a, b),
            "overlap": len(set(a) & set(b)),
        }
    return result


def auc(labels: np.ndarray, scores: np.ndarray) -> float | None:
    positives = int(labels.sum())
    negatives = int(len(labels) - positives)
    if not positives or not negatives:
        return None
    ranks = rankdata(scores, method="average")
    return float((ranks[labels].sum() - positives * (positives + 1) / 2) / (positives * negatives))


def average_precision(labels: np.ndarray, scores: np.ndarray, ids: np.ndarray) -> float | None:
    positives = int(labels.sum())
    if not positives:
        return None
    order = np.lexsort((ids.astype(str), -scores))
    ordered = labels[order].astype(int)
    precision = np.cumsum(ordered) / np.arange(1, len(ordered) + 1)
    return float(precision[ordered == 1].sum() / positives)


def captures(decision: set[str], positives: set[str]) -> int:
    return len(decision & positives)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, default=Path("inputs"))
    parser.add_argument("--out", type=Path, default=Path("results"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    score_maps = {
        stamp: load_epss(args.inputs / f"epss_{stamp}.csv.gz") for stamp in DATES
    }
    kev = load_kev(args.inputs / "known_exploited_vulnerabilities.csv")
    common = set.intersection(*(set(values) for values in score_maps.values()))
    prior_kev = {cve for cve, added in kev.items() if added <= date(2023, 3, 6)}
    ids = np.asarray(sorted(common - prior_kev), dtype=object)
    scores = {
        stamp: np.asarray([score_maps[stamp][str(cve)] for cve in ids], dtype=float)
        for stamp in DATES
    }

    future_primary = {
        cve for cve, added in kev.items() if date(2023, 3, 8) <= added <= PRIMARY_END
    } & set(map(str, ids))
    labels = np.asarray([str(cve) in future_primary for cve in ids], dtype=bool)

    result: dict = {
        "protocol_id": "RIDI-CYBER-NATURAL-UPDATE-v1",
        "n_candidates": int(len(ids)),
        "n_prior_kev_excluded": int(len(common & prior_kev)),
        "n_future_kev_primary": int(len(future_primary)),
        "treatment": audit_pair(ids, scores["2023_03_06"], scores["2023_03_07"]),
        "pre_update_control": audit_pair(ids, scores["2023_03_05"], scores["2023_03_06"]),
        "post_update_control": audit_pair(ids, scores["2023_03_07"], scores["2023_03_08"]),
        "external_outcome": {"primary_window_end": PRIMARY_END.isoformat(), "cutoffs": {}},
    }

    v2, v3 = scores["2023_03_06"], scores["2023_03_07"]
    result["external_outcome"]["full_universe"] = {
        "v2_auroc": auc(labels, v2),
        "v3_auroc": auc(labels, v3),
        "v2_average_precision": average_precision(labels, v2, ids),
        "v3_average_precision": average_precision(labels, v3, ids),
    }
    for k in KS:
        a, b = set(topk(ids, v2, k)), set(topk(ids, v3, k))
        v2_hits, v3_hits = captures(a, future_primary), captures(b, future_primary)
        result["external_outcome"]["cutoffs"][str(k)] = {
            "v2_future_kev": v2_hits,
            "v3_future_kev": v3_hits,
            "difference_v3_minus_v2": v3_hits - v2_hits,
            "entrants_future_kev": captures(b - a, future_primary),
            "leavers_future_kev": captures(a - b, future_primary),
            "retained_future_kev": captures(a & b, future_primary),
            "classification": "beneficial" if v3_hits > v2_hits else ("adverse" if v3_hits < v2_hits else "neutral"),
        }

    result["external_outcome"]["sensitivity"] = {}
    for days in [30, 90, 180]:
        end = UPDATE_DATE + timedelta(days=days)
        positives = {
            cve for cve, added in kev.items() if date(2023, 3, 8) <= added <= end
        } & set(map(str, ids))
        a, b = set(topk(ids, v2, PRIMARY_K)), set(topk(ids, v3, PRIMARY_K))
        result["external_outcome"]["sensitivity"][str(days)] = {
            "window_end": end.isoformat(),
            "n_positive": len(positives),
            "v2_future_kev": captures(a, positives),
            "v3_future_kev": captures(b, positives),
        }

    frontier = identity_utility_frontier(ids, v2, v3, PRIMARY_K)
    control_rows = []
    v3_set = set(topk(ids, v3, PRIMARY_K))
    v3_hits = captures(v3_set, future_primary)
    for eta in ETA_LADDER:
        selected = select_identity_control(frontier, eta)
        selected_set = set(map(str, ids[selected.pop("selected_indices")]))
        hits = captures(selected_set, future_primary)
        selected["future_kev"] = hits
        selected["external_retention"] = None if v3_hits == 0 else hits / v3_hits
        selected["passes_95pct_external_retention"] = bool(
            selected["j_eta"] < selected["delta_unconstrained"]
            and (v3_hits == 0 or hits / v3_hits >= 0.95)
        )
        control_rows.append(selected)
    result["identity_control"] = control_rows

    primary = result["treatment"]["cutoffs"][str(PRIMARY_K)]
    pre = result["pre_update_control"]["cutoffs"][str(PRIMARY_K)]
    post = result["post_update_control"]["cutoffs"][str(PRIMARY_K)]
    result["gates"] = {
        "update_exceeds_both_temporal_controls": bool(
            primary["changed_slots"] > pre["changed_slots"]
            and primary["changed_slots"] > post["changed_slots"]
        ),
        "primary_outcome_classification": result["external_outcome"]["cutoffs"][str(PRIMARY_K)]["classification"],
    }

    (args.out / "locked_results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result["gates"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
