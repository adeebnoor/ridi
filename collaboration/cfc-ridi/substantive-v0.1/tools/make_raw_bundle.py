#!/usr/bin/env python3
"""Create a deterministic immutable CFC-RIDI raw ZIP bundle.

The source directory must contain the complete raw bundle contents except
SHA256_MANIFEST.tsv. ZIP members are sorted and stored without compression with
a fixed DOS timestamp so identical inputs produce identical bytes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import zipfile
from pathlib import Path, PurePosixPath

MANIFEST = "SHA256_MANIFEST.tsv"
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_relative(root: Path, p: Path) -> str:
    rel = p.relative_to(root).as_posix()
    q = PurePosixPath(rel)
    if q.is_absolute() or ".." in q.parts:
        raise ValueError(f"unsafe path: {rel}")
    return rel


def collect(root: Path) -> list[tuple[str, bytes]]:
    out = []
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        rel = safe_relative(root, p)
        if rel == MANIFEST:
            raise ValueError(f"source directory must not contain {MANIFEST}")
        out.append((rel, p.read_bytes()))
    if not out:
        raise ValueError("source directory contains no files")
    return out


def build_manifest(items: list[tuple[str, bytes]]) -> bytes:
    buf = io.StringIO(newline="")
    w = csv.writer(buf, delimiter="\t", lineterminator="\n")
    w.writerow(["relative_path", "sha256", "bytes", "role"])
    for rel, data in items:
        w.writerow([rel, h(data), len(data), "RAW"])
    return buf.getvalue().encode("utf-8")


def make_zip(source: Path, output: Path) -> None:
    items = collect(source)
    manifest = build_manifest(items)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as z:
        for rel, data in items + [(MANIFEST, manifest)]:
            info = zipfile.ZipInfo(rel, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    raw = output.read_bytes()
    print(f"bundle_sha256={h(raw)}")
    print(f"bundle_bytes={len(raw)}")
    print(f"member_count={len(items)+1}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("source_dir")
    p.add_argument("output_zip")
    args = p.parse_args()
    make_zip(Path(args.source_dir), Path(args.output_zip))


if __name__ == "__main__":
    main()
