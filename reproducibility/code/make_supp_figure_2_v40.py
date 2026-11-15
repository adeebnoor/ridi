"""Supplementary Fig. 2 (v40; post hoc, exploratory). Reads posthoc_v40/Hidden_turnover_by_comparison_v40.csv.
Run from 03_Source_Data:  python code/make_supp_figure_2_v40.py --out rendered"""
import argparse, os, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
ap = argparse.ArgumentParser(); ap.add_argument('--out', default='rendered'); a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 7, 'pdf.fonttype': 42, 'axes.spines.top': False, 'axes.spines.right': False})
d = pd.read_csv('posthoc_v40/Hidden_turnover_by_comparison_v40.csv')
ig, mu = d[d.group == 'Identical grades'], d[d.group == 'Model updates']
fig, (A, Bx) = plt.subplots(1, 2, figsize=(7.2, 3.7), gridspec_kw={'width_ratios': [1, 1.25]})
A.plot([0, 55], [0, 55], ls='--', lw=0.7, c='0.5'); A.text(13.5, 9.5, 'all change visible\nin mean accuracy', fontsize=6, color='0.4', rotation=20)
A.scatter(mu.net_pp.abs(), mu.turnover_pct, s=14, facecolors='none', edgecolors='#999999', lw=0.8, label=f'Model updates, evidence fixed (n = {len(mu)})')
A.scatter(ig.net_pp.abs(), ig.turnover_pct, s=16, c='#c0392b', label=f'Identical relevance grades (n = {len(ig)})')
A.set_xlim(-0.5, 21); A.set_ylim(0, 55); A.set_xlabel('|Net accuracy change| (percentage points)'); A.set_ylabel('Answers whose correctness changed (%)')
A.legend(frameon=False, fontsize=6, loc='upper left', bbox_to_anchor=(0.12, 0.98)); A.text(-0.18, 1.02, 'a', transform=A.transAxes, fontsize=9, fontweight='bold')
ig = ig.reset_index(drop=True); y = range(len(ig))[::-1]
lab = [f"{s.split(' (')[0]}: {c}" for s, c in zip(ig.study, ig.comparison)]
Bx.barh(list(y), ig.turnover_pct, color='#f2d7d5', height=0.7, label='Changed answers')
Bx.errorbar(ig.masked_pct, list(y), xerr=[ig.masked_pct - ig.masked_ci95_low, ig.masked_ci95_high - ig.masked_pct], fmt='o', ms=3, c='#c0392b', lw=0.8, capsize=1.5, label='Cancelled in the mean (95% CI)')
Bx.scatter(ig.net_pp.abs(), list(y), marker='|', s=40, c='k', label='|Net accuracy change|')
Bx.set_yticks(list(y)); Bx.set_yticklabels(lab, fontsize=5.6); Bx.set_xlabel('Percentage of paired answers'); Bx.set_xlim(0, 20)
Bx.legend(frameon=False, fontsize=5.6, loc='upper center', bbox_to_anchor=(0.3, -0.13), ncol=3); Bx.text(-0.02, 1.02, 'b', transform=Bx.transAxes, fontsize=9, fontweight='bold', ha='right')
fig.tight_layout(); fig.savefig(os.path.join(a.out, 'Supplementary_Figure_2.pdf')); fig.savefig(os.path.join(a.out, 'Supplementary_Figure_2.png'), dpi=200)
