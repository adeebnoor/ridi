"""Synthetic software tests only; none are RIDI study observations."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "review_tools" / "rag_parser_sensitivity.py"
spec = importlib.util.spec_from_file_location("rag_parser_sensitivity_review", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


@pytest.mark.parametrize("answer,label", [
    ("SUPPORTS [1]", "SUPPORTS"),
    ("REFUTES.", "REFUTES"),
    ("NOT_ENOUGH_INFO", "NOT_ENOUGH_INFO"),
    ("Verdict: SUPPORTS [1]", "SUPPORTS"),
    ("Answer: REFUTES [1]", "REFUTES"),
    ("Classification: NOT_ENOUGH_INFO", "NOT_ENOUGH_INFO"),
    ("  label: supports\nExplanation", "SUPPORTS"),
    ("**Verdict:** **SUPPORTS**", "SUPPORTS"),
    ("> Verdict: REFUTES", "REFUTES"),
    ("`SUPPORTS`", "SUPPORTS"),
    ("", "UNPARSEABLE"),
    ("   ", "UNPARSEABLE"),
    ("The evidence SUPPORTS the claim", "UNPARSEABLE"),
    ("This does not SUPPORTS", "UNPARSEABLE"),
    ("SUPPORTS_NOT_SURE", "UNPARSEABLE"),
    ("SUPPORTS1", "UNPARSEABLE"),
    ("UNSUPPORTED", "UNPARSEABLE"),
    ("Verdict is SUPPORTS", "UNPARSEABLE"),
    ("NOT ENOUGH INFO", "UNPARSEABLE"),
    ("```json\nSUPPORTS\n```", "UNPARSEABLE"),
])
def test_prefix_parser(answer, label):
    assert mod.parse_prefix(answer) == label


def test_non_string_answer_is_not_imputed():
    with pytest.raises(ValueError):
        mod.parse_prefix(None)


def synthetic_record(dataset, qid, reference, alternative, ref_label, alt_label, gold="SUPPORTS"):
    return {
        "dataset": dataset, "query_id": qid, "gold": gold,
        "answers": {"reference": reference, "identity": reference,
                    "permutation": reference, "random": alternative},
        "registered_labels": {"reference": ref_label, "identity": ref_label,
                              "permutation": ref_label, "random": alt_label},
    }


@pytest.fixture
def synthetic_inputs(tmp_path):
    panel = {"fever": ["f1", "f2"], "scifact": ["s1", "s2"]}
    rows = [
        synthetic_record("fever", "f1", "Verdict: SUPPORTS", "REFUTES", "UNPARSEABLE", "REFUTES"),
        synthetic_record("fever", "f2", "SUPPORTS", "Answer: SUPPORTS", "SUPPORTS", "UNPARSEABLE"),
        synthetic_record("scifact", "s1", "SUPPORTS", "REFUTES", "SUPPORTS", "REFUTES", "REFUTES"),
        synthetic_record("scifact", "s2", "Cannot determine", "Still unknown", "UNPARSEABLE", "UNPARSEABLE"),
    ]
    panel_path = tmp_path / "synthetic_panel.json"
    responses = tmp_path / "synthetic_responses.jsonl"
    panel_path.write_text(json.dumps(panel), encoding="utf-8")
    responses.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return panel, rows, panel_path, responses


def test_panel_strict_default_rejects_small_fixture(synthetic_inputs):
    _, _, panel_path, _ = synthetic_inputs
    with pytest.raises(ValueError):
        mod.load_panel(panel_path)


def test_read_panel_and_inputs(synthetic_inputs):
    panel, rows, panel_path, responses = synthetic_inputs
    assert mod.load_panel(panel_path, expected_per_dataset=2) == panel
    assert mod.load_records(responses, panel) == rows


def test_input_order_is_irrelevant(synthetic_inputs):
    panel, rows, _, responses = synthetic_inputs
    responses.write_text("".join(json.dumps(r) + "\n" for r in reversed(rows)), encoding="utf-8")
    assert mod.load_records(responses, panel) == rows


@pytest.mark.parametrize("mutation", ["duplicate", "missing", "outside", "condition", "bad_gold", "bad_label", "nonstring", "blank"])
def test_reject_invalid_input(synthetic_inputs, mutation):
    panel, rows, _, responses = synthetic_inputs
    rows = copy.deepcopy(rows)
    if mutation == "duplicate":
        rows.append(rows[0])
    elif mutation == "missing":
        rows.pop()
    elif mutation == "outside":
        rows[0]["query_id"] = "outside"
    elif mutation == "condition":
        del rows[0]["answers"]["identity"]
    elif mutation == "bad_gold":
        rows[0]["gold"] = "UNPARSEABLE"
    elif mutation == "bad_label":
        rows[0]["registered_labels"]["random"] = "GUESS"
    elif mutation == "nonstring":
        rows[0]["answers"]["random"] = None
    text = "".join(json.dumps(r) + "\n" for r in rows)
    if mutation == "blank":
        text += "\n"
    responses.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError):
        mod.load_records(responses, panel)


def test_no_silent_correctness_reconciliation(synthetic_inputs):
    panel, rows, _, responses = synthetic_inputs
    rows = copy.deepcopy(rows)
    rows[0]["registered_correctness"] = dict.fromkeys(mod.CONDITIONS, 1)
    responses.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    with pytest.raises(ValueError, match="inconsistency"):
        mod.load_records(responses, panel)


def test_duplicate_panel_id_rejected(synthetic_inputs):
    panel, _, panel_path, _ = synthetic_inputs
    panel["fever"] = ["f1", "f1"]
    panel_path.write_text(json.dumps(panel), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        mod.load_panel(panel_path, expected_per_dataset=2)


def test_synthetic_flip_decomposition_and_controls(synthetic_inputs):
    _, rows, _, _ = synthetic_inputs
    report, diagnostics = mod.audit(rows, draws=100, seed=7)
    assert report["random_comparison_flip_persistence"] == {
        "registered_flips_persist": 1, "registered_flips_resolve": 1,
        "new_flips": 1, "neither_rule_flips": 1,
    }
    assert len(diagnostics) == 16
    assert report["n_queries"] == 4
    assert report["new_model_calls"] == 0
    assert report["registered_endpoint_modified"] is False
    assert report["human_adjudication"] is False
    assert report["identity_raw_text_mismatches"] == 0
    for metric in report["metrics"]:
        assert metric["correctness_flips"] == metric["correct_to_incorrect"] + metric["incorrect_to_correct"]
        assert metric["correctness_flips"] == metric["both_parseable_correctness_flips"] + metric["flips_involving_unparseable"]
        if metric["comparison"] == "identity":
            assert metric["correctness_flips"] == 0


def test_repeatability_and_no_mutation(synthetic_inputs):
    _, rows, _, _ = synthetic_inputs
    before = copy.deepcopy(rows)
    assert mod.audit(rows, draws=100, seed=9) == mod.audit(rows, draws=100, seed=9)
    assert rows == before


def test_all_unparseable_has_no_parseable_rate():
    row = synthetic_record("fever", "f1", "Unknown", "Unknown", "UNPARSEABLE", "UNPARSEABLE")
    result = mod.comparison_metrics([row], "registered", "random")
    assert result["both_parseable"] == 0
    assert result["both_parseable_flip_rate"] is None
    assert result["correctness_flips"] == 0


def test_text_label_change_is_not_necessarily_correctness_flip():
    row = synthetic_record("fever", "f1", "SUPPORTS", "REFUTES", "SUPPORTS", "REFUTES", "NOT_ENOUGH_INFO")
    result = mod.comparison_metrics([row], "registered", "random")
    assert result["canonical_label_changes"] == 1
    assert result["correctness_flips"] == 0


def test_bootstrap_is_paired_when_rules_agree():
    rows = [synthetic_record(ds, "q1", "SUPPORTS", "REFUTES", "SUPPORTS", "REFUTES") for ds in mod.DATASETS]
    result = mod.paired_bootstrap(rows, draws=50, seed=1)
    assert result["intervals_95"]["difference_new_minus_registered"] == [0.0, 0.0]


def test_bootstrap_requires_both_datasets():
    rows = [synthetic_record("fever", "q1", "SUPPORTS", "REFUTES", "SUPPORTS", "REFUTES")]
    with pytest.raises(ValueError):
        mod.paired_bootstrap(rows, draws=50, seed=1)


def test_percentile_definition():
    assert mod.percentile([0.0, 1.0], 0.25) == 0.25
    assert mod.percentile([0.0, 1.0], 0) == 0
    assert mod.percentile([0.0, 1.0], 1) == 1
    with pytest.raises(ValueError):
        mod.percentile([], 0.5)


def test_cli_complete_synthetic_panel_and_overwrite_refusal(tmp_path):
    panel = {ds: [f"synthetic_{i}" for i in range(150)] for ds in mod.DATASETS}
    rows = [synthetic_record(ds, q, "Verdict: SUPPORTS", "REFUTES", "UNPARSEABLE", "REFUTES")
            for ds, ids in panel.items() for q in ids]
    pp = tmp_path / "panel.json"
    rp = tmp_path / "responses.jsonl"
    output = tmp_path / "audit"
    pp.write_text(json.dumps(panel), encoding="utf-8")
    rp.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    original_hash = mod.sha256(rp)
    command = [sys.executable, str(SCRIPT), "--panel", str(pp), "--responses", str(rp),
               "--out", str(output), "--draws", "20"]
    first = subprocess.run(command, capture_output=True, text=True, timeout=30)
    assert first.returncode == 0, first.stderr
    result = json.loads((output / "sensitivity_report.json").read_text(encoding="utf-8"))
    assert result["n_queries"] == 300
    assert result["inputs"]["responses_sha256"] == original_hash
    assert result["new_model_calls"] == 0
    assert mod.sha256(rp) == original_hash
    second = subprocess.run(command, capture_output=True, text=True, timeout=30)
    assert second.returncode == 2
    assert "overwrite" in second.stderr
