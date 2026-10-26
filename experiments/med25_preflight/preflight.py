#!/usr/bin/env python3
"""RIDI-MED25 read-only source/schema provenance check; NO inference or preregistration."""
import argparse,hashlib,json,re
from collections import Counter
from pathlib import Path
def stable(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf8')
def digest(x):return hashlib.sha256(stable(x)).hexdigest()
def options(o):
    if isinstance(o,dict):d={str(k).upper():str(v).strip() for k,v in o.items()}
    elif isinstance(o,list):d={str(x['key']).upper():str(x['value']).strip() for x in o}
    else:raise ValueError('MedQA options unsupported')
    if set(d)!=set('ABCD') or not all(d.values()):raise ValueError('MedQA requires 4 nonempty options A-D')
    return d
def check_medqa(rows):
    if len(rows)!=1273:raise ValueError(f'MedQA requires 1273 rows; got {len(rows)}')
    ids=[]; labels=Counter(); hashes=[]
    for r in rows:
        q=str(r.get('question') or '').strip(); d=options(r.get('options'));g=str(r.get('answer_idx') or '').upper()
        if not q or g not in d:raise ValueError('Missing MedQA gold field')
        ids.append(digest([q,d]));labels[g]+=1;hashes.append(digest(r))
    if len(set(ids))!=1273:raise ValueError('Duplicate MedQA question')
    return {'n':len(ids),'unique':len(set(ids)),'labels':dict(labels),'ordered_row_sha256':digest(hashes)}
def check_pubmed(rows):
    if len(rows)!=1000:raise ValueError(f'PubMedQA requires 1000 rows; got {len(rows)}')
    ids=[];labels=Counter();hashes=[]
    for r in rows:
        q=str(r.get('question') or '').strip();pid=str(r.get('pubid') or '')
        g=str(r.get('final_decision') or '').lower()
        if not q or not pid or g not in ('yes','no','maybe'):raise ValueError('Invalid PubMedQA question/gold')
        ids.append(pid);labels[g]+=1;hashes.append(digest(r))
    if len(set(ids))!=1000:raise ValueError('Duplicate PubMedQA pubid')
    return {'n':len(ids),'unique':len(set(ids)),'labels':dict(labels),'ordered_row_sha256':digest(hashes)}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='preflight_receipt.json');ap.add_argument('--self-test',action='store_true');a=ap.parse_args()
    if a.self_test:
        assert options([{'key':k,'value':k} for k in 'ABCD'])['A']=='A'
        try: options({'A':'x'});raise AssertionError('fail closed')
        except ValueError:pass
        print('PASS schema self-test');return
    from huggingface_hub import HfApi
    from datasets import load_dataset
    api=HfApi(); sources={'pubmedqa':('qiaojin/PubMedQA','pqa_labeled','train'),'medqa':('GBaker/MedQA-USMLE-4-options',None,'test'),'corpus':('MedRAG/textbooks',None,'train')}
    revs={}
    for key,(repo,conf,split) in sources.items():
        sha=api.dataset_info(repo).sha
        if not re.fullmatch('[a-f0-9]{40}',sha):raise ValueError('Unpinned source '+key)
        revs[key]={'repo':repo,'config':conf,'split':split,'revision':sha}
    def load(key,stream=False):
        entry=revs[key]; kw={'path':entry['repo'],'split':entry['split'],'revision':entry['revision'],'streaming':stream,'trust_remote_code':False}
        if entry['config']:kw['name']=entry['config']
        if key=='medqa':kw['data_files']={'test':'phrases_no_exclude_test.jsonl'}
        return load_dataset(**kw)
    pm=check_pubmed(list(load('pubmedqa')));med=check_medqa(list(load('medqa')))
    first=[];ds=iter(load('corpus',True))
    for _ in range(20):
        row=next(ds)
        if not all(key in row for key in ('id','title','content','contents')):raise ValueError('Corpus schema changed')
        first.append({'id':str(row['id']),'sha256':digest(row)})
    out={'status':'SCHEMA_PREFLIGHT_ONLY_NO_PREREGISTRATION_OR_INFERENCE','sources':revs,
         'panels':{'pubmedqa':pm,'medqa':med},'textbooks':{'expected_n':125847,'first20_sha256':digest(first),
         'retriever':'Not yet built: BM25 k1=0.9, b=0.4','human_relevance_grades':'None established'},
         'disclosure':'Receipt contains no original question text, copyrighted corpus passages, or model output'}
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
