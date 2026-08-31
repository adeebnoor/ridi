"""Layered audit-equivalence on the real ProPublica COMPAS two-year cohort.

An audit that records only cell COUNTS (cells = the variables the audit conditions on)
cannot distinguish any two selections with identical per-cell counts.  Class size = prod_c C(N_c, m_c).
Every member of the class is realisable by a deployable scorer (score 1 on selected, 0 elsewhere),
so the class is not a mathematical strawman: each element is an actual fieldable system.

Layer 0  outcome                      -> a pure performance audit (precision@k, recall@k pinned)
Layer 1  outcome x race               -> + a group-fairness audit (per-race selection counts pinned)
Layer 2  outcome x race x decile      -> + risk-score calibration pinned
Layer 3  outcome x race x decile x sex-> + sex pinned
"""
import pandas as pd, numpy as np, json, math
from math import lgamma

d = pd.read_csv('compas_analysis_min.csv').reset_index(drop=True)
d['black'] = (d.race == "African-American").astype(int)
d['female'] = (d.sex == "Female").astype(int)
N = len(d); P = int(d.two_year_recid.sum())

def log10C(n, k):
    if k < 0 or k > n: return float('-inf')
    return (lgamma(n+1) - lgamma(k+1) - lgamma(n-k+1)) / math.log(10)

K = 1000
dep = d.sort_values(['decile_score','id'], ascending=[False,True]).head(K)
sel = list(dep.index)
d['sel'] = d.index.isin(set(sel)).astype(int)
h = int(dep.two_year_recid.sum())
prec, rec = h/K, h/P

LAYERS = [
    ("outcome",                       ['two_year_recid']),
    ("outcome x race",                ['two_year_recid','black']),
    ("outcome x race x decile",       ['two_year_recid','black','decile_score']),
    ("outcome x race x decile x sex", ['two_year_recid','black','decile_score','female']),
]
TARGETS = [("African-American share", 'black',        '%'),
           ("mean age",               'age',          'y'),
           ("female share",           'female',       '%'),
           ("mean prior convictions", 'priors_count', 'n')]

out = []
for lname, keys in LAYERS:
    logsz = 0.0; ncells = 0
    rng = {}
    for tname, tcol, unit in TARGETS:
        lo_vals, hi_vals = [], []
        for _, cell in d.groupby(keys, sort=False):
            m = int(cell.sel.sum())
            if m == 0: continue
            v = np.sort(cell[tcol].values)
            lo_vals += list(v[:m]); hi_vals += list(v[-m:])
        rng[tname] = (float(np.mean(lo_vals)), float(np.mean(hi_vals)))
    for _, cell in d.groupby(keys, sort=False):
        m = int(cell.sel.sum())
        if m == 0: continue
        ncells += 1; logsz += log10C(len(cell), m)
    obs = {t: float(d.loc[sel, c].mean()) for t, c, _ in TARGETS}
    out.append(dict(layer=lname, cells=ncells, log10class=round(logsz,1),
                    observed={k: round(v,4) for k,v in obs.items()},
                    ranges={k: [round(a,4), round(b,4)] for k,(a,b) in rng.items()}))

print(f"COMPAS two-year cohort: N={N}, positives={P} ({P/N:.1%}), African-American {int(d.black.sum())} ({d.black.mean():.1%})")
print(f"Deployed top-{K} by decile_score: precision@{K}={prec:.4f}  recall={rec:.4f}\n")
hdr = f"{'audit conditions on':<32}{'cells':>6}{'log10|class|':>13}   " + "".join(f"{t[0]:>24}" for t in TARGETS)
print(hdr); print('-'*len(hdr))
for r in out:
    row = f"{r['layer']:<32}{r['cells']:>6}{r['log10class']:>13}   "
    for tname, tcol, unit in TARGETS:
        a, b = r['ranges'][tname]
        s = f"{a*100:.1f}-{b*100:.1f}%" if unit == '%' else f"{a:.2f}-{b:.2f}"
        row += s.rjust(24)
    print(row)
print()
print("deployed (observed): " + ",  ".join(
    (f"{t[0]}={out[0]['observed'][t[0]]*100:.1f}%" if t[2] == '%' else f"{t[0]}={out[0]['observed'][t[0]]:.2f}")
    for t in TARGETS))
json.dump(dict(K=K, N=N, P=P, precision=prec, recall=rec, layers=out),
          open('layered_results.json', 'w'), indent=1)
