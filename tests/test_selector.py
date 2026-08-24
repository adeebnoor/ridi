import itertools

import numpy as np

from ridi_audit import (
    deterministic_percentiles,
    identity_utility_frontier,
    select_identity_control,
)


def _brute_force_max(ids, scores_r0, scores_r1, k, j):
    utility0 = deterministic_percentiles(scores_r0, ids)
    utility1 = deterministic_percentiles(scores_r1, ids)
    baseline = set(np.lexsort((np.asarray(ids), -utility0))[:k])
    best = -1.0
    for combination in itertools.combinations(range(len(ids)), k):
        chosen = set(combination)
        if len(chosen - baseline) == j:
            best = max(best, float(utility1[list(combination)].sum()))
    return best


def test_frontier_matches_brute_force():
    rng = np.random.default_rng(20260823)
    for n in range(4, 9):
        ids = np.asarray([f"c{i}" for i in range(n)])
        for k in range(1, min(3, n) + 1):
            for _ in range(8):
                scores_r0 = rng.normal(size=n)
                scores_r1 = rng.normal(size=n)
                frontier = identity_utility_frontier(ids, scores_r0, scores_r1, k)
                for position, j in enumerate(frontier.j):
                    brute = _brute_force_max(ids, scores_r0, scores_r1, k, int(j))
                    assert abs(float(frontier.utility[position]) - brute) < 1e-12


def test_selector_returns_minimum_feasible_turnover():
    ids = ["a", "b", "c", "d", "e", "f"]
    baseline = [6, 5, 4, 3, 2, 1]
    updated = [5.9, 5.1, 3.9, 6.1, 2, 1]
    frontier = identity_utility_frontier(ids, baseline, updated, 3)
    output = select_identity_control(frontier, eta=0.1)
    assert output["utility_regret"] <= 0.1 + 1e-12
    eligible = np.flatnonzero(frontier.regret <= 0.1 + 1e-15)
    assert output["j_eta"] == int(frontier.j[eligible[0]])


def test_invariant_representation_has_no_turnover():
    ids = [f"z{i}" for i in range(20)]
    scores = np.random.default_rng(3).normal(size=20)
    frontier = identity_utility_frontier(ids, scores, scores.copy(), 5)
    output = select_identity_control(frontier, eta=0.001)
    assert frontier.delta_unconstrained == 0
    assert output["j_eta"] == 0
    assert output["avoidable_turnover_fraction"] is None

