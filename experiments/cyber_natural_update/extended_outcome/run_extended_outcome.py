#!/usr/bin/env python3
"""Post hoc EPSS delayed-outcome sensitivity using the locked v2->v3 universe.

The registered/locked 365-day analysis remains primary. This script extends only the
CISA KEV follow-up horizon to calendar-year anniversaries ending 2025-03-07 and
2026-03-07 while preserving the original candidate universe, prior-KEV exclusion,
score snapshots, deterministic score/CVE tie-breaking, and selection capacities.
"""

from __future__ import annotations

import argparse
import csv
from datetime import date
import gzip
import hashlib
import json
from pathlib import Path

DATES = ["2023_03_05", "2023_03_06", "2023_03_07", "2023_03_08"]
KS = [100, 500, 1000, 5000]
PRIMARY_K = 1000
START = date(2023, 3, 8)
WINDOWS = {
    "1y_primary": date(2024, 3, 7),
    "2y_sensitivity": date(2025, 3, 7),
    "3y_sensitivity": date(2026, 3, 7),
}
EXPECTED_PRIMARY = {"n_candidates": 195886, "n_positive": 58, "v2_hits_k1000": 8, "v3_hits_k1000": 12}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_epss(path: Path) -> dict[str, float]:
    scores: dict[str, float] = {}
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        rows = (line for line in handle if not line.startswith("#"))
        for row in csv.DictReader(rows):
            scores[row["cve"].strip()] = float(row["epss"])
    return scores


def load_kev(path: Path) -> dict[str, date]:
    out: dict[str, date] = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            out[row["cveID"].strip()] = date.fromisoformat(row["dateAdded"].strip())
    return out


def deterministic_topk(score_map: dict[str, float], ids: set[str], k: int) -> list[str]:
    return [cve for cve in sorted(ids, key=lambda cve: (-score_map[cve], cve))[:k]]


def metrics(selected: set[str], positives: set[str], n_positive: int) -> dict:
    hits = len(selected & positives)
    return {
        "hits": hits,
        "precision": hits / len(selected),
        "recall": None if n_positive == 0 else hits / n_positive,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--inputs", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    score_maps = {stamp: load_epss(args.inputs / f"epss_{stamp}.csv.gz") for stamp in DATES}
    kev_path = args.inputs / "known_exploited_vulnerabilities.csv"
    kev = load_kev(kev_path)

    common = set.intersection(*(set(m) for m in score_maps.values()))
    prior_kev = {cve for cve, added in kev.items() if added <= date(2023, 3, 6)}
    universe = common - prior_kev
    if len(universe) != EXPECTED_PRIMARY["n_candidates"]:
        raise RuntimeError(f"Locked universe mismatch: {len(universe)} != {EXPECTED_PRIMARY['n_candidates']}")
    if max(kev.values()) < WINDOWS["3y_sensitivity"]:
        raise RuntimeError("Pinned KEV snapshot does not cover the complete 3-year window")

    v2_map, v3_map = score_maps["2023_03_06"], score_maps["2023_03_07"]
    top_sets = {
        str(k): {
            "v2": set(deterministic_topk(v2_map, universe, k)),
            "v3": set(deterministic_topk(v3_map, universe, k)),
        }
        for k in KS
    }

    result = {
        "analysis_id": "RIDI-EPSS-EXTENDED-OUTCOME-v1",
        "status": "post_hoc_sensitivity; original 365-day window remains primary",
        "locked_parent_protocol": "RIDI-CYBER-NATURAL-UPDATE-v1",
        "outcome_source": "CISA KEV dateAdded from the same source-pinned snapshot used by the locked runner",
        "window_start": START.isoformat(),
        "n_candidates": len(universe),
        "pinned_kev_max_date": max(kev.values()).isoformat(),
        "input_sha256": {
            path.name: sha256(path)
            for path in sorted(args.inputs.iterdir())
            if path.is_file()
        },
        "windows": {},
    }

    for label, end in WINDOWS.items():
        positives = {cve for cve, added in kev.items() if START <= added <= end} & universe
        row = {"window_end": end.isoformat(), "n_positive_in_locked_universe": len(positives), "cutoffs": {}}
        for k in KS:
            a = top_sets[str(k)]["v2"]
            b = top_sets[str(k)]["v3"]
            row["cutoffs"][str(k)] = {
                "v2": metrics(a, positives, len(positives)),
                "v3": metrics(b, positives, len(positives)),
                "difference_v3_minus_v2_hits": len(b & positives) - len(a & positives),
                "entrants_future_kev": len((b - a) & positives),
                "leavers_future_kev": len((a - b) & positives),
                "retained_future_kev": len((a & b) & positives),
            }
        result["windows"][label] = row

    primary = result["windows"]["1y_primary"]
    check = {
        "n_positive": primary["n_positive_in_locked_universe"],
        "v2_hits_k1000": primary["cutoffs"][str(PRIMARY_K)]["v2"]["hits"],
        "v3_hits_k1000": primary["cutoffs"][str(PRIMARY_K)]["v3"]["hits"],
    }
    expected = {k: EXPECTED_PRIMARY[k] for k in check}
    result["primary_reproduction_check"] = {"observed": check, "expected": expected, "pass": check == expected}
    if check != expected:
        raise RuntimeError(f"365-day reproduction failed: observed={check}, expected={expected}")

    out = args.out / "EPSS_extended_outcomes_v1.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "primary_reproduction": result["primary_reproduction_check"],
        "k1000": {
            label: {
                "n_positive": row["n_positive_in_locked_universe"],
                "v2_hits": row["cutoffs"]["1000"]["v2"]["hits"],
                "v3_hits": row["cutoffs"]["1000"]["v3"]["hits"],
                "difference": row["cutoffs"]["1000"]["difference_v3_minus_v2_hits"],
            }
            for label, row in result["windows"].items()
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
