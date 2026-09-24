#!/usr/bin/env python3
"""Post hoc, non-confirmatory diagnostic for the failed P5 qualification gate."""
import json, math, statistics as st, sys
from collections import defaultdict

pairs = json.load(open(sys.argv[1]))['all_pairs']
by = defaultdict(list)
for p in pairs:
    hw_n = (p['ndcg_ci90'][1] - p['ndcg_ci90'][0]) / 2
    hw_r = (p['recall_ci90'][1] - p['recall_ci90'][0]) / 2
    m = max(abs(p['ndcg_ci90'][0]), abs(p['ndcg_ci90'][1]), abs(p['recall_ci90'][0]), abs(p['recall_ci90'][1]))
    sd_n = hw_n * math.sqrt(p['n']) / 1.645 if p['n'] else float('nan')
    sd_r = hw_r * math.sqrt(p['n']) / 1.645 if p['n'] else float('nan')
    by[p['dataset']].append({'pair': f"{p['a']}|{p['b']}", 'n': p['n'], 'hw_ndcg': hw_n, 'hw_recall': hw_r, 'min_margin': m,
                             'n_needed_0.01_at_zero_difference': math.ceil(max((1.645 * sd_n / 0.01) ** 2, (1.645 * sd_r / 0.01) ** 2))})
out = {'status': 'post hoc descriptive diagnostic; does not alter the registered P5 decision', 'datasets': {}}
for ds, rows in sorted(by.items()):
    mm = [r['min_margin'] for r in rows]
    out['datasets'][ds] = {
        'n_pairs': len(rows), 'qualification_n': rows[0]['n'],
        'median_halfwidth_ndcg': st.median(r['hw_ndcg'] for r in rows),
        'median_halfwidth_recall': st.median(r['hw_recall'] for r in rows),
        'smallest_min_margin': min(mm), 'median_min_margin': st.median(mm),
        'pairs_within_0.01': sum(m <= 0.01 for m in mm), 'pairs_within_0.02': sum(m <= 0.02 for m in mm),
        'pairs_within_0.05': sum(m <= 0.05 for m in mm),
        'median_n_needed_for_0.01_at_zero_difference': st.median(r['n_needed_0.01_at_zero_difference'] for r in rows),
        'closest_pairs': sorted(rows, key=lambda r: r['min_margin'])[:5]}
json.dump(out, sys.stdout, indent=2)
