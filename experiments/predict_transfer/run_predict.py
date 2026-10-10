#!/usr/bin/env python3
"""RIDI-PREDICT-v1: one model x benchmark x exchange draw per call.
Derived from frozen scale-curve runner 869abda18a17ba528ecfcddcb4461914b8b113c1.
Fresh input panel, independent draws, input-only G; generation and scoring
preserve the parent behavior. Correctness is never printed to logs.
"""
from __future__ import annotations
import argparse, hashlib, io, json, os, random, re, shutil, signal, sys, tempfile, time, urllib.request, zipfile, unicodedata
from datetime import datetime, timezone
from pathlib import Path

STUDY = "RIDI-PREDICT-v1"
SEED = 20260902
REGISTERED_BUNDLE_SHA = "1a3c4909fa9c351826a7b9a861173b8d64df534ae095c96dd15d2d6281eed31b"
FROZEN_MANIFEST_SHA = "0dd99d3737b9fe4d92ce2228d4227e42d3b15b52b9f204be11dc5b53d03d2885"
CONTROL_SHA = "4b5bc603fcbd5165766beabc05d17ec7e0cefa6e0d8c9c47fd65b06eca61c864"
DATA_SHA = {
    "nq": "5b1e813b5e486f9c588c0a73a3d04a1402f4959d991a1c1631fa007f8559bc13",
    "hotpotqa": "783f1f41db0f22e9ca59ce8ddb9520d06105dd7a817746d8032295cd57025bfb",
    "fever": "b2cc0868918569047ba7b44f193e26a759a4e268d964cf8f20141c7d15eecd63",
    "scifact": "fcc9483c65b06df889c34267a358c79bc7720d507f2d03c0419a8d1d772be5dc",
}
PROMPT_DATASET_SHA = {'fever': '80693d571ec113db8195d73cc638a548e56e3b32c40340b646dc895e64189a7f', 'hotpotqa': 'b9857ee12397a760565444d6a4ed8e28f37a3a5d7cf438a48cc59adf81cae3a4', 'nq': '4136b752292816212a3d56ee5758f0c6dc1e7eed03aa2589239345c258c8ab51', 'scifact': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}
EXPECTED_N = {"nq": 250, "hotpotqa": 250, "fever": 300}
EXCHANGE_SEEDS = {"A": 20260902, "B": 20261016}
KNOWN_FILTER_SHA = "bc2aecee5a27fc33b75e5caf5c000764ee1c88598533075ace19884a8c613df8"
BATCH = 16
MAX_NEW = 128
DET_CHECK_N = 16
FIRE_API = "https://api.firestorage.ai/dev/file/shares"
HERE = Path(__file__).resolve().parent
LOCK_FILES = {"models.json", "run_predict.py", "FRESH_PANEL.json", "analyze_predict.py",
              "predict_config.json", "annotation/CODING_MANUAL_EN_AR.md", "annotation/coder_sheet.csv",
              "known_source_filter.json", "make_lock.py"}
SEALED_KEY_SHA = "75b0833b4eb35134646cf28443c5ad0031cc24364f23b0da512b14e2ce8e4d89"
# Usable memory reported for an 80-GB-class device can be lower than its nominal size.
MIN_GPU_MEMORY_BYTES = 75 * (1 << 30)


class ProtocolError(RuntimeError):
    """An integrity/configuration error is not a retryable infrastructure failure."""


class InfrastructureInterrupted(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ProtocolError(message)


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def atomic_json(path, value):
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write("\n"); f.flush(); os.fsync(f.fileno())
    os.replace(temporary, path)


def configuration_sha256(lock, model, dataset, draw):
    config = {"study": STUDY, "lock": lock["files"], "model": model, "dataset": dataset,
              "draw": draw, "exchange_seed": EXCHANGE_SEEDS[draw],
              "source_sha256": {"control": CONTROL_SHA, "data": DATA_SHA[dataset]},
              "generation": {"seed": SEED, "max_new_tokens": MAX_NEW, "batch": BATCH,
                             "dtype": "bfloat16", "greedy": True, "thinking": False}}
    return sha_bytes(json.dumps(config, sort_keys=True, separators=(",", ":")).encode())


def begin_attempt(outroot, model_key, dataset, attempt, config_sha):
    require(1 <= attempt <= 3, "attempt must be 1-3")
    base = outroot / model_key / dataset
    base.mkdir(parents=True, exist_ok=True)
    existing = sorted(base.glob("attempt*"))
    require({p.name for p in existing} == {f"attempt{i}" for i in range(1, attempt)},
            "attempts are immutable and must be sequential; an existing attempt cannot be reused")
    for i in range(1, attempt):
        previous = base / f"attempt{i}" / "attempt_status.json"
        require(previous.is_file(), "preceding attempt has no recorded terminal status")
        status = json.loads(previous.read_text())
        require(status.get("study") == STUDY and status.get("model_key") == model_key
                and status.get("dataset") == dataset and status.get("attempt") == i,
                "preceding attempt identity mismatch")
        require(status.get("status") == "failed" and status.get("failure_kind") == "technical",
                "retry requires a recorded technical failure; success/running/blocked cannot be retried")
        require(status.get("configuration_sha256") == config_sha,
                "retry configuration differs from the preceding attempt")
    out = base / f"attempt{attempt}"
    out.mkdir(exist_ok=False)
    now = utc_now()
    status = {"study": STUDY, "model_key": model_key, "dataset": dataset, "attempt": attempt,
              "configuration_sha256": config_sha, "status": "running",
              "started_at_utc": now, "updated_at_utc": now}
    atomic_json(out / "attempt_status.json", status)
    return out, status


def technical_failure(error):
    if isinstance(error, ProtocolError):
        return False
    if isinstance(error, (OSError, TimeoutError, MemoryError, KeyboardInterrupt, InfrastructureInterrupted)):
        return True
    # PyTorch CUDA OOM/errors may be RuntimeError without importing torch during preflight/tests.
    return isinstance(error, RuntimeError) and bool(re.search(
        r"CUDA out of memory|CUDA error:|CUBLAS_STATUS_|CUDNN_STATUS_", str(error), re.I))


def finish_failure(out, status, error):
    technical = technical_failure(error)
    status.update(status="failed" if technical else "blocked",
                  failure_kind="technical" if technical else "protocol_or_code",
                  error_type=type(error).__name__, updated_at_utc=utc_now())
    # Do not expose exception payloads: some libraries include model inputs/outputs in them.
    atomic_json(out / "attempt_status.json", status)


def persist_answer(out, query_id, condition, answer):
    # Every completed answer survives a later crash. Failed attempts are never analysed.
    with (out / "partial_answers.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"query_id": query_id, "condition": condition, "answer": answer},
                           ensure_ascii=False, sort_keys=True) + "\n")
        f.flush(); os.fsync(f.fileno())


def verify_gpu_memory(memory_bytes, minimum_count):
    require(len(memory_bytes) >= minimum_count, f"at least {minimum_count} CUDA GPUs required")
    require(all(n >= MIN_GPU_MEMORY_BYTES for n in memory_bytes),
            "all visible CUDA GPUs must be 80-GB-class devices")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for x in iter(lambda: f.read(1 << 20), b""):
            h.update(x)
    return h.hexdigest()


def verify_lock() -> dict:
    lp = HERE / "LOCK.json"
    if not lp.exists():
        raise SystemExit("LOCK.json missing: run make_lock.py and commit it publicly before any generation")
    lock = json.loads(lp.read_text())
    require(lock.get("study") == STUDY, "LOCK.json study mismatch")
    require(isinstance(lock.get("files"), dict) and set(lock["files"]) == LOCK_FILES,
            "LOCK.json file set mismatch")
    require(all(isinstance(h, str) and re.fullmatch(r"[0-9a-f]{64}", h)
                for h in lock["files"].values()), "invalid LOCK.json SHA-256")
    bad = [f for f, h in lock["files"].items() if sha_file(HERE / f) != h]
    if bad:
        raise SystemExit(f"files differ from LOCK.json: {bad}")
    require(lock.get("sealed_key_sha256") == SEALED_KEY_SHA, "sealed key hash mismatch")
    return lock


def safe_extract(z, dest):
    dest = dest.resolve()
    for info in z.infolist():
        require((dest / info.filename).resolve().is_relative_to(dest), "unsafe ZIP member")
        require(((info.external_attr >> 16) & 0o170000) != 0o120000, "ZIP symlink prohibited")
    z.extractall(dest)


def normalized_question_sha(text):
    return sha_bytes(" ".join(unicodedata.normalize("NFKC", text).casefold().split()).encode())


def validate_tokenizer(tok, metadata, prepared, draw, model_key):
    probe = tok.apply_chat_template([{"role": "user", "content": metadata["template_probe_text"]}],
        tokenize=False, add_generation_prompt=True, enable_thinking=False)
    require(sha_bytes(probe.encode()) == metadata["rendered_template_sha256"], "chat template changed")
    for _, row, prompts in prepared:
        for cond, prompt in prompts.items():
            rendered = tok.apply_chat_template([{"role":"user", "content":prompt}], tokenize=False,
                add_generation_prompt=True, enable_thinking=False)
            length = len(tok(rendered, truncation=False)["input_ids"])
            name = "reference" if cond == "reference" else "draw" + draw
            require(length == row["token_lengths"][model_key][name], "preflight token length changed")
            require(length + MAX_NEW <= metadata["max_position_embeddings"], "context length gate failed")


def verify_publication_receipt(lock):
    p = HERE / "PUBLICATION_RECEIPT.json"
    require(p.is_file(), "registration and public lock publication receipt required before generation")
    r = json.loads(p.read_text())
    require(r.get("study") == STUDY and r.get("public_lock_verified") is True,
            "public scientific lock has not been verified")
    require(r.get("lock_sha256") == sha_file(HERE / "LOCK.json"), "published lock hash mismatch")
    require(r.get("registration_url") == lock["registration_receipt"]["registration_url"],
            "registration receipt mismatch")
    require(bool(re.fullmatch(r"[0-9a-f]{40}", r.get("github_commit", ""))), "publication commit missing")


def fire_bytes(slug: str, expected_name: str | None = None) -> bytes:
    u = f"{FIRE_API}/{slug}"
    req = urllib.request.Request(u + "/files?maxResults=1000", headers={"User-Agent": "RIDI-scale-curve/1.0"})
    files = json.load(urllib.request.urlopen(req, timeout=60)).get("files", [])
    if expected_name is not None:
        files = [x for x in files if x.get("fileName") == expected_name]
    if len(files) != 1:
        raise RuntimeError(f"share {slug}: expected one file {expected_name!r}")
    req = urllib.request.Request(u + f"/files/{files[0]['fileId']}/download", data=b"", method="POST",
                                 headers={"User-Agent": "RIDI-scale-curve/1.0"})
    meta = json.load(urllib.request.urlopen(req, timeout=60))
    return urllib.request.urlopen(meta["downloadUrl"], timeout=600).read()


def load_source(local: list[str] | None, shares: list[str] | None, name: str | None) -> bytes:
    if local:
        return b"".join(Path(p).read_bytes() for p in local)
    if shares:
        return b"".join(fire_bytes(s, name) for s in shares)
    raise SystemExit(f"no source given for {name}")


def model_entry(key: str) -> dict:
    M = json.loads((HERE / "models.json").read_text())
    require(M.get("study") == STUDY, "model manifest study mismatch")
    for m in M["models"]:
        if m["key"] == key:
            return m
    raise SystemExit(f"unknown model key {key}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-key", required=True)
    ap.add_argument("--draw", choices=["A", "B"], required=True)
    ap.add_argument("--tokenizer-dir", type=Path, help="preflight-only local tokenizer root")
    ap.add_argument("--dataset", choices=list(EXPECTED_N), required=True)
    ap.add_argument("--attempt", type=int, default=1, help="attempt number (max 3, see protocol section 7)")
    ap.add_argument("--control-zip", action="append"); ap.add_argument("--control-share", action="append")
    ap.add_argument("--data-zip", action="append", help="dataset archive (or its chunks in locked order)")
    ap.add_argument("--data-share", action="append")
    ap.add_argument("--out", type=Path, default=Path("ridi_predict_out"))
    ap.add_argument("--preflight-only", action="store_true",
                    help="verify selected fresh inputs and tokenizers before locking; no weights or attempt is created")
    a = ap.parse_args()
    m = model_entry(a.model_key)
    require(m["role"] == "predictor" or a.draw == "A", "targets run draw A only")
    require(a.tokenizer_dir is None or a.preflight_only, "local tokenizer override allowed only for preflight")
    if a.preflight_only:
        execute_job(a, None, m, None, None)
        return
    if not 1 <= a.attempt <= 3:
        raise SystemExit("attempt must be 1-3")
    lock = verify_lock()
    verify_publication_receipt(lock)
    if not re.fullmatch(r"[0-9a-f]{40}", m["revision"]):
        raise SystemExit("model revision not resolved/locked")
    config_sha = configuration_sha256(lock, m, a.dataset, a.draw)
    out, status = begin_attempt(a.out / ("draw" + a.draw), a.model_key, a.dataset, a.attempt, config_sha)
    status["draw"] = a.draw
    atomic_json(out / "attempt_status.json", status)

    def interrupted(signum, frame):
        raise InfrastructureInterrupted(f"received signal {signum}")

    old_term = signal.signal(signal.SIGTERM, interrupted)
    try:
        execute_job(a, lock, m, out, status)
        status.update(status="succeeded", updated_at_utc=utc_now())
        atomic_json(out / "attempt_status.json", status)
        print("DONE", a.model_key, a.dataset, "attempt", a.attempt, flush=True)
    except BaseException as error:
        finish_failure(out, status, error)
        print("ATTEMPT_STATUS", status["status"], status["error_type"], flush=True)
        raise SystemExit(1) from None
    finally:
        signal.signal(signal.SIGTERM, old_term)


def execute_job(a, lock, m, out, status):
    dname = a.dataset
    if lock is not None:
        print("LOCK_VERIFIED", json.dumps(lock["files"], sort_keys=True), flush=True)

    control = load_source(a.control_zip, a.control_share, "RIDI_RAG_NATURE_CONTROL_POSTREG_20260902.zip")
    data_zip = load_source(a.data_zip, a.data_share, None)
    require(sha_bytes(control) == CONTROL_SHA, "control archive hash mismatch")
    require(sha_bytes(data_zip) == DATA_SHA[dname], "dataset archive hash mismatch")
    print("SOURCE_ZIPS_VERIFIED", dname, flush=True)

    with tempfile.TemporaryDirectory(prefix=f"ridi_scale_{dname}_") as td:
        td = Path(td); stage = td / "stage"; root = td / "root"; stage.mkdir(); root.mkdir()
        with zipfile.ZipFile(io.BytesIO(control)) as z:
            safe_extract(z, stage)
        reg = stage / "RIDI_RAG_NATURE_OSF_COMPACT_REGISTRATION_V2_20260902.zip"
        receipts = stage / "RIDI_RAG_POST_REGISTRATION_RECEIPTS_20260902.zip"
        require(sha_file(reg) == REGISTERED_BUNDLE_SHA, "registered bundle hash mismatch")
        with zipfile.ZipFile(reg) as z:
            safe_extract(z, root)
        with zipfile.ZipFile(receipts) as z:
            safe_extract(z, root)
        with zipfile.ZipFile(io.BytesIO(data_zip)) as z:
            safe_extract(z, root)
        shutil.copy2(reg, root / "protocol" / "REGISTRATION_BUNDLE.zip")
        require(sha_file(root / "protocol" / "FROZEN_MANIFEST.json") == FROZEN_MANIFEST_SHA,
                "frozen manifest hash mismatch")
        manifest = json.loads((root / "protocol" / "FROZEN_MANIFEST.json").read_text())
        amap = manifest["artifact_sha256"]
        bad = [rel for rel, exp in amap.items() if (root / rel).exists() and sha_file(root / rel) != exp]
        if bad:
            raise ProtocolError(f"registered artifact hash mismatch: {bad[:10]}")
        required = [x for x in amap if (not x.startswith(("data/beir/", "runs/", "data/gold/"))
                                        or x.startswith(f"data/beir/{dname}/") or x.startswith(f"runs/{dname}/")
                                        or x == f"data/gold/{dname}.jsonl")]
        missing = [x for x in required if not (root / x).exists()]
        if missing:
            raise ProtocolError(f"missing frozen artifacts: {missing[:10]}")
        print("REGISTERED_ARTIFACTS_VERIFIED", dname, len(required), flush=True)

        sys.path.insert(0, str(root / "code"))
        from equivalence import build_equivalent
        from io_utils import load_beir, load_gold, load_run, sha256_text
        from panels import select_universal_panel
        from prompts import get_prompt
        from scoring import canonical_answer, is_correct, normalize_qa
        from study import by_id

        c = manifest["resolved_config"]
        require(c["study_id"] == "RIDI-RAG-NATURE-v2-PROSPECTIVE", "registered study mismatch")
        require(c["max_new_tokens"] == MAX_NEW and c["seed"] == SEED and c["passage_chars"] == 1200,
                "registered generation configuration mismatch")
        require(c["primary_retriever"] == "bm25" and c["primary_k"] == 10 and c["primary_variant"] == "random",
                "registered retrieval configuration mismatch")
        ds = by_id(c["datasets"], dname)
        corpus, queries, qrels, _ = load_beir(root / ds["data_dir"])
        gold = load_gold(root / ds["gold_file"])
        all_runs = {rid: load_run(root / rp, "trec") for rid, rp in ds["runs"].items()}
        fresh = json.loads((HERE / "FRESH_PANEL.json").read_text())
        require(fresh.get("study") == STUDY, "fresh panel study mismatch")
        selected = fresh["datasets"][dname]
        require(len(selected) == EXPECTED_N[dname], "fresh panel length mismatch")
        pm_bytes = "".join(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n" for r in selected).encode()
        require(sha_bytes(pm_bytes) == fresh["prompt_manifest_sha256"][dname]
                == PROMPT_DATASET_SHA[dname], "fresh prompt manifest mismatch")
        frozen = set(select_universal_panel(all_runs, queries, qrels, c["panel_ks"], c["pool_depth"], ds["panel_n"]))
        eligible = set(select_universal_panel(all_runs, queries, qrels, c["panel_ks"], c["pool_depth"], len(queries)))
        fp = HERE / "known_source_filter.json"
        require(sha_file(fp) == KNOWN_FILTER_SHA, "known-source filter hash mismatch")
        known = {x["question_sha256"] for x in json.loads(fp.read_text())["queries"]}
        require(len(known) == 7280, "known-source count mismatch")
        require(len({r["question_sha256"] for rows in fresh["datasets"].values() for r in rows})
                == sum(len(rows) for rows in fresh["datasets"].values()), "duplicate fresh question")
        panel = [r["query_id"] for r in selected]
        require(len(set(panel)) == len(panel), "duplicate selected identifier")
        require([q for q in queries if q in set(panel)] == panel, "fresh panel order mismatch")
        prompt_t = get_prompt(ds["task"])
        pkey = "qa" if ds["task"] == "qa" else "classification"
        require(sha256_text(prompt_t) == manifest["prompt_sha256"][pkey], "prompt template hash mismatch")
        ranked = all_runs["bm25"]

        prepared = []
        for row in selected:
            qid = row["query_id"]
            require(qid in eligible and qid not in frozen, "fresh question eligibility mismatch")
            h = normalized_question_sha(queries[qid])
            require(h == row["question_sha256"] and h not in known, "question exclusion mismatch")
            require(row["dataset"] == dname and row["task"] == ds["task"], "fresh task mismatch")
            docs = {"reference": list(ranked[qid][:10])}
            for draw, seed in EXCHANGE_SEEDS.items():
                docs["draw" + draw] = list(build_equivalent(qid, ranked[qid], qrels[qid], 10,
                    c["pool_depth"], "random", seed, f"{dname}:bm25").doc_ids)
                require(docs["draw" + draw] != docs["reference"], "no exchanged passage; stop without resampling")
            require(docs == row["doc_ids"], "fresh document identities mismatch")
            full_prompts = {}
            for cond, ids in docs.items():
                passages = "\n\n".join(f"[{j+1}] {corpus[x][:c['passage_chars']]}" for j, x in enumerate(ids))
                prompt = prompt_t.format(passages=passages, query=queries[qid])
                require(sha_bytes(prompt.encode()) == row["prompt_sha256"][cond], "fresh prompt bytes mismatch")
                require(sha_bytes(("\n".join(ids) + "\n").encode()) == row["doc_ids_sha256"][cond],
                        "fresh document hash mismatch")
                full_prompts[cond] = prompt
            accepted = [normalize_qa(str(x)) for x in gold[qid].get("answers", [])
                        if normalize_qa(str(x))] if ds["task"] == "qa" else []
            changed = set(docs["drawA"]) ^ set(docs["reference"])
            G = bool(accepted and any(g in normalize_qa(corpus[doc][:1200]) for doc in changed for g in accepted))
            require(type(row["exchanged_gold_string"]) is bool and G == row["exchanged_gold_string"],
                    "input-only G mismatch")
            prepared.append((qid, row, {"reference": full_prompts["reference"],
                                        "random": full_prompts["draw" + a.draw]}))
        print("PROMPT_MANIFEST_VERIFIED", dname, a.draw, flush=True)
        metadata = next(x for x in fresh["models"] if x["key"] == a.model_key)
        require(metadata["revision"] == m["revision"] and metadata["model_id"] == m["model_id"],
                "preflight model identity mismatch")
        if a.preflight_only:
            from transformers import AutoTokenizer
            if a.tokenizer_dir:
                tp = a.tokenizer_dir / a.model_key
                for name, expected in metadata["tokenizer_files_sha256"].items():
                    require(sha_file(tp / name) == expected, "local tokenizer bytes mismatch")
                tok = AutoTokenizer.from_pretrained(tp, local_files_only=True)
            else:
                tok = AutoTokenizer.from_pretrained(m["model_id"], revision=m["revision"])
            validate_tokenizer(tok, metadata, prepared, a.draw, a.model_key)
            print("PREFLIGHT_COMPLETE", json.dumps({"study": STUDY, "dataset": dname,
                  "model_key": a.model_key, "draw": a.draw, "n": len(prepared),
                  "source_sha256": {"control": CONTROL_SHA, "data": DATA_SHA[dname]},
                  "prompt_manifest_sha256": sha_bytes(pm_bytes), "generation_performed": False}, sort_keys=True), flush=True)
            return

        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
        import torch, transformers, huggingface_hub, accelerate
        from transformers import AutoModelForCausalLM, AutoTokenizer
        random.seed(SEED); torch.manual_seed(SEED)
        if not torch.cuda.is_available():
            raise ProtocolError("CUDA required")
        gpu_memory = [torch.cuda.get_device_properties(i).total_memory for i in range(torch.cuda.device_count())]
        verify_gpu_memory(gpu_memory, m["min_gpus_80gb"])
        torch.cuda.manual_seed_all(SEED)
        torch.use_deterministic_algorithms(True)
        torch.backends.cuda.matmul.allow_tf32 = False; torch.backends.cudnn.allow_tf32 = False
        tok = AutoTokenizer.from_pretrained(m["model_id"], revision=m["revision"])
        validate_tokenizer(tok, metadata, prepared, a.draw, a.model_key)
        model = AutoModelForCausalLM.from_pretrained(m["model_id"], revision=m["revision"],
                                                   torch_dtype=torch.bfloat16, device_map="auto")
        require(model.config.max_position_embeddings == metadata["max_position_embeddings"], "model context limit changed")
        model.eval()
        floating_dtypes = {str(p.dtype) for p in model.parameters() if p.is_floating_point()}
        require(floating_dtypes == {"torch.bfloat16"}, "all floating model parameters must use bfloat16")
        require(not getattr(model, "is_loaded_in_4bit", False) and not getattr(model, "is_loaded_in_8bit", False),
                "quantized weights are not permitted")
        env = {"python": sys.version.split()[0], "torch": torch.__version__, "transformers": transformers.__version__,
               "huggingface_hub": huggingface_hub.__version__, "accelerate": accelerate.__version__,
               "cuda": torch.version.cuda, "gpu": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
               "gpu_memory_bytes": gpu_memory, "device_map": {k: str(v) for k, v in getattr(model, "hf_device_map", {}).items()},
               "parameter_dtype": str(next(model.parameters()).dtype), "floating_parameter_dtypes": sorted(floating_dtypes),
               "deterministic_algorithms": True,
               "do_sample": False, "tf32": False, "cublas_workspace_config": os.environ.get("CUBLAS_WORKSPACE_CONFIG")}
        print("ENV", json.dumps(env, sort_keys=True), flush=True)

        def chat(p):
            return tok.apply_chat_template([{"role": "user", "content": p}], tokenize=False,
                                           add_generation_prompt=True, enable_thinking=False)

        def gen_single(p):
            ids = tok(chat(p), return_tensors="pt").to(model.device)
            with torch.inference_mode():
                o = model.generate(**ids, do_sample=False, max_new_tokens=MAX_NEW, pad_token_id=tok.eos_token_id)
            return tok.decode(o[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()

        def gen_batch(ps):
            tok.padding_side = "left"
            if tok.pad_token is None:
                tok.pad_token = tok.eos_token
            enc = tok([chat(p) for p in ps], return_tensors="pt", padding=True).to(model.device)
            with torch.inference_mode():
                o = model.generate(**enc, do_sample=False, max_new_tokens=MAX_NEW, pad_token_id=tok.pad_token_id)
            L = enc["input_ids"].shape[1]
            return [tok.decode(o[i][L:], skip_special_tokens=True).strip() for i in range(len(ps))]

        t0 = time.time()
        ans = {qid: {} for qid, _, _ in prepared}
        for i, (qid, _, prompts) in enumerate(prepared, 1):
            ans[qid]["reference_single"] = gen_single(prompts["reference"])
            persist_answer(out, qid, "reference_single", ans[qid]["reference_single"])
            ans[qid]["random_single"] = gen_single(prompts["random"])
            persist_answer(out, qid, "random_single", ans[qid]["random_single"])
            if i % 25 == 0:
                print("PROGRESS_SINGLE", a.model_key, dname, i, len(prepared), round(time.time() - t0, 1), flush=True)
        for s in range(0, len(prepared), BATCH):
            block = prepared[s:s + BATCH]
            outs = gen_batch([p["reference"] for _, _, p in block])
            for (qid, _, _), o in zip(block, outs):
                ans[qid]["reference_fixed16"] = o
                persist_answer(out, qid, "reference_fixed16", o)
        print("PROGRESS_FIXED16_DONE", a.model_key, dname, round(time.time() - t0, 1), flush=True)
        # determinism check: re-generate the first DET_CHECK_N reference prompts one at a time
        det = []
        for qid, _, p in prepared[:DET_CHECK_N]:
            repeated = gen_single(p["reference"])
            persist_answer(out, qid, "reference_determinism_check", repeated)
            det.append(repeated == ans[qid]["reference_single"])

        labels = ds.get("labels"); task = ds["task"]
        rows = []
        for qid, panelrow, _ in prepared:
            r = {"dataset": dname, "query_id": qid, "task": task, "model_key": a.model_key}
            for cond in ("reference_single", "random_single", "reference_fixed16"):
                t = ans[qid][cond]
                r[f"{cond}_answer"] = t
                r[f"{cond}_answer_sha256"] = sha_bytes(t.encode())
                r[f"{cond}_correct"] = bool(is_correct(t, gold[qid], task, labels))
                r[f"{cond}_canonical"] = canonical_answer(t, task, labels)
            r["intervention_changed"] = r["reference_single_correct"] != r["random_single_correct"]
            r["floor_changed"] = r["reference_single_correct"] != r["reference_fixed16_correct"]
            r["correct_to_wrong"] = r["reference_single_correct"] and not r["random_single_correct"]
            r["wrong_to_correct"] = (not r["reference_single_correct"]) and r["random_single_correct"]
            r["canonical_changed"] = r["reference_single_canonical"] != r["random_single_canonical"]
            r["exchanged_gold_string"] = panelrow["exchanged_gold_string"]
            r["random_doc_ids_sha256"] = panelrow["doc_ids_sha256"]["draw" + a.draw]
            r["draw"] = a.draw
            r["exchange_seed"] = EXCHANGE_SEEDS[a.draw]
            rows.append(r)
        check = {"determinism_first16_identical": sum(det), "determinism_n": len(det)}
        raw = out / f"{a.model_key}__{dname}__records.jsonl"
        raw_tmp = raw.with_name(raw.name + ".tmp")
        with raw_tmp.open("x", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
            f.flush(); os.fsync(f.fileno())
        os.replace(raw_tmp, raw)
        meta = {"study": STUDY, "model": m, "dataset": dname, "n": len(rows), "attempt": a.attempt,
                "status": "succeeded", "configuration_sha256": status["configuration_sha256"],
                "draw": a.draw, "exchange_seed": EXCHANGE_SEEDS[a.draw],
                "fresh_panel_sha256": sha_file(HERE / "FRESH_PANEL.json"),
                "prompt_manifest_sha256": sha_bytes(pm_bytes),
                "generation": {"max_new_tokens": MAX_NEW, "seed": SEED, "greedy": True, "enable_thinking": False,
                               "fixed_batch": BATCH, "padding_side": "left"},
                "environment": env, "checks": check, "records_sha256": sha_file(raw),
                "partial_answers_sha256": sha_file(out / "partial_answers.jsonl"),
                "lock": lock["files"], "elapsed_seconds": round(time.time() - t0, 1)}
        atomic_json(out / "run_meta.json", meta)


if __name__ == "__main__":
    main()
