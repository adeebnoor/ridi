#!/usr/bin/env python3
"""Synthetic-only integrity and decision-boundary tests; never uses study outputs."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "code" / "aggregate_scale_curve.py"
spec = importlib.util.spec_from_file_location("aggregate_scale_curve", SOURCE)
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class AggregateIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="ridi_synthetic_analysis_")
        self.root = Path(self.tmp.name)
        self.code = self.root / "code"
        self.code.mkdir()
        self.out = self.root / "SYNTHETIC_ONLY"
        self.original_here = analysis.HERE
        analysis.HERE = self.code
        self.models = [{"key": "qwen3-" + name, "model_id": "synthetic/" + name,
                        "revision": "a" * 40, "params_b": size}
                       for name, size in (("0.6b", .6), ("1.7b", 1.7), ("4b", 4),
                                          ("8b", 8), ("14b", 14), ("32b", 32))]
        model_file = {"study": analysis.STUDY, "primary_family": self.models, "optional_tier": []}
        (self.code / "models.json").write_text(json.dumps(model_file))
        (self.code / "run_scale_curve.py").write_text("# SYNTHETIC TEST PLACEHOLDER; not executable\n")
        (self.code / "aggregate_scale_curve.py").write_bytes(SOURCE.read_bytes())
        files = {name: digest(self.code / name) for name in
                 ("models.json", "run_scale_curve.py", "aggregate_scale_curve.py")}
        self.lock = {"study": analysis.STUDY, "files": files}
        # This is a disposable synthetic fixture, never a study lock.
        (self.code / "LOCK.json").write_text(json.dumps(self.lock))
        for model in self.models:
            for dataset, n in analysis.EXPECTED_N.items():
                succeeds = model["key"] == "qwen3-32b"
                for attempt in range(1, 2 if succeeds else 4):
                    path = self.out / model["key"] / dataset / f"attempt{attempt}"
                    path.mkdir(parents=True)
                    state = {"study": analysis.STUDY, "model_key": model["key"],
                             "dataset": dataset, "attempt": attempt,
                             "configuration_sha256": "b" * 64,
                             "status": "succeeded" if succeeds else "failed"}
                    if not succeeds:
                        state["failure_kind"] = "technical"
                    (path / "attempt_status.json").write_text(json.dumps(state))
                if succeeds:
                    rows = []
                    for i in range(n):
                        flip = dataset in ("nq", "hotpotqa") and i < 26
                        floor = dataset in ("nq", "hotpotqa") and i < 1
                        rows.append({"dataset": dataset, "query_id": str(i), "model_key": model["key"],
                                     "task": "qa" if dataset in ("nq", "hotpotqa") else "classification",
                                     "reference_single_correct": True, "random_single_correct": not flip,
                                     "reference_fixed16_correct": not floor,
                                     "intervention_changed": flip, "floor_changed": floor,
                                     "canonical_changed": flip, "correct_to_wrong": flip, "wrong_to_correct": False})
                    raw = path / f"{model['key']}__{dataset}__records.jsonl"
                    raw.write_text("".join(json.dumps(row) + "\n" for row in rows))
                    meta = {"study": analysis.STUDY, "model": model, "dataset": dataset, "n": n,
                            "attempt": 1, "status": "succeeded", "configuration_sha256": "b" * 64,
                            "records_sha256": digest(raw), "lock": files,
                            "checks": {"synthetic_only": True}}
                    (path / "run_meta.json").write_text(json.dumps(meta))
        features = []
        for dataset, n in analysis.EXPECTED_N.items():
            for i in range(n):
                index = len(features)
                features.append({"dataset": dataset, "qid": str(i),
                                 "task": "qa" if dataset in ("nq", "hotpotqa") else "classification",
                                 "tot_either": int(index >= 93), "tot_both": int(index >= 238),
                                 "clean_original_rule": int(index < 86), "tot_gold": int(index >= 282)})
        self.features = self.root / "SYNTHETIC_features.jsonl"
        self.features.write_text("".join(json.dumps(row) + "\n" for row in features))
        self.lock["feature_sha256"] = digest(self.features)
        (self.code / "LOCK.json").write_text(json.dumps(self.lock))

    def tearDown(self):
        analysis.HERE = self.original_here
        self.tmp.cleanup()

    def test_closed_synthetic_panel_is_accepted(self):
        _, _, _, data, status = analysis.load(self.out)
        self.assertEqual(list(data), ["qwen3-32b"])
        self.assertEqual(status["qwen3-0.6b"], "not executed (0/4 datasets complete)")
        self.assertEqual(len(analysis.load_features(self.features, data["qwen3-32b"])), 800)

    def test_unfinished_job_blocks_before_outcomes_are_read(self):
        state = self.out / "qwen3-0.6b" / "nq" / "attempt3" / "attempt_status.json"
        record = json.loads(state.read_text()); record["status"] = "running"
        state.write_text(json.dumps(record))
        raw = self.out / "qwen3-32b" / "nq" / "attempt1" / "qwen3-32b__nq__records.jsonl"
        raw.write_text("DELIBERATELY INVALID OUTCOME DATA")
        with self.assertRaisesRegex(ValueError, "not terminal"):
            analysis.load(self.out)

    def test_modified_records_rejected(self):
        raw = self.out / "qwen3-32b" / "nq" / "attempt1" / "qwen3-32b__nq__records.jsonl"
        raw.write_text(raw.read_text() + "\n")
        with self.assertRaisesRegex(ValueError, "records SHA256 mismatch"):
            analysis.load(self.out)

    def test_modified_locked_script_rejected(self):
        (self.code / "run_scale_curve.py").write_text("# changed\n")
        with self.assertRaisesRegex(ValueError, "locked file changed"):
            analysis.load(self.out)

    def test_mismatched_metadata_lock_rejected(self):
        path = self.out / "qwen3-32b" / "nq" / "attempt1" / "run_meta.json"
        meta = json.loads(path.read_text()); meta["lock"] = {}
        path.write_text(json.dumps(meta))
        with self.assertRaisesRegex(ValueError, "different lock"):
            analysis.load(self.out)

    def test_bad_frozen_strata_rejected(self):
        _, _, _, data, _ = analysis.load(self.out)
        rows = self.features.read_text().splitlines()
        row = json.loads(rows[0]); row["tot_either"] = 1
        rows[0] = json.dumps(row)
        self.features.write_text("\n".join(rows) + "\n")
        # Rebind the disposable fixture hash to exercise the independent count gate.
        self.lock["feature_sha256"] = digest(self.features)
        (self.code / "LOCK.json").write_text(json.dumps(self.lock))
        with self.assertRaisesRegex(ValueError, "expected 93, got 92"):
            analysis.load_features(self.features, data["qwen3-32b"])

    def test_exact_thresholds_keep_inclusive_and_strict_rules(self):
        self.assertEqual(analysis.decision(150, [111, 189]), "supported")
        self.assertEqual(analysis.decision(150, [60, 189]), "inconclusive")
        self.assertEqual(analysis.decision(50, [30, 60]), "inconclusive")
        self.assertEqual(analysis.decision(50, [30, 59]), "falsified (vanishes)")

    def test_full_registered_bootstrap_exact_5pp_is_supported(self):
        proc = subprocess.run([sys.executable, str(self.code / "aggregate_scale_curve.py"), str(self.out),
                               "--features", str(self.features)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads((self.out / "SCALE_CURVE_RESULTS.json").read_text())
        self.assertEqual(result["bootstrap"]["draws"], 100000)
        self.assertEqual(result["H1_persistence_at_32B"], "supported")
        model = result["results"]["qwen3-32b"]
        self.assertEqual(model["macro_excess"], .05)
        self.assertAlmostEqual(model["macro_excess_ci95"][0], .037)
        self.assertIn("pooled_excess", model)
        self.assertIn("pooled_canonical", model)
        self.assertEqual(model["accuracy"]["pooled_reference_fixed16"], 798 / 800)
        self.assertEqual(result["S5_content_strata"]["qwen3-32b"]["qa_no_gold_string"]["n"], 282)

    def test_all_sizes_identical_changes_have_no_trend_and_maximal_overlap(self):
        for model in self.models[:-1]:
            base = self.out / model["key"]
            shutil.rmtree(base)
            for dataset in analysis.DATASETS:
                source = self.out / "qwen3-32b" / dataset / "attempt1"
                target = base / dataset / "attempt1"
                target.mkdir(parents=True)
                rows = [json.loads(line) for line in (source / f"qwen3-32b__{dataset}__records.jsonl").read_text().splitlines()]
                for row in rows:
                    row["model_key"] = model["key"]
                raw = target / f"{model['key']}__{dataset}__records.jsonl"
                raw.write_text("".join(json.dumps(row) + "\n" for row in rows))
                meta = json.loads((source / "run_meta.json").read_text())
                meta["model"] = model
                meta["records_sha256"] = digest(raw)
                (target / "run_meta.json").write_text(json.dumps(meta))
                state = json.loads((source / "attempt_status.json").read_text())
                state["model_key"] = model["key"]
                (target / "attempt_status.json").write_text(json.dumps(state))
        proc = subprocess.run([sys.executable, str(self.code / "aggregate_scale_curve.py"), str(self.out),
                               "--features", str(self.features)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads((self.out / "SCALE_CURVE_RESULTS.json").read_text())
        self.assertTrue(result["H2_all_primary_sizes_executed"])
        self.assertEqual(result["H3_scale_trend"]["classification"], "no detectable trend")
        self.assertAlmostEqual(result["H3_scale_trend"]["slope_excess_per_decade_params"], 0)
        overlap = result["S4_cross_scale_overlap"]
        self.assertTrue(all(pair["jaccard"] == 1 for pair in overlap["pairs"].values()))
        self.assertEqual(overlap["fragility_count_distribution"]["6"], 52)
        self.assertEqual(overlap["permutation_p_concentration"], 1 / 10001)


if __name__ == "__main__":
    unittest.main()
