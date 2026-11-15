#!/usr/bin/env python3
"""Score completed commercial runs with the frozen scorer and run the frozen H1–H4 script unmodified.
Refuses to read smoke/ outputs. Run only after all registered runs have finished or stopped."""
import csv, json, sys, subprocess, hashlib, re, importlib.util, argparse
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
FI = HERE / 'frozen_inputs'
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
assert sha(FI / 'scoring.py') == '5b9f02f7a8bcd4df98f3bf28e66017e86e4cfa3e36d495acb6d1e2828488c7ee'
assert sha(FI / 'holdout_analysis.py') == '09fe6ee38e535205bc117aa6e212e7d31158cc3686cee776f38c2d7b24d11b3c'
assert sha(FI / 'flags_W_AND_H3_D_FROZEN.csv') == '9b8c8d9f7eae36712a98e7ba919610ed5ca68e00c8ce9e0906eeb7ea5cbd33f0'
spec = importlib.util.spec_from_file_location('frozen', FI / 'scoring.py'); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
LABELS = ['SUPPORTS', 'REFUTES', 'NOT_ENOUGH_INFO']
def score(ds, text, answers, variant):   # identical logic to frozen_scorer_adapter_v1.py
    text = text or ''
    if variant == 'format': text = re.sub(r"\[\s*\d+(?:\s*[,;\-–]\s*\d+)+\s*\]", " ", text)
    task = 'qa' if ds in ('nq', 'hotpotqa') else 'classification'
    return int(S.is_correct(text, {'answers': answers, 'labels': answers}, task, LABELS if task == 'classification' else None))
ap = argparse.ArgumentParser(); ap.add_argument('--gold', required=True); ap.add_argument('--gold-sha256', default='f899b9727dd6612fca12bc6f0b6d42bb4ef15e3807815714a973cb5585e89203')
a = ap.parse_args()
if sha(a.gold) != a.gold_sha256: sys.exit('gold SHA mismatch')
gold = {}
for line in open(a.gold, encoding='utf8'):
    r = json.loads(line); gold[(r['dataset'], str(r['qid']))] = r.get('answers') or r.get('labels') or r.get('gold')
rows, models = [], []
for d in sorted((HERE / 'runs').iterdir()):
    if not (d / 'raw_outputs.jsonl').exists(): continue
    models.append(d.name)
    for line in open(d / 'raw_outputs.jsonl', encoding='utf8'):
        r = json.loads(line)
        if 'text' not in r: continue                      # failed call = missing arm (registered rule)
        g = gold.get((r['dataset'], r['qid']))
        if g is None: continue                             # no reference: excluded (registered rule)
        for v in ('frozen', 'format'):
            rows.append([r['dataset'], r['qid'], d.name, r['arm'], v, score(r['dataset'], r['text'], g, v)])
out = HERE / 'analysis'; out.mkdir(exist_ok=True)
with open(out / 'scores_commercial.csv', 'w', newline='', encoding='utf8') as f:
    w = csv.writer(f); w.writerow(['dataset', 'qid', 'model', 'arm', 'scorer', 'correct']); w.writerows(rows)
subprocess.run([sys.executable, str(FI / 'holdout_analysis.py'), '--flags', str(FI / 'flags_W_AND_H3_D_FROZEN.csv'),
                '--scores', str(out / 'scores_commercial.csv'), '--models', *models, '--out', str(out / 'H1_H4_commercial.json')], check=True)
print('scores', sha(out / 'scores_commercial.csv'), 'report', sha(out / 'H1_H4_commercial.json'))
