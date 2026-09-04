from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

from .core import audit_scores
from .report import render_markdown_report
from .selector import identity_utility_frontier, select_identity_control


def _cutoffs(k: int | Sequence[int]) -> list[int]:
    if isinstance(k, (int, np.integer)):
        return [int(k)]
    values = [int(value) for value in k]
    if not values:
        raise ValueError("k must contain at least one cutoff")
    return values


def _aligned_frames(
    before: pd.DataFrame,
    after: pd.DataFrame,
    id_col: str,
    score_col: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if not isinstance(before, pd.DataFrame) or not isinstance(after, pd.DataFrame):
        raise TypeError("before and after must be pandas DataFrames")
    for label, frame in (("before", before), ("after", after)):
        missing = [name for name in (id_col, score_col) if name not in frame.columns]
        if missing:
            raise ValueError(f"{label} is missing required column(s): {', '.join(missing)}")
        if frame[id_col].duplicated().any():
            raise ValueError(f"{label} contains duplicate candidate identities")

    left = before[[id_col, score_col]].rename(columns={score_col: "score_r0"})
    right = after[[id_col, score_col]].rename(columns={score_col: "score_r1"})
    merged = left.merge(
        right,
        on=id_col,
        how="outer",
        validate="one_to_one",
        indicator=True,
    )
    if not (merged["_merge"] == "both").all():
        raise ValueError("before and after must contain exactly the same candidate identities")
    merged = merged.drop(columns="_merge").sort_values(id_col, kind="mergesort")
    ids = merged[id_col].astype(str).to_numpy()
    scores_r0 = merged["score_r0"].to_numpy(dtype=float)
    scores_r1 = merged["score_r1"].to_numpy(dtype=float)
    return ids, scores_r0, scores_r1


@dataclass
class AuditReport:
    """Researcher-facing result returned by :func:`audit`.

    The object keeps the aligned score vectors privately so the same audit can
    immediately compute an identity-control solution without asking the user to
    rebuild inputs.
    """

    result: dict
    _ids: np.ndarray = field(repr=False)
    _scores_r0: np.ndarray = field(repr=False)
    _scores_r1: np.ndarray = field(repr=False)

    @property
    def n_candidates(self) -> int:
        return int(self.result["n_candidates"])

    @property
    def global_spearman(self) -> float:
        return float(self.result["global_spearman"])

    @property
    def cutoffs(self) -> list[dict]:
        return list(self.result["cutoffs"])

    def to_dict(self) -> dict:
        return {
            "schema_version": self.result["schema_version"],
            "n_candidates": self.n_candidates,
            "global_spearman": self.global_spearman,
            "cutoffs": [dict(row) for row in self.result["cutoffs"]],
        }

    def to_markdown(self) -> str:
        return render_markdown_report(self.result)

    def control(self, *, k: int, eta: float) -> dict:
        """Return the minimum-turnover set within an updated-utility regret budget."""
        frontier = identity_utility_frontier(
            self._ids, self._scores_r0, self._scores_r1, int(k)
        )
        selected = select_identity_control(frontier, float(eta))
        selected["selected_ids"] = [
            str(self._ids[int(index)]) for index in selected.pop("selected_indices")
        ]
        return selected

    def __str__(self) -> str:
        lines = [
            "RIDI Allocation Audit",
            "---------------------",
            f"Candidates:       {self.n_candidates}",
            f"Global Spearman:  {self.global_spearman:.6f}",
        ]
        for row in self.result["cutoffs"]:
            certificate = row["margin_certified"]
            if certificate is None:
                certificate_text = "n/a"
            else:
                certificate_text = "yes" if certificate else "no"
            lines.extend(
                [
                    "",
                    f"k={row['k']}",
                    f"  Changed slots: {row['changed_slots']}",
                    f"  Overlap:       {row['overlap']}",
                    f"  RIDI:          {row['ridi']:.6f}",
                    f"  Stable cert.:  {certificate_text}",
                ]
            )
        return "\n".join(lines)


def audit(
    before: pd.DataFrame,
    after: pd.DataFrame,
    *,
    k: int | Sequence[int],
    id_col: str = "id",
    score_col: str = "score",
) -> AuditReport:
    """Audit allocation identity before and after a score change.

    Parameters
    ----------
    before, after:
        DataFrames containing the same candidate identities and one score column.
        Row order may differ; identities are aligned deterministically.
    k:
        One cutoff or a sequence of cutoffs.
    id_col, score_col:
        Column names. Defaults are ``id`` and ``score``.

    Returns
    -------
    AuditReport
        A compact result with ``to_dict()``, ``to_markdown()`` and
        ``control(k=..., eta=...)`` helpers.
    """
    ids, scores_r0, scores_r1 = _aligned_frames(before, after, id_col, score_col)
    result = audit_scores(ids, scores_r0, scores_r1, _cutoffs(k))
    return AuditReport(result, ids, scores_r0, scores_r1)
