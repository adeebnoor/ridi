import json, subprocess, sys, time
from pathlib import Path
H=Path('/workspace/COMMERCIAL_v45')
while not all((H/'logs'/f'DONE_{m}.json').exists() for m in ('gpt-5.4-mini','claude-sonnet-5.5','gemini-3.8-flash')): time.sleep(120)
r=subprocess.run([sys.executable,str(H/'code'/'make_results.py')],cwd=str(H),capture_output=True,text=True)
(H/'logs'/'finisher.log').write_text(r.stdout+'\n'+r.stderr)
