#!/usr/bin/env python
"""v27.1 corrected post hoc analyses on existing RIDI case records (no new generation).
Run from the package root:  python 6_revision_analysis/analyze_v27.py
Inputs: 5_source_data/*.csv and the scale-curve raw records inside
5_source_data/archive/RIDI_v22_REVIEWER_EVIDENCE.zip (public_deposit_archives/RIDI_ScaleCurve_A1_Results_20261013.zip).
Outputs: 6_revision_analysis/results/*_v27_1.json / .csv
All analyses are post hoc and descriptive; registered endpoints are not altered.
"""
import json, re, glob, os, sys, zipfile, io, time
import numpy as np, pandas as pd
from scipy.stats import rankdata, binomtest
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
S = os.path.join(ROOT, "5_source_data"); OUT = os.path.join(ROOT, "6_revision_analysis", "results"); os.makedirs(OUT, exist_ok=True)
SEED_AUC, SEED_RIDI = 20261029, 2026102901

# ---------- 1. transition decomposition (six Qwen3 sizes, primary panel) ----------
def load_scale_records():
    outer = zipfile.ZipFile(os.path.join(S, "archive", "RIDI_v22_REVIEWER_EVIDENCE.zip"))
    inner_name = [n for n in outer.namelist() if n.endswith("RIDI_ScaleCurve_A1_Results_20261013.zip")][0]
    inner = zipfile.ZipFile(io.BytesIO(outer.read(inner_name)))
    recs, feats = [], None
    for n in inner.namelist():
        if n.endswith("__records.jsonl") and "/combined_A1/" in n:
            recs += [json.loads(l) for l in inner.read(n).decode().splitlines() if l.strip()]
        if n.endswith("locked_code/per_question_features.jsonl"):
            feats = pd.read_json(io.BytesIO(inner.read(n)), lines=True)
    return pd.DataFrame(recs), feats
sc, feat = load_scale_records()
assert len(sc) == 4800 and not sc.duplicated(["model_key", "dataset", "query_id"]).any()
scale_csv = pd.read_csv(os.path.join(S, "Scale_4800_paired_correctness.csv"))
chk = scale_csv.merge(sc, left_on=["model", "dataset", "query_id"], right_on=["model_key", "dataset", "query_id"])
assert (chk.reference == chk.reference_single_correct.astype(int)).all() and (chk.exchange == chk.random_single_correct.astype(int)).all()

ABST = re.compile(r"^\W*(INSUFFICIENT|NOT_ENOUGH_INFO|NOT ENOUGH INFO|Verdict:\s*NOT_ENOUGH_INFO)", re.I)
ABST2 = re.compile(r"INSUFFICIENT|NOT_ENOUGH_INFO|not enough information|do(es)? not (give|provide|mention|contain)|cannot be determined|no information", re.I)
def is_abst(a):
    a = str(a).strip(); return bool(ABST.search(a)) or bool(ABST2.search(a[:80]))
def classify(ds, ref_c, exc_c, ref_a, exc_a, ref_can, exc_can):
    inc_a = exc_a if exc_c == 0 else ref_a
    if is_abst(inc_a): return "abstention"
    if ds in ("nq", "hotpotqa"):
        ic = str(exc_can if exc_c == 0 else ref_can).lower().split(); cc = str(ref_can if exc_c == 0 else exc_can).lower().split()
        if cc and ic and (set(cc) <= set(ic) or set(ic) <= set(cc)): return "containment"
    return "other"
sc["ref_c"] = sc.reference_single_correct.astype(int); sc["exc_c"] = sc.random_single_correct.astype(int)
sc["chg"] = (sc.ref_c != sc.exc_c).astype(int); sc["reg"] = ((sc.ref_c == 1) & (sc.exc_c == 0)).astype(int); sc["gain"] = ((sc.ref_c == 0) & (sc.exc_c == 1)).astype(int)
sc["ref_abst"] = sc.reference_single_answer.map(is_abst); sc["exc_abst"] = sc.random_single_answer.map(is_abst)
sc["cls"] = [classify(*t) if ch else None for *t, ch in zip(sc.dataset, sc.ref_c, sc.exc_c, sc.reference_single_answer, sc.random_single_answer, sc.reference_single_canonical, sc.random_single_canonical, sc.chg)]
order = ["qwen3-0.6b", "qwen3-1.7b", "qwen3-4b", "qwen3-8b", "qwen3-14b", "qwen3-32b"]
dec = {}
for m in order:
    g = sc[sc.model_key == m]; t = g[g.chg == 1]
    g2 = g.assign(chg_x=((g.chg == 1) & (g.cls != "containment")).astype(int), reg_x=((g.reg == 1) & (g.cls != "containment")).astype(int), gain_x=((g.gain == 1) & (g.cls != "containment")).astype(int))
    rc, rw = g[g.ref_c == 1], g[g.ref_c == 0]
    b = int((g.ref_abst & ~g.exc_abst).sum()); c = int((~g.ref_abst & g.exc_abst).sum())
    dec[m] = dict(n=len(g), changes=int(g.chg.sum()), regressions=int(g.reg.sum()), gains=int(g.gain.sum()),
        macro_change_pct=round(g.groupby("dataset").chg.mean().mean() * 100, 2),
        macro_change_excl_containment_pct=round(g2.groupby("dataset").chg_x.mean().mean() * 100, 2),
        changes_excl_containment=int(g2.chg_x.sum()), regressions_excl_containment=int(g2.reg_x.sum()), gains_excl_containment=int(g2.gain_x.sum()),
        class_counts=t.cls.value_counts().to_dict(),
        class_by_direction={d: t[t.reg == (1 if d == "regression" else 0)].cls.value_counts().to_dict() for d in ["regression", "gain"]},
        class_by_benchmark={d: x.cls.value_counts().to_dict() for d, x in t.groupby("dataset")},
        regression_rate_among_ref_correct_pct=round(rc.reg.mean() * 100, 2), n_ref_correct=len(rc),
        gain_rate_among_ref_wrong_pct=round(rw.gain.mean() * 100, 2), n_ref_wrong=len(rw),
        ref_accuracy_pct=round(g.ref_c.mean() * 100, 2), exc_accuracy_pct=round(g.exc_c.mean() * 100, 2),
        abstention_ref_pct=round(g.ref_abst.mean() * 100, 2), abstention_exc_pct=round(g.exc_abst.mean() * 100, 2),
        abstention_by_benchmark={d: dict(ref=round(x.ref_abst.mean() * 100, 1), exc=round(x.exc_abst.mean() * 100, 1), n=len(x)) for d, x in g.groupby("dataset")},
        regressions_into_abstention=int(((g.reg == 1) & g.exc_abst).sum()), gains_out_of_abstention=int(((g.gain == 1) & g.ref_abst).sum()),
        abstention_mcnemar=dict(ref_only_abstain=b, exchange_only_abstain=c, p_exact=float(binomtest(min(b, c), b + c).pvalue) if b + c else None))
dec["_note"] = "Abstention: incorrect-side answer begins with INSUFFICIENT/NOT_ENOUGH_INFO or an equivalent phrase. Containment (QA only): the token set of one canonical answer is a subset of the other's, i.e. a verbosity/specificity difference under exact matching. Other: all remaining transitions; not independently adjudicated as substantive. Post hoc, rule-based, not human-adjudicated."
json.dump(dec, open(os.path.join(OUT, "transition_decomposition_v27_1.json"), "w"), indent=1)
sc[["model_key", "dataset", "query_id", "ref_c", "exc_c", "chg", "reg", "gain", "cls", "ref_abst", "exc_abst"]].to_csv(os.path.join(OUT, "transition_classes_4800_v27_1.csv"), index=False)

# content strata on the primary 8B exchange using locked per-question judge features
f8 = feat.merge(sc[sc.model_key == "qwen3-8b"][["dataset", "query_id", "chg", "reg", "gain"]], left_on=["dataset", "qid"], right_on=["dataset", "query_id"])
assert (f8.changed == f8.chg).all()
strata = {}
for name, mask in {"no_gold_string_added": f8.added_gold == 0, "gold_string_added": f8.added_gold > 0,
                   "no_gold_string_added_or_removed": (f8.added_gold == 0) & (f8.removed_gold == 0),
                   "all_added_judged_uninformative_by_both_judges": f8.added_either == 0, "some_added_judged_informative_by_either_judge": f8.added_either > 0, "no_added_passage_jointly_informative": f8.added_both == 0, "some_added_passage_jointly_informative": f8.added_both > 0}.items():
    g = f8[mask]; strata[name] = dict(n=int(len(g)), pooled_change_pct=round(g.chg.mean() * 100, 2), macro_change_pct=round(g.groupby("dataset").chg.mean().mean() * 100, 2), regressions=int(g.reg.sum()), gains=int(g.gain.sum()))
json.dump(strata, open(os.path.join(OUT, "primary_content_strata_v27_1.json"), "w"), indent=1)

# ---------- 2. fragility vs difficulty on the transfer panel ----------
def auc(score, y):
    score = np.asarray(score, float); y = np.asarray(y, int); n1 = y.sum(); n0 = len(y) - n1
    if n1 == 0 or n0 == 0: return np.nan
    r = rankdata(score); return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
tr = pd.read_csv(os.path.join(S, "Transfer_800_paired_correctness.csv"))
tr["frag"] = sum((tr[f"predictor_{m}_reference"] != tr[f"predictor_{m}_exchange"]).astype(int) for m in ["1_7b", "4b", "8b"])
tr["difficulty"] = sum((tr[f"predictor_{m}_reference"] == 0).astype(int) for m in ["1_7b", "4b", "8b"]); tr["comb"] = tr.frag + tr.difficulty
rng = np.random.default_rng(SEED_AUC); B = 10000; res = {}
for tgt in ["qwen3_32b", "olmo2_32b"]:
    rc = tr[tr[f"{tgt}_reference"] == 1].reset_index(drop=True); y = (rc[f"{tgt}_exchange"] == 0).astype(int).values
    yall = (tr[f"{tgt}_reference"] != tr[f"{tgt}_exchange"]).astype(int).values; keys = ["frag", "difficulty", "comb"]
    pts = {k: auc(rc[k], y) for k in keys}; idx_by = [np.where(rc.dataset == d)[0] for d in rc.dataset.unique()]
    boots = {k: [] for k in keys + ["frag_minus_diff", "comb_minus_diff"]}
    for _ in range(B):
        ii = np.concatenate([rng.choice(ix, len(ix), replace=True) for ix in idx_by]); a = {k: auc(rc[k].values[ii], y[ii]) for k in keys}
        for k in a: boots[k].append(a[k])
        boots["frag_minus_diff"].append(a["frag"] - a["difficulty"]); boots["comb_minus_diff"].append(a["comb"] - a["difficulty"])
    ci = lambda v: [float(x) for x in np.round(np.nanpercentile(v, [2.5, 97.5]), 3)]
    res[tgt] = dict(n_reference_correct=int(len(rc)), regressions=int(y.sum()), auc_regression={k: round(float(pts[k]), 3) for k in keys}, ci_regression={k: ci(boots[k]) for k in keys},
        fragility_minus_difficulty=dict(point=round(float(pts["frag"] - pts["difficulty"]), 3), ci=ci(boots["frag_minus_diff"])),
        combined_minus_difficulty=dict(point=round(float(pts["comb"] - pts["difficulty"]), 3), ci=ci(boots["comb_minus_diff"])),
        auc_any_change_all800={k: round(float(auc(tr[k], yall)), 3) for k in keys},
        per_benchmark_auc_regression={d: dict(frag=round(float(auc(rc[rc.dataset == d].frag, y[rc.dataset == d])), 3), difficulty=round(float(auc(rc[rc.dataset == d].difficulty, y[rc.dataset == d])), 3), n=int((rc.dataset == d).sum()), regs=int(y[rc.dataset == d].sum())) for d in rc.dataset.unique()},
        regression_rate_by_fragility={int(k): dict(n=int(len(v)), regressions=int(v.sum()), pct=round(float(v.mean()) * 100, 1)) for k, v in pd.Series(y).groupby(rc.frag.values)},
        regression_rate_by_difficulty={int(k): dict(n=int(len(v)), regressions=int(v.sum()), pct=round(float(v.mean()) * 100, 1)) for k, v in pd.Series(y).groupby(rc.difficulty.values)})
res["spearman_frag_difficulty_all800"] = round(float(tr[["frag", "difficulty"]].corr("spearman").iloc[0, 1]), 3)
res["_note"] = "Regression = target reference-correct and exchange-incorrect. Fragility = number of probes (Qwen3-1.7B/4B/8B) changing correctness under independent draw B. Difficulty = number of probes incorrect on the reference input. 10,000 benchmark-stratified bootstrap draws, seed 20261029. Post hoc."
json.dump(res, open(os.path.join(OUT, "transfer_fragility_vs_difficulty_v27_1.json"), "w"), indent=1)

# ---------- 3. execution-floor calibration across 44 executions ----------
rows = []
for m in order:
    g = scale_csv[scale_csv.model == m]; fl = (g.reference != g.batched_reference).astype(int); ch = (g.reference != g.exchange).astype(int)
    rows.append(dict(study="Scale (OSF whjbs)", model=m, panel="primary 800", n=800, floor_pct=round(fl.groupby(g.dataset).mean().mean() * 100, 3), floor_n=int(fl.sum()), intervention_pct=round(ch.groupby(g.dataset).mean().mean() * 100, 2), intervention="passage exchange"))
for tgt, name in [("qwen3_32b", "Qwen3-32B"), ("olmo2_32b", "OLMo-2-32B")]:
    fl = (tr[f"{tgt}_reference"] != tr[f"{tgt}_batched_reference"]).astype(int); ch = (tr[f"{tgt}_reference"] != tr[f"{tgt}_exchange"]).astype(int)
    rows.append(dict(study="Transfer (OSF xrzp5)", model=name, panel="fresh 800", n=800, floor_pct=round(fl.groupby(tr.dataset).mean().mean() * 100, 3), floor_n=int(fl.sum()), intervention_pct=round(ch.groupby(tr.dataset).mean().mean() * 100, 2), intervention="passage exchange"))
rel = pd.read_csv(os.path.join(S, "Release_4800_paired_correctness.csv"))
rel["chg"] = (rel.incumbent_main != rel.successor_main).astype(int); rel["fl_i"] = (rel.incumbent_main != rel.incumbent_floor).astype(int); rel["fl_s"] = (rel.successor_main != rel.successor_floor).astype(int)
for pr_, g in rel.groupby("pair"):
    for role, col in [("incumbent", "fl_i"), ("successor", "fl_s")]:
        rows.append(dict(study="Release (OSF e35tp)", model=f"pair {pr_} {role}", panel="fresh 800", n=800, floor_pct=round(g.groupby("dataset")[col].mean().mean() * 100, 3), floor_n=int(g[col].sum()), intervention_pct=round(g.groupby("dataset").chg.mean().mean() * 100, 2), intervention="model update"))
r = pd.read_csv(os.path.join(S, "RIDI24_scores_registered.csv"))
inc = r[r.model_key.str.endswith("__inc") & (r.arm == "reference")]
pv = inc.pivot_table(index=["model_key", "domain", "qid"], columns="regime", values="correct").dropna(); pv["fl"] = (pv.fixed16 != pv.floor16).astype(int)
for (mk, dom), g in pv.groupby(level=[0, 1]):
    rows.append(dict(study="RIDI-24 (OSF 7uzv5)", model=f'{mk.replace("__inc", "")} [{dom}]', panel=f"{dom} 1500", n=len(g), floor_pct=round(g.fl.mean() * 100, 3), floor_n=int(g.fl.sum()), intervention_pct=None, intervention="model update (incumbent repeat in permuted order)"))
Fdf = pd.DataFrame(rows); Fdf.to_csv(os.path.join(OUT, "execution_floor_calibration_v27_1.csv"), index=False)
summ = {st: dict(n_executions=int(len(g)), median=float(g.floor_pct.median()), max=float(g.floor_pct.max()), min=float(g.floor_pct.min())) for st, g in Fdf.groupby("study")}
summ["all"] = dict(n_executions=int(len(Fdf)), median=float(Fdf.floor_pct.median()), p90=float(Fdf.floor_pct.quantile(.9)), max=float(Fdf.floor_pct.max()), n_above_2pct=int((Fdf.floor_pct > 2).sum()))
ex = Fdf[(Fdf.intervention == "passage exchange") & (Fdf.floor_pct > 0)]; summ["min_exchange_to_floor_ratio"] = float(round((ex.intervention_pct / ex.floor_pct).min(), 1))
json.dump(summ, open(os.path.join(OUT, "execution_floor_summary_v27_1.json"), "w"), indent=1)

# ---------- 4. RIDI-24 domain-separated capture and finance degeneracy ----------
probes = ["qwen3-1.7b", "qwen3-4b", "qwen3-8b"]; pr = r[r.model_key.isin(probes)]
ref = pr[(pr.arm == "reference") & (pr.regime == "fixed16")].pivot_table(index=["domain", "qid"], columns="model_key", values="correct")
exc = pr[pr.arm == "exch_pred"].pivot_table(index=["domain", "qid"], columns="model_key", values="correct")
scores = pd.DataFrame({"D": (ref == 0).sum(axis=1), "F": (ref != exc).sum(axis=1)})
pairs = sorted(set(k.rsplit("__", 1)[0] for k in r.model_key if "__" in k)); data = {}
for pdom in ["medical", "finance"]:
    for pair in pairs:
        i_ = r[(r.model_key == pair + "__inc") & (r.arm == "reference") & (r.regime == "fixed16") & (r.domain == pdom)].set_index("qid").correct
        s_ = r[(r.model_key == pair + "__suc") & (r.arm == "reference") & (r.regime == "fixed16") & (r.domain == pdom)].set_index("qid").correct
        df = pd.DataFrame({"inc": i_, "suc": s_}).join(scores.loc[pdom]); df["DF"] = df.D + df.F; df["reg"] = ((df.inc == 1) & (df.suc == 0)).astype(int); data[(pdom, pair)] = df.sort_index()
def capture_vec(score, elig, reg, B=300):
    sc_ = score[elig]; rg = reg[elig]
    if len(sc_) <= B: return rg.sum()
    o = np.argsort(-sc_, kind="stable"); sc_ = sc_[o]; rg = rg[o]; thr = sc_[B - 1]; above = sc_ > thr; tie = sc_ == thr
    return rg[above].sum() + rg[tie].sum() * (B - above.sum()) / tie.sum()
arr = {k: (v.inc.values == 1, v.reg.values, v.D.values.astype(float), v.DF.values.astype(float), v.F.values.astype(float)) for k, v in data.items()}
def domain_stats(pdom, pair_idx, q_idx):
    tot = {"D": 0., "DF": 0., "F": 0., "naive": 0.}; regs = 0
    for pi in pair_idx:
        elig, reg, Dv, DFv, Fv = [x[q_idx] for x in arr[(pdom, pairs[pi])]]
        tot["D"] += capture_vec(Dv, elig, reg); tot["DF"] += capture_vec(DFv, elig, reg); tot["F"] += capture_vec(Fv, elig, reg)
        tot["naive"] += reg.sum() * min(1, 300 / max(1, elig.sum())); regs += reg.sum()
    return {k: v / regs * 100 for k, v in tot.items()}
point = {pdom: domain_stats(pdom, range(12), np.arange(1500)) for pdom in ["medical", "finance"]}
eq = {k: np.mean([point["medical"][k], point["finance"][k]]) for k in point["medical"]}
assert abs(eq["DF"] - 71.108) < 0.01 and abs(eq["D"] - 69.957) < 0.01, eq   # reproduces the registered equal-domain headline
rng = np.random.default_rng(SEED_RIDI); Bn = 20000; boots = {d: [] for d in ["medical", "finance"]}
for b in range(Bn):
    for pdom in ["medical", "finance"]:
        st = domain_stats(pdom, rng.integers(0, 12, 12), rng.integers(0, 1500, 1500)); boots[pdom].append([st["DF"] - st["D"], st["D"], st["DF"], st["DF"] - st["naive"], st["D"] - st["naive"]])
res_r = {"registered_equal_domain_reproduced": {k: round(float(v), 3) for k, v in eq.items()}}
for pdom in ["medical", "finance"]:
    a = np.array(boots[pdom]); ci = lambda j: [float(x) for x in np.round(np.percentile(a[:, j], [2.5, 97.5]), 3)]
    res_r[pdom] = dict(point={k: round(float(v), 3) for k, v in point[pdom].items()}, DF_minus_D=dict(point=round(float(point[pdom]["DF"] - point[pdom]["D"]), 3), ci95=ci(0)), D_ci95=ci(1), DF_ci95=ci(2),
                       DF_minus_naive=dict(point=round(float(point[pdom]["DF"] - point[pdom]["naive"]), 3), ci95=ci(3)), D_minus_naive=dict(point=round(float(point[pdom]["D"] - point[pdom]["naive"]), 3), ci95=ci(4)))
deg = []
for pair in pairs:
    df = data[("finance", pair)]; ne = int((df.inc == 1).sum()); deg.append(dict(pair=pair, n_eligible=ne, regressions=int(df.reg.sum()), budget_covers_all=bool(ne <= 300), coverage_pct=round(min(1, 300 / ne) * 100, 1), incumbent_accuracy_pct=round(float(df.inc.mean()) * 100, 1)))
res_r["finance_degeneracy"] = deg; res_r["n_finance_pairs_budget_covers_all_eligible"] = int(sum(d["budget_covers_all"] for d in deg))
res_r["_note"] = "Post hoc domain-separated re-analysis of registered RIDI-24 outcomes; two-stage bootstrap (12 pairs with replacement, then one shared 1,500-question draw), 20,000 draws, seed 2026102901; fixed 300-case budget as registered. Not a replacement for the registered equal-domain primary."
json.dump(res_r, open(os.path.join(OUT, "ridi24_domain_separated_v27_1.json"), "w"), indent=1)
print("done", OUT)
