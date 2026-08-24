from ridi_audit import audit_scores
from ridi_audit.report import render_markdown_report


def test_markdown_report_contains_core_fields():
    result = audit_scores(
        ["a", "b", "c", "d"],
        [4.0, 3.0, 2.0, 1.0],
        [4.0, 2.0, 3.0, 1.0],
        [1, 2],
    )
    text = render_markdown_report(result)
    assert "Global Spearman agreement" in text
    assert "Changed slots" in text
    assert "Margin certificate" in text
    assert "| 2 |" in text

