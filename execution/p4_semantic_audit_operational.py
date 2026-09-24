#!/usr/bin/env python3
"""Operational P4 execution copy. Scientific prompt and endpoint unchanged from frozen v95.4."""
import argparse, csv, random, json
from collections import defaultdict
from pathlib import Path
import numpy as np
from ridi_exp import stats
from ridi_exp.backends import make_backend
from ridi_exp.io import append_jsonl, read_jsonl
from ridi_exp.scoring import normalize

JUDGE_PROMPT = (
    "You are auditing evidence for a {kind}.\n{label}: {question}\n\nPassage:\n{passage}\n\n"
    "Does this passage contain any information that would help {goal}, including partial, indirect or misleading "
    "evidence that a reader could use? Reply with exactly one word: YES or NO."
)

def exchanged(contexts):
    by = defaultdict(dict)
    for c in contexts:
        if c.get('draw', 0) == 0: by[c['qid']][c['condition']] = c
    rows = []
    for q, d in by.items():
        if 'reference' not in d or 'random' not in d: continue
        ref_ids={p['docid'] for p in d['reference']['passages']}; ran_ids={p['docid'] for p in d['random']['passages']}
        c=d['reference']
        for p in d['reference']['passages']:
            if p['docid'] not in ran_ids: rows.append((c,p,'removed'))
        for p in d['random']['passages']:
            if p['docid'] not in ref_ids: rows.append((c,p,'added'))
    return rows

def judge_prompt(c,p):
    if c['task']=='qa':
        return JUDGE_PROMPT.format(kind='question',label='Question',question=c['question'],passage=p['text'],goal='answer the question')
    return JUDGE_PROMPT.format(kind='claim',label='Claim',question=c['question'],passage=p['text'],goal='support or refute the claim')

def parse_yes_no(raw):
    t=raw.strip().upper()
    return 1 if t.startswith('YES') else 0 if t.startswith('NO') else -1

def gold_in(c,p):
    if c['task']!='qa': return 0
    txt=normalize(p['text'])
    return int(any(normalize(g) and f' {normalize(g)} ' in f' {txt} ' for g in c['gold']))

def stage_judge(a,ctx):
    rows=exchanged(ctx); out=a.out/'passage_labels.jsonl'
    done={(r['qid'],r['docid'],r['role'],r['judge']) for r in read_jsonl(out)}
    for jname,spec,revision in (('judge1',a.judge1,a.judge1_revision),('judge2',a.judge2,a.judge2_revision)):
        kind,model=spec.split(':',1)
        if kind=='mock': be=make_backend(kind,model)
        elif kind in ('hf','vllm'): be=make_backend(kind,model,revision=revision,max_new_tokens=8)
        else: be=make_backend(kind,model,max_new_tokens=8,workers=a.workers)
        todo=[(c,p,role) for c,p,role in rows if (c['qid'],p['docid'],role,jname) not in done]
        for i in range(0,len(todo),a.chunk_size):
            chunk=todo[i:i+a.chunk_size]
            outs=be.generate_batches([[judge_prompt(c,p) for c,p,_ in chunk]])[0]
            append_jsonl(out,[{'qid':c['qid'],'dataset':c['dataset'],'docid':p['docid'],'role':role,'judge':jname,
                'model':model,'revision':revision,'raw':o,'informative':parse_yes_no(o),'gold_string':gold_in(c,p)}
                for (c,p,role),o in zip(chunk,outs)])
            if i % (a.chunk_size*20)==0: print(jname,i,len(todo),flush=True)
        print(f'{jname}: {len(todo)} passages judged',flush=True)

def stage_analyze(a,ctx):
    labels=read_jsonl(a.out/'passage_labels.jsonl'); lab=defaultdict(dict); gold={}
    for r in labels:
        lab[(r['qid'],r['docid'])][r['judge']]=r['informative']; gold[(r['qid'],r['docid'])]=r['gold_string']
    pairs=[v for v in lab.values() if 'judge1' in v and 'judge2' in v and v['judge1']>=0 and v['judge2']>=0]
    S={'experiment':'P4','n_passages_judged':len(lab),'judge_unparsed':sum(1 for r in labels if r['informative']<0),
       'judge_kappa':stats.cohen_kappa([v['judge1'] for v in pairs],[v['judge2'] for v in pairs]) if pairs else None,
       'informative_rate_judge1':float(np.mean([v['judge1'] for v in pairs])) if pairs else None,
       'informative_rate_judge2':float(np.mean([v['judge2'] for v in pairs])) if pairs else None}
    per_query=defaultdict(list)
    for (q,d),v in lab.items():
        per_query[q].append(int(v.get('judge1',1)==0 and v.get('judge2',1)==0 and gold.get((q,d),0)==0))
    clean={q for q,v in per_query.items() if all(v)}
    if a.generations:
        res=[r for r in read_jsonl(a.generations) if r['batch_regime']==a.regime and r.get('run',0)==0 and r.get('draw',0)==0]
        by=defaultdict(dict)
        for r in res: by[r['qid']][r['condition']]=r
        change={q:int(v['reference']['correct']!=v['random']['correct']) for q,v in by.items() if 'reference' in v and 'random' in v}
        ds={q:v['reference']['dataset'] for q,v in by.items() if 'reference' in v}
        for name,subset in (('clean',clean),('not_clean',set(change)-clean),('all',set(change))):
            vals=defaultdict(list)
            for q in subset & set(change): vals[ds[q]].append(change[q])
            if vals:
                lo,hi=stats.stratified_bootstrap_macro(vals,n_boot=20000)
                S[f'change_{name}']={'n':sum(len(v) for v in vals.values()),'pooled':stats.rate(sum(vals.values(),[])),
                    'macro':stats.macro(vals),'macro_ci95':(lo,hi),'n_by_dataset':{k:len(v) for k,v in vals.items()}}
    S['n_clean_queries']=len(clean); S['n_queries_with_exchanges']=len(per_query)
    from ridi_exp.cli import dump
    dump(S,a.out/'P4_summary.json'); print(json.dumps(S,sort_keys=True),flush=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--stage',choices=['judge','analyze'],required=True); ap.add_argument('--contexts',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True); ap.add_argument('--judge1',default='mock:judge-a'); ap.add_argument('--judge2',default='mock:judge-b')
    ap.add_argument('--judge1-revision',default=None); ap.add_argument('--judge2-revision',default=None); ap.add_argument('--chunk-size',type=int,default=32)
    ap.add_argument('--workers',type=int,default=8); ap.add_argument('--generations',type=Path,default=None); ap.add_argument('--regime',default='fixed:16')
    a=ap.parse_args(); ctx=read_jsonl(a.contexts)
    {'judge':stage_judge,'analyze':stage_analyze}[a.stage](a,ctx)
if __name__=='__main__': main()
