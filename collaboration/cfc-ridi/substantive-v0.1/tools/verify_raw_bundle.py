#!/usr/bin/env python3
"""Verify an immutable CFC-RIDI raw ZIP bundle against its internal manifest."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import zipfile
from pathlib import PurePosixPath, Path

MANIFEST = "SHA256_MANIFEST.tsv"


def h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_member_name(name: str) -> None:
    p = PurePosixPath(name)
    if p.is_absolute() or ".." in p.parts or "\\" in name:
        raise ValueError(f"unsafe ZIP member path: {name}")


def verify(path: Path) -> None:
    raw = path.read_bytes()
    print(f"bundle_sha256={h(raw)}")
    print(f"bundle_bytes={len(raw)}")
    with zipfile.ZipFile(io.BytesIO(raw), "r") as z:
        names = z.namelist()
        if MANIFEST not in names:
            raise ValueError(f"missing {MANIFEST}")
        for n in names:
            validate_member_name(n)

        manifest_bytes = z.read(MANIFEST)
        if b"\r" in manifest_bytes or not manifest_bytes.endswith(b"\n"):
            raise ValueError("manifest must be UTF-8 LF-terminated")
        text = manifest_bytes.decode("utf-8")
        rows = list(csv.DictReader(text.splitlines(), delimiter="\t"))
        if not rows:
            raise ValueError("empty manifest")

        listed = set()
        for row in rows:
            rel = row["relative_path"]
            if rel == MANIFEST:
                raise ValueError("manifest must not self-hash")
            if rel in listed:
                raise ValueError(f"duplicate manifest path: {rel}")
            listed.add(rel)
            if rel not in names:
                raise ValueError(f"manifest member missing from ZIP: {rel}")
            data = z.read(rel)
            if h(data) != row["sha256"]:
                raise ValueError(f"SHA-256 mismatch: {rel}")
            if len(data) != int(row["bytes"]):
                raise ValueError(f"byte-size mismatch: {rel}")

        extra = set(names) - listed - {MANIFEST}
        if extra:
            raise ValueError(f"unmanifested ZIP members: {sorted(extra)}")

    print("bundle_verification=PASS")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("bundle")
    args = p.parse_args()
    verify(Path(args.bundle))


if __name__ == "__main__":
    main()
