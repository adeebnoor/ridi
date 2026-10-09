#!/usr/bin/env python3
"""CPU-only integrity checks. No source datasets, model download, or generation is used."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "scale_runner", Path(__file__).resolve().parents[1] / "code" / "run_scale_curve.py")
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class RunnerIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def begin(self, attempt=1, config="a" * 64):
        return runner.begin_attempt(self.root, "qwen3-8b", "nq", attempt, config)

    def test_existing_attempt_cannot_be_reused_or_skipped(self):
        self.begin()
        with self.assertRaises(runner.ProtocolError):
            self.begin()
        with self.assertRaises(runner.ProtocolError):
            self.begin(3)
        with self.assertRaises(runner.ProtocolError):
            self.begin(2)  # Still running, not a technical failure.

    def test_success_cannot_be_rerun(self):
        out, status = self.begin()
        status["status"] = "succeeded"
        runner.atomic_json(out / "attempt_status.json", status)
        with self.assertRaises(runner.ProtocolError):
            self.begin(2)

    def test_technical_retries_are_sequential_and_bounded(self):
        for attempt in range(1, 4):
            out, status = self.begin(attempt)
            runner.finish_failure(out, status, MemoryError())
        with self.assertRaises(runner.ProtocolError):
            self.begin(4)
        self.assertEqual(len(list((self.root / "qwen3-8b" / "nq").glob("attempt*"))), 3)

    def test_retry_cannot_change_configuration(self):
        out, status = self.begin()
        runner.finish_failure(out, status, TimeoutError())
        with self.assertRaises(runner.ProtocolError):
            self.begin(2, "b" * 64)

    def test_protocol_failure_is_not_retryable(self):
        out, status = self.begin()
        runner.finish_failure(out, status, runner.ProtocolError("hash mismatch"))
        self.assertEqual(status["status"], "blocked")
        with self.assertRaises(runner.ProtocolError):
            self.begin(2)

    def test_completed_answers_survive_later_failure_without_error_payload(self):
        out, status = self.begin()
        runner.persist_answer(out, "synthetic-question", "reference_single", "synthetic answer")
        runner.finish_failure(out, status, RuntimeError("CUDA out of memory; synthetic secret payload"))
        record = json.loads((out / "partial_answers.jsonl").read_text())
        saved_status = (out / "attempt_status.json").read_text()
        self.assertEqual(record["answer"], "synthetic answer")
        self.assertEqual(status["status"], "failed")
        self.assertNotIn("synthetic secret payload", saved_status)
        self.assertFalse((out / "run_meta.json").exists())

    def test_lock_requires_exact_files_study_and_valid_hashes(self):
        for name in runner.LOCK_FILES:
            (self.root / name).write_text("synthetic locked file\n")
        valid = {"study": runner.STUDY, "files": {
            name: runner.sha_file(self.root / name) for name in runner.LOCK_FILES}}
        with patch.object(runner, "HERE", self.root):
            runner.atomic_json(self.root / "LOCK.json", valid)
            self.assertEqual(runner.verify_lock(), valid)
            for invalid in ({"study": runner.STUDY, "files": {}},
                            {"study": "wrong-study", "files": valid["files"]},
                            {"study": runner.STUDY, "files": {**valid["files"], "extra.py": "0" * 64}}):
                runner.atomic_json(self.root / "LOCK.json", invalid)
                with self.assertRaises(runner.ProtocolError):
                    runner.verify_lock()
            runner.atomic_json(self.root / "LOCK.json", valid)
            (self.root / "models.json").write_text("changed\n")
            with self.assertRaises(SystemExit):
                runner.verify_lock()

    def test_gpu_count_and_memory_gate(self):
        enough = runner.MIN_GPU_MEMORY_BYTES
        runner.verify_gpu_memory([enough], 1)
        runner.verify_gpu_memory([enough] * 8, 8)
        with self.assertRaises(runner.ProtocolError):
            runner.verify_gpu_memory([enough] * 7, 8)
        with self.assertRaises(runner.ProtocolError):
            runner.verify_gpu_memory([enough - 1], 1)

    def test_preflight_cli_does_not_consume_attempt_or_require_lock(self):
        with patch("sys.argv", ["runner", "--model-key", "qwen3-8b", "--dataset", "nq", "--preflight-only"]), \
             patch.object(runner, "verify_lock") as lock, \
             patch.object(runner, "begin_attempt") as attempt, \
             patch.object(runner, "execute_job") as execute:
            runner.main()
            lock.assert_not_called()
            attempt.assert_not_called()
            execute.assert_called_once()
            self.assertTrue(execute.call_args.args[0].preflight_only)
            self.assertEqual(execute.call_args.args[1:], (None, None, None, None))


if __name__ == "__main__":
    unittest.main()
