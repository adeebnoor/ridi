#!/usr/bin/env python3
"""Technical format check (no scoring, no correctness). Samples 30 frozen prompts stratified over 3 arms x 3 datasets
(seed 20261112, smoke questions excluded) and records only emptiness / finish_reason / token usage per item.
Usage: tech_check.py --model <key in models_pinned.json> --max-tokens N --out smoke/tech_check_30/<model>/mtN
Works for every pinned vendor (openai, anthropic, openrouter); reads the API key from the environment and never prints it.
Truncation = finish_reason 'length' (OpenAI/OpenRouter) or 'max_tokens' (Anthropic)."""
import argparse, json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_commercial as R
ap = argparse.ArgumentParser()
ap.add_argument('--model', default='gemini-3.8-flash'); ap.add_argument('--max-tokens', type=int, required=True)
ap.add_argument('--out', required=True); ap.add_argument('--cap', type=float, default=0.5)
a = ap.parse_args()
H = R.HERE
W = R.load_prompts(H/'frozen_inputs'/'W_3000_PROMPTS_PRE_GENERATION.jsonl', 'W'); D = R.load_prompts(H/'frozen_inputs'/'H3_D_1500_PROMPTS_PRE_GENERATION.jsonl', 'D')
allp = {**W, **D}
smoke = {(json.loads(l)['dataset'], json.loads(l)['qid']) for l in open(H/'smoke'/'gemini-3.8-flash'/'raw_outputs.jsonl')}
rng = random.Random(20261112)
sel = []
for arm, n in (('bm25_whole', 10), ('bm25_window', 10), ('contriever', 10)):
    per = {'nq': 4, 'hotpotqa': 3, 'fever': 3}
    if arm == 'bm25_window': per = {'nq': 3, 'hotpotqa': 4, 'fever': 3}
    if arm == 'contriever': per = {'nq': 3, 'hotpotqa': 3, 'fever': 4}
    for ds, k in per.items():
        pool = sorted(k_ for k_ in allp if k_[0] == ds and k_[2] == arm and (k_[0], k_[1]) not in smoke)
        sel += rng.sample(pool, k)
assert len(sel) == 30 and len(set(sel)) == 30
m = dict(R.CFG['models'][a.model]); m['max_output_tokens'] = a.max_tokens
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
led = R.Ledger(H/'SPEND_LEDGER.json', 200.0, a.cap, 'TECHCHECK:%s:mt%d' % (a.model, a.max_tokens))
rows = []
for k in sel:
    ok, t, mm = led.reserve(R.cost(m, len(allp[k].get('text') or json.dumps(allp[k]['messages'])) / 2.5, 0, a.max_tokens))
    if not ok: print('ABORT cap', t, mm); sys.exit(3)
    err = None; res = None
    try: res = R.CALL[m['vendor']](m, R.as_messages(allp[k]))
    except Exception as e: err = repr(e)[:200]
    c = 0.0
    if res:
        c = R.cost(m, res['in_tok'], res['cached_tok'], res['out_tok'])
        if res['raw_usage'].get('cost') is not None: c = max(c, float(res['raw_usage']['cost']))
    led.add(c, 'techcheck %s/%s/%s mt%d' % (k[0], k[1], k[2], a.max_tokens))
    rec = {'dataset': k[0], 'qid': k[1], 'arm': k[2], 'max_tokens': a.max_tokens, 'cost_usd': c, 'error': err}
    if res: rec.update({'text': res['text'], 'finish': res['finish'], 'provider': str(res['fingerprint'] or '').split('|')[0], 'model_reported': res['model_reported'],
        'in_tok': res['in_tok'], 'out_tok': res['out_tok'], 'reasoning_tok': ((res['raw_usage'].get('completion_tokens_details') or {}).get('reasoning_tokens') or (res['raw_usage'].get('output_tokens_details') or {}).get('thinking_tokens') or 0), 'raw_usage': res['raw_usage']})
    rows.append(rec)
with open(out/'raw_outputs.jsonl', 'w', encoding='utf8') as f:
    for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
ok_rows = [r for r in rows if r.get('error') is None]
summ = {'max_tokens': a.max_tokens, 'n': len(rows), 'errors': len(rows) - len(ok_rows),
        'empty': sum(1 for r in ok_rows if not r['text'].strip()), 'finish_length': sum(1 for r in ok_rows if r['finish'] in ('length', 'max_tokens')),
        'finish_stop': sum(1 for r in ok_rows if r['finish'] in ('stop', 'end_turn')), 'items_with_reasoning': sum(1 for r in ok_rows if r['reasoning_tok'] > 0),
        'reasoning_tok_total': sum(r['reasoning_tok'] for r in ok_rows), 'reasoning_tok_max': max([r['reasoning_tok'] for r in ok_rows] or [0]),
        'out_tok_mean': round(sum(r['out_tok'] for r in ok_rows) / max(1, len(ok_rows)), 2), 'out_tok_max': max([r['out_tok'] for r in ok_rows] or [0]),
        'in_tok_mean': round(sum(r['in_tok'] for r in ok_rows) / max(1, len(ok_rows)), 1), 'cost_usd': round(sum(r['cost_usd'] for r in rows), 6),
        'by_arm_dataset': {}, 'status': 'FORMAT_ONLY_NO_SCORING_EXCLUDED_FROM_ANALYSIS'}
for r in rows: summ['by_arm_dataset']['%s/%s' % (r['arm'], r['dataset'])] = summ['by_arm_dataset'].get('%s/%s' % (r['arm'], r['dataset']), 0) + 1
(out/'summary.json').write_text(json.dumps(summ, indent=1))
print(json.dumps({k: v for k, v in summ.items() if k != 'by_arm_dataset'}))
