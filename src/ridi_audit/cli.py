from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .core import audit_scores
from .report import render_markdown_report
from .selector import identity_utility_frontier, select_identity_control


def _read(path: str, id_col: str, score_col: str) -> pd.DataFrame:
    frame = pd.read_csv(path)
    if id_col not in frame or score_col not in frame:
        raise SystemExit(f"Missing required columns in {path}: {id_col}, {score_col}")
    return frame[[id_col, score_col]].copy()


def _align(
    r0: str, r1: str, id_col: str, score_col: str
) -> pd.DataFrame:
    baseline = _read(r0, id_col, score_col).rename(columns={score_col: "score_r0"})
    updated = _read(r1, id_col, score_col).rename(columns={score_col: "score_r1"})
    merged = baseline.merge(
        updated,
        on=id_col,
        how="outer",
        validate="one_to_one",
        indicator=True,
    )
    if not (merged["_merge"] == "both").all():
        raise SystemExit("R0 and R1 must contain the same candidate identities")
    return merged.drop(columns="_merge").sort_values(id_col, kind="mergesort")


def _write_json(payload: dict, output: str) -> None:
    serializable = dict(payload)
    if "selected_indices" in serializable:
        serializable["selected_indices"] = [
            int(value) for value in serializable["selected_indices"]
        ]
    text = json.dumps(serializable, indent=2, sort_keys=True)
    if output == "-":
        print(text)
    else:
        Path(output).write_text(text + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ridi-audit",
        description="Audit and control allocation identity in capacity-limited score-to-action systems",
    )
    parser.add_argument("--version", action="version", version="ridi-audit 1.1.0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    compare = subparsers.add_parser(
        "compare", help="Audit allocation identity between two candidate-score tables"
    )
    compare.add_argument("--r0", required=True, help="Baseline CSV")
    compare.add_argument("--r1", required=True, help="Updated CSV")
    compare.add_argument("--id-col", default="id")
    compare.add_argument("--score-col", default="score")
    compare.add_argument("--k", nargs="+", type=int, required=True)
    compare.add_argument("--out", default="-", help="JSON path, or - for stdout")
    compare.add_argument("--report", default=None, help="Optional Markdown report path")

    control = subparsers.add_parser(
        "control", help="Select the minimum-turnover set within a utility-regret budget"
    )
    control.add_argument("--r0", required=True, help="Baseline CSV")
    control.add_argument("--r1", required=True, help="Updated CSV")
    control.add_argument("--id-col", default="id")
    control.add_argument("--score-col", default="score")
    control.add_argument("--k", type=int, required=True)
    control.add_argument(
        "--eta",
        type=float,
        required=True,
        help="Maximum normalized updated-score utility regret (0.001 means 0.1%%)",
    )
    control.add_argument("--out", default="-", help="JSON path, or - for stdout")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    aligned = _align(args.r0, args.r1, args.id_col, args.score_col)
    ids = aligned[args.id_col].astype(str).to_numpy()
    scores_r0 = aligned.score_r0.to_numpy()
    scores_r1 = aligned.score_r1.to_numpy()

    if args.command == "compare":
        result = audit_scores(ids, scores_r0, scores_r1, args.k)
        _write_json(result, args.out)
        if args.report:
            Path(args.report).write_text(
                render_markdown_report(result), encoding="utf-8"
            )
        return

    frontier = identity_utility_frontier(ids, scores_r0, scores_r1, args.k)
    result = select_identity_control(frontier, args.eta)
    result["selected_ids"] = [str(ids[int(index)]) for index in result["selected_indices"]]
    _write_json(result, args.out)


if __name__ == "__main__":
    main()
