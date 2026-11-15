#!/usr/bin/env python3
"""RIDI-CONFIRM-C commercial-model runner (v1.0, 10 Nov 2026). Generation only; never scores.

Arms (labels match the frozen analysis script so it runs unmodified):
  bm25_whole, bm25_window   <- W_3000_PROMPTS_PRE_GENERATION.jsonl (byte-identical prompt text)
  contriever                <- H3_D_1500_PROMPTS_PRE_GENERATION.jsonl
  whole_rep_b1, whole_rep_b16 <- two further independent calls of the bm25_whole prompt
                                 (API re-execution floor; labels kept for script compatibility)
Spending: every call is pre-checked against a worst-case cost; the run aborts before any call that
could push the global ledger past the global cap (default $200 including the smoke test) or the
per-model cap. Costs are recorded from API-reported usage.
API keys are read from environment variables only and are never written to disk or logs.
"""
import argparse, hashlib, json, os, random, sys, time, fcntl, datetime
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent.parent
CFG = json.load(open(HERE / 'code' / 'models_pinned.json'))
SEED = 20261110

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

# ---------- frozen prompt loading ----------
TEXT_KEYS = ('prompt', 'prompt_text', 'input', 'text')
ARM_KEYS = ('arm', 'condition', 'retrieval', 'config', 'system')
def norm_arm(v, source):
    v = str(v).lower()
    if source == 'D': return 'contriever'
    if 'window' in v or 'win' == v: return 'bm25_window'
    if 'whole' in v or 'doc' in v: return 'bm25_whole'
    raise ValueError('unrecognised W arm label: %r' % v)

def load_prompts(path, source):
    out = {}
    for ln, line in enumerate(open(path, encoding='utf8'), 1):
        r = json.loads(line)
        ds = r.get('dataset'); qid = str(r.get('qid', r.get('id')))
        if 'messages' in r: payload = {'messages': r['messages']}
        else:
            k = [k for k in TEXT_KEYS if k in r]
            if not k: raise SystemExit(f'{path}:{ln}: no prompt field among {TEXT_KEYS}+messages; keys={list(r)}')
            payload = {'text': r[k[0]]}
        txt = payload.get('text') or json.dumps(payload['messages'])
        if any(t in txt for t in ('<|im_start|>', '[INST]', '<s>', '<|begin_of_text|>')):
            raise SystemExit(f'{path}:{ln}: prompt contains an open-weight chat template; a pre-registered decision is required before sending it to a commercial API')
        if source == 'D': arm = 'contriever'
        else:
            ak = [k for k in ARM_KEYS if k in r]
            if not ak: raise SystemExit(f'{path}:{ln}: no arm field among {ARM_KEYS}; keys={list(r)}')
            arm = norm_arm(r[ak[0]], source)
        out[(ds, qid, arm)] = payload
    return out

def as_messages(payload):
    if 'messages' in payload: return payload['messages']
    return [{'role': 'user', 'content': payload['text']}]

# ---------- vendors ----------
import time as _t
_raw_post = requests.post
def _post_retry(*a, **k):
    for i in range(6):
        r = _raw_post(*a, **k)
        if r.status_code not in (429, 500, 502, 503, 504, 529): return r
        _t.sleep(min(60, 5 * 2 ** i))
    return r
requests.post = _post_retry  # transient-error retry only; failed (non-billed) responses are not charged
def call_openai(m, msgs):
    body = {'model': m['model_id'], 'messages': msgs, 'temperature': m['temperature'],
            'max_completion_tokens': m['max_output_tokens'], 'seed': SEED, 'n': 1}
    if m.get('reasoning_effort'): body['reasoning_effort'] = m['reasoning_effort']
    r = requests.post('https://api.openai.com/v1/chat/completions', timeout=120,
                      headers={'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY']}, json=body)
    r.raise_for_status(); j = r.json(); u = j.get('usage', {})
    cached = (u.get('prompt_tokens_details') or {}).get('cached_tokens', 0) or 0
    return {'text': j['choices'][0]['message'].get('content') or '', 'finish': j['choices'][0].get('finish_reason'),
            'model_reported': j.get('model'), 'fingerprint': j.get('system_fingerprint'),
            'in_tok': u.get('prompt_tokens', 0) - cached, 'cached_tok': cached, 'out_tok': u.get('completion_tokens', 0), 'raw_usage': u}

def call_anthropic(m, msgs):
    body = {'model': m['model_id'], 'max_tokens': m['max_output_tokens'], 'messages': msgs}
    if m.get('temperature') is not None: body['temperature'] = m['temperature']
    if m.get('thinking'): body['thinking'] = m['thinking']
    r = requests.post('https://api.anthropic.com/v1/messages', timeout=120, json=body,
                      headers={'x-api-key': os.environ['ANTHROPIC_API_KEY'], 'anthropic-version': '2023-06-01'})
    r.raise_for_status(); j = r.json(); u = j.get('usage', {})
    text = ''.join(c.get('text', '') for c in j.get('content', []) if c.get('type') == 'text')
    return {'text': text, 'finish': j.get('stop_reason'), 'model_reported': j.get('model'), 'fingerprint': j.get('id'),
            'in_tok': u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0), 'cached_tok': u.get('cache_read_input_tokens', 0),
            'out_tok': u.get('output_tokens', 0), 'raw_usage': u}

def call_google(m, msgs):
    contents = [{'role': 'user' if x['role'] != 'assistant' else 'model', 'parts': [{'text': x['content']}]} for x in msgs if x['role'] != 'system']
    sysm = [x['content'] for x in msgs if x['role'] == 'system']
    gc = {'temperature': m['temperature'], 'maxOutputTokens': m['max_output_tokens'], 'candidateCount': 1, 'seed': SEED}
    if m.get('thinking_level'): gc['thinkingConfig'] = {'thinkingLevel': m['thinking_level']}
    body = {'contents': contents, 'generationConfig': gc}
    if sysm: body['systemInstruction'] = {'parts': [{'text': '\n'.join(sysm)}]}
    r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{m['model_id']}:generateContent", timeout=120,
                      headers={'x-goog-api-key': os.environ['GEMINI_API_KEY']}, json=body)
    r.raise_for_status(); j = r.json(); u = j.get('usageMetadata', {})
    cand = (j.get('candidates') or [{}])[0]
    text = ''.join(p.get('text', '') for p in (cand.get('content') or {}).get('parts', []) if not p.get('thought'))
    cached = u.get('cachedContentTokenCount', 0) or 0
    return {'text': text, 'finish': cand.get('finishReason'), 'model_reported': j.get('modelVersion'), 'fingerprint': j.get('responseId'),
            'in_tok': u.get('promptTokenCount', 0) - cached, 'cached_tok': cached,
            'out_tok': u.get('candidatesTokenCount', 0) + u.get('thoughtsTokenCount', 0), 'raw_usage': u}

def call_openrouter(m, msgs):
    """OpenAI-compatible chat completions via OpenRouter; provider pinned, data collection denied."""
    body = {'model': m['model_id'], 'messages': msgs, 'max_tokens': m['max_output_tokens'], 'seed': SEED, 'n': 1,
            'provider': m['provider_prefs'], 'usage': {'include': True}}
    if m.get('temperature') is not None: body['temperature'] = m['temperature']
    if m.get('reasoning'): body['reasoning'] = m['reasoning']
    r = requests.post('https://openrouter.ai/api/v1/chat/completions', timeout=180,
                      headers={'Authorization': 'Bearer ' + os.environ['OPENROUTER_API_KEY']}, json=body)
    r.raise_for_status(); j = r.json()
    if 'error' in j and not j.get('choices'):
        raise requests.HTTPError('openrouter error: ' + json.dumps(j['error'])[:300], response=r)
    u = j.get('usage', {}); ch = j['choices'][0]
    cached = (u.get('prompt_tokens_details') or {}).get('cached_tokens', 0) or 0
    out = {'text': ch['message'].get('content') or '', 'finish': ch.get('finish_reason'),
           'model_reported': j.get('model'), 'fingerprint': (j.get('provider') or '') + '|' + str(j.get('id')),
           'in_tok': u.get('prompt_tokens', 0) - cached, 'cached_tok': cached, 'out_tok': u.get('completion_tokens', 0), 'raw_usage': u}
    return out

CALL = {'openai': call_openai, 'anthropic': call_anthropic, 'google': call_google, 'openrouter': call_openrouter}
KEYVAR = {'openai': 'OPENAI_API_KEY', 'anthropic': 'ANTHROPIC_API_KEY', 'google': 'GEMINI_API_KEY', 'openrouter': 'OPENROUTER_API_KEY'}

def cost(m, in_tok, cached, out_tok):
    p = m['price_per_mtok']
    return (in_tok * p['input'] + cached * p['cached_input'] + out_tok * p['output']) / 1e6

def worst_case(m, payload):
    chars = len(payload.get('text') or json.dumps(payload['messages']))
    est_in = chars / 2.5 * 1.0  # deliberately pessimistic (real ~4 chars/token)
    return cost(m, est_in, 0, m['worst_case_output_tokens'])

# ---------- ledger (global, file-locked) ----------
class Ledger:
    def __init__(self, path, gcap, mcap, key):
        self.path, self.gcap, self.mcap, self.key = Path(path), gcap, mcap, key
        if not self.path.exists(): self.path.write_text(json.dumps({'total': 0.0, 'by_model': {}, 'events': []}))
    def reserve(self, amount):
        with open(self.path, 'r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX); d = json.load(f)
            t = d['total']; mm = d['by_model'].get(self.key, 0.0)
            ok = t + amount <= self.gcap and mm + amount <= self.mcap
            fcntl.flock(f, fcntl.LOCK_UN)
            return ok, t, mm
    def add(self, amount, note):
        with open(self.path, 'r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX); d = json.load(f)
            d['total'] += amount; d['by_model'][self.key] = d['by_model'].get(self.key, 0.0) + amount
            d['events'].append([now(), self.key, round(amount, 6), note])
            f.seek(0); f.truncate(); json.dump(d, f, indent=0); fcntl.flock(f, fcntl.LOCK_UN)
            return d['total']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', required=True, choices=list(CFG['models']))
    ap.add_argument('--w-prompts', default=str(HERE / 'frozen_inputs' / 'W_3000_PROMPTS_PRE_GENERATION.jsonl'))
    ap.add_argument('--d-prompts', default=str(HERE / 'frozen_inputs' / 'H3_D_1500_PROMPTS_PRE_GENERATION.jsonl'))
    ap.add_argument('--smoke', type=int, default=0, help='technical check: first N questions only; outputs go to smoke/ and are EXCLUDED')
    ap.add_argument('--ledger', default=str(HERE / 'SPEND_LEDGER.json'))
    ap.add_argument('--global-cap', type=float, default=CFG['global_cap_usd'])
    ap.add_argument('--smoke-cap', type=float, default=CFG['smoke_cap_usd'])
    a = ap.parse_args()
    m = CFG['models'][a.model]; vendor = m['vendor']
    if not os.environ.get(KEYVAR[vendor]): raise SystemExit(f'missing env var {KEYVAR[vendor]} (key not set)')
    exp = CFG['frozen_sha256']
    for p, k in ((a.w_prompts, 'W_3000_PROMPTS_PRE_GENERATION.jsonl'), (a.d_prompts, 'H3_D_1500_PROMPTS_PRE_GENERATION.jsonl')):
        got = sha(p)
        if exp.get(k) and exp[k] != got: raise SystemExit(f'SHA mismatch for {k}: {got}')
    W = load_prompts(a.w_prompts, 'W'); D = load_prompts(a.d_prompts, 'D')
    qs = sorted({(k[0], k[1]) for k in W} | {(k[0], k[1]) for k in D})
    jobs = []
    for ds, q in qs:
        for arm in ('bm25_whole', 'bm25_window'):
            if (ds, q, arm) in W: jobs.append((0, ds, q, arm, W[(ds, q, arm)]))
        if (ds, q, 'contriever') in D: jobs.append((0, ds, q, 'contriever', D[(ds, q, 'contriever')]))
        if (ds, q, 'bm25_whole') in W:
            jobs.append((1, ds, q, 'whole_rep_b1', W[(ds, q, 'bm25_whole')]))
            jobs.append((2, ds, q, 'whole_rep_b16', W[(ds, q, 'bm25_whole')]))
    if a.smoke:
        keep = set(qs[:: max(1, len(qs) // a.smoke)][: a.smoke])
        jobs = [j for j in jobs if (j[1], j[2]) in keep and j[3] == 'bm25_whole']
        outdir = HERE / 'smoke' / a.model; gcap = min(a.global_cap, CFG['global_cap_usd']); mcap = a.smoke_cap
    else:
        outdir = HERE / 'runs' / a.model; gcap = a.global_cap; mcap = m['model_cap_usd']
    outdir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    passes = {}
    for j in jobs: passes.setdefault(j[0], []).append(j)
    order = []
    for pnum in sorted(passes): blk = passes[pnum]; rng.shuffle(blk); order += blk   # pass 0, then rep pass 1, then rep pass 2
    led = Ledger(a.ledger, gcap, mcap, ('SMOKE:' if a.smoke else '') + a.model)
    outp = outdir / 'raw_outputs.jsonl'
    done = set()
    if outp.exists():
        for line in open(outp): r = json.loads(line); done.add((r['dataset'], r['qid'], r['arm']))
    meta = {'started_utc': now(), 'model_key': a.model, 'pinned': m, 'n_jobs': len(order), 'smoke': bool(a.smoke),
            'status': 'TECHNICAL_CHECK_EXCLUDED_FROM_ANALYSIS' if a.smoke else 'CONFIRMATORY_RUN', 'seed': SEED}
    (outdir / 'run_meta.json').write_text(json.dumps(meta, indent=1))
    with open(outp, 'a', encoding='utf8') as fo:
        for pnum, ds, q, arm, payload in order:
            if (ds, q, arm) in done: continue
            wc = worst_case(m, payload)
            ok, t, mm = led.reserve(wc)
            if not ok:
                print(f'ABORT: cap reached (global {t:.4f}/{gcap}, model {mm:.4f}/{mcap}); next worst-case {wc:.4f}', file=sys.stderr)
                meta['aborted_utc'] = now(); meta['abort_reason'] = 'cap'; (outdir / 'run_meta.json').write_text(json.dumps(meta, indent=1)); sys.exit(3)
            res, err = None, None
            for attempt in range(6):
                try: res = CALL[vendor](m, as_messages(payload)); break
                except requests.HTTPError as e:
                    code = e.response.status_code
                    err = f'HTTP {code}: {e.response.text[:300]}'
                    if code in (400, 401, 403, 404): break
                    time.sleep(min(60, 2 ** attempt))
                except Exception as e:
                    err = repr(e)[:300]; time.sleep(min(60, 2 ** attempt))
            c = cost(m, res['in_tok'], res['cached_tok'], res['out_tok']) if res else 0.0
            if res and isinstance(res['raw_usage'], dict) and res['raw_usage'].get('cost') is not None: c = max(c, float(res['raw_usage']['cost']))
            total = led.add(c, f'{ds}/{q}/{arm}')
            rec = {'dataset': ds, 'qid': q, 'arm': arm, 'pass': pnum, 'model_key': a.model, 'utc': now(), 'cost_usd': c,
                   'prompt_sha256': hashlib.sha256((payload.get('text') or json.dumps(payload['messages'])).encode()).hexdigest()}
            if res: rec.update({k: res[k] for k in ('text', 'finish', 'model_reported', 'fingerprint', 'in_tok', 'cached_tok', 'out_tok', 'raw_usage')})
            else: rec['error'] = err
            fo.write(json.dumps(rec, ensure_ascii=False) + '\n'); fo.flush()
            if not res and err and err.startswith(('HTTP 401', 'HTTP 403', 'HTTP 404')):
                print('ABORT on auth/model error:', err, file=sys.stderr); sys.exit(4)
    meta['finished_utc'] = now(); meta['raw_outputs_sha256'] = sha(outp); (outdir / 'run_meta.json').write_text(json.dumps(meta, indent=1))
    print(json.dumps({'model': a.model, 'jobs': len(order), 'ledger_total_usd': round(json.load(open(a.ledger))['total'], 4)}))

if __name__ == '__main__':
    main()
