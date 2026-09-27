#!/usr/bin/env python3
"""CFC-RIDI v0.1 pool and commit-reveal utilities.

Preparatory tool only. This file does not create seeds, freeze a pool, or select
a substantive case unless the user explicitly supplies a frozen eligible pool
and both already-revealed seeds.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
from pathlib import Path

ASCII_ID = re.compile(r"^[\x21-\x7E]+$")
SEED = re.compile(r"^[0-9a-f]{64}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")

POOL_COLUMNS = [
    "case_id",
    "pair_fingerprint",
    "source_a_sha256",
    "offline_endpoint_a_sha256",
    "source_ref_a",
    "source_b_sha256",
    "offline_endpoint_b_sha256",
    "source_ref_b",
    "evaluation_definition_id",
    "evaluation_definition_sha256",
    "original_support_requirement_status",
    "prior_public_exposure",
    "eligibility_rationale",
]

ELIGIBLE_SUPPORT_STATUS = {
    "AUTHORITATIVE_1",
    "NO_AUTHORITATIVE_REQUIREMENT_SPECIFIED",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_exact_pool(path: Path) -> bytes:
    data = path.read_bytes()
    if b"\r" in data:
        raise ValueError("pool must use LF only; CR byte found")
    if not data.endswith(b"\n"):
        raise ValueError("pool must be LF-terminated")
    data.decode("utf-8")
    return data


def arm_binding(source_sha: str, endpoint_sha: str) -> str:
    return sha256_bytes(
        f"CFC-RIDI-ARM-v0.1|{source_sha}|{endpoint_sha}".encode("utf-8")
    )


def expected_pair_fingerprint(row: dict[str, str]) -> str:
    a = arm_binding(row["source_a_sha256"], row["offline_endpoint_a_sha256"])
    b = arm_binding(row["source_b_sha256"], row["offline_endpoint_b_sha256"])
    lo, hi = sorted((a, b))
    return sha256_bytes(f"CFC-RIDI-PAIR-v0.1|{lo}|{hi}".encode("utf-8"))


def validate_pool_rows(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        raise ValueError("eligible pool contains no candidates")

    ids: list[str] = []
    fps: list[str] = []
    for n, row in enumerate(rows, start=2):
        cid = row["case_id"]
        if not cid or not ASCII_ID.fullmatch(cid):
            raise ValueError(f"line {n}: case_id must be non-empty printable ASCII")
        ids.append(cid)

        for field in (
            "pair_fingerprint",
            "source_a_sha256",
            "offline_endpoint_a_sha256",
            "source_b_sha256",
            "offline_endpoint_b_sha256",
            "evaluation_definition_sha256",
        ):
            if not HEX64.fullmatch(row[field]):
                raise ValueError(f"line {n}: {field} must be 64 lowercase hex characters")

        expected = expected_pair_fingerprint(row)
        if row["pair_fingerprint"] != expected:
            raise ValueError(f"line {n}: pair_fingerprint mismatch")
        fps.append(row["pair_fingerprint"])

        for field in (
            "source_ref_a",
            "source_ref_b",
            "evaluation_definition_id",
            "eligibility_rationale",
        ):
            if not row[field].strip():
                raise ValueError(f"line {n}: {field} must be non-empty")

        if row["original_support_requirement_status"] not in ELIGIBLE_SUPPORT_STATUS:
            raise ValueError(f"line {n}: ineligible original support requirement status")

        if row["prior_public_exposure"] not in {"TRUE", "FALSE", "UNKNOWN"}:
            raise ValueError(
                f"line {n}: prior_public_exposure must be TRUE, FALSE or UNKNOWN"
            )

    if len(ids) != len(set(ids)):
        raise ValueError("duplicate case_id")
    if len(fps) != len(set(fps)):
        raise ValueError("duplicate pair_fingerprint")
    if ids != sorted(ids):
        raise ValueError("eligible_pool.tsv must be sorted lexicographically by case_id")
    return ids


def parse_pool(path: Path) -> tuple[list[str], str]:
    data = read_exact_pool(path)
    reader = csv.DictReader(data.decode("utf-8").splitlines(), delimiter="\t")
    if reader.fieldnames != POOL_COLUMNS:
        raise ValueError("pool header does not match required columns/order")
    rows = list(reader)
    ids = validate_pool_rows(rows)
    return ids, sha256_bytes(data)


def seed_commitment(participant: str, seed_hex: str) -> str:
    if participant not in {"ADEEB", "KRZYSZTOF"}:
        raise ValueError("participant must be ADEEB or KRZYSZTOF")
    if not SEED.fullmatch(seed_hex):
        raise ValueError("seed must be exactly 64 lowercase hex characters")
    msg = f"CFC-RIDI-SEED-v0.1|{participant}|{seed_hex}".encode("utf-8")
    return sha256_bytes(msg)


def combined_hash(seed_adeeb: str, seed_krzysztof: str, pool_sha256_hex: str) -> str:
    if not SEED.fullmatch(seed_adeeb) or not SEED.fullmatch(seed_krzysztof):
        raise ValueError("both seeds must be exactly 64 lowercase hex characters")
    if not HEX64.fullmatch(pool_sha256_hex):
        raise ValueError("pool SHA-256 must be 64 lowercase hex characters")
    msg = (
        "CFC-RIDI-SELECT-v0.1|"
        + seed_adeeb
        + "|"
        + seed_krzysztof
        + "|"
        + pool_sha256_hex
    ).encode("utf-8")
    return sha256_bytes(msg)


def score_case(combined_hex: str, case_id: str) -> str:
    if not HEX64.fullmatch(combined_hex):
        raise ValueError("combined hash must be 64 lowercase hex characters")
    if not case_id or not ASCII_ID.fullmatch(case_id):
        raise ValueError("case_id must be printable ASCII")
    msg = f"CFC-RIDI-CASE-v0.1|{combined_hex}|{case_id}".encode("utf-8")
    return sha256_bytes(msg)


def select_case(ids: list[str], combined_hex: str) -> tuple[str, list[tuple[str, str]]]:
    scores = [(case_id, score_case(combined_hex, case_id)) for case_id in ids]
    scores.sort(key=lambda x: (x[1], x[0]))
    return scores[0][0], scores


def cmd_pool(args: argparse.Namespace) -> None:
    ids, pool_hash = parse_pool(Path(args.pool))
    print(f"pool_sha256={pool_hash}")
    print(f"candidate_count={len(ids)}")


def cmd_commit(args: argparse.Namespace) -> None:
    print(seed_commitment(args.participant, args.seed))


def cmd_select(args: argparse.Namespace) -> None:
    ids, pool_hash = parse_pool(Path(args.pool))
    if args.expected_pool_sha256 and pool_hash != args.expected_pool_sha256:
        raise SystemExit("pool hash mismatch")
    if args.commit_adeeb and seed_commitment("ADEEB", args.seed_adeeb) != args.commit_adeeb:
        raise SystemExit("ADEEB seed commitment mismatch")
    if args.commit_krzysztof and seed_commitment("KRZYSZTOF", args.seed_krzysztof) != args.commit_krzysztof:
        raise SystemExit("KRZYSZTOF seed commitment mismatch")
    combined = combined_hash(args.seed_adeeb, args.seed_krzysztof, pool_hash)
    chosen, scores = select_case(ids, combined)
    print(f"pool_sha256={pool_hash}")
    print(f"combined_sha256={combined}")
    for cid, score in scores:
        print(f"score\t{cid}\t{score}")
    print(f"selected_case_id={chosen}")


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("pool-hash")
    q.add_argument("pool")
    q.set_defaults(func=cmd_pool)

    q = sub.add_parser("commit")
    q.add_argument("participant", choices=["ADEEB", "KRZYSZTOF"])
    q.add_argument("seed")
    q.set_defaults(func=cmd_commit)

    q = sub.add_parser("select")
    q.add_argument("pool")
    q.add_argument("--seed-adeeb", required=True)
    q.add_argument("--seed-krzysztof", required=True)
    q.add_argument("--expected-pool-sha256")
    q.add_argument("--commit-adeeb")
    q.add_argument("--commit-krzysztof")
    q.set_defaults(func=cmd_select)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
