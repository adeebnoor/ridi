# RIDI-PREDICT-v1 — runner specification for the operator

Derive `run_predict.py` from the locked `run_scale_curve.py` (whjbs, commit 869abda…). Change **only** the items below; everything else (source verification, exchange, prompts, scorer, three conditions, generation settings, determinism check, blinding, attempt handling, failure classes) stays byte-for-byte equivalent in behaviour.

## 1. Constants
- `STUDY = "RIDI-PREDICT-v1"`.
- Remove `PRIMARY_RESULTS_SHA`, the `--primary-results-*` arguments and the archived-panel/identity checks against the primary results archive (fresh questions have no archived rows). Keep `CONTROL_SHA`, `DATA_SHA`, `REGISTERED_BUNDLE_SHA`, `FROZEN_MANIFEST_SHA` and the registered-artifact verification unchanged.
- Replace `PROMPT_DATASET_SHA` with the values written to `FRESH_PANEL.json` at preflight (step 3) and committed in `LOCK.json`.
- Remove the `archived_qwen3_8b_*` fields from records (no archive for fresh questions).
- Add to every record `exchanged_gold_string` (bool): for QA tasks, true if any passage in `set(rnd) ^ set(ref)` (added or removed) contains a gold answer after the registered scorer's normalization; false for verdict tasks. Compute it at preflight, store it per question in `FRESH_PANEL.json`, and copy it into records (it is input-only and does not depend on model output).

## 2. Fresh panel (new function, used by preflight and by every job)
```
frozen = select_universal_panel(all_runs, queries, qrels, c["panel_ks"], c["pool_depth"], ds["panel_n"])   # unchanged call
eligible = <every query id that satisfies select_universal_panel's eligibility criteria>               # see note
def nq_hash(text):  # identical to the P14 known-source filter
    t = " ".join(unicodedata.normalize("NFKC", text).casefold().split())
    return hashlib.sha256(t.encode("utf-8")).hexdigest()
known = <the 7,280 hashes of the known-source filter; verify filter SHA-256 bc2aecee…13df8 before use>
fresh_pool, seen = [], set()
for q in <original query order>:
    if q not in eligible or q in set(frozen): continue
    h = nq_hash(queries[q])
    if h in known or h in seen: continue          # prior project input, or within-panel duplicate
    if not fits_all_models(q): continue           # context-length gate, see §2a
    seen.add(h); fresh_pool.append(q)
target = {"nq": 250, "hotpotqa": 250, "fever": 150, "scifact": 150}[dname]
if dname == "fever" and len(<scifact fresh_pool>) < 75: target = 300   # prereg §2.1 reallocation
k = min(target, len(fresh_pool))
fresh = sorted(random.Random(20261012).sample(fresh_pool, k), key=<original query order>)
```
Note on `eligible`: use the eligibility predicate inside `panels.select_universal_panel` without modifying it (e.g. call it with `n = len(queries)` if it returns all eligible queries when n exceeds the eligible count; otherwise import and call its internal predicate). Record which route was used in `FRESH_PANEL.json`. If a benchmark has < 75 fresh eligible questions, record it; no jobs are run for it and it is removed from `datasets` in `predict_config.json` before the lock (prereg §2.1). SciFact is expected to be excluded (299/300 BEIR test claims are already in the filter).

### 2a. Context-length gate
`fits_all_models(q)`: build the reference, draw A and draw B contexts; render each prompt with every model's tokenizer and `apply_chat_template(..., add_generation_prompt=True, enable_thinking=False)`; require `len(tokens) + 128 <= max_position_embeddings` (OLMo-2 4,096; Qwen3 from its config). Never pass `truncation=True`. Record removals per benchmark in `FRESH_PANEL.json`.

For each fresh question build both contexts exactly as the registered runner does:
`ref = ranked[qid][:10]`; `rnd = build_equivalent(qid, ranked[qid], qrels[qid], 10, c["pool_depth"], "random", 20260902, f"{dname}:bm25").doc_ids`.
Require `rnd != ref` (at least one exchanged passage); if a sampled question has no exchangeable grade-zero passage it is ineligible by construction — record and stop (do not resample silently).

## 3. Preflight (no model loaded, no attempt directory created)
`run_predict.py --preflight-only --dataset D` for all four datasets writes, per dataset, the fresh question ids (in order), the SHA-256 of each context's doc-id list and of each prompt, and the prompt-manifest SHA-256 into `FRESH_PANEL.json`. Then `make_lock.py` freezes: `run_predict.py`, `models.json`, `FRESH_PANEL.json`, `analyze_predict.py`, `predict_config.json`, and the coding manual. Publish `LOCK.json` (GitHub commit + attach to the OSF registration) **before** the first generation job.

## 4. models.json
Predictors qwen3-1.7b, qwen3-4b, qwen3-8b and target qwen3-32b with the revisions in the preregistration table; target `olmo2-32b` = `allenai/OLMo-2-0325-32B-Instruct`, revision resolved with `resolve_revisions.py` and recorded before the lock. `min_gpus_80gb`: 1 for ≤ 8B, 2 for both 32B targets (Amendment A1 configuration).

## 5. Chat template
Call `apply_chat_template(..., add_generation_prompt=True, enable_thinking=False)` for every model (unknown keyword arguments are ignored by templates that do not use them). At preflight, render one prompt per model with the tokenizer only and record the SHA-256 of the rendered template text in `FRESH_PANEL.json`; for OLMo-2 confirm that no thinking block is produced.

## 6. Two exchange draws and jobs
Add `--draw {A,B}`: draw A uses exchange seed 20260902 (registered), draw B uses 20261016; everything else identical. Output roots `ridi_predict_out/drawA/` and `ridi_predict_out/drawB/`. Record in every row `random_doc_ids_sha256` (SHA-256 of the newline-joined exchanged doc-id list) and `task`.
Jobs (32): predictors qwen3-1.7b, qwen3-4b, qwen3-8b × 4 datasets × draws A and B (24); targets qwen3-32b and olmo2-32b × 4 datasets × draw A (8). Any order; attempts 1–3 under the whjbs failure rules; correctness never printed to logs.
Before filing the registration: run preflight eligibility counts per dataset (no model weights; tokenizers only), with the number removed by each exclusion (frozen panel, known-source filter, duplicates, context-length gate), and send them to the PI.
Optional, before any generation: run the frozen ms4w8 P4 judgement prompt with both registered judges on draw A's exchanged passages and store `exchanged_judge_flag_any` per question in FRESH_PANEL.json and records.

## 7. Analysis (once, after all jobs are terminal)
`python3 analyze_predict.py ridi_predict_out --config predict_config.json --lock LOCK.json --draws 100000`

## 8. Part A export for the research assistants (DONE by the PI side; nothing for the operator)
Already produced from the frozen audit package with `annotation/build_partA_export.py` and `annotation/sample_partA.py`; sheet and key hashes go into `LOCK.json`. The original instructions are kept below for reference.
From the frozen panel (registered code, same contexts as txwdv), export for every question: dataset, query id, question text, gold answer(s), and for each passage that is in `rnd` but not in `ref` ("exchanged-in"): doc id and the first 1,200 characters of text. Output `partA_export.jsonl`. Then run `annotation/sample_partA.py` (seeded) to draw the 200 items. Do not include model answers, change status or AI-judge labels in the coders' sheet.
