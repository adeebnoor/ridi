#!/usr/bin/env python3
"""Fetch the protocol-pinned public inputs and record integrity hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen


EPSS_COMMIT = "3b3ae5b793011090800848c75ceea4cecaa9d309"
KEV_COMMIT = "fea466c2e713d1f44e74c903ad4f60b81470bb22"
FILES = {
    "epss_2023_03_05.csv.gz": f"https://raw.githubusercontent.com/empiricalsec/epss_scores/{EPSS_COMMIT}/2023/epss_scores-2023-03-05.csv.gz",
    "epss_2023_03_06.csv.gz": f"https://raw.githubusercontent.com/empiricalsec/epss_scores/{EPSS_COMMIT}/2023/epss_scores-2023-03-06.csv.gz",
    "epss_2023_03_07.csv.gz": f"https://raw.githubusercontent.com/empiricalsec/epss_scores/{EPSS_COMMIT}/2023/epss_scores-2023-03-07.csv.gz",
    "epss_2023_03_08.csv.gz": f"https://raw.githubusercontent.com/empiricalsec/epss_scores/{EPSS_COMMIT}/2023/epss_scores-2023-03-08.csv.gz",
    "known_exploited_vulnerabilities.csv": f"https://raw.githubusercontent.com/cisagov/kev-data/{KEV_COMMIT}/known_exploited_vulnerabilities.csv",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("inputs"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    manifest = {"protocol_id": "RIDI-CYBER-NATURAL-UPDATE-v1", "files": {}}
    for name, url in FILES.items():
        target = args.out / name
        with urlopen(url, timeout=120) as response, target.open("wb") as output:
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                output.write(block)
        manifest["files"][name] = {
            "url": url,
            "bytes": target.stat().st_size,
            "sha256": sha256(target),
        }
    (args.out / "input_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
