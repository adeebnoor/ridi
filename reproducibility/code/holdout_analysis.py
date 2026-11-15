"""RIDI confirmatory holdout — frozen analysis (H1–H4). Version 1.0, 2 November 2026.

Inputs (CSV, UTF-8):
  flags.csv  : dataset,qid,E1_win,E2_win,E3_win,E1_dense,E3_dense        (0/1; computed before generation)
  scores.csv : dataset,qid,model,arm,scorer,correct
               arm    in {bm25_whole, bm25_window, contriever, whole_rep_b1, whole_rep_b16}
               scorer in {frozen, format}; correct in {0,1}
Output: JSON report to stdout (and --out).

Definitions (fixed before any holdout output):
  change(q, m, X vs Y)  = correct[X] != correct[Y]
  control(q, m)         = 1 if any of {bm25_whole, whole_rep_b1, whole_rep_b16} disagree (conservative floor)
  rate                  = equal-weight mean of per-benchmark rates (primary); pooled rate reported too
  excess                = rate(change) - rate(control), same questions, paired
  H1 (per model, E1_win, frozen scorer): supported if one-sided bootstrap P(excess <= 0.02) passes Holm
      across the two models at one-sided alpha = 0.025 (equivalent to a 95% lower bound above 2 points).
  H2: as H1 within E3_win (descriptive if fewer than 100 questions).
  H3: contriever vs bm25_whole within E1_dense, per model and per benchmark (excess over control).
  H4: overlap of changed questions between models; either-model rate with exact 95% CI.
"""
import argparse, csv, json, random, sys
from collections import defaultdict
from scipy.stats import beta

SEED = 20261102
DRAWS = 20000
MARGIN = 0.02
ALPHA = 0.025

def cp(k, n):
    if n == 0: return [None, None]
    lo = 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(0.975, k + 1, n - k)
    return [round(lo, 4), round(hi, 4)]

def load(flags_path, scores_path, scorer):
    flags = {}
    for r in csv.DictReader(open(flags_path, encoding='utf8')):
        flags[(r['dataset'], r['qid'])] = {k: int(v) for k, v in r.items() if k.startswith('E')}
    sc = defaultdict(dict)
    for r in csv.DictReader(open(scores_path, encoding='utf8')):
        if r['scorer'] != scorer: continue
        sc[(r['dataset'], r['qid'], r['model'])][r['arm']] = int(r['correct'])
    return flags, sc

def indicators(flags, sc, model, gate, a, b):
    """Per question: (dataset, change, control); questions missing any arm are excluded and counted."""
    rows, missing = [], 0
    for (ds, q), f in flags.items():
        if not f.get(gate): continue
        s = sc.get((ds, q, model), {})
        need = [a, b, 'bm25_whole', 'whole_rep_b1', 'whole_rep_b16']
        if any(x not in s for x in need): missing += 1; continue
        ctrl = int(len({s['bm25_whole'], s['whole_rep_b1'], s['whole_rep_b16']}) > 1)
        rows.append((ds, int(s[a] != s[b]), ctrl, q))
    return rows, missing

def eqw(rows, idx):
    by = defaultdict(list)
    for r in rows: by[r[0]].append(r[idx])
    return sum(sum(v) / len(v) for v in by.values()) / len(by) if by else float('nan')

def boot(rows, rng):
    """Within-benchmark question bootstrap of the paired excess (equal benchmark weights)."""
    import numpy as np
    g = np.random.default_rng(rng.randrange(2**32))
    by = defaultdict(list)
    for r in rows: by[r[0]].append(r)
    acc = np.zeros(DRAWS)
    for v in by.values():
        d = np.array([r[1] - r[2] for r in v], dtype=float)
        idx = g.integers(0, len(v), size=(DRAWS, len(v)))
        acc += d[idx].mean(axis=1)
    out = sorted((acc / len(by)).tolist()); return out

def summarize(rows, missing, rng, test=True):
    n = len(rows); k = sum(r[1] for r in rows); c = sum(r[2] for r in rows)
    res = {'n': n, 'excluded_missing_arm': missing, 'changes': k, 'control_changes': c,
           'change_rate_eqw': eqw(rows, 1) if n else None, 'control_rate_eqw': eqw(rows, 2) if n else None,
           'change_rate_pooled': k / n if n else None, 'change_exact95': cp(k, n), 'control_exact95': cp(c, n)}
    if n and test:
        bs = boot(rows, rng)
        res['excess_eqw'] = res['change_rate_eqw'] - res['control_rate_eqw']
        res['excess_95ci'] = [bs[int(0.025 * DRAWS)], bs[int(0.975 * DRAWS) - 1]]
        res['p_one_sided_excess_le_margin'] = sum(1 for x in bs if x <= MARGIN) / DRAWS
    return res

def holm(pvals):
    order = sorted(pvals, key=pvals.get); m = len(order); out = {}; stop = False
    for i, k in enumerate(order):
        ok = (not stop) and pvals[k] <= ALPHA / (m - i)
        out[k] = ok; stop = stop or not ok
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--flags', required=True); ap.add_argument('--scores', required=True)
    ap.add_argument('--models', nargs='+', default=['Qwen3-8B', 'Mistral-7B-Instruct-v0.3'])
    ap.add_argument('--out')
    a = ap.parse_args()
    report = {'version': '1.0', 'seed': SEED, 'draws': DRAWS, 'margin': MARGIN}
    for scorer in ('frozen', 'format'):
        flags, sc = load(a.flags, a.scores, scorer)
        rng = random.Random(SEED)
        R = {'H1': {}, 'H2': {}, 'H3': {}, 'H4': {}}
        changed = {}
        for m in a.models:
            rows, miss = indicators(flags, sc, m, 'E1_win', 'bm25_whole', 'bm25_window')
            R['H1'][m] = summarize(rows, miss, rng)
            changed[m] = {(r[0], r[3]) for r in rows if r[1]}
            rows3, miss3 = indicators(flags, sc, m, 'E3_win', 'bm25_whole', 'bm25_window')
            R['H2'][m] = summarize(rows3, miss3, rng, test=len(rows3) >= 100)
            R['H2'][m]['descriptive_only'] = len(rows3) < 100
            rowsd, missd = indicators(flags, sc, m, 'E1_dense', 'bm25_whole', 'contriever')
            R['H3'][m] = {'all': summarize(rowsd, missd, rng)}
            for ds in sorted({r[0] for r in rowsd}):
                R['H3'][m][ds] = summarize([r for r in rowsd if r[0] == ds], 0, rng)
        if scorer == 'frozen':
            dec = holm({m: R['H1'][m]['p_one_sided_excess_le_margin'] for m in a.models if 'p_one_sided_excess_le_margin' in R['H1'][m]})
            for m, ok in dec.items(): R['H1'][m]['H1_supported_holm'] = ok
        n1 = len([1 for f in flags.values() if f.get('E1_win')])
        ms = list(changed)
        either = set().union(*changed.values()) if changed else set()
        both = set.intersection(*changed.values()) if len(changed) > 1 else set()
        R['H4'] = {'n_E1': n1, 'either': len(either), 'either_exact95': cp(len(either), n1), 'both': len(both),
                   'only': {m: len(changed[m] - set().union(*(changed[o] for o in ms if o != m))) for m in ms}}
        report[scorer] = R
    txt = json.dumps(report, indent=1, default=float)
    print(txt)
    if a.out: open(a.out, 'w').write(txt)

if __name__ == '__main__':
    main()
