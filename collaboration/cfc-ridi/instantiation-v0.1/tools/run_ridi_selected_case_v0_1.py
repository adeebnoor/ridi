#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

EXPECTED_INPUT_SHA256 = "0f92f41721a452c7045c4c384d4345ba7335fc5ee724150c880ca2174edf75e0"
EXPECTED = {
    "source_A.jsonl": "60e19ea94ff13ded74e6ca19d6063909d374951f86218a9e3e68833b46126734",
    "source_B.jsonl": "018f1de8876594e57a383b69a1fcd605e811cf062695cc2ab947c737a697e308",
    "endpoint_A.jsonl": "e03c1c6433cd197f780537a90d1541744b314cf8eb196ca426f7dc4a41779c67",
    "endpoint_B.jsonl": "e66408834f040464bb8146e4ed814a26f15bb871519db4194c7a764b4e8580c5",
}

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def exact_jsonl(path: Path, expected_sha: str) -> dict:
    b = path.read_bytes()
    if not b.endswith(b"\n") or b"\r" in b:
        raise SystemExit(f"{path}: exact JSONL record must be LF-terminated and contain no CR")
    got = sha256_bytes(b)
    if got != expected_sha:
        raise SystemExit(f"{path}: SHA-256 mismatch: got {got}, expected {expected_sha}")
    return json.loads(b)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--neutral-dir", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    input_bytes = args.input.read_bytes()
    if sha256_bytes(input_bytes) != EXPECTED_INPUT_SHA256:
        raise SystemExit("RIDI input SHA-256 mismatch")
    inp = json.loads(input_bytes)

    rec = {}
    for name, digest in EXPECTED.items():
        rec[name] = exact_jsonl(args.neutral_dir / name, digest)

    a_s, b_s = rec["source_A.jsonl"], rec["source_B.jsonl"]
    a_e, b_e = rec["endpoint_A.jsonl"], rec["endpoint_B.jsonl"]

    required_equal = [
        ("case_id", a_s["case_id"], b_s["case_id"]),
        ("dataset", a_s["dataset"], b_s["dataset"]),
        ("qid", a_s["qid"], b_s["qid"]),
        ("task", a_s["task"], b_s["task"]),
        ("relevance_grade_vector", a_s["relevance_grade_vector"], b_s["relevance_grade_vector"]),
    ]
    failed = [name for name, x, y in required_equal if x != y]

    canonical_a = a_e.get("canonical")
    canonical_b = b_e.get("canonical")
    if failed or canonical_a is None or canonical_b is None:
        primary = "NOT_EVALUABLE"
    else:
        primary = "PASS" if canonical_a == canonical_b else "FAIL"

    docids_a = [x["docid"] for x in a_s["passages"]]
    docids_b = [x["docid"] for x in b_s["passages"]]
    changed_positions = [i + 1 for i, (x, y) in enumerate(zip(docids_a, docids_b)) if x != y]

    out = {
        "schema": "CFC-RIDI-RIDI-OUTPUT-v0.1",
        "case_id": inp["case_id"],
        "input_sha256": EXPECTED_INPUT_SHA256,
        "entry_condition": {
            "required_equal_fields": [x[0] for x in required_equal],
            "failed_fields": failed,
            "status": "APPLICABLE" if not failed and canonical_a is not None and canonical_b is not None else "NOT_EVALUABLE"
        },
        "primary": {
            "endpoint": inp["evaluation_definition"]["primary_endpoint"],
            "comparison_function": inp["evaluation_definition"]["comparison_function"],
            "canonical_A": canonical_a,
            "canonical_B": canonical_b,
            "result": primary
        },
        "secondary": {
            "ordered_context_identity_equal": docids_a == docids_b,
            "membership_identity_equal": set(docids_a) == set(docids_b),
            "changed_rank_positions": changed_positions,
            "changed_rank_count": len(changed_positions)
        },
        "ground_truth_correctness": "WITHHELD_POST_RAW_BUNDLE_COMMITMENT",
        "interpretation": "WITHHELD_UNTIL_BILATERAL_RAW_BUNDLE_VERIFICATION"
    }

    out_bytes = (json.dumps(out, sort_keys=True, indent=2) + "\n").encode("utf-8")
    args.output.write_bytes(out_bytes)
    print(f"input_sha256={EXPECTED_INPUT_SHA256}")
    print(f"output_sha256={sha256_bytes(out_bytes)}")
    print(f"primary_result={primary}")

if __name__ == "__main__":
    main()
