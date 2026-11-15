"""Standalone domain-separated bootstrap audit adapted by extracting the unchanged
RIDI-24 section from analyze_v27_1.py. It uses the original frozen scoring CSV,
20,000 draws, 2026102901 seed and registered 300-case tie rule. No DDI files needed.
"""
from pathlib import Path
import os
import json
import numpy as np
import pandas as pd
S = str(Path(__file__).resolve().parent)
OUT = S
SEED_RIDI = 2026102901
r = pd.read_csv(os.path.join(S, "RIDI24_scores_registered.csv"))
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
json.dump(res_r, open(os.path.join(OUT, "ridi24_domain_separated_REGENERATED.json"), "w"), indent=1)
print("done", OUT)
