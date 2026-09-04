import pandas as pd

from ridi_audit import AuditReport, audit


def _frames():
    before = pd.DataFrame(
        {
            "id": ["a", "b", "c", "d", "e", "f"],
            "score": [0.99, 0.90, 0.80, 0.70, 0.60, 0.50],
        }
    )
    after = pd.DataFrame(
        {
            "id": ["f", "e", "d", "c", "b", "a"],
            "score": [0.95, 0.58, 0.69, 0.81, 0.89, 0.98],
        }
    )
    return before, after


def test_audit_aligns_rows_and_returns_report():
    before, after = _frames()
    report = audit(before, after, k=[3, 5])
    assert isinstance(report, AuditReport)
    assert report.n_candidates == 6
    assert [row["k"] for row in report.cutoffs] == [3, 5]
    assert "RIDI Allocation Audit" in str(report)
    assert "# RIDI decision-reproducibility audit" in report.to_markdown()


def test_audit_control_reuses_aligned_inputs():
    before, after = _frames()
    report = audit(before, after, k=3)
    controlled = report.control(k=3, eta=0.5)
    assert controlled["eta"] == 0.5
    assert len(controlled["selected_ids"]) == 3
    assert "selected_indices" not in controlled


def test_audit_rejects_mismatched_candidate_universe():
    before, after = _frames()
    after = after.iloc[:-1].copy()
    try:
        audit(before, after, k=3)
    except ValueError as exc:
        assert "same candidate identities" in str(exc)
    else:
        raise AssertionError("mismatched candidate universe should fail")
