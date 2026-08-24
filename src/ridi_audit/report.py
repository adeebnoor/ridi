from __future__ import annotations

from typing import Any, Mapping


def render_markdown_report(result: Mapping[str, Any]) -> str:
    """Render a compact, publication-friendly RIDI audit report."""
    lines = [
        "# RIDI decision-reproducibility audit",
        "",
        f"- Candidate universe: **{result['n_candidates']}**",
        f"- Global Spearman agreement: **{result['global_spearman']:.6f}**",
        "",
        "| k | RIDI | Changed slots | Overlap | Margin certificate | gamma_k | epsilon |",
        "|---:|---:|---:|---:|:---:|---:|---:|",
    ]
    for row in result["cutoffs"]:
        certificate = row["margin_certified"]
        certificate_text = (
            "n/a" if certificate is None else ("PASS" if certificate else "not certified")
        )
        gamma = "n/a" if row["gamma_k"] is None else f"{row['gamma_k']:.6g}"
        epsilon = "n/a" if row["epsilon"] is None else f"{row['epsilon']:.6g}"
        lines.append(
            f"| {row['k']} | {row['ridi']:.6f} | {row['changed_slots']} | "
            f"{row['overlap']} | {certificate_text} | {gamma} | {epsilon} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "RIDI measures identity turnover in the selected decision set; it does not "
            "replace task-performance metrics. A high global rank correlation does not "
            "certify top-k identity. A PASS is a sufficient zero-turnover guarantee for "
            "the supplied paired score vectors. Learned systems should additionally be "
            "calibrated against same-representation retraining variability.",
            "",
        ]
    )
    return "\n".join(lines)

