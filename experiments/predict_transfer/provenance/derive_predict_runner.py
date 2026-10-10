#!/usr/bin/env python3
"""Auditable derivation of the PREDICT runner; never edits parent science."""
import ast, hashlib, json, shutil
from pathlib import Path
BASE=Path(__file__).resolve().parent
DEST=BASE/'registration_ready'
src=BASE.parent/'frozen_science/code/run_scale_curve.py'
assert hashlib.sha256(src.read_bytes()).hexdigest()=='2e5cf0747440f1eca2a0a55651b365f5e7e014a79d833a935df0bd7abe3e9eef'
s=src.read_text()
def replace(a,b):
    global s
    assert s.count(a)==1,(a[:100],s.count(a))
    s=s.replace(a,b)
start=s.index('"""');end=s.index('"""',start+3)+3
s=s[:start]+'''"""RIDI-PREDICT-v1: one model x benchmark x exchange draw per call.
Derived from frozen scale-curve runner 869abda18a17ba528ecfcddcb4461914b8b113c1.
Fresh input panel, independent draws, input-only G; generation and scoring
preserve the parent behavior. Correctness is never printed to logs.
"""'''+s[end:]
replace('import argparse, hashlib, io, json, os, random, re, shutil, signal, sys, tempfile, time, urllib.request, zipfile',
        'import argparse, hashlib, io, json, os, random, re, shutil, signal, sys, tempfile, time, urllib.request, zipfile, unicodedata')
replace('STUDY = "RIDI-RAG-QWEN3-SCALE-CURVE-v1"','STUDY = "RIDI-PREDICT-v1"')
replace('PRIMARY_RESULTS_SHA = "c19942d0eb4a0087195c46a45831a1cf864676b813485dcf4e5565a2a676f231"\n','')
a=s.index('PROMPT_DATASET_SHA = {');b=s.index('BATCH = 16',a)
panel=json.loads((BASE/'preflight_output_final/FRESH_PANEL.json').read_text())
s=s[:a]+'PROMPT_DATASET_SHA = '+repr(panel['prompt_manifest_sha256'])+'\nEXPECTED_N = {"nq": 250, "hotpotqa": 250, "fever": 300}\nEXCHANGE_SEEDS = {"A": 20260902, "B": 20261016}\nKNOWN_FILTER_SHA = "bc2aecee5a27fc33b75e5caf5c000764ee1c88598533075ace19884a8c613df8"\n'+s[b:]
replace('LOCK_FILES = {"models.json", "run_scale_curve.py", "aggregate_scale_curve.py"}',
'''LOCK_FILES = {"models.json", "run_predict.py", "FRESH_PANEL.json", "analyze_predict.py",
              "predict_config.json", "annotation/CODING_MANUAL_EN_AR.md", "annotation/coder_sheet.csv",
              "known_source_filter.json", "make_lock.py"}
SEALED_KEY_SHA = "75b0833b4eb35134646cf28443c5ad0031cc24364f23b0da512b14e2ce8e4d89"''')
replace('def configuration_sha256(lock, model, dataset):','def configuration_sha256(lock, model, dataset, draw):')
replace('"source_sha256": {"control": CONTROL_SHA, "primary": PRIMARY_RESULTS_SHA,\n                                "data": DATA_SHA[dataset]},',
'''"draw": draw, "exchange_seed": EXCHANGE_SEEDS[draw],
              "source_sha256": {"control": CONTROL_SHA, "data": DATA_SHA[dataset]},''')
replace('"LOCK.json must contain exactly the expected runner, analysis and model files"','"LOCK.json file set mismatch"')
replace('    return lock\n\n\ndef fire_bytes',
'''    require(lock.get("sealed_key_sha256") == SEALED_KEY_SHA, "sealed key hash mismatch")
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


def fire_bytes''')
a=s.index('    for tier in ("primary_family", "optional_tier"):');b=s.index('\n\ndef main():',a)
s=s[:a]+'''    require(M.get("study") == STUDY, "model manifest study mismatch")
    for m in M["models"]:
        if m["key"] == key:
            return m
    raise SystemExit(f"unknown model key {key}")
'''+s[b:]
replace('    ap.add_argument("--model-key", required=True)','    ap.add_argument("--model-key", required=True)\n    ap.add_argument("--draw", choices=["A", "B"], required=True)\n    ap.add_argument("--tokenizer-dir", type=Path, help="preflight-only local tokenizer root")')
replace('    ap.add_argument("--primary-results-zip", action="append"); ap.add_argument("--primary-results-share", action="append")\n','')
replace('default=Path("ridi_scale_out")','default=Path("ridi_predict_out")')
replace('verify frozen archives/panel/prompts before locking; no model, output or attempt is created','verify selected fresh inputs and tokenizers before locking; no weights or attempt is created')
replace('    if a.preflight_only:\n        execute_job(a, None, None, None, None)',
'''    m = model_entry(a.model_key)
    require(m["role"] == "predictor" or a.draw == "A", "targets run draw A only")
    require(a.tokenizer_dir is None or a.preflight_only, "local tokenizer override allowed only for preflight")
    if a.preflight_only:
        execute_job(a, None, m, None, None)''')
replace('    lock = verify_lock()\n    m = model_entry(a.model_key)','    lock = verify_lock()\n    verify_publication_receipt(lock)')
replace('configuration_sha256(lock, m, a.dataset)','configuration_sha256(lock, m, a.dataset, a.draw)')
replace('begin_attempt(a.out, a.model_key, a.dataset, a.attempt, config_sha)', 'begin_attempt(a.out / ("draw" + a.draw), a.model_key, a.dataset, a.attempt, config_sha)\n    status["draw"] = a.draw\n    atomic_json(out / "attempt_status.json", status)')
replace('    primary_zip = load_source(a.primary_results_zip, a.primary_results_share, "RIDI_RAG_RESULTS__PRIMARY_H1_H2.zip")\n','')
replace('    require(sha_bytes(primary_zip) == PRIMARY_RESULTS_SHA, "primary results hash mismatch")\n','')
s=s.replace('z.extractall(stage)','safe_extract(z, stage)').replace('z.extractall(root)','safe_extract(z, root)')
replace('from scoring import canonical_answer, is_correct','from scoring import canonical_answer, is_correct, normalize_qa')
a=s.index('        panel = select_universal_panel(');b=s.index('        prompt_t = get_prompt',a)
s=s[:a]+'''        fresh = json.loads((HERE / "FRESH_PANEL.json").read_text())
        require(fresh.get("study") == STUDY, "fresh panel study mismatch")
        selected = fresh["datasets"][dname]
        require(len(selected) == EXPECTED_N[dname], "fresh panel length mismatch")
        pm_bytes = "".join(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\\n" for r in selected).encode()
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
'''+s[b:]
a=s.index('        prepared, pm = [], []');b=s.index('        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG"',a)
s=s[:a]+'''        prepared = []
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
                passages = "\\n\\n".join(f"[{j+1}] {corpus[x][:c['passage_chars']]}" for j, x in enumerate(ids))
                prompt = prompt_t.format(passages=passages, query=queries[qid])
                require(sha_bytes(prompt.encode()) == row["prompt_sha256"][cond], "fresh prompt bytes mismatch")
                require(sha_bytes(("\\n".join(ids) + "\\n").encode()) == row["doc_ids_sha256"][cond],
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

'''+s[b:]
replace('        model = AutoModelForCausalLM.from_pretrained',
'''        validate_tokenizer(tok, metadata, prepared, a.draw, a.model_key)
        model = AutoModelForCausalLM.from_pretrained''')
replace('        model.eval()','        require(model.config.max_position_embeddings == metadata["max_position_embeddings"], "model context limit changed")\n        model.eval()')
replace('for qid, oldrow, _ in prepared:', 'for qid, panelrow, _ in prepared:')
a=s.index('            r["archived_qwen3_8b_ref_correct"]');b=s.index('            rows.append(r)',a)
s=s[:a]+'''            r["exchanged_gold_string"] = panelrow["exchanged_gold_string"]
            r["random_doc_ids_sha256"] = panelrow["doc_ids_sha256"]["draw" + a.draw]
            r["draw"] = a.draw
            r["exchange_seed"] = EXCHANGE_SEEDS[a.draw]
'''+s[b:]
a=s.index('        if a.model_key == "qwen3-8b":');b=s.index('        raw = out /',a)
s=s[:a]+s[b:]
replace('"generation": {"max_new_tokens": MAX_NEW, "seed": SEED, "greedy": True, "enable_thinking": False,',
'''"draw": a.draw, "exchange_seed": EXCHANGE_SEEDS[a.draw],
                "fresh_panel_sha256": sha_file(HERE / "FRESH_PANEL.json"),
                "prompt_manifest_sha256": sha_bytes(pm_bytes),
                "generation": {"max_new_tokens": MAX_NEW, "seed": SEED, "greedy": True, "enable_thinking": False,''')
assert 'PRIMARY_RESULTS_SHA' not in s and 'archived_qwen3' not in s and 'oldrow' not in s
ast.parse(s)
(DEST/'run_predict.py').write_text(s)
shutil.copy2(BASE/'models_preflight.json',DEST/'models.json')
shutil.copy2(BASE/'preflight_output_final/FRESH_PANEL.json',DEST/'FRESH_PANEL.json')
shutil.copy2(BASE/'RIDI_PREDICT_v1.1/analysis/analyze_predict.py',DEST/'analyze_predict.py')
shutil.copy2(BASE/'RIDI_PREDICT_v1.1/annotation/CODING_MANUAL_EN_AR.md',DEST/'annotation/CODING_MANUAL_EN_AR.md')
shutil.copy2(BASE/'RIDI_PREDICT_v1.1/annotation/partA_sheets/coder_sheet.csv',DEST/'annotation/coder_sheet.csv')
shutil.copy2(BASE/'recovered_originals/P14_KAGGLE_EXTENDED_INPUT_FILTER_10177_RECORDS_7280_HASHES.json',DEST/'known_source_filter.json')
cfg=json.loads((BASE/'RIDI_PREDICT_v1.1/analysis/predict_config.json').read_text())
cfg['datasets']=['nq','hotpotqa','fever']
cfg['panel_targets']['fever']=300
cfg['datasets_note']='Tokenizer-only preflight completed: nq=250, hotpotqa=250, fever=300 selected; scifact excluded (0 fresh eligible). Prespecified reallocation applied before registration and lock.'
(DEST/'predict_config.json').write_text(json.dumps(cfg,indent=2)+'\n')
print('Derived runner and scientific payload prepared; LOCK not created; no generation.')
