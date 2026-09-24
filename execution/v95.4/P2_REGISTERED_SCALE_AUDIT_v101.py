#!/usr/bin/env python3
"""Reconstruct the preregistered equal-dataset P2 decision from persisted marginals.

The remote P2 job persisted dataset-specific main/floor event counts but not the
fixed-batch query-level generation file. For binary paired events, the unknown
within-dataset overlap is bounded by the two marginals. This script enumerates
all 48 admissible overlap structures and applies the frozen excess-bootstrap
algorithm's group order, resample count and seed to every structure.

This is not a substitute for the lost raw pairing; it proves whether the H-P2
support decision can vary across any pairing consistent with the persisted data.
"""
import itertools, json
from pathlib import Path
import numpy as np

N_BOOT = 20_000
SEED = 20260923
DATA = [
    ("scifact", 150, 39, 3),
    ("fever", 150, 19, 2),
    ("hotpotqa", 250, 27, 1),
    ("nq", 250, 49, 1),
]

def interval(overlaps):
    rng = np.random.default_rng(SEED)
    boots = np.zeros(N_BOOT)
    for (_, n, a, b), c in zip(DATA, overlaps):
        d = np.array([1] * (a - c) + [-1] * (b - c) + [0] * (n - a - b + 2 * c), dtype=float)
        assert len(d) == n and d.sum() == a - b
        idx = rng.integers(0, n, size=(N_BOOT, n))
        boots += d[idx].mean(axis=1)
    boots /= len(DATA)
    return float(np.quantile(boots, .025)), float(np.quantile(boots, .975))

ranges = [range(max(0, a + b - n), min(a, b) + 1) for _, n, a, b in DATA]
rows = []
for overlaps in itertools.product(*ranges):
    lo, hi = interval(overlaps)
    rows.append({
        "overlap": {d[0]: int(c) for d, c in zip(DATA, overlaps)},
        "macro_excess": 0.16233333333333333,
        "ci95": [lo, hi],
        "h_p2_supported": bool(0.16233333333333333 >= .05 and lo > 0),
    })

out = {
    "method": "exhaustive enumeration of all within-dataset overlaps consistent with persisted P2 main/floor marginals",
    "bootstrap": {"n": N_BOOT, "seed": SEED, "group_order": [x[0] for x in DATA]},
    "n_admissible_pairings": len(rows),
    "macro_main": (39/150 + 19/150 + 27/250 + 49/250) / 4,
    "macro_floor": (3/150 + 2/150 + 1/250 + 1/250) / 4,
    "macro_excess": 0.16233333333333333,
    "minimum_lower95": min(x["ci95"][0] for x in rows),
    "maximum_lower95": max(x["ci95"][0] for x in rows),
    "minimum_upper95": min(x["ci95"][1] for x in rows),
    "maximum_upper95": max(x["ci95"][1] for x in rows),
    "all_pairings_support_h_p2": all(x["h_p2_supported"] for x in rows),
    "rows": rows,
}
Path("P2_REGISTERED_SCALE_AUDIT_v101.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=2))
