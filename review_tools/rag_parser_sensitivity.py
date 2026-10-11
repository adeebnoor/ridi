"""Post hoc classification-parser sensitivity; no generation or network access.

The imported registered labels are preserved, not reconstructed by a guessed
implementation of the frozen parser. This module compares them with one declared
format-tolerant, answer-prefix-only parser. It is NOT human adjudication.

CLI input: exactly the frozen 150 FEVER and 150 SciFact queries, in normalized
JSONL records documented in README.md. An explicit frozen panel is mandatory.
No manuscript data are bundled with this tool.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
import sys
from pathlib import Path
from typing import Any

DATASETS = ("fever", "scifact")
CONDITIONS = ("reference", "identity", "permutation", "random")
COMPARISONS = ("identity", "permutation", "random")
GOLD_LABELS = frozenset({"SUPPORTS", "REFUTES", "NOT_ENOUGH_INFO"})
LABELS = GOLD_LABELS | {"UNPARSEABLE"}
PARSER_ID = "anchored_optional_wrapper_v1"

# An answer must START with a permitted label, optionally preceded by opening
# Markdown and one explicitly enumerated colon-terminated wrapper. Do not search
# arbitrary explanation text for labels and do not guess semantic equivalents.
_PREFIX = re.compile(
    r"\A\s*(?:[>#*_`]+\s*)*"
    r"(?:(?:verdict|answer|label|classification)\s*:\s*(?:[*_`]+\s*)*)?"
    r"(NOT_ENOUGH_INFO|SUPPORTS|REFUTES)(?![A-Za-z0-9_])",
    flags=re.IGNORECASE,
)
_QUERY_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]*\Z")


def parse_prefix(answer: str) -> str:
    """Return a prefix label; formatting normalization is not meaning assessment."""
    if not isinstance(answer, str):
        raise ValueError("Answer must be a string; missing responses are not labels.")
    match = _PREFIX.match(answer)
    return match.group(1).upper() if match else "UNPARSEABLE"


def correct(label: str, gold: str) -> int:
    if label not in LABELS or gold not in GOLD_LABELS:
        raise ValueError("Invalid canonical label or benchmark gold label.")
    return int(label == gold)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_panel(path: Path, expected_per_dataset: int = 150) -> dict[str, list[str]]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict) or set(obj) != set(DATASETS):
        raise ValueError("Panel must contain exactly 'fever' and 'scifact'.")
    if expected_per_dataset < 1:
        raise ValueError("Expected panel size must be positive.")
    for dataset, ids in obj.items():
        if not isinstance(ids, list) or len(ids) != expected_per_dataset:
            raise ValueError(f"{dataset}: wrong frozen-panel size.")
        if any(not isinstance(q, str) or not _QUERY_ID.fullmatch(q) for q in ids):
            raise ValueError(f"{dataset}: invalid query identifier.")
        if len(ids) != len(set(ids)):
            raise ValueError(f"{dataset}: duplicate panel identifier.")
    return obj


def load_records(path: Path, panel: dict[str, list[str]]) -> list[dict[str, Any]]:
    expected = {(dataset, qid) for dataset, ids in panel.items() for qid in ids}
    seen: dict[tuple[str, str], dict[str, Any]] = {}
    required = {"dataset", "query_id", "gold", "answers", "registered_labels"}
    with path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                raise ValueError(f"Line {lineno}: blank record is not permitted.")
            row = json.loads(line)
            if not isinstance(row, dict) or not required.issubset(row):
                raise ValueError(f"Line {lineno}: missing normalized fields.")
            if not isinstance(row["dataset"], str) or not isinstance(row["query_id"], str):
                raise ValueError(f"Line {lineno}: identifiers must be strings.")
            key = (row["dataset"], row["query_id"])
            if key not in expected or key in seen:
                raise ValueError(f"Line {lineno}: outside-panel or duplicate query.")
            if row["gold"] not in GOLD_LABELS:
                raise ValueError(f"Line {lineno}: invalid benchmark gold label.")
            answers, labels = row["answers"], row["registered_labels"]
            if not isinstance(answers, dict) or set(answers) != set(CONDITIONS):
                raise ValueError(f"Line {lineno}: all four answer conditions are required.")
            if not isinstance(labels, dict) or set(labels) != set(CONDITIONS):
                raise ValueError(f"Line {lineno}: all archived registered labels are required.")
            if any(not isinstance(answer, str) for answer in answers.values()):
                raise ValueError(f"Line {lineno}: missing or non-string answer.")
            if any(not isinstance(label, str) or label not in LABELS for label in labels.values()):
                raise ValueError(f"Line {lineno}: invalid archived registered label.")
            # Optional archived correctness is checked, never silently reconciled.
            if "registered_correctness" in row:
                cc = row["registered_correctness"]
                if not isinstance(cc, dict) or set(cc) != set(CONDITIONS):
                    raise ValueError(f"Line {lineno}: incomplete registered correctness.")
                for condition in CONDITIONS:
                    if type(cc[condition]) is not int or cc[condition] not in (0, 1):
                        raise ValueError(f"Line {lineno}: correctness must be integer 0 or 1.")
                    if cc[condition] != correct(labels[condition], row["gold"]):
                        raise ValueError(f"Line {lineno}: archived label/correctness inconsistency.")
            seen[key] = row
    if set(seen) != expected:
        raise ValueError(f"Missing {len(expected - set(seen))} frozen-panel queries.")
    # Preserve declared panel order, not file order; do not modify raw answer text.
    return [seen[(dataset, qid)] for dataset in DATASETS for qid in panel[dataset]]


def comparison_metrics(rows: list[dict[str, Any]], method: str, condition: str) -> dict[str, Any]:
    if not rows or condition not in COMPARISONS:
        raise ValueError("Nonempty rows and a declared comparison are required.")
    if method not in ("registered", PARSER_ID):
        raise ValueError("Unknown scoring method.")
    result: dict[str, Any] = {
        "n": len(rows), "reference_correct": 0, "alternative_correct": 0,
        "correctness_flips": 0, "correct_to_incorrect": 0,
        "incorrect_to_correct": 0, "canonical_label_changes": 0,
        "reference_unparseable": 0, "alternative_unparseable": 0,
        "both_parseable": 0, "both_parseable_correctness_flips": 0,
        "flips_involving_unparseable": 0,
    }
    for row in rows:
        labels = row["registered_labels"] if method == "registered" else {
            c: parse_prefix(row["answers"][c]) for c in CONDITIONS
        }
        ref, alt = labels["reference"], labels[condition]
        a, b = correct(ref, row["gold"]), correct(alt, row["gold"])
        flip = a != b
        parsed = ref != "UNPARSEABLE" and alt != "UNPARSEABLE"
        result["reference_correct"] += a
        result["alternative_correct"] += b
        result["correctness_flips"] += int(flip)
        result["correct_to_incorrect"] += int(a == 1 and b == 0)
        result["incorrect_to_correct"] += int(a == 0 and b == 1)
        result["canonical_label_changes"] += int(ref != alt)
        result["reference_unparseable"] += int(ref == "UNPARSEABLE")
        result["alternative_unparseable"] += int(alt == "UNPARSEABLE")
        result["both_parseable"] += int(parsed)
        result["both_parseable_correctness_flips"] += int(parsed and flip)
        result["flips_involving_unparseable"] += int(not parsed and flip)
    n = result["n"]
    result["correctness_flip_rate"] = result["correctness_flips"] / n
    result["accuracy_difference"] = (result["alternative_correct"] - result["reference_correct"]) / n
    denom = result["both_parseable"]
    result["both_parseable_flip_rate"] = (
        result["both_parseable_correctness_flips"] / denom if denom else None
    )
    assert result["correctness_flips"] == result["correct_to_incorrect"] + result["incorrect_to_correct"]
    return result


def percentile(values: list[float], q: float) -> float:
    if not values or not 0 <= q <= 1:
        raise ValueError("Invalid percentile request.")
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)


def paired_bootstrap(rows: list[dict[str, Any]], draws: int, seed: int) -> dict[str, Any]:
    """Paired, dataset-stratified resampling for the random-context comparison.

    This estimates a two-classification-dataset macro, NOT the four-dataset H2.
    """
    if draws < 2:
        raise ValueError("At least two bootstrap draws are required.")
    groups: list[list[tuple[int, int]]] = []
    for dataset in DATASETS:
        pairs = []
        for row in rows:
            if row["dataset"] != dataset:
                continue
            gold = row["gold"]
            old = row["registered_labels"]
            new = {c: parse_prefix(row["answers"][c]) for c in CONDITIONS}
            pairs.append((
                int(correct(old["reference"], gold) != correct(old["random"], gold)),
                int(correct(new["reference"], gold) != correct(new["random"], gold)),
            ))
        if not pairs:
            raise ValueError("Both classification datasets are required.")
        groups.append(pairs)
    rng = random.Random(seed)
    samples = {"registered": [], PARSER_ID: [], "difference_new_minus_registered": []}
    for _ in range(draws):
        totals = [0.0, 0.0]
        for group in groups:
            a = b = 0
            for _ in range(len(group)):
                x, y = group[rng.randrange(len(group))]
                a += x
                b += y
            totals[0] += a / len(group) / len(groups)
            totals[1] += b / len(group) / len(groups)
        samples["registered"].append(totals[0])
        samples[PARSER_ID].append(totals[1])
        samples["difference_new_minus_registered"].append(totals[1] - totals[0])
    return {
        "draws": draws, "seed": seed, "scope": "two-dataset classification macro",
        "interval_type": "paired stratified percentile bootstrap, descriptive post hoc",
        "intervals_95": {
            key: [percentile(values, 0.025), percentile(values, 0.975)]
            for key, values in samples.items()
        },
    }


def audit(rows: list[dict[str, Any]], draws: int = 10000, seed: int = 20260914) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not rows or {r["dataset"] for r in rows} != set(DATASETS):
        raise ValueError("Both nonempty classification panels are required.")
    metrics = []
    for dataset in DATASETS:
        group = [r for r in rows if r["dataset"] == dataset]
        for method in ("registered", PARSER_ID):
            for condition in COMPARISONS:
                metrics.append({"dataset": dataset, "method": method, "comparison": condition,
                                **comparison_metrics(group, method, condition)})
    diagnostics = []
    persistence = {"registered_flips_persist": 0, "registered_flips_resolve": 0,
                   "new_flips": 0, "neither_rule_flips": 0}
    for row in rows:
        gold = row["gold"]
        old = row["registered_labels"]
        new = {c: parse_prefix(row["answers"][c]) for c in CONDITIONS}
        a = correct(old["reference"], gold) != correct(old["random"], gold)
        b = correct(new["reference"], gold) != correct(new["random"], gold)
        key = ("registered_flips_persist" if a and b else
               "registered_flips_resolve" if a else "new_flips" if b else "neither_rule_flips")
        persistence[key] += 1
        for condition in CONDITIONS:
            diagnostics.append({
                "dataset": row["dataset"], "query_id": row["query_id"],
                "condition": condition, "gold": gold,
                "registered_label": old[condition], "sensitivity_label": new[condition],
                "registered_correct": correct(old[condition], gold),
                "sensitivity_correct": correct(new[condition], gold),
            })
    report = {
        "analysis": "RIDI post hoc classification-parser sensitivity",
        "parser": PARSER_ID,
        "registered_endpoint_modified": False,
        "new_model_calls": 0,
        "human_adjudication": False,
        "formal_independent_review": False,
        "n_queries": len(rows),
        "identity_raw_text_mismatches": sum(
            row["answers"]["reference"] != row["answers"]["identity"] for row in rows),
        "metrics": metrics,
        "random_comparison_flip_persistence": persistence,
        "bootstrap": paired_bootstrap(rows, draws, seed),
        "limitations": [
            "Archived registered labels are imported, not independently regenerated by the original scorer.",
            "Prefix-format parsing does not establish semantic correctness or correct benchmark labels.",
            "Both-parseable subsets are conditional and have different denominators.",
            "Classification macro is not the four-dataset primary H2 endpoint.",
            "No new model responses, prospective registration, or independent clinical review are supplied.",
        ],
    }
    return report, diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--responses", required=True, type=Path)
    parser.add_argument("--panel", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--draws", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260914)
    args = parser.parse_args()
    try:
        if args.out.exists():
            raise ValueError("Output destination exists; refusing to overwrite prior results.")
        panel = load_panel(args.panel)
        rows = load_records(args.responses, panel)
        report, diagnostics = audit(rows, args.draws, args.seed)
        report["inputs"] = {"responses_sha256": sha256(args.responses),
                            "panel_sha256": sha256(args.panel),
                            "code_sha256": sha256(Path(__file__))}
        report["python"] = sys.version
        args.out.mkdir(parents=True, exist_ok=False)
        (args.out / "sensitivity_report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        with (args.out / "per_query_diagnostics.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(diagnostics[0]))
            writer.writeheader()
            writer.writerows(diagnostics)
        print(f"Audited {len(rows)} archived queries. No model generation was performed.")
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"Analysis stopped: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
