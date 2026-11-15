#!/usr/bin/env python3
"""RIDI-CONFIRM-C: post-outcome check of the registered reference-answer exclusion (v51, 13 November 2026).

The addendum (section 6) excludes questions without a reference answer. The saved score table
(scores_commercial.csv) nevertheless contains the 174 Natural Questions items that are absent from
the open-weight RIDI-CONFIRM score table (which holds the 1,326 questions with an accepted
reference); every one of their cells is scored 0.

This script (1) documents that fact, (2) removes those questions and (3) runs the frozen,
unmodified holdout_analysis.py on the remaining scores, with the same model order as the saved
report. It makes no model call and changes no frozen file.

Run from 03_Source_Data:
  python commercial_confirm/posthoc_reference_exclusion_v51/reference_exclusion_sensitivity.py
"""
import csv, hashlib, json, subprocess, sys
from collections import defaultdict
from pathlib import Path
from scipy.stats import beta

SD = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
COMM = SD / 'commercial_confirm' / 'scores_commercial.csv'
OPEN = SD / 'holdout' / 'scores_W_AND_H3_D_REAL.csv'
FLAGS = SD / 'holdout' / 'flags_W_AND_H3_D_FROZEN.csv'
ANALYSIS = SD / 'code' / 'holdout_analysis.py'
MODELS = ['claude-sonnet-5.5', 'gemini-3.8-flash', 'gpt-5.4-mini']   # order of the saved report

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
assert sha(ANALYSIS) == '09fe6ee38e535205bc117aa6e212e7d31158cc3686cee776f38c2d7b24d11b3c'
assert sha(FLAGS) == '9b8c8d9f7eae36712a98e7ba919610ed5ca68e00c8ce9e0906eeb7ea5cbd33f0'
assert sha(COMM) == '70d4c6990235099a8f0379f793b0f7e0177d0f21266fde9f1109e2fd3d35b6ec'

with_ref = {(r['dataset'], r['qid']) for r in csv.DictReader(open(OPEN, encoding='utf8'))}
rows = list(csv.DictReader(open(COMM, encoding='utf8')))
comm_q = {(r['dataset'], r['qid']) for r in rows}
no_ref = comm_q - with_ref
cells = [r for r in rows if (r['dataset'], r['qid']) in no_ref]
flags = {(r['dataset'], r['qid']): r for r in csv.DictReader(open(FLAGS, encoding='utf8'))}
audit = {
    'questions_in_open_weight_score_table': len(with_ref),
    'questions_in_commercial_score_table': len(comm_q),
    'questions_only_in_commercial_table': len(no_ref),
    'their_datasets': dict(sorted(defaultdict(int, {d: sum(1 for x in no_ref if x[0] == d) for d in {x[0] for x in no_ref}}).items())),
    'their_score_cells': len(cells),
    'their_score_cells_scored_correct': sum(int(r['correct']) for r in cells),
    'of_which_E1_win': sum(int(flags[q]['E1_win']) for q in no_ref),
    'of_which_E3_win': sum(int(flags[q]['E3_win']) for q in no_ref),
    'of_which_E1_dense': sum(int(flags[q]['E1_dense']) for q in no_ref),
}
assert audit['their_score_cells_scored_correct'] == 0

kept = OUT / 'scores_commercial_reference_available.csv'
with open(kept, 'w', newline='', encoding='utf8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader()
    for r in rows:
        if (r['dataset'], r['qid']) in with_ref: w.writerow(r)

# (a) the saved report is reproduced from the saved score table
chk = OUT / '_replay_as_run.json'
subprocess.run([sys.executable, str(ANALYSIS), '--flags', str(FLAGS), '--scores', str(COMM), '--models', *MODELS, '--out', str(chk)],
               check=True, stdout=subprocess.DEVNULL)
audit['as_run_report_sha256_reproduced'] = sha(chk) == sha(SD / 'commercial_confirm' / 'H1_H4_commercial.json')
chk.unlink()
# (b) frozen analysis with the exclusion applied
rep = OUT / 'H1_H4_commercial_reference_available.json'
subprocess.run([sys.executable, str(ANALYSIS), '--flags', str(FLAGS), '--scores', str(kept), '--models', *MODELS, '--out', str(rep)],
               check=True, stdout=subprocess.DEVNULL)
R = json.load(open(rep))['frozen']
A = json.load(open(SD / 'commercial_confirm' / 'H1_H4_commercial.json'))['frozen']

def cp(k, n):
    lo = 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1); hi = 1.0 if k == n else beta.ppf(0.975, k + 1, n - k)
    return [round(100 * lo, 2), round(100 * hi, 2)]
def line(h, m, r, a):
    return {'hypothesis': h, 'model': m, 'n': r['n'], 'changed': r['changes'], 'control': r['control_changes'],
            'change_rate_pct': round(100 * r['change_rate_eqw'], 2), 'control_rate_pct': round(100 * r['control_rate_eqw'], 2),
            'excess_pp': round(100 * r['excess_eqw'], 2), 'ci95_pp': [round(100 * x, 2) for x in r['excess_95ci']],
            'p_one_sided_vs_2pp': r['p_one_sided_excess_le_margin'], 'holm_supported': r.get('H1_supported_holm'),
            'as_run_n': a['n'], 'as_run_excess_pp': round(100 * a['excess_eqw'], 2), 'as_run_ci95_pp': [round(100 * x, 2) for x in a['excess_95ci']],
            'as_run_holm_supported': a.get('H1_supported_holm')}
table = []
for m in ['gpt-5.4-mini', 'claude-sonnet-5.5', 'gemini-3.8-flash']:
    table.append(line('H1c', m, R['H1'][m], A['H1'][m]))
for m in ['gpt-5.4-mini', 'claude-sonnet-5.5', 'gemini-3.8-flash']:
    table.append(line('H2c', m, R['H2'][m], A['H2'][m]))
for m in ['gpt-5.4-mini', 'claude-sonnet-5.5', 'gemini-3.8-flash']:
    table.append(line('H3c', m, R['H3'][m]['all'], A['H3'][m]['all']))
n_ref_e1 = sum(1 for q, f in flags.items() if int(f['E1_win']) and q in with_ref)
h4 = {'changed_in_at_least_one_model': R['H4']['either'], 'in_all_three': R['H4']['both'], 'only': R['H4']['only'],
      'E1_win_questions_with_reference': n_ref_e1, 'rate_pct': round(100 * R['H4']['either'] / n_ref_e1, 2),
      'exact95_pct': cp(R['H4']['either'], n_ref_e1), 'as_run_denominator': A['H4']['n_E1']}
summary = {'note': 'Post-outcome correction; not a registered analysis. Decisions refer to the frozen rule (Holm, one-sided alpha 0.025, margin 2 points).',
           'audit': audit, 'table': table, 'H4c': h4,
           'report_sha256': sha(rep), 'kept_scores_sha256': sha(kept)}
json.dump(summary, open(OUT / 'reference_exclusion_summary.json', 'w'), indent=1)
print(json.dumps(summary, indent=1))
