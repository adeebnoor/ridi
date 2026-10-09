#!/usr/bin/env python3
"""Pre-specified analysis for RIDI-RAG-QWEN3-SCALE-CURVE-v1 (see preregistration, section 6).

Usage: python3 aggregate_scale_curve.py OUT_DIR --features per_question_features.jsonl [--draws 100000]
OUT_DIR is the --out directory of run_scale_curve.py. Every primary job must first succeed or
exhaust three technical attempts. Only the unique successful attempt is used, after verifying
the preregistered lock, terminal status, configuration identity and records hash. A model
enters the analysis only if all four datasets completed.
"""
from __future__ import annotations
import argparse, hashlib, json, math, pathlib, re
import numpy as np

DATASETS = ["nq", "hotpotqa", "fever", "scifact"]
EXPECTED_N = {"nq": 250, "hotpotqa": 250, "fever": 150, "scifact": 150}
SEED = 20261010
H1_MODEL = "qwen3-32b"
SUPPORT_POINT, SUPPORT_LOWER, VANISH_UPPER = 0.05, 0.02, 0.02
TOST_MARGIN = 0.05
HERE = pathlib.Path(__file__).resolve().parent
STUDY = "RIDI-RAG-QWEN3-SCALE-CURVE-v1"
MACRO_DENOM = math.lcm(*(len(DATASETS) * n for n in EXPECTED_N.values()))
MACRO_WEIGHTS = {d: MACRO_DENOM // (len(DATASETS) * n) for d, n in EXPECTED_N.items()}
STRATA_N = {"none_flagged_by_either_judge": 93, "judges_never_agreed": 238,
            "strict_registered_clean": 86, "qa_no_gold_string": 282}
STRATA = {"none_flagged_by_either_judge": lambda f: f["tot_either"] == 0,
          "judges_never_agreed": lambda f: f["tot_both"] == 0,
          "strict_registered_clean": lambda f: f["clean_original_rule"] == 1,
          "qa_no_gold_string": lambda f: f["task"] == "qa" and f["tot_gold"] == 0}


def sha_file(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify_lock():
    path = HERE / "LOCK.json"
    require(path.is_file(), "LOCK.json missing; analysis must use the preregistered lock")
    lock = json.loads(path.read_text())
    require(lock.get("study") == STUDY, "lock study mismatch")
    require({"models.json", "run_scale_curve.py", "aggregate_scale_curve.py"} <= set(lock.get("files", {})),
            "lock omits required code/model files")
    for name, expected in lock["files"].items():
        require(sha_file(HERE / name) == expected, f"locked file changed: {name}")
    return lock


def macro_numerator(v):
    return sum(int(v[d].sum()) * MACRO_WEIGHTS[d] for d in DATASETS)


def decision(excess_num, ci_num):
    # The panel defines an exact 1/3000 lattice. Compare in integer units so
    # E = exactly 5 pp cannot fall below the inclusive threshold by rounding.
    lo, hi = ci_num
    if excess_num >= 150 and lo > 60:
        return "supported"
    if hi < 60:
        return "falsified (vanishes)"
    return "inconclusive"


def load_features(path, rows_by_dataset):
    require(path.is_file(), f"required frozen P4 feature file missing: {path}")
    expected_hash = verify_lock().get("feature_sha256")
    require(isinstance(expected_hash, str) and sha_file(path) == expected_hash, "P4 feature SHA256 differs from frozen lock")
    features = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        key = (row["dataset"], str(row["qid"]))
        require(key not in features, f"duplicate P4 feature key: {key}")
        for field in ("tot_either", "tot_both", "tot_gold"):
            require(isinstance(row.get(field), int) and row[field] >= 0,
                    f"invalid P4 field {field}: {key}")
        require(row.get("clean_original_rule") in (0, 1), f"invalid clean rule: {key}")
        features[key] = row
    expected = {(d, str(r["query_id"])) for d in DATASETS for r in rows_by_dataset[d]["rows"]}
    require(set(features) == expected, "P4 features do not cover exactly the frozen 800-question panel")
    for d in DATASETS:
        for row in rows_by_dataset[d]["rows"]:
            require(features[(d, str(row["query_id"]))]["task"] == row["task"], "P4 task mismatch")
    for name, selector in STRATA.items():
        count = sum(selector(f) for f in features.values())
        require(count == STRATA_N[name], f"frozen P4 stratum {name}: expected {STRATA_N[name]}, got {count}")
    return features


def wilson(k, n, z=1.959964):
    if n == 0:
        return [float("nan")] * 2
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [c - h, c + h]


def binom_two_sided(k, n):
    if n == 0:
        return float("nan")
    pmf = [math.comb(n, i) * 0.5 ** n for i in range(n + 1)]
    return min(1.0, sum(p for p in pmf if p <= pmf[k] * (1 + 1e-12)))


def load(outdir: pathlib.Path):
    lock = verify_lock()
    M = json.loads((HERE / "models.json").read_text())
    entries = M["primary_family"] + M["optional_tier"]
    tier = {m["key"]: t for t in ("primary_family", "optional_tier") for m in M[t]}
    # First inspect execution metadata only. Never open outcome records before
    # every primary job (and any started optional tier) has a terminal state.
    completed, status = {}, {}
    for m in entries:
        k = m["key"]; completed[k] = {}
        if tier[k] == "optional_tier" and not (outdir / k).exists():
            status[k] = "not executed (optional tier not started)"
            continue
        for d in DATASETS:
            base = outdir / k / d
            atts = sorted(base.glob("attempt*"), key=lambda p: p.name) if base.exists() else []
            require(atts, f"analysis blocked: job {k}/{d} has no terminal attempt")
            require([p.name for p in atts] == [f"attempt{i}" for i in range(1, len(atts) + 1)]
                    and len(atts) <= 3, f"invalid attempt sequence: {k}/{d}")
            configuration = None
            for i, p in enumerate(atts, 1):
                path = p / "attempt_status.json"
                require(path.is_file(), f"analysis blocked: missing attempt status: {p}")
                state = json.loads(path.read_text())
                require((state.get("study"), state.get("model_key"), state.get("dataset"), state.get("attempt"))
                        == (STUDY, k, d, i), f"attempt identity mismatch: {p}")
                digest = state.get("configuration_sha256", "")
                require(re.fullmatch(r"[0-9a-f]{64}", digest) is not None, f"missing configuration hash: {p}")
                require(configuration is None or digest == configuration, f"retry configuration changed: {p}")
                configuration = digest
                if i < len(atts):
                    require(state.get("status") == "failed" and state.get("failure_kind") == "technical",
                            f"retry after nontechnical failure/success: {p}")
                elif state.get("status") == "succeeded":
                    completed[k][d] = (p, state)
                else:
                    require(i == 3 and state.get("status") == "failed" and state.get("failure_kind") == "technical",
                            f"analysis blocked: job not terminal: {p} ({state.get('status')})")
        status[k] = "executed" if len(completed[k]) == 4 else f"not executed ({len(completed[k])}/4 datasets complete)"

    data = {}
    for m in entries:
        k = m["key"]
        if status[k] != "executed":
            continue
        per = {}
        for d in DATASETS:
            p, state = completed[k][d]
            meta = json.loads((p / "run_meta.json").read_text())
            require((meta.get("study"), meta.get("dataset"), meta.get("n"), meta.get("attempt"), meta.get("status"))
                    == (STUDY, d, EXPECTED_N[d], state["attempt"], "succeeded"), f"run metadata mismatch: {p}")
            require(meta.get("configuration_sha256") == state["configuration_sha256"], f"run configuration mismatch: {p}")
            require(meta.get("lock") == lock["files"], f"run used a different lock: {p}")
            require(all(meta.get("model", {}).get(f) == m[f] for f in ("key", "model_id", "revision")),
                    f"run model/revision mismatch: {p}")
            raw = p / f"{k}__{d}__records.jsonl"
            require(sha_file(raw) == meta.get("records_sha256"), f"records SHA256 mismatch: {p}")
            rows = [json.loads(x) for x in raw.read_text(encoding="utf-8").splitlines() if x.strip()]
            require(len(rows) == EXPECTED_N[d] and len({str(r["query_id"]) for r in rows}) == EXPECTED_N[d],
                    f"panel count or duplicate question mismatch: {p}")
            for r in rows:
                require(r.get("dataset") == d and r.get("model_key") == k, f"record identity mismatch: {p}")
                for f in ("reference_single_correct", "random_single_correct", "reference_fixed16_correct",
                          "intervention_changed", "floor_changed", "canonical_changed", "correct_to_wrong", "wrong_to_correct"):
                    require(type(r.get(f)) is bool, f"non-boolean record field {f}: {p}")
                ref, rnd, floor = (r[f"{c}_correct"] for c in ("reference_single", "random_single", "reference_fixed16"))
                require(r["intervention_changed"] == (ref != rnd) and r["floor_changed"] == (ref != floor)
                        and r["correct_to_wrong"] == (ref and not rnd) and r["wrong_to_correct"] == (not ref and rnd),
                        f"derived record flags mismatch: {p}")
            per[d] = {"rows": rows, "meta": meta, "attempt": p.name}
        data[k] = per
    return M, entries, tier, data, status


def vec(per, field):
    return {d: np.array([bool(r[field]) for r in per[d]["rows"]], dtype=float) for d in DATASETS}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir", type=pathlib.Path)
    ap.add_argument("--features", type=pathlib.Path, required=True)
    ap.add_argument("--draws", type=int, default=100000)
    a = ap.parse_args()
    require(a.draws == 100000, "registered analysis requires exactly 100000 bootstrap draws")
    require(not any((a.outdir / name).exists() for name in ("SCALE_CURVE_RESULTS.json", "SCALE_CURVE_RESULTS.md")),
            "analysis outputs already exist; preregistered analysis runs once and never overwrites results")
    M, entries, tier, data, status = load(a.outdir)
    keys = [m["key"] for m in entries if m["key"] in data]
    params = {m["key"]: m["params_b"] for m in entries}
    if not keys:
        raise SystemExit("no model completed all datasets")
    # question order must match across models (same frozen panel)
    ref = keys[0]
    for k in keys[1:]:
        for d in DATASETS:
            require([r["query_id"] for r in data[k][d]["rows"]] == [r["query_id"] for r in data[ref][d]["rows"]],
                    f"cross-model question order mismatch: {k}/{d}")
    feat = load_features(a.features, data[ref])

    I = {k: vec(data[k], "intervention_changed") for k in keys}
    F = {k: vec(data[k], "floor_changed") for k in keys}
    C = {k: vec(data[k], "canonical_changed") for k in keys}
    ACCR = {k: vec(data[k], "reference_single_correct") for k in keys}
    ACCX = {k: vec(data[k], "random_single_correct") for k in keys}
    ACCB = {k: vec(data[k], "reference_fixed16_correct") for k in keys}

    def macro(v):
        return float(np.mean([v[d].mean() for d in DATASETS]))

    # ---- joint, paired, dataset-stratified bootstrap (same resampled questions for every model) ----
    rng = np.random.default_rng(SEED)
    B = a.draws; CH = 5000
    fields = ("I", "F", "E", "E_num", "C", "dacc", "dacc_num", "R", "X", "B",
              "pooled_I", "pooled_F", "pooled_E", "pooled_C", "pooled_R", "pooled_X", "pooled_B", "pooled_dacc")
    stats = {k: {f: [] for f in fields} for k in keys}
    vectors = {"I": I, "F": F, "C": C, "R": ACCR, "X": ACCX, "B": ACCB}
    for s in range(0, B, CH):
        b = min(CH, B - s)
        idx = {d: rng.integers(0, EXPECTED_N[d], size=(b, EXPECTED_N[d])) for d in DATASETS}
        for k in keys:
            numerators, pooled = {}, {}
            for name, values in vectors.items():
                counts = {d: values[k][d][idx[d]].sum(1).astype(np.int64) for d in DATASETS}
                numerators[name] = sum(counts[d] * MACRO_WEIGHTS[d] for d in DATASETS)
                pooled[name] = sum(counts.values()) / 800
                stats[k][name].append(numerators[name] / MACRO_DENOM)
                stats[k]["pooled_" + name].append(pooled[name])
            en = numerators["I"] - numerators["F"]
            an = numerators["X"] - numerators["R"]
            stats[k]["E_num"].append(en); stats[k]["E"].append(en / MACRO_DENOM)
            stats[k]["dacc_num"].append(an); stats[k]["dacc"].append(an / MACRO_DENOM)
            stats[k]["pooled_E"].append(pooled["I"] - pooled["F"])
            stats[k]["pooled_dacc"].append(pooled["X"] - pooled["R"])

    for k in keys:
        for f in stats[k]:
            stats[k][f] = np.concatenate(stats[k][f])

    def ci(x, lo=2.5, hi=97.5):
        return [float(np.percentile(x, lo)), float(np.percentile(x, hi))]

    res = {}; exact_excess = {}; exact_intervals = {}
    for k in keys:
        per_ds = {}
        for d in DATASETS:
            rows = data[k][d]["rows"]
            per_ds[d] = {"n": len(rows), "intervention_changed": int(I[k][d].sum()), "floor_changed": int(F[k][d].sum()),
                         "correct_to_wrong": sum(r["correct_to_wrong"] for r in rows),
                         "wrong_to_correct": sum(r["wrong_to_correct"] for r in rows),
                         "canonical_changed": int(C[k][d].sum()),
                         "acc_reference": float(ACCR[k][d].mean()), "acc_random": float(ACCX[k][d].mean()),
                         "acc_reference_fixed16": float(ACCB[k][d].mean())}
        ctw = sum(v["correct_to_wrong"] for v in per_ds.values()); wtc = sum(v["wrong_to_correct"] for v in per_ds.values())
        exact_excess[k] = macro_numerator(I[k]) - macro_numerator(F[k])
        exact_intervals[k] = ci(stats[k]["E_num"])
        Em = exact_excess[k] / MACRO_DENOM
        dacc = (macro_numerator(ACCX[k]) - macro_numerator(ACCR[k])) / MACRO_DENOM
        dci90_num = ci(stats[k]["dacc_num"], 5, 95)
        dci90 = [v / MACRO_DENOM for v in dci90_num]
        pooled = lambda values: sum(int(values[d].sum()) for d in DATASETS) / 800
        res[k] = {"tier": tier[k], "params_b": params[k], "per_dataset": per_ds,
                  "macro_intervention": macro(I[k]), "macro_intervention_ci95": ci(stats[k]["I"]),
                  "macro_floor": macro(F[k]), "macro_floor_ci95": ci(stats[k]["F"]),
                  "macro_excess": Em, "macro_excess_ci95": [v / MACRO_DENOM for v in exact_intervals[k]],
                  "pooled_intervention": pooled(I[k]), "pooled_intervention_ci95": ci(stats[k]["pooled_I"]),
                  "pooled_floor": pooled(F[k]), "pooled_floor_ci95": ci(stats[k]["pooled_F"]),
                  "pooled_excess": pooled(I[k]) - pooled(F[k]), "pooled_excess_ci95": ci(stats[k]["pooled_E"]),
                  "macro_canonical": macro(C[k]), "macro_canonical_ci95": ci(stats[k]["C"]),
                  "pooled_canonical": pooled(C[k]), "pooled_canonical_ci95": ci(stats[k]["pooled_C"]),
                  "direction": {"correct_to_wrong": ctw, "wrong_to_correct": wtc, "binomial_p": binom_two_sided(min(ctw, wtc), ctw + wtc) if ctw + wtc else None},
                  "accuracy": {"macro_reference": macro(ACCR[k]), "macro_reference_ci95": ci(stats[k]["R"]),
                               "macro_random": macro(ACCX[k]), "macro_random_ci95": ci(stats[k]["X"]),
                               "macro_reference_fixed16": macro(ACCB[k]), "macro_reference_fixed16_ci95": ci(stats[k]["B"]),
                               "macro_difference": dacc, "difference_ci90": dci90,
                               "pooled_reference": pooled(ACCR[k]), "pooled_reference_ci95": ci(stats[k]["pooled_R"]),
                               "pooled_random": pooled(ACCX[k]), "pooled_random_ci95": ci(stats[k]["pooled_X"]),
                               "pooled_reference_fixed16": pooled(ACCB[k]), "pooled_reference_fixed16_ci95": ci(stats[k]["pooled_B"]),
                               "pooled_difference": pooled(ACCX[k]) - pooled(ACCR[k]),
                               "pooled_difference_ci90": ci(stats[k]["pooled_dacc"], 5, 95),
                               "equivalent_within_5pp": bool(dci90_num[0] > -150 and dci90_num[1] < 150)},
                  "checks": {d: data[k][d]["meta"]["checks"] for d in DATASETS},
                  "attempts": {d: data[k][d]["attempt"] for d in DATASETS}}

    def decide(k):
        return decision(exact_excess[k], exact_intervals[k]) if k in res else "not executed"

    prim = [k for k in keys if tier[k] == "primary_family"]
    H1 = decide(H1_MODEL)
    H2 = ("supported" if prim and all(exact_intervals[k][0] > 60 for k in prim) else "not supported")
    H2_complete = len(prim) == len(M["primary_family"])
    # H3: OLS slope of excess on log10(params) across executed primary sizes, joint bootstrap CI
    H3 = None
    if len(prim) >= 3:
        x = np.log10([params[k] for k in prim]); xc = x - x.mean()
        Y = np.vstack([stats[k]["E"] for k in prim])  # (models, draws)
        slope_b = (xc[:, None] * (Y - Y.mean(0))).sum(0) / (xc ** 2).sum()
        y = np.array([res[k]["macro_excess"] for k in prim])
        slope = float((xc * (y - y.mean())).sum() / (xc ** 2).sum())
        lo, hi = ci(slope_b)
        H3 = {"slope_excess_per_decade_params": slope, "ci95": [lo, hi], "models": prim,
              "classification": "decreasing" if hi < 0 else ("increasing" if lo > 0 else "no detectable trend"),
              "note": "within the tested range only; no extrapolation"}
    S6 = {k: decide(k) for k in keys if tier[k] == "optional_tier"}

    # S4 cross-scale overlap of flipped questions (primary sizes)
    S4 = None
    if len(prim) >= 2:
        flips = {k: np.concatenate([I[k][d] for d in DATASETS]).astype(bool) for k in prim}
        pairs = {}
        for i, k1 in enumerate(prim):
            for k2 in prim[i + 1:]:
                a1, a2 = flips[k1], flips[k2]
                inter = int((a1 & a2).sum()); uni = int((a1 | a2).sum())
                n11, n10, n01, n00 = inter, int((a1 & ~a2).sum()), int((~a1 & a2).sum()), int((~a1 & ~a2).sum())
                orr = ((n11 + .5) * (n00 + .5)) / ((n10 + .5) * (n01 + .5))
                pairs[f"{k1}|{k2}"] = {"jaccard": inter / uni if uni else None, "both": inter, "odds_ratio_haldane": orr}
        cnt = sum(flips[k].astype(int) for k in prim)
        obs = float(cnt.var())
        obs_sumsq = int(np.dot(cnt, cnt))
        prng = np.random.default_rng(SEED + 1); P = 10000; ge = 0
        offs = np.cumsum([0] + [EXPECTED_N[d] for d in DATASETS])
        for _ in range(P):
            tot = np.zeros(800, dtype=int)
            for k in prim:
                v = flips[k].astype(int).copy()
                for j in range(4):
                    seg = v[offs[j]:offs[j + 1]]; prng.shuffle(seg); v[offs[j]:offs[j + 1]] = seg
                tot += v
            # The total count is fixed by permutation, so integer sum-of-squares
            # orders variance exactly and preserves ties without roundoff.
            ge += int(np.dot(tot, tot)) >= obs_sumsq
        S4 = {"pairs": pairs, "fragility_count_distribution": {int(c): int((cnt == c).sum()) for c in range(len(prim) + 1)},
              "variance_of_count": obs, "permutation_p_concentration": (ge + 1) / (P + 1), "permutations": P}

    # S5 uses the required, validated frozen P4 panel; no stratum-specific floor.
    S5 = {}
    for k in keys:
        S5[k] = {}
        for name, fn in STRATA.items():
            sel = [(d, i) for d in DATASETS for i, r in enumerate(data[k][d]["rows"])
                   if fn(feat[(d, str(r["query_id"]))])]
            kk = int(sum(I[k][d][i] for d, i in sel))
            S5[k][name] = {"n": len(sel), "changed": kk, "rate": kk / len(sel), "wilson95": wilson(kk, len(sel))}

    out = {"study": "RIDI-RAG-QWEN3-SCALE-CURVE-v1", "status": status, "bootstrap": {"draws": B, "seed": SEED,
           "scheme": "joint paired resampling of questions within dataset, shared across models; equal dataset weights"},
           "features_sha256": sha_file(a.features), "analysis_lock": verify_lock(),
           "results": res,
           "H1_persistence_at_32B": H1, "H2_persistence_all_sizes": H2, "H2_all_primary_sizes_executed": H2_complete,
           "H3_scale_trend": H3, "S6_optional_tier": S6, "S4_cross_scale_overlap": S4, "S5_content_strata": S5,
           "decision_rules": {"support": "macro excess >= 5 pp and 95% lower bound > 2 pp",
                              "falsified": "95% upper bound < 2 pp", "otherwise": "inconclusive"}}
    (a.outdir / "SCALE_CURVE_RESULTS.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    L = ["# RIDI-RAG-QWEN3-SCALE-CURVE-v1 — results", "",
         f"H1 (persistence at Qwen3-32B): **{H1}**", f"H2 (lower bound > 2 pp at every executed size): **{H2}** (all six sizes executed: {H2_complete})",
         f"H3 (trend in log10 parameters): **{H3['classification'] if H3 else 'not estimable'}**"
         + (f", slope {100*H3['slope_excess_per_decade_params']:+.2f} pp per tenfold parameters (95% CI {100*H3['ci95'][0]:+.2f} to {100*H3['ci95'][1]:+.2f})" if H3 else ""), "",
         "| Model | Params (B) | Intervention | Floor | Excess (95% CI) | C→W / W→C | Accuracy Δ (90% CI) |", "|---|---:|---:|---:|---:|---:|---:|"]
    for k in keys:
        r = res[k]
        L.append(f"| {k} | {r['params_b']} | {100*r['macro_intervention']:.2f}% | {100*r['macro_floor']:.2f}% | "
                 f"{100*r['macro_excess']:.2f} ({100*r['macro_excess_ci95'][0]:.2f}–{100*r['macro_excess_ci95'][1]:.2f}) | "
                 f"{r['direction']['correct_to_wrong']} / {r['direction']['wrong_to_correct']} | "
                 f"{100*r['accuracy']['macro_difference']:+.2f} ({100*r['accuracy']['difference_ci90'][0]:+.2f} to {100*r['accuracy']['difference_ci90'][1]:+.2f}) |")
    for k, v in status.items():
        if v != "executed":
            L.append(f"\n{k}: {v}")
    (a.outdir / "SCALE_CURVE_RESULTS.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
