from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Sequence

import numpy as np
from scipy.stats import spearmanr


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


def deterministic_topk(
    ids: Sequence[str], scores: Sequence[float], k: int
) -> list[str]:
    """Return score-descending top-k IDs with lexical identity tie-breaking."""
    ids_arr, values = _aligned(ids, scores)
    if not (1 <= int(k) <= len(values)):
        raise ValueError("k must be between 1 and the candidate count")
    order = np.lexsort((ids_arr.astype(str), -values))
    return [str(x) for x in ids_arr[order[: int(k)]]]


def ridi(a: Iterable[str], b: Iterable[str]) -> float:
    """Jaccard distance between two decision-identity sets."""
    left, right = set(map(str, a)), set(map(str, b))
    if not left and not right:
        return 0.0
    return float(1.0 - len(left & right) / len(left | right))


def changed_slots(a: Iterable[str], b: Iterable[str]) -> int:
    """Count identities present in the first equal-size set but not the second."""
    left, right = set(map(str, a)), set(map(str, b))
    if len(left) != len(right):
        raise ValueError("changed_slots assumes equal-size decision sets")
    return int(len(left - right))


def margin_certificate(
    scores_r0: Sequence[float],
    scores_r1: Sequence[float],
    ids: Sequence[str],
    k: int,
) -> dict:
    """Evaluate the sufficient zero-turnover certificate gamma_k > 2*epsilon."""
    ids_arr, baseline = _aligned(ids, scores_r0)
    ids_updated, updated = _aligned(ids, scores_r1)
    if not np.array_equal(ids_arr.astype(str), ids_updated.astype(str)):
        raise ValueError("both score vectors must use the same aligned identities")
    if not (1 <= int(k) < len(baseline)):
        raise ValueError("margin certificate requires 1 <= k < n")
    order = np.lexsort((ids_arr.astype(str), -baseline))
    gamma = float(baseline[order[int(k) - 1]] - baseline[order[int(k)]])
    epsilon = float(np.max(np.abs(updated - baseline)))
    return {
        "gamma_k": gamma,
        "epsilon": epsilon,
        "certified_stable": bool(gamma > 2.0 * epsilon),
    }


@dataclass(frozen=True)
class CutoffAudit:
    k: int
    ridi: float
    changed_slots: int
    overlap: int
    gamma_k: float | None
    epsilon: float | None
    margin_certified: bool | None


def audit_scores(
    ids: Sequence[str],
    scores_r0: Sequence[float],
    scores_r1: Sequence[float],
    ks: Sequence[int],
) -> dict:
    """Audit global agreement, top-k identity and score-margin stability."""
    ids_arr, baseline = _aligned(ids, scores_r0)
    ids_updated, updated = _aligned(ids, scores_r1)
    if not np.array_equal(ids_arr.astype(str), ids_updated.astype(str)):
        raise ValueError("both score vectors must use the same aligned identities")
    if not ks:
        raise ValueError("at least one cutoff is required")
    cutoffs = sorted(set(map(int, ks)))
    if cutoffs[0] < 1 or cutoffs[-1] > len(ids_arr):
        raise ValueError("all cutoffs must satisfy 1 <= k <= n")

    rho_result = spearmanr(baseline, updated)
    rho = float(rho_result.statistic)
    if not np.isfinite(rho):
        raise ValueError("global Spearman agreement is undefined for constant scores")

    rows: list[dict] = []
    for k in cutoffs:
        left = deterministic_topk(ids_arr, baseline, k)
        right = deterministic_topk(ids_arr, updated, k)
        certificate = (
            margin_certificate(baseline, updated, ids_arr, k)
            if k < len(ids_arr)
            else None
        )
        rows.append(
            asdict(
                CutoffAudit(
                    k=k,
                    ridi=ridi(left, right),
                    changed_slots=changed_slots(left, right),
                    overlap=len(set(left) & set(right)),
                    gamma_k=None if certificate is None else certificate["gamma_k"],
                    epsilon=None if certificate is None else certificate["epsilon"],
                    margin_certified=(
                        None
                        if certificate is None
                        else certificate["certified_stable"]
                    ),
                )
            )
        )
    return {
        "schema_version": "1.0",
        "n_candidates": int(len(ids_arr)),
        "global_spearman": rho,
        "cutoffs": rows,
    }

