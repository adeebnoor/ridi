"""Post-hoc 512-token sensitivity for the frozen RIDI RAG primary cell.

This script reuses the frozen 800-query prompt bundle and Qwen3-8B revision.
It generates only reference and primary random-replacement conditions because
those two conditions define the H2 contrast. It does not modify the registered
128-token endpoint. Outputs are paired against the archived 128-token primary
cell and include both the registered scorer and a format-tolerant classification
parser sensitivity.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import math
import os
import random
import re
import time
import urllib.request
import zipfile
from pathlib import Path

import requests

SHARE = "l5ppqdrXbxy_"
API = f"https://api.firestorage.ai/dev/file/shares/{SHARE}"
WORK = Path("/tmp/ridi512final")
WORK.mkdir(parents=True, exist_ok=True)
DATASETS = ["nq", "hotpotqa", "fever", "scifact"]
CONDITIONS = ["reference", "random"]
REG_BUNDLE_SHA = "1a3c4909fa9c351826a7b9a861173b8d64df534ae095c96dd15d2d6281eed31b"
WRAPPER = re.compile(
    r"\A\s*(?:[>#*_`]+\s*)*"
    r"(?:(?:verdict|answer|label|classification)\s*:\s*(?:[*_`]+\s*)*)?"
    r"(NOT_ENOUGH_INFO|SUPPORTS|REFUTES)(?![A-Za-z0-9_])",
    re.I,
)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def share_download(substr: str) -> bytes:
    listing = json.load(urllib.request.urlopen(API + "/files?maxResults=1000", timeout=30))
    hits = [x for x in listing["files"] if substr in x["fileName"]]
    if len(hits) != 1:
        raise RuntimeError((substr, hits))
    req = urllib.request.Request(
        API + f"/files/{hits[0]['fileId']}/download", method="POST"
    )
    meta = json.load(urllib.request.urlopen(req, timeout=30))
    return urllib.request.urlopen(meta["downloadUrl"], timeout=120).read()


def percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)


def wrapper_correct(answer: str, gold: dict) -> bool:
    m = WRAPPER.match(answer)
    pred = m.group(1).upper() if m else "UNPARSEABLE"
    accepted = {
        str(x).upper().replace(" ", "_").replace("-", "_")
        for x in gold.get("labels", [])
    }
    return pred in accepted


def main() -> int:
    prompt_zip = share_download("PROMPT_BUNDLE_EXPORT")
    reg_zip = share_download("OSF_COMPACT_REGISTRATION")
    v54 = share_download("v54_SUBMISSION_PACKAGE")
    if sha_bytes(reg_zip) != REG_BUNDLE_SHA:
        raise RuntimeError("registered bundle SHA-256 mismatch")

    with zipfile.ZipFile(io.BytesIO(reg_zip)) as zf:
        zf.extractall(WORK / "reg")
    with zipfile.ZipFile(io.BytesIO(prompt_zip)) as zf:
        prompt_raw = zf.read("RIDI_RAG_512_PROMPTS.jsonl")
        prompt_manifest = json.loads(zf.read("RIDI_RAG_512_PROMPTS.manifest.json"))
    if hashlib.sha256(prompt_raw).hexdigest() != prompt_manifest["prompt_jsonl_sha256"]:
        raise RuntimeError("prompt JSONL SHA-256 mismatch")
    prompt_rows = [json.loads(x) for x in prompt_raw.decode().splitlines() if x.strip()]
    if len(prompt_rows) != 800:
        raise RuntimeError("expected exactly 800 frozen queries")

    outer = zipfile.ZipFile(io.BytesIO(v54))
    primary128 = zipfile.ZipFile(io.BytesIO(outer.read("RIDI_RAG_RESULTS__PRIMARY_H1_H2.zip")))
    rows128 = []
    for dataset in DATASETS:
        name = [
            x
            for x in primary128.namelist()
            if x.endswith(f"{dataset}__bm25__qwen3-8b__k10__primary.jsonl")
        ][0]
        rows128.extend(
            json.loads(x)
            for x in primary128.read(name).decode().splitlines()
            if x.strip()
        )
    map128 = {(r["dataset"], str(r["query_id"])): r for r in rows128}
    if len(map128) != 800:
        raise RuntimeError("archived 128-token primary panel is incomplete")

    import sys

    sys.path.insert(0, str(WORK / "reg" / "code"))
    from backend import HFBackend
    import scoring

    backend = HFBackend(
        prompt_manifest["model_id"],
        prompt_manifest["revision"],
        512,
        prompt_manifest["seed"],
        {"enable_thinking": False},
    )
    env = backend.environment
    print("ENV", json.dumps(env, sort_keys=True), flush=True)
    required = {
        "torch": "2.11.0+cu128",
        "transformers": "4.57.6",
        "huggingface_hub": "0.36.2",
        "accelerate": "1.14.0",
    }
    for key, value in required.items():
        if env.get(key) != value:
            raise RuntimeError(f"runtime mismatch for {key}: {env.get(key)} != {value}")

    raw_path = WORK / "RIDI_RAG_512_PRIMARY_RAW.jsonl"
    rows512 = []
    started = time.time()
    calls = 0
    with raw_path.open("w", encoding="utf-8") as handle:
        for query_index, row in enumerate(prompt_rows, 1):
            answers = {}
            for condition in CONDITIONS:
                answers[condition] = backend.generate(row["prompts"][condition])
                calls += 1
                if calls % 25 == 0:
                    print(
                        "PROGRESS",
                        calls,
                        "/",
                        1600,
                        "queries",
                        query_index,
                        "elapsed_s",
                        round(time.time() - started, 1),
                        flush=True,
                    )
            rec = {
                "dataset": row["dataset"],
                "query_id": str(row["query_id"]),
                "task": row["task"],
                "gold": row["gold"],
                "labels": row.get("labels"),
                "answers": answers,
                "prompt_sha256": {
                    c: hashlib.sha256(row["prompts"][c].encode()).hexdigest()
                    for c in CONDITIONS
                },
                "answer_sha256": {
                    c: hashlib.sha256(answers[c].encode()).hexdigest()
                    for c in CONDITIONS
                },
            }
            rows512.append(rec)
            handle.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()

    map512 = {(r["dataset"], r["query_id"]): r for r in rows512}
    if set(map512) != set(map128):
        raise RuntimeError("128/512 query sets differ")

    def correct128(row: dict, condition: str, method: str) -> bool:
        if method == "registered" or row["task"] == "qa":
            return bool(row["correct__" + condition])
        gold = map512[(row["dataset"], str(row["query_id"]))]["gold"]
        return wrapper_correct(row["answer__" + condition], gold)

    def correct512(row: dict, condition: str, method: str) -> bool:
        if method == "wrapper" and row["task"] == "classification":
            return wrapper_correct(row["answers"][condition], row["gold"])
        return bool(
            scoring.is_correct(
                row["answers"][condition], row["gold"], row["task"], row.get("labels")
            )
        )

    summary = {
        "study": "RIDI-RAG-512-SENSITIVITY-v1",
        "status": "completed",
        "post_hoc": True,
        "n_queries": 800,
        "generation_calls": 1600,
        "conditions": CONDITIONS,
        "source_max_new_tokens": 128,
        "sensitivity_max_new_tokens": 512,
        "model_id": prompt_manifest["model_id"],
        "revision": prompt_manifest["revision"],
        "seed": prompt_manifest["seed"],
        "environment": env,
        "original_128_environment": {
            "python": "3.13.15",
            "torch": "2.11.0+cu128",
            "transformers": "4.57.6",
            "huggingface_hub": "0.36.2",
            "accelerate": "1.14.0",
            "gpu": "NVIDIA A100-SXM4-40GB",
            "tf32": False,
            "do_sample": False,
            "deterministic_algorithms": True,
            "cublas_workspace_config": ":4096:8",
        },
        "runtime_deviations": [
            "Python 3.12.3 vs original 3.13.15",
            "A100-SXM4-80GB vs original A100-SXM4-40GB",
        ],
        "input_hashes": {
            "prompt_bundle": sha_bytes(prompt_zip),
            "registered_bundle": sha_bytes(reg_zip),
            "prompt_jsonl": prompt_manifest["prompt_jsonl_sha256"],
        },
        "datasets": {},
    }
    paired = []
    for dataset in DATASETS:
        keys = [k for k in map512 if k[0] == dataset]
        dsum = {"n": len(keys)}
        for method in ("registered", "wrapper"):
            by_tokens = {}
            for token_budget, source_map, scorer in (
                (128, map128, correct128),
                (512, map512, correct512),
            ):
                flips = ctw = wtc = refc = randc = raw_changes = 0
                for key in keys:
                    row = source_map[key]
                    a = scorer(row, "reference", method)
                    b = scorer(row, "random", method)
                    flips += a != b
                    ctw += a and not b
                    wtc += (not a) and b
                    refc += a
                    randc += b
                    if token_budget == 128:
                        raw_changes += row["answer__reference"] != row["answer__random"]
                    else:
                        raw_changes += row["answers"]["reference"] != row["answers"]["random"]
                by_tokens[str(token_budget)] = {
                    "flips": flips,
                    "rate": flips / len(keys),
                    "correct_to_wrong": ctw,
                    "wrong_to_correct": wtc,
                    "reference_correct": refc,
                    "random_correct": randc,
                    "raw_text_changes": raw_changes,
                }
            both = only128 = only512 = neither = 0
            for key in keys:
                f128 = correct128(map128[key], "reference", method) != correct128(
                    map128[key], "random", method
                )
                f512 = correct512(map512[key], "reference", method) != correct512(
                    map512[key], "random", method
                )
                both += f128 and f512
                only128 += f128 and not f512
                only512 += (not f128) and f512
                neither += (not f128) and (not f512)
                paired.append(
                    {
                        "dataset": dataset,
                        "query_id": key[1],
                        "method": method,
                        "flip128": int(f128),
                        "flip512": int(f512),
                        "ref_correct128": int(correct128(map128[key], "reference", method)),
                        "random_correct128": int(correct128(map128[key], "random", method)),
                        "ref_correct512": int(correct512(map512[key], "reference", method)),
                        "random_correct512": int(correct512(map512[key], "random", method)),
                        "reference_text_same_128_512": int(
                            map128[key]["answer__reference"]
                            == map512[key]["answers"]["reference"]
                        ),
                        "random_text_same_128_512": int(
                            map128[key]["answer__random"]
                            == map512[key]["answers"]["random"]
                        ),
                    }
                )
            discordant = only128 + only512
            if discordant:
                p_value = min(
                    1.0,
                    2
                    * sum(
                        math.comb(discordant, j)
                        for j in range(min(only128, only512) + 1)
                    )
                    / 2**discordant,
                )
            else:
                p_value = 1.0
            dsum[method] = {
                "by_tokens": by_tokens,
                "paired": {
                    "both": both,
                    "only128": only128,
                    "only512": only512,
                    "neither": neither,
                    "discordant": discordant,
                    "exact_two_sided_p": p_value,
                },
            }
        summary["datasets"][dataset] = dsum

    for method in ("registered", "wrapper"):
        summary[method] = {}
        for token_budget in ("128", "512"):
            rates = [
                summary["datasets"][d][method]["by_tokens"][token_budget]["rate"]
                for d in DATASETS
            ]
            summary[method][token_budget] = {
                "macro_rate": sum(rates) / 4,
                "pooled_flips": sum(
                    summary["datasets"][d][method]["by_tokens"][token_budget]["flips"]
                    for d in DATASETS
                ),
                "dataset_rates": dict(zip(DATASETS, rates)),
            }
        summary[method]["macro_difference_512_minus_128"] = (
            summary[method]["512"]["macro_rate"]
            - summary[method]["128"]["macro_rate"]
        )
        rng = random.Random(20260902)
        boot128, boot512, differences = [], [], []
        groups = []
        for dataset in DATASETS:
            keys = [k for k in map512 if k[0] == dataset]
            groups.append(
                [
                    (
                        int(
                            correct128(map128[k], "reference", method)
                            != correct128(map128[k], "random", method)
                        ),
                        int(
                            correct512(map512[k], "reference", method)
                            != correct512(map512[k], "random", method)
                        ),
                    )
                    for k in keys
                ]
            )
        for _ in range(100000):
            m128 = m512 = 0.0
            for group in groups:
                a = b = 0
                for __ in range(len(group)):
                    u, v = group[rng.randrange(len(group))]
                    a += u
                    b += v
                m128 += a / len(group) / 4
                m512 += b / len(group) / 4
            boot128.append(m128)
            boot512.append(m512)
            differences.append(m512 - m128)
        summary[method]["bootstrap"] = {
            "draws": 100000,
            "seed": 20260902,
            "macro128_ci95": [percentile(boot128, 0.025), percentile(boot128, 0.975)],
            "macro512_ci95": [percentile(boot512, 0.025), percentile(boot512, 0.975)],
            "difference_ci95": [
                percentile(differences, 0.025),
                percentile(differences, 0.975),
            ],
        }

    summary["cross_budget_exact_text"] = {
        "reference": sum(
            map128[k]["answer__reference"] == map512[k]["answers"]["reference"]
            for k in map128
        ),
        "random": sum(
            map128[k]["answer__random"] == map512[k]["answers"]["random"]
            for k in map128
        ),
        "n": 800,
    }
    summary["named_queries"] = {}
    for qid in ("185", "275"):
        key = ("scifact", qid)
        summary["named_queries"][qid] = {
            "registered_flip128": int(
                correct128(map128[key], "reference", "registered")
                != correct128(map128[key], "random", "registered")
            ),
            "registered_flip512": int(
                correct512(map512[key], "reference", "registered")
                != correct512(map512[key], "random", "registered")
            ),
            "wrapper_flip512": int(
                correct512(map512[key], "reference", "wrapper")
                != correct512(map512[key], "random", "wrapper")
            ),
            "reference_512": map512[key]["answers"]["reference"],
            "random_512": map512[key]["answers"]["random"],
        }

    summary["raw_outputs_sha256"] = sha_file(raw_path)
    summary["elapsed_generation_seconds"] = time.time() - started
    summary_path = WORK / "RIDI_RAG_512_FINAL_ANALYSIS.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    paired_path = WORK / "RIDI_RAG_512_QUERY_PAIRED.csv"
    with paired_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(paired[0]))
        writer.writeheader()
        writer.writerows(paired)
    meta_path = WORK / "RIDI_RAG_512_EXECUTION_METADATA.json"
    meta_path.write_text(
        json.dumps(
            {
                "hf_job_id": os.environ.get("JOB_ID"),
                "environment": env,
                "raw_outputs_sha256": sha_file(raw_path),
                "analysis_sha256": sha_file(summary_path),
                "paired_csv_sha256": sha_file(paired_path),
                "prompt_bundle_sha256": sha_bytes(prompt_zip),
                "registered_bundle_sha256": sha_bytes(reg_zip),
                "v54_package_sha256": sha_bytes(v54),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    output_zip = WORK / "RIDI_RAG_512_FINAL_RESULTS.zip"
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in (raw_path, summary_path, paired_path, meta_path):
            zf.write(path, path.name)
    print("FINAL_SUMMARY_JSON", json.dumps(summary, sort_keys=True), flush=True)
    print("FINAL_ZIP_SHA256", sha_file(output_zip), "BYTES", output_zip.stat().st_size, flush=True)
    with output_zip.open("rb") as handle:
        response = requests.post(
            "https://tmpfiles.org/api/v1/upload",
            files={"file": (output_zip.name, handle, "application/zip")},
            timeout=180,
        )
    response.raise_for_status()
    print(
        "FINAL_DOWNLOAD_URL",
        response.json()["data"]["url"].replace(
            "https://tmpfiles.org/", "https://tmpfiles.org/dl/"
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
