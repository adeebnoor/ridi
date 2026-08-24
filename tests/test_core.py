import numpy as np
import pytest

from ridi_audit import (
    audit_scores,
    changed_slots,
    deterministic_topk,
    margin_certificate,
    ridi,
)


def test_ridi_identity_and_disjoint():
    assert ridi(["a", "b"], ["a", "b"]) == 0
    assert ridi(["a", "b"], ["c", "d"]) == 1


def test_tie_break_is_identity_deterministic():
    assert deterministic_topk(["z", "a", "m"], [1, 1, 0], 2) == ["a", "z"]


def test_margin_certificate_is_sufficient_in_certified_case():
    ids = ["a", "b", "c", "d"]
    baseline = np.array([4.0, 3.0, 1.0, 0.0])
    updated = baseline + np.array([0.1, -0.1, 0.1, -0.1])
    certificate = margin_certificate(baseline, updated, ids, 2)
    assert certificate["certified_stable"]
    result = audit_scores(ids, baseline, updated, [1, 2])
    assert result["cutoffs"][1]["ridi"] == 0


def test_audit_rejects_duplicate_ids_and_bad_cutoffs():
    with pytest.raises(ValueError, match="unique"):
        audit_scores(["a", "a"], [2, 1], [2, 1], [1])
    with pytest.raises(ValueError, match="cutoffs"):
        audit_scores(["a", "b"], [2, 1], [1, 2], [3])


def test_changed_slots_requires_equal_decision_set_sizes():
    with pytest.raises(ValueError, match="equal-size"):
        changed_slots(["a"], ["a", "b"])

