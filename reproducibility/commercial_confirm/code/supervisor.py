#!/usr/bin/env python3
"""Operational supervisor for one model (not part of the registered analysis). Runs the unmodified runner, restarts it (resumable)
after crashes or a stalled call (no new output for 10 min), and stops the model on: >2% empty answers, repeated failures,
a nearly reached cap. Writes logs/DONE_<model>.json when it exits.  Usage: supervisor.py <model-key>"""
import json, subprocess, sys, time, os, datetime
from pathlib import Path
H = Path('/workspace/COMMERCIAL_v45'); m = sys.argv[1]
CAP = json.load(open(H/'code'/'models_pinned.json'))['models'][m]['model_cap_usd']
out = H/'runs'/m/'raw_outputs.jsonl'; LOG = H/'logs'/f'{m}.supervisor.log'
def log(s):
    with open(LOG, 'a') as f: f.write(datetime.datetime.now().astimezone().isoformat() + ' ' + s + '\n')
def led():
    for _ in range(5):
        try: return json.load(open(H/'SPEND_LEDGER.json'))
        except Exception: time.sleep(0.5)
    return None
def check():
    rows = []
    if out.exists():
        for l in open(out):
            try: rows.append(json.loads(l))
            except Exception: pass
    ok = [r for r in rows if 'error' not in r]
    empty = sum(1 for r in ok if not (r.get('text') or '').strip())
    last = rows[-50:]; lerr = sum(1 for r in last if 'error' in r)
    if len(last) >= 20 and lerr / len(last) > 0.2: return f'repeated failures: {lerr}/{len(last)} errors in the last calls'
    if len(ok) >= 200 and empty / len(ok) > 0.02: return f'empty-answer rate {empty}/{len(ok)} > 2%'
    L = led()
    if L and L['by_model'].get(m, 0) > 0.92 * CAP: return f'cap near: {L["by_model"].get(m,0):.2f}/{CAP}'
    if L and L['total'] > 185: return f'global ledger near cap: {L["total"]:.2f}/200'
    return None
restarts = 0; fast = 0; reason = None; rc = None
while True:
    t0 = time.time(); logf = open(H/'logs'/f'{m}.log', 'a')
    p = subprocess.Popen([sys.executable, str(H/'code'/'run_commercial.py'), '--model', m], stdout=logf, stderr=logf, cwd=str(H))
    log(f'started runner pid {p.pid} (restart #{restarts})')
    last_check = 0; killed = None
    while p.poll() is None:
        time.sleep(15)
        if time.time() - last_check > 60:
            last_check = time.time(); why = check()
            if why: killed = ('STOP', why); break
            age = time.time() - out.stat().st_mtime if out.exists() else 0
            if age > 600: killed = ('STALL', f'no output for {int(age)} s'); break
    if killed:
        p.kill(); p.wait(); log(f'{killed[0]}: {killed[1]}')
        if killed[0] == 'STOP': reason = killed[1]; break
        restarts += 1; time.sleep(5); continue
    rc = p.returncode; log(f'runner exit {rc}')
    if rc in (0, 3, 4): break
    restarts += 1; fast = fast + 1 if time.time() - t0 < 60 else 0
    if fast >= 5: reason = 'five consecutive fast crashes'; break
    time.sleep(10)
json.dump({'model': m, 'exit_code': rc, 'stopped_reason': reason, 'restarts': restarts, 'finished': datetime.datetime.now().astimezone().isoformat()}, open(H/'logs'/f'DONE_{m}.json', 'w'))
log(f'DONE rc={rc} reason={reason} restarts={restarts}')
