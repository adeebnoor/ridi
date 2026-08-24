#!/usr/bin/env python3
"""Blind executor for a separately operated RIDI cybersecurity replication."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

import numpy
import scipy


HERE = Path(__file__).resolve()
REPO = HERE.parents[3]
EXPERIMENT = REPO / "experiments/cyber_natural_update"
OUTPUT = REPO / "replication_output"
INPUTS = OUTPUT / "inputs"
RESULTS = OUTPUT / "results"
PROTOCOL_COMMIT = "773219057b03fafb21dbc9c4623284a2da0ca83a"
LOCKED_HASHES = {
    "experiments/cyber_natural_update/PROTOCOL_LOCK.md": "8e467481b2107e291e914c40dcd422bb11ed4fac580105fc0aac3964e42aff61",
    "experiments/cyber_natural_update/protocol.json": "18f2126078ad8b57c0b6a9ed36a6ada471bd04ce47ff3366da8aa65dd0fd8c88",
    "experiments/cyber_natural_update/fetch_inputs.py": "d4b67bd8a093961a32ce52e0151408d1478b638187997955bb9d42ad41661d20",
    "experiments/cyber_natural_update/run_locked_analysis.py": "c08c954c8e290bcb0c3e5daa12b58ffc3dc2843b1acf5dfaf5e836078e55d803",
    "src/ridi_audit/__init__.py": "8dbbd33102fa1579384673149b98ca3a0572f62a2c623473d71982f744835062",
    "src/ridi_audit/core.py": "3bfd8cbb01781202fc79c62498c33af97e579788828aa62dc0dad61e1b47fb61",
    "src/ridi_audit/selector.py": "d53243735851e3ebeab5e2b5cdc10f91ea88523136ace3a9263f9610278bbefa",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_value(*args: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO), *args], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=REPO, check=True)


def main() -> None:
    started = datetime.now(timezone.utc).isoformat()
    verified = {}
    for relative, expected in LOCKED_HASHES.items():
        actual = sha256(REPO / relative)
        if actual != expected:
            raise SystemExit(f"locked-file hash mismatch: {relative}: {actual}")
        verified[relative] = actual

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    INPUTS.mkdir(parents=True)
    RESULTS.mkdir(parents=True)

    run([sys.executable, str(EXPERIMENT / "fetch_inputs.py"), "--out", str(INPUTS)])
    run([
        sys.executable,
        str(EXPERIMENT / "run_locked_analysis.py"),
        "--inputs", str(INPUTS),
        "--out", str(RESULTS),
    ])

    shutil.copy2(INPUTS / "input_manifest.json", OUTPUT / "input_manifest.json")
    shutil.copy2(RESULTS / "locked_results.json", OUTPUT / "locked_results.json")
    record = {
        "protocol_id": "RIDI-CYBER-NATURAL-UPDATE-v1",
        "protocol_commit": PROTOCOL_COMMIT,
        "repository_head": git_value("rev-parse", "HEAD"),
        "repository_status_porcelain": git_value("status", "--porcelain"),
        "started_utc": started,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "python_executable": sys.executable,
            "numpy": numpy.__version__,
            "scipy": scipy.__version__,
            "hostname_hash": hashlib.sha256(platform.node().encode()).hexdigest(),
        },
        "locked_files": verified,
        "outputs": {
            "input_manifest.json": sha256(OUTPUT / "input_manifest.json"),
            "locked_results.json": sha256(OUTPUT / "locked_results.json"),
        },
        "independence_attestation": "Requires separately signed TEAM_DECLARATION.md",
        "author_result_compared_during_run": False,
    }
    execution_path = OUTPUT / "replication_execution.json"
    execution_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(f"Sealed outputs written to {OUTPUT}")
    print(f"execution SHA-256: {sha256(execution_path)}")


if __name__ == "__main__":
    os.environ.setdefault("PYTHONHASHSEED", "0")
    main()
