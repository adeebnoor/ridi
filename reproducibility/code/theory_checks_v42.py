"""Verification of Proposition 1 (v42). Brute-force checks of every algebraic claim and the
empirical witness computed from Source Data. Run from 03_Source_Data: python code/theory_checks_v42.py"""
import itertools, json
from pathlib import Path
import pandas as pd
D = Path(__file__).resolve().parents[1] / 'figure_data'
out = {}
# (b) feasible changed counts given marginals: exhaustive over all paired 2x2 tables, n<=14
ok = True
for n in range(1, 15):
    feas = {}
    for n11 in range(n+1):
        for n10 in range(n+1-n11):
            for n01 in range(n+1-n11-n10):
                k0, k1, m = n11+n10, n11+n01, n10+n01
                feas.setdefault((k0, k1), set()).add(m)
    for k0 in range(n+1):
        for k1 in range(n+1):
            pred = {m for m in range(n+1) if abs(k1-k0) <= m <= min(k0+k1, 2*n-k0-k1) and (m-(k1-k0)) % 2 == 0}
            ok &= feas.get((k0, k1), set()) == pred
out['b_feasible_range_exhaustive_n1_14'] = ok
# (b) d >= |Delta| and m - |k1-k0| = 2 min(R, I)
ok2 = all(R+I >= abs(I-R) and (R+I)-abs(I-R) == 2*min(R, I) for R in range(60) for I in range(60))
out['b_identities'] = ok2
# (c) itemwise triangle inequality, all 8 label patterns, and exhaustive for vectors n<=6
ok3 = all((a != c) <= (a != b) + (b != c) for a, b, c in itertools.product((0, 1), repeat=3))
for n in range(1, 7):
    for v in itertools.product(itertools.product((0, 1), repeat=3), repeat=n):
        y_ce, y_ce2, y_c2e = zip(*v)  # Y(C,e), Y(C,e'), Y(C',e)
        d = sum(a != c for a, c in zip(y_ce, y_c2e)); f = sum(a != b for a, b in zip(y_ce, y_ce2))
        g = sum(b != c for b, c in zip(y_ce2, y_c2e))
        ok3 &= g >= d - f
out['c_triangle_exhaustive_n1_6'] = ok3
# (a) the five measures are functions of the grade vector (randomized check with positive-only qrels)
import random, math
random.seed(42)
def metrics(lst, qrels, k=10):
    g = [qrels.get(p, 0) for p in lst[:k]]; nrel = sum(1 for v in qrels.values() if v > 0)
    prec = sum(x > 0 for x in g)/k; rec = sum(x > 0 for x in g)/nrel
    dcg = sum((2**x-1)/math.log2(i+2) for i, x in enumerate(g))
    ideal = sorted(qrels.values(), reverse=True)[:k]; idcg = sum((2**x-1)/math.log2(i+2) for i, x in enumerate(ideal))
    rr = next((1/(i+1) for i, x in enumerate(g) if x > 0), 0.0)
    hits = 0; ap = 0.0
    for i, x in enumerate(g):
        if x > 0: hits += 1; ap += hits/(i+1)
    return (prec, rec, dcg/idcg, rr, ap/min(nrel, k)), tuple(g)
ok4 = True
for _ in range(20000):
    rel = random.sample(range(200), random.randint(1, 4)); qrels = {p: 1 for p in rel}
    pool = [p for p in range(200) if p not in qrels]
    lst = random.sample(range(200), 10)
    lst2 = [p if p in qrels else pool.pop(random.randrange(len(pool))) for p in lst]  # exchange uncredited only
    m1, g1 = metrics(lst, qrels); m2, g2 = metrics(lst2, qrels)
    ok4 &= (g1 == g2) and (m1 == m2)
out['a_five_measures_identical_under_exchange_20000_random'] = ok4
# Witness from Source Data
p = pd.read_csv(D/'Primary_800_paired_outcomes.csv')
s = pd.read_csv(D/'Scale_4800_paired_correctness.csv')
n = len(p); k0 = int(p.reference_correct.sum()); k1 = int(p.exchange_correct.sum())
R = int(((p.reference_correct == 1) & (p.exchange_correct == 0)).sum()); I = int(((p.reference_correct == 0) & (p.exchange_correct == 1)).sum())
q8 = s[s.model == 'qwen3-8b'].merge(p, on=['dataset', 'query_id'])
q8['chg'] = (q8.reference != q8.exchange).astype(int); q8['flr'] = (q8.reference != q8.batched_reference).astype(int)
ew = q8.groupby('dataset')[['chg', 'flr']].mean().mean()
w = dict(n=n, grades_identical_all=bool(p.retrieval_metrics_identical.all()), k0=k0, k1=k1, a0_pct=100*k0/n, a1_pct=100*k1/n,
         regressions=R, improvements=I, changed=R+I, d_pooled_pct=100*(R+I)/n, delta_pp=100*(k1-k0)/n,
         feasible_min_pct=100*abs(k1-k0)/n, feasible_max_pct=100*min(k0+k1, 2*n-k0-k1)/n,
         changes_cancelled_in_mean=2*min(R, I), changes_visible_in_mean=abs(I-R),
         scale_8b_matches_primary=bool((q8.reference == q8.reference_correct).all() and (q8.exchange == q8.exchange_correct).all()),
         floor_changed=int(q8.flr.sum()), floor_reg=int(((q8.reference == 1) & (q8.batched_reference == 0)).sum()),
         floor_imp=int(((q8.reference == 0) & (q8.batched_reference == 1)).sum()),
         d_equal_weight_pct=100*ew.chg, f_equal_weight_pct=100*ew.flr, gap_equal_weight_pp=100*(ew.chg-ew.flr))
w['observed_in_feasible_range'] = w['feasible_min_pct'] <= w['d_pooled_pct'] <= w['feasible_max_pct']
out['witness_primary_qwen3_8b'] = w
sizes = {}
for m, g in s.groupby('model'):
    a, b = int(g.reference.sum()), int(g.exchange.sum()); N = len(g); ch = int((g.reference != g.exchange).sum())
    sizes[m] = dict(k0=a, k1=b, changed=ch, floor=int((g.reference != g.batched_reference).sum()),
                    feasible=[100*abs(b-a)/N, 100*min(a+b, 2*N-a-b)/N], inside=abs(b-a) <= ch <= min(a+b, 2*N-a-b))
out['scale_sizes'] = sizes
census = Path(__file__).resolve().parents[1]/'figure_data'/'BEIR_qrels_grade_census_v42.json'
if census.exists(): out['beir_qrels_census'] = json.loads(census.read_text())
out['ALL_CHECKS_PASS'] = bool(ok and ok2 and ok3 and ok4 and w['observed_in_feasible_range'] and w['grades_identical_all'] and all(v['inside'] for v in sizes.values()))
print(json.dumps(out, indent=1))
