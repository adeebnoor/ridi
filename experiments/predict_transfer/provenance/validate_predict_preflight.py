"""Exercise all 24 input paths in isolated CPU-only subprocesses; no generation."""
import concurrent.futures, hashlib, json, os, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE/'registration_ready'
OUT=ROOT/'provenance/runner_preflight'
OUT.mkdir(exist_ok=True)
models=json.loads((ROOT/'models.json').read_text())['models']
units=[(m['key'],d,draw) for m in models for d in ['nq','hotpotqa','fever']
       for draw in (['A','B'] if m['role']=='predictor' else ['A'])]
env=os.environ.copy();env.update(USE_TORCH='0',USE_TF='0',TOKENIZERS_PARALLELISM='false',
    PYTHONPATH=str(BASE/'tokenizer_env'))
def run(unit):
    model,d,draw=unit
    name=f'{model}__{d}__draw{draw}'
    command=[str(BASE/'preflight_venv/bin/python'),str(ROOT/'run_predict.py'),
        '--preflight-only','--model-key',model,'--dataset',d,'--draw',draw,
        '--tokenizer-dir',str(BASE/'tokenizers'),
        '--control-zip',str(BASE/'input_archives/RIDI_RAG_NATURE_CONTROL_POSTREG_20260902.zip'),
        '--data-zip',str(BASE/f'input_archives/prepared-v4-{d}.zip')]
    t=time.time()
    with (OUT/(name+'.log')).open('x') as log:
        result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,env=env)
    text=(OUT/(name+'.log')).read_text()
    complete=[json.loads(line.split(' ',1)[1]) for line in text.splitlines() if line.startswith('PREFLIGHT_COMPLETE ')]
    ok=result.returncode==0 and len(complete)==1 and complete[0]['generation_performed'] is False
    rec={'model_key':model,'dataset':d,'draw':draw,'exit_code':result.returncode,
         'verified':ok,'elapsed_seconds':round(time.time()-t,2),'receipt':complete}
    print(name,'PASS' if ok else 'FAIL',flush=True)
    return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(run,units))
receipt={'study':'RIDI-PREDICT-v1','completed_at_utc':datetime.now(timezone.utc).isoformat(),
         'runner_sha256':hashlib.sha256((ROOT/'run_predict.py').read_bytes()).hexdigest(),
         'units':results,'all_24_verified':len(results)==24 and all(r['verified'] for r in results),
         'model_weights_loaded':False,'generation_performed':False,'scientific_attempts_created':False}
(ROOT/'provenance/RUNNER_PREFLIGHT_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
assert receipt['all_24_verified'],'preflight validation failed; inspect technical logs'
