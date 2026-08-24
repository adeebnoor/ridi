from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


def _aligned(
    ids: Sequence[str], scores: Sequence[float]
) -> tuple[np.ndarray, np.ndarray]:
    ids_arr = np.asarray(ids, dtype=object)
    values = np.asarray(scores, dtype=float)
    if ids_arr.ndim != 1 or values.ndim != 1 or len(ids_arr) != len(values):
        raise ValueError("ids and scores must be aligned one-dimensional arrays")
    if len(ids_arr) == 0:
        raise ValueError("candidate universe must not be empty")
    if len(set(map(str, ids_arr))) != len(ids_arr):
        raise ValueError("candidate ids must be unique")
    if not np.isfinite(values).all():
        raise ValueError("scores must be finite")
    return ids_arr, values


def stable_order(scores: Sequence[float], ids: Sequence[str]) -> np.ndarray:
    ids_arr, values = _aligned(ids, scores)
    return np.lexsort((ids_arr.astype(str), -values))


def deterministic_percentiles(
    scores: Sequence[float], ids: Sequence[str]
) -> np.ndarray:
    """Return deterministic rank utility in [0, 1], with 1 at rank one."""
    ids_arr, values = _aligned(ids, scores)
    n = len(values)
    order = stable_order(values, ids_arr)
    output = np.empty(n, dtype=float)
    if n == 1:
        output[order] = 1.0
    else:
        output[order] = 1.0 - np.arange(n, dtype=float) / float(n - 1)
    return output


def ridi_from_changed_slots(k: int, changed: int) -> float:
    if not (0 <= int(changed) <= int(k)):
        raise ValueError("changed must be between zero and k")
    return float(2.0 * changed / (k + changed))


@dataclass(frozen=True)
class Frontier:
    """Exact identity–utility frontier indexed by allowed changed slots j."""

    k: int
    delta_unconstrained: int
    utility_star: float
    j: np.ndarray
    utility: np.ndarray
    regret: np.ndarray
    baseline_order: np.ndarray
    outsider_order: np.ndarray


def identity_utility_frontier(
    ids: Sequence[str],
    scores_r0: Sequence[float],
    scores_r1: Sequence[float],
    k: int,
) -> Frontier:
    """Compute the exact frontier between retained identity and updated utility.

    For each feasible number j of entrants from outside the baseline set, the
    optimal set contains the k-j highest-updated-utility baseline candidates and
    the j highest-updated-utility outsiders. Sorting dominates: O(n log n).
    """
    ids_arr, baseline_scores = _aligned(ids, scores_r0)
    updated_ids, updated_scores = _aligned(ids, scores_r1)
    if not np.array_equal(ids_arr.astype(str), updated_ids.astype(str)):
        raise ValueError("both score vectors must use the same aligned identities")
    n = len(ids_arr)
    if not (1 <= int(k) <= n):
        raise ValueError("identity-control frontier requires 1 <= k <= n")

    utility0 = deterministic_percentiles(baseline_scores, ids_arr)
    utility1 = deterministic_percentiles(updated_scores, ids_arr)
    baseline_order = stable_order(utility0, ids_arr)
    updated_order = stable_order(utility1, ids_arr)
    baseline = baseline_order[: int(k)]
    updated = updated_order[: int(k)]

    baseline_mask = np.zeros(n, dtype=bool)
    baseline_mask[baseline] = True
    delta = int(np.count_nonzero(~baseline_mask[updated]))

    inside = baseline[stable_order(utility1[baseline], ids_arr[baseline])]
    outside_idx = np.flatnonzero(~baseline_mask)
    outside = (
        outside_idx[stable_order(utility1[outside_idx], ids_arr[outside_idx])]
        if len(outside_idx)
        else np.empty(0, dtype=int)
    )

    inside_prefix = np.concatenate(([0.0], np.cumsum(utility1[inside], dtype=float)))
    outside_prefix = np.concatenate(([0.0], np.cumsum(utility1[outside], dtype=float)))
    max_j = min(int(k), len(outside))
    js = np.arange(max_j + 1, dtype=int)
    utilities = np.asarray(
        [inside_prefix[int(k) - int(j)] + outside_prefix[int(j)] for j in js],
        dtype=float,
    )
    utility_star = float(np.max(utilities))
    if utility_star <= 0:
        raise RuntimeError("updated percentile utility must be positive")
    regret = np.maximum(0.0, (utility_star - utilities) / utility_star)
    return Frontier(
        k=int(k),
        delta_unconstrained=delta,
        utility_star=utility_star,
        j=js,
        utility=utilities,
        regret=regret,
        baseline_order=inside,
        outsider_order=outside,
    )


def select_identity_control(frontier: Frontier, eta: float) -> dict:
    """Return the minimum-turnover frontier point satisfying regret <= eta."""
    if float(eta) < 0:
        raise ValueError("eta must be non-negative")
    eligible = np.flatnonzero(frontier.regret <= float(eta) + 1e-15)
    if not len(eligible):
        raise RuntimeError("no feasible frontier point meets eta")
    position = int(eligible[0])
    changed = int(frontier.j[position])
    selected = np.concatenate(
        (
            frontier.baseline_order[: frontier.k - changed],
            frontier.outsider_order[:changed],
        )
    )
    delta = frontier.delta_unconstrained
    return {
        "eta": float(eta),
        "j_eta": changed,
        "delta_unconstrained": delta,
        "avoidable_turnover_fraction": (
            None if delta == 0 else float(1.0 - changed / delta)
        ),
        "utility": float(frontier.utility[position]),
        "utility_star": float(frontier.utility_star),
        "utility_regret": float(frontier.regret[position]),
        "ridi_unconstrained": ridi_from_changed_slots(frontier.k, delta),
        "ridi_controlled": ridi_from_changed_slots(frontier.k, changed),
        "selected_indices": selected,
    }

