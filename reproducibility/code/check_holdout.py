"""Replay the unchanged registered analysis and audit the W/D inputs and paired accuracy."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import numpy as np
import pandas as pd

SOURCE = Path(__file__).resolve().parents[1]
HOLDOUT = SOURCE / 'holdout'
FLAGS = HOLDOUT / 'flags_W_AND_H3_D_FROZEN.csv'
SCORES = HOLDOUT / 'scores_W_AND_H3_D_REAL.csv'
ANALYZER = SOURCE / 'code' / 'holdout_analysis.py'
MODELS = ('qwen3', 'mistral')
SCORE_HASH_W = '61f7144366b83f405b9c02d5ccb5c61280bfb33579e6e1ad0fee1e56274cda3e'
def sha(data):
    return hashlib.sha256(data).hexdigest()

def replay(flags_path, scores_path, report_path, temp):
    dest = temp / 'replay.json'
    subprocess.run([sys.executable, str(ANALYZER), '--flags', str(flags_path),
                    '--scores', str(scores_path), '--models', *MODELS, '--out', str(dest)],
                   check=True, stdout=subprocess.DEVNULL)
    ref = report_path.read_bytes()
    # The original Windows text writer used CRLF. Keep the deposited object unchanged.
    generated = dest.read_bytes().replace(b'\r\n', b'\n')
    if b'\r\n' in ref:
        generated = generated.replace(b'\n', b'\r\n')
    assert generated == ref, report_path.name
    return sha(generated)

def main():
    flags = pd.read_csv(FLAGS, dtype={'qid': str})
    prior_flags = pd.read_csv(HOLDOUT / 'flags_W_plus_D_NOT_RUN.csv', dtype={'qid': str})
    same_columns = ['dataset', 'qid', 'E1_win', 'E2_win', 'E3_win']
    assert flags[same_columns].equals(prior_flags[same_columns]) and len(flags) == 1500
    receipt = json.loads((HOLDOUT / 'H3_D_AUTOMATED_ANALYSIS_RECEIPT.json').read_bytes())
    assert sha(FLAGS.read_bytes()) == receipt['flags_sha256']
    assert sha(SCORES.read_bytes()) == receipt['scores_sha256']
    assert sha(ANALYZER.read_bytes()) == receipt['registered_code_sha256']
    scores = pd.read_csv(SCORES, dtype={'qid': str})
    assert not scores.duplicated(['dataset', 'qid', 'model', 'arm', 'scorer']).any()
    score_lines = SCORES.read_bytes().splitlines(keepends=True)
    historical = b''.join(score_lines[:21217])
    assert sha(historical) == SCORE_HASH_W
    assert set(scores.iloc[:21216].arm) == {'bm25_whole','bm25_window','whole_rep_b1','whole_rep_b16'}
    assert set(scores.iloc[21216:].arm) == {'contriever'} and len(scores.iloc[21216:]) == 5304
    with tempfile.TemporaryDirectory() as folder:
        folder = Path(folder)
        w_csv = folder / 'w.csv'
        w_csv.write_bytes(historical)
        w_digest = replay(HOLDOUT/'flags_W_plus_D_NOT_RUN.csv', w_csv,
                          HOLDOUT/'h1_h4_rerun_20261107.json', folder)
        wd_digest = replay(FLAGS, SCORES, HOLDOUT/'Holdout_Frozen_Analysis.json', folder)
    rng = np.random.default_rng(20261109)
    records = []
    for contrast, gate, arm in [('W','E1_win','bm25_window'),('D','E1_dense','contriever')]:
        for model in MODELS:
            s = scores.query("scorer == 'frozen' and model == @model").pivot(index=['dataset','qid'],columns='arm',values='correct')
            sel = flags.loc[flags[gate].eq(1), ['dataset','qid']].merge(s.reset_index(),on=['dataset','qid'],how='left')
            data = sel.dropna(subset=['bm25_whole',arm,'whole_rep_b1','whole_rep_b16']).copy()
            data['difference'] = (data[arm] - data.bm25_whole).astype(int)
            # In each stratum resample paired outcome differences, using their multinomial counts.
            # The unit is a question. Each of the three benchmark means gets weight one third.
            boot = np.zeros(100000)
            for _,g in data.groupby('dataset',sort=True):
                values = np.bincount(g.difference + 1,minlength=3)
                samples = rng.multinomial(len(g), values/len(g), size=len(boot))
                boot += (samples[:,2]-samples[:,0]) / len(g) / 3
            point = 100*data.groupby('dataset').difference.mean().mean()
            lo,hi = 100*np.quantile(boot,[.05,.95])
            records.append(dict(contrast=contrast,model=model,eligible=len(sel),n=len(data),
                                regressions=int((data.difference==-1).sum()),gains=int((data.difference==1).sum()),
                                delta_pp=float(point),ci90_pp=[float(lo),float(hi)],
                                within_posthoc_margin_2pp=bool(lo> -2 and hi < 2)))
    print(json.dumps(dict(W_flag_projection_rows=1500,old_W_score_rows=21216,added_D_score_rows=5304,
                          W_score_sha256=SCORE_HASH_W,W_report_sha256=w_digest,combined_report_sha256=wd_digest,
                          seed=20261109,draws=100000,interval='unadjusted paired 90% percentile, benchmark-stratified',
                          status='post hoc; margin selected after observing outcomes',paired_net_accuracy=records),
                     indent=2))
if __name__ == '__main__':
    main()
