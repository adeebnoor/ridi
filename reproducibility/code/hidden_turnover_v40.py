"""Post hoc, exploratory (added in v40; not preregistered).
Hidden turnover: how much paired answer change is invisible to mean accuracy.
For each paired comparison with R regressions and I improvements out of n questions:
  turnover   = (R + I) / n          (answers whose scored correctness changed)
  net        = (I - R) / n          (what mean accuracy shows)
  masked     = 2 min(R, I) / n      (changes cancelled in the mean = turnover - |net|)
  masked_share = 2 min(R, I) / (R + I)
  ratio      = (R + I) / |I - R|    (changed answers per unit of net accuracy change)
95% intervals: 10,000 question-level bootstrap draws (seed 20261110; unstratified;
holdout rows resampled from their archived transition counts).
Uses only files in 03_Source_Data. Run from 03_Source_Data:  python code/hidden_turnover_v40.py
"""
import json, numpy as np, pandas as pd, os
rng = np.random.default_rng(20261110); B = 10000
rows = []
def add(group, study, label, ref, cmp_, source, n=None, R=None, I=None):
    if ref is not None:
        ref = np.asarray(ref, int); cmp_ = np.asarray(cmp_, int)
        reg = (ref == 1) & (cmp_ == 0); imp = (ref == 0) & (cmp_ == 1)
        n = len(ref); R = int(reg.sum()); I = int(imp.sum())
    # bootstrap of masked rate via multinomial over (reg, imp, unchanged)
    p = np.array([R, I, n - R - I]) / n
    draws = rng.multinomial(n, p, size=B)
    m = 2 * np.minimum(draws[:, 0], draws[:, 1]) / n
    t = (draws[:, 0] + draws[:, 1]) / n
    rows.append(dict(group=group, study=study, comparison=label, n=n, regressions=R, improvements=I,
        turnover_pct=100*(R+I)/n, net_pp=100*(I-R)/n, masked_pct=100*2*min(R,I)/n,
        masked_ci95_low=100*np.percentile(m, 2.5), masked_ci95_high=100*np.percentile(m, 97.5),
        turnover_ci95_low=100*np.percentile(t, 2.5), turnover_ci95_high=100*np.percentile(t, 97.5),
        masked_share_pct=100*2*min(R,I)/(R+I) if R+I else np.nan,
        ratio=(R+I)/abs(I-R) if I != R else np.inf, source=source))
fd = 'figure_data/'
# A. identical relevance grades: controlled exchange
# The Qwen3-8B scale panel is the primary panel (same 800 questions and labels; checked below), so it is counted once.
p = pd.read_csv(fd+'Primary_800_paired_outcomes.csv')
s = pd.read_csv(fd+'Scale_4800_paired_correctness.csv')
for m in ['qwen3-0.6b','qwen3-1.7b','qwen3-4b','qwen3-8b','qwen3-14b','qwen3-32b']:
    g = s[s.model == m]
    lab = m.replace('qwen3','Qwen3').replace('b','B') + (' (primary panel)' if m == 'qwen3-8b' else '')
    if m == 'qwen3-8b':
        assert (int(((g.reference==1)&(g.exchange==0)).sum()), int(((g.reference==0)&(g.exchange==1)).sum())) == \
               (int(((p.reference_correct==1)&(p.exchange_correct==0)).sum()), int(((p.reference_correct==0)&(p.exchange_correct==1)).sum())) == (60, 74)
    add('Identical grades', 'Scale study (registered)', lab, g.reference, g.exchange, 'Scale_4800_paired_correctness.csv')
t = pd.read_csv(fd+'Transport_1600_paired_correctness_v23.csv')
for m, lab in [('MISTRAL','Mistral-7B'),('OLMO','OLMo-2-7B')]:
    g = t[t.model == m]
    add('Identical grades', 'Family transfer (registered)', lab, g.reference_correct, g.random_correct, 'Transport_1600_paired_correctness_v23.csv')
tr = pd.read_csv(fd+'Transfer_800_paired_correctness.csv')
for c, lab in [('qwen3_32b','Qwen3-32B'),('olmo2_32b','OLMo-2-32B')]:
    add('Identical grades', 'Large-model transfer (registered)', lab, tr[c+'_reference'], tr[c+'_exchange'], 'Transfer_800_paired_correctness.csv')
e = pd.read_csv(fd+'E2b_711_paired_outcomes.csv')
add('Identical grades', 'Filtered exchange (exploratory)', 'Qwen3-8B', e.reference_single, e.filtered_single, 'E2b_711_paired_outcomes.csv')
# B. identical grades after routine retrieval updates (held-out, registered); counts archived
h = json.load(open('holdout/paired_accuracy_and_replay.json'))['paired_net_accuracy']
for r in h:
    lab = {'qwen3':'Qwen3-8B','mistral':'Mistral-7B'}[r['model']]
    st = {'W':'Held-out segmentation (H1 set)','D':'Held-out dense retrieval (H3 set)'}[r['contrast']]
    add('Identical grades', st, lab, None, None, 'holdout/paired_accuracy_and_replay.json', n=r['n'], R=r['regressions'], I=r['gains'])
# SciFact natural retrieval updates, exact grade-by-rank record (post hoc; 294 question-update pairs; archived counts)
nt = pd.read_csv(fd+'Figure5_natural_transitions_v28.csv').set_index('stratum').loc['exact_grade_vector']
add('Identical grades', 'SciFact natural updates (post hoc)', 'Qwen3-8B, 3 updates', None, None,
    'Figure5_natural_transitions_v28.csv (exact_grade_vector)', n=int(nt.pairs), R=int(nt.regressions), I=int(nt.gains))
# Not included: the three-corpus windowed-BM25 comparison (561 questions), whose archived summary
# (Natural_segmentation_561_summary.json) gives changes but not regressions and improvements separately.
# C. contrast group: model updates with evidence fixed (grades not the manipulated quantity)
rel = pd.read_csv(fd+'Release_4800_paired_correctness.csv')
for k, g in rel.groupby('pair'):
    add('Model updates', 'Public releases (registered)', f'pair {k}', g.incumbent_main, g.successor_main, 'Release_4800_paired_correctness.csv')
u = pd.read_csv(fd+'Figure4_update_cases_v27_1.csv')
for _, r in u.iterrows():
    R = int(r.regressions); I = int(round(R + r.accuracy_difference_pp*15))
    add('Model updates', 'RIDI-24 updates (registered)', f'{r.pair} ({r.domain})', None, None,
        'Figure4_update_cases_v27_1.csv (improvements = regressions + accuracy difference x 1,500/100)', n=1500, R=R, I=I)
df = pd.DataFrame(rows)
os.makedirs('posthoc_v40', exist_ok=True)
df.to_csv('posthoc_v40/Hidden_turnover_by_comparison_v40.csv', index=False)
summ = {}
for gname, g in df.groupby('group'):
    summ[gname] = dict(comparisons=len(g), questions=int(g.n.sum()), changed=int((g.regressions+g.improvements).sum()),
        regressions=int(g.regressions.sum()), improvements=int(g.improvements.sum()),
        median_turnover_pct=float(g.turnover_pct.median()), median_abs_net_pp=float(g.net_pp.abs().median()),
        median_masked_share_pct=float(g.masked_share_pct.median()), min_masked_share_pct=float(g.masked_share_pct.min()),
        max_masked_share_pct=float(g.masked_share_pct.max()),
        median_ratio=float(g.ratio.replace(np.inf, np.nan).median()), comparisons_with_ratio_ge_3=int((g.ratio >= 3).sum()),
        comparisons_with_masked_ci_above_zero=int((g.masked_ci95_low > 0).sum()))
from scipy.stats import binomtest
ig = df[df.group=='Identical grades']
summ['Identical grades']['pooled_sign_test_regressions_vs_improvements_p'] = float(binomtest(int(ig.regressions.sum()), int((ig.regressions+ig.improvements).sum()), 0.5).pvalue)
summ['status'] = 'post hoc, exploratory; added in v40; uses archived paired outcomes only; no new model output'
json.dump(summ, open('posthoc_v40/Hidden_turnover_summary_v40.json','w'), indent=1)
print(df[['group','study','comparison','n','regressions','improvements','turnover_pct','net_pp','masked_pct','masked_share_pct','ratio']].round(2).to_string())
print(json.dumps(summ, indent=1))
