#!/usr/bin/env python3
"""RIDI-PREDICT-v1 — POST-RUN RECOVERY under amendment 2026-10-11.
Original frozen analysis is retained, failed once, and is not overwritten.

Primary question: does a fragility score computed from small models under an INDEPENDENT exchange draw (draw B)
predict which FRESH questions change correctness under the registered exchange (draw A) in larger target models?

Layout:  OUTDIR/drawA/<model>/<dataset>/attempt<i>/...   predictors and targets, registered exchange seed
         OUTDIR/drawB/<model>/<dataset>/attempt<i>/...   predictors only, independent exchange seed
Usage:   python3 analyze_predict.py OUTDIR --config predict_config.json [--lock LOCK.json] [--draws 100000]
Writes OUTDIR/PREDICT_RECOVERY_RESULTS.json and OUTDIR/PREDICT_RECOVERY_RESULTS.md.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib
import numpy as np

BOOL_FIELDS = ("reference_single_correct", "random_single_correct", "reference_fixed16_correct",
               "intervention_changed", "floor_changed", "exchanged_gold_string")

def require(c, msg):
    if not c:
        raise SystemExit(f"ANALYSIS BLOCKED: {msg}")

def sha_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def load_job(root, k, d, study):
    base = root / k / d
    atts = sorted(base.glob("attempt*"), key=lambda p: int(p.name[7:])) if base.exists() else []
    if not atts:
        return None
    require([p.name for p in atts] == [f"attempt{i}" for i in range(1, len(atts) + 1)] and len(atts) <= 3,
            f"invalid attempt sequence {base}")
    for i, p in enumerate(atts, 1):
        st = json.loads((p / "attempt_status.json").read_text())
        require(st.get("study") == study, f"study mismatch {p}")
        require((st.get("model_key"), st.get("dataset"), st.get("attempt")) == (k, d, i), f"identity mismatch {p}")
        if i < len(atts):
            require(st.get("status") == "failed" and st.get("failure_kind") == "technical", f"non-technical retry {p}")
        elif st.get("status") != "succeeded":
            return None
    p = atts[-1]
    meta = json.loads((p / "run_meta.json").read_text())
    raw = p / f"{k}__{d}__records.jsonl"
    require(sha_file(raw) == meta.get("records_sha256"), f"records hash mismatch {p}")
    rows = [json.loads(x) for x in raw.read_text().splitlines() if x.strip()]
    for r in rows:
        for f in BOOL_FIELDS:
            require(type(r.get(f)) is bool, f"field {f} missing or not boolean in {p}")
        require(r.get("task") in ("qa", "classification"), f"task field missing in {p}")
        ref, rnd, flo = r["reference_single_correct"], r["random_single_correct"], r["reference_fixed16_correct"]
        require(r["intervention_changed"] == (ref != rnd) and r["floor_changed"] == (ref != flo), f"flag mismatch {p}")
    return {str(r["query_id"]): r for r in rows}

def auc_from_counts(pos, neg):
    P, N = pos.sum(-1), neg.sum(-1)
    cneg = np.cumsum(neg, -1) - neg
    with np.errstate(invalid="ignore", divide="ignore"):
        return (pos * (cneg + 0.5 * neg)).sum(-1) / (P * N)

def auc_scores(score, y):
    """Mann–Whitney AUC for a real-valued score (ties count one half)."""
    y = np.asarray(y, bool); order = np.argsort(score, kind="mergesort"); s = np.asarray(score)[order]; yy = y[order]
    ranks = np.empty(len(s)); i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]: j += 1
        ranks[i:j + 1] = (i + j) / 2 + 1; i = j + 1
    P = yy.sum(); N = len(yy) - P
    return float((ranks[yy].sum() - P * (P + 1) / 2) / (P * N)) if P and N else float("nan")

def logit(y, X):
    b = np.zeros(X.shape[1]); ok = False
    for _ in range(200):
        p = np.clip(1 / (1 + np.exp(-X @ b)), 1e-12, 1 - 1e-12); W = p * (1 - p)
        H = X.T @ (X * W[:, None]); g = X.T @ (y - p)
        step = np.linalg.lstsq(H, g, rcond=None)[0]; b += step
        if np.max(np.abs(step)) < 1e-9: ok = True; break
    p = np.clip(1 / (1 + np.exp(-X @ b)), 1e-12, 1 - 1e-12)
    se = np.sqrt(np.diag(np.linalg.pinv(X.T @ (X * (p * (1 - p))[:, None]))))
    return b, se, ok, p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir", type=pathlib.Path)
    ap.add_argument("--config", type=pathlib.Path, required=True)
    ap.add_argument("--lock", type=pathlib.Path)
    ap.add_argument("--draws", type=int, default=100000)
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    out = a.outdir
    require(not (out / "PREDICT_RECOVERY_RESULTS.json").exists(), "results already exist — the analysis runs once")
    if a.lock:
        lock = json.loads(a.lock.read_text())["files"]
        for name, path in (("analyze_predict.py", a.lock.parent / "analyze_predict.py"), ("predict_config.json", a.config)):
            require(lock.get(name) == sha_file(path), f"{name} differs from LOCK.json")
    cfg = json.loads(a.config.read_text())
    D, preds, targets, rule, study = cfg["datasets"], cfg["predictors"], cfg["targets"], cfg["decision_rule"], cfg["study"]
    A, Bd = out / cfg["draw_targets"], out / cfg["draw_independent"]

    def load_model(root, k):
        per = {}
        for d in D:
            j = load_job(root, k, d, study)
            if j is None: return None          # one failed benchmark job => model not executed (prereg §7)
            per[d] = j
        return per
    dataA = {k: load_model(A, k) for k in preds + targets}
    dataB = {k: load_model(Bd, k) for k in preds}
    status = {**{f"{k} (draw A)": ("executed" if dataA[k] else "not executed") for k in preds + targets},
              **{f"{k} (draw B)": ("executed" if dataB[k] else "not executed") for k in preds}}
    for k in preds:
        require(dataA[k] is not None and dataB[k] is not None, f"predictor {k} not executed in both draws — F undefined")
    present = [dataA[k] for k in preds + targets if dataA[k]] + [dataB[k] for k in preds]
    qids = {d: sorted(present[0][d]) for d in D}
    for m in present:
        for d in D:
            require(set(m[d]) == set(qids[d]), f"question sets differ ({d})")
    used = [d for d in D if len(qids[d]) >= cfg["min_questions_per_dataset"]]
    def arr(src, k, d, f): return np.array([src[k][d][q][f] for q in qids[d]])
    for d in used:   # content covariate is input-only and must agree across every draw-A model
        g0 = arr(dataA, preds[0], d, "exchanged_gold_string")
        for k in preds + targets:
            if dataA[k]: require(np.array_equal(arr(dataA, k, d, "exchanged_gold_string"), g0), f"G differs across models ({k}/{d})")
    cat = lambda f: np.concatenate([f(d) for d in used])
    FB = cat(lambda d: sum(arr(dataB, k, d, "intervention_changed").astype(int) for k in preds))
    FA = cat(lambda d: sum(arr(dataA, k, d, "intervention_changed").astype(int) for k in preds))
    FFL = cat(lambda d: sum(arr(dataA, k, d, "floor_changed").astype(int) for k in preds))
    NC = cat(lambda d: sum(arr(dataA, k, d, "reference_single_correct").astype(int) for k in preds))
    G = cat(lambda d: arr(dataA, preds[0], d, "exchanged_gold_string")).astype(bool)
    QA = cat(lambda d: arr(dataA, preds[0], d, "task") == "qa")
    DS = np.concatenate([np.full(len(qids[d]), i) for i, d in enumerate(used)])
    JF = None
    jf = cfg.get("judge_flag_field")
    if jf and all(jf in dataA[preds[0]][d][q] for d in used for q in qids[d]):
        JF = cat(lambda d: arr(dataA, preds[0], d, jf)).astype(bool)
    nF = len(preds) + 1
    rng = np.random.default_rng(cfg["bootstrap_seed"])
    B = a.draws; chunk = 2000
    starts = np.cumsum([0] + [len(qids[d]) for d in used])[:-1]
    idx = []
    for s in range(0, B, chunk):
        m = min(chunk, B - s)
        idx.append(np.concatenate([st + rng.integers(0, len(qids[d]), (m, len(qids[d]))) for st, d in zip(starts, used)], 1))
    ci = lambda v: [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))]

    def boot_auc(F, Y, mask=None):
        vals = []
        for I in idx:
            f, y = F[I], Y[I]
            if mask is not None:
                mk = mask[I]; f = np.where(mk, f, -1); y = np.where(mk, y, False)
            pos = np.stack([((f == v) & y).sum(1) for v in range(nF)], -1)
            neg = np.stack([((f == v) & ~y).sum(1) for v in range(nF)], -1)
            vals.append(auc_from_counts(pos, neg))
        return np.concatenate(vals)

    def point_auc(F, Y, mask=None):
        if mask is not None: F, Y = F[mask], Y[mask]
        return float(auc_from_counts(np.bincount(F[Y], minlength=nF), np.bincount(F[~Y], minlength=nF)))

    def decide(point, lo, hi, pmin, lbmin):
        return "supported" if point >= pmin and lo > lbmin else "falsified" if hi < lbmin else "inconclusive"

    overlap = None
    if all("random_doc_ids_sha256" in dataA[preds[0]][d][q] and "random_doc_ids_sha256" in dataB[preds[0]][d][q] for d in used for q in qids[d]):
        same = cat(lambda d: np.array([dataA[preds[0]][d][q]["random_doc_ids_sha256"] == dataB[preds[0]][d][q]["random_doc_ids_sha256"] for q in qids[d]]))
        overlap = {"identical_exchanged_context_A_vs_B": int(same.sum()), "n": int(len(same))}
    res = {"study": study, "label": a.label, "status": status, "datasets_used": used,
           "n_per_dataset": {d: len(qids[d]) for d in D}, "predictors": preds, "draw_overlap": overlap, "targets": {}}
    dummies = [(DS == i).astype(float) for i in range(1, len(used))]
    for t in targets:
        if not dataA[t]:
            res["targets"][t] = {"status": "not executed", "H1_H2": "not evaluable", "H3": "not evaluable"}; continue
        Y = cat(lambda d: arr(dataA, t, d, "intervention_changed")).astype(bool)
        FL = cat(lambda d: arr(dataA, t, d, "floor_changed")).astype(bool)
        TR = cat(lambda d: arr(dataA, t, d, "reference_single_correct")).astype(float)
        exc_pt = float(np.mean([Y[DS == i].mean() - FL[DS == i].mean() for i in range(len(used))]))
        exc_b = np.concatenate([np.mean([Y[I][:, DS == i].mean(1) - FL[I][:, DS == i].mean(1) for i in range(len(used))], 0) for I in idx])
        exc_ci = ci(exc_b)
        evaluable = exc_ci[0] > rule["target_excess_lower_bound_min"]
        aucB, aucB_b = point_auc(FB, Y), boot_auc(FB, Y); aucB_ci = ci(aucB_b)
        aucA, aucA_b = point_auc(FA, Y), boot_auc(FA, Y)
        h12 = decide(aucB, *aucB_ci, rule["auc_point_min"], rule["auc_lower_bound_min"]) if evaluable else "not evaluable (target excess not above floor)"
        basecols = [np.ones(len(Y)), G.astype(float), NC.astype(float), NC.astype(float) ** 2, TR, FFL.astype(float)] + dummies
        if JF is not None: basecols.append(JF.astype(float))
        Xb = np.column_stack(basecols); Xf = np.column_stack(basecols + [FB.astype(float)])
        bf, sef, okf, pf = logit(Y.astype(float), Xf); bb, _, okb, pb = logit(Y.astype(float), Xb)
        regression_ok = bool(okf and okb and np.all(np.isfinite(bf)) and np.isfinite(sef[-1]))
        orB = orB_ci = d_auc = None
        h3 = "not estimable under registered MLE and Wald procedure"
        dvals = []
        if regression_ok:
            orB = float(np.exp(bf[-1])); orB_ci = [float(np.exp(bf[-1] - 1.959964 * sef[-1])), float(np.exp(bf[-1] + 1.959964 * sef[-1]))]
            h3 = ("supported" if orB_ci[0] > rule["adjusted_or_sesoi"] else "falsified" if orB_ci[1] < rule["adjusted_or_sesoi"] else "inconclusive") if evaluable else "not evaluable"
            d_auc = auc_scores(pf, Y) - auc_scores(pb, Y)
            drng = np.random.default_rng(cfg["bootstrap_seed"] + 1)
            for _ in range(cfg["delta_auc_bootstrap"]):
                I = np.concatenate([np.flatnonzero(DS == i)[drng.integers(0, (DS == i).sum(), (DS == i).sum())] for i in range(len(used))])
                b1, _, o1, p1 = logit(Y[I].astype(float), Xf[I]); b0, _, o0, p0 = logit(Y[I].astype(float), Xb[I])
                if o1 and o0: dvals.append(auc_scores(p1, Y[I]) - auc_scores(p0, Y[I]))
        clean = QA & ~G
        sec = {
            "same_draw_F_A": {"auc": aucA, "auc_ci95": ci(aucA_b)},
            "placebo_F_floor_auc": point_auc(FFL, Y),
            "delta_auc_baseline_to_baseline_plus_FB": d_auc, "delta_auc_ci95": ci(np.array(dvals)) if dvals else None, "delta_auc_bootstrap_converged": len(dvals),
            "delta_auc_bootstrap_attempted": cfg["delta_auc_bootstrap"] if regression_ok else 0,
            "regression_status": "registered MLE converged" if regression_ok else "unavailable due to registered regression nonconvergence",
            "auc_FB_QA_without_gold_string": point_auc(FB, Y, clean), "auc_FB_QA_without_gold_string_ci95": ci(boot_auc(FB, Y, clean)),
            "n_QA_without_gold_string": int(clean.sum()), "changed_QA_without_gold_string": int((clean & Y).sum()),
            "single_predictor_auc_draw_B": {k: auc_scores(cat(lambda d: arr(dataB, k, d, "intervention_changed")).astype(float), Y) for k in preds},
            "change_rate_by_FB": {int(f): {"n": int((FB == f).sum()), "changed": int((Y & (FB == f)).sum()),
                                           "correct_to_wrong": int((Y & (FB == f) & (TR == 1)).sum()),
                                           "wrong_to_correct": int((Y & (FB == f) & (TR == 0)).sum())} for f in range(nF)},
            "judge_flag_covariate_used": JF is not None}
        res["targets"][t] = {"status": "executed", "target_excess": exc_pt, "target_excess_ci95": exc_ci,
                             "H1_H2": h12, "auc_FB": aucB, "auc_FB_ci95": aucB_ci,
                             "H3": h3, "adjusted_or_FB": orB, "adjusted_or_FB_ci95_wald": orB_ci,
                             "H3_covariates": ["G (gold string in an exchanged passage)", "predictors correct on reference (linear + quadratic)",
                                               "target correct on reference", "predictors' floor changes", "benchmark"] + (["judge flag"] if JF is not None else []),
                             "secondary": sec}
    if len(targets) == 2 and all(dataA[t] for t in targets):
        y1 = cat(lambda d: arr(dataA, targets[0], d, "intervention_changed")); y2 = cat(lambda d: arr(dataA, targets[1], d, "intervention_changed"))
        a11 = int((y1 & y2).sum()); a10 = int((y1 & ~y2).sum()); a01 = int((~y1 & y2).sum()); a00 = int((~y1 & ~y2).sum())
        res["S5_target_concordance"] = {"both": a11, "jaccard": a11 / max(1, a11 + a10 + a01),
                                        "odds_ratio_haldane": (a11 + .5) * (a00 + .5) / ((a10 + .5) * (a01 + .5))}
    res["decision_rule"] = rule
    res["bootstrap"] = {"draws": B, "seed": cfg["bootstrap_seed"], "delta_auc_draws": cfg["delta_auc_bootstrap"],
                        "scheme": "questions resampled within benchmark; shared across targets"}
    require(overlap is not None and overlap["identical_exchanged_context_A_vs_B"] == 0,
            "S8 requires subset implementation for nonzero overlap; do not silently substitute")
    res["S8_excluding_identical_contexts"] = {"excluded": 0, "retained": sum(res["n_per_dataset"].values()),
        "status": "identical to primary analysis because no contexts are identical; no additional fit or bootstrap",
        "targets": {k: {key:v[key] for key in ("H1_H2","auc_FB","auc_FB_ci95","H3","adjusted_or_FB","adjusted_or_FB_ci95_wald")} for k,v in res["targets"].items()}}
    res["recovery_disclosure"] = {"status": "post-run amendment", "date": "2026-10-11",
        "amendment_commit": "8206e706de74f97d3215a5ae4a071bcd73f5a086",
        "original_frozen_analysis_failed_once": True, "data_regeneration": False,
        "unavailable_regression_does_not_block_other_tests": True,
        "unmodified_estimator_covariates_thresholds_seeds": True}
    (out / "PREDICT_RECOVERY_RESULTS.json").write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")
    L = [f"# RIDI-PREDICT-v1 results {a.label}", "", f"Predictors {', '.join(preds)}; F_B from the independent exchange draw. Benchmarks: {', '.join(used)}.", "",
         "| Target | Excess pp (95% CI) | H1/H2: AUC of F_B (95% CI) | H3: adjusted OR of F_B (95% Wald CI) | ΔAUC over baseline (95% CI) | Same-draw AUC F_A | Placebo AUC F_floor |",
         "|---|---|---|---|---|---|---|"]
    def fmt_num(x): return "NA" if x is None else f"{x:.3f}"
    def fmt_ci(x): return "NA" if x is None else f"{x[0]:.3f} to {x[1]:.3f}"
    for t, v in res["targets"].items():
        if v["status"] != "executed":
            L.append(f"| {t} | — | not evaluable | not evaluable | — | — | — |"); continue
        s = v["secondary"]
        L.append(f"| {t} | {100*v['target_excess']:.2f} ({100*v['target_excess_ci95'][0]:.2f}–{100*v['target_excess_ci95'][1]:.2f}) | "
                 f"**{v['H1_H2']}** {v['auc_FB']:.3f} ({v['auc_FB_ci95'][0]:.3f}–{v['auc_FB_ci95'][1]:.3f}) | "
                 f"**{v['H3']}** {fmt_num(v['adjusted_or_FB'])} ({fmt_ci(v['adjusted_or_FB_ci95_wald'])}) | "
                 f"{fmt_num(s['delta_auc_baseline_to_baseline_plus_FB'])} ({fmt_ci(s['delta_auc_ci95'])}) | "
                 f"{s['same_draw_F_A']['auc']:.3f} | {s['placebo_F_floor_auc']:.3f} |")
    L += ["", "POST-RUN RECOVERY: original frozen analysis failed once. See amendment 8206e706de74f97d3215a5ae4a071bcd73f5a086.",
          "S8: 0 identical contexts excluded; retained sample and all primary results are unchanged.",
          "Unavailable H3/S3 estimates are not falsification and are not replaced with a different estimator."]
    (out / "PREDICT_RECOVERY_RESULTS.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    main()
