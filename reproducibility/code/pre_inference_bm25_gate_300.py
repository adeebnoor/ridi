#!/usr/bin/env python3
"""Development-only BM25 pre-inference screen on frozen RunPod source. NO MODEL RUNS."""
from pathlib import Path
import csv,json,hashlib,collections,math,re,time
P=Path(r'C:\Users\USER\Downloads\RIDI_DDI_RUNPOD_STAGE_20261109')
ROOT=P/'RUNPOD_PREINFERENCE_SOURCE_SCREEN_COMBINED_300'
OUT=P/'RUNPOD_PREINFERENCE_RETRIEVAL_300'
OUT.mkdir(exist_ok=True)
def norm(x):return ' '.join(x.lower().split())
def tokens(x):return re.findall('[a-z0-9]+',x.lower())
def sha(x):return hashlib.sha256(x.encode('utf-8')).hexdigest()
def mention(text,name):return bool(re.search(r'(?<!\w)'+re.escape(name)+r'(?!\w)',text,re.I))
WARN=re.compile(r'contraindicat\w*|avoid (?:concomitant |concurrent |co[- ]?)?(?:use|administration|coadministration)|do not (?:coadminister|use (?:together|concomitantly))|should not be (?:coadministered|used (?:together|concomitantly))',re.I)
def witness(d,a,b):
 owner=norm(d['owner'])
 if owner==norm(a):other=b
 elif owner==norm(b):other=a
 else:return False
 t=' '.join(d['text'].split())
 for m in re.finditer(r'(?<!\w)'+re.escape(other)+r'(?!\w)',t,re.I):
  if WARN.search(t[max(0,m.start()-300):m.end()+300]):return True
 return False
def make_docs(source,n,stride,arm):
 out=[]
 for r in source:
  words=r['text'].split()
  for j,i in enumerate(range(0,len(words),stride)):
   out.append({'id':r['id']+':'+arm+':'+str(j),'owner':r['drug'],
      'text':'DailyMed drug label: '+r['drug']+'\n'+' '.join(words[i:i+n]),
      'source_sha256':r['xml_sha256']})
   if i+n>=len(words):break
 return out
def build_index(ds):
 ts=[tokens(d['text']) for d in ds]
 df=collections.Counter()
 for t in ts:df.update(set(t))
 avg=sum(len(t) for t in ts)/max(1,len(ts))
 postings=collections.defaultdict(list)
 for i,t in enumerate(ts):
  for w,count in collections.Counter(t).items():postings[w].append((i,count))
 return postings,df,avg,[len(t) for t in ts]
def search(q,ds,idx):
 posts,df,avg,lengths=idx
 scores=collections.defaultdict(float)
 for word in set(tokens(q)):
  post=posts.get(word,[])
  idf=math.log(1+(len(ds)-len(post)+.5)/(len(post)+.5))
  for i,f in post:
   scores[i]+=idf*f*2.2/(f+1.2*(.25+.75*lengths[i]/max(avg,1)))
 return [ds[i] for i in sorted(scores,key=lambda x:(-scores[x],ds[x]['id']))[:10]]
def proxy(docs,a,b):
 vals=[int(mention(d['text'],a) and mention(d['text'],b)) for d in docs]
 s=sum(v/math.log2(i+2) for i,v in enumerate(vals))
 best=sum(1/math.log2(i+2) for i in range(sum(vals)))
 return (s/best if best else 0.0),any(vals)
def txt_hash(docs):return sha(json.dumps([d['text'] for d in docs],ensure_ascii=False,separators=(',',':')))
source=[json.loads(x) for x in (ROOT/'evidence_corpus.jsonl').open(encoding='utf8') if x.strip()]
cov=[json.loads(x) for x in (ROOT/'source_pair_coverage.jsonl').open(encoding='utf8') if x.strip()]
assert len({d['id'] for d in source})==len(source)
pairs={}
for r in cov:
 k='|'.join(sorted((norm(r['drug_a']),norm(r['drug_b']))))
 assert k==r['pair_key']
 val=(r['drug_a'],r['drug_b'],r['ddinter_class'])
 if k in pairs:assert pairs[k][2]==val[2]
 else:pairs[k]=val
# Exclude previously inspected source-coverage and GPU pilot pairs.
pilots={('|'.join(sorted((norm(r['drug_a']),norm(r['drug_b']))))) for r in csv.DictReader((P/'PILOTS_EXCLUDE_42.csv').open(encoding='utf8'))}
excluded=set(pairs).intersection(pilots)
for k in excluded:del pairs[k]
print('EXCLUDED_PILOT_PAIRS',len(excluded),flush=True)
arm0=make_docs(source,480,240,'B0')
arm1=make_docs(source,220,110,'B1')
ix0=build_index(arm0);ix1=build_index(arm1)
audit=[];eligible=[];logs=[]
for n,(k,(a,b,sev)) in enumerate(sorted(pairs.items()),1):
 if sev not in ('Major','Moderate','Minor'):continue
 b0=search(a+' '+b,arm0,ix0);b1=search(a+' '+b,arm1,ix1)
 if not b0 or not b1:continue
 m0,p0=proxy(b0,a,b);m1,p1=proxy(b1,a,b)
 w0=any(witness(d,a,b) for d in b0);w1=any(witness(d,a,b) for d in b1)
 h0=txt_hash(b0);h1=txt_hash(b1)
 qualified=bool(p0 and p1 and abs(m0-m1)<1e-12 and h0!=h1 and w0 and w1)
 cid='DDI-EF-'+sha(k)[:20]
 row={'case_id':cid,'drug_a':a,'drug_b':b,'severity':sev,
  'proxy_B0':repr(m0),'proxy_B1':repr(m1),'both_drugs_B0':int(p0),'both_drugs_B1':int(p1),
  'warning_B0':int(w0),'warning_B1':int(w1),'changed_content':int(h0!=h1),
  'equal_proxy':int(abs(m0-m1)<1e-12),'strictly_qualified':int(qualified),
  'context_hash_B0':h0,'context_hash_B1':h1}
 audit.append(row)
 if qualified:
  eligible.append({'case_id':cid,'drug_a':a,'drug_b':b,'severity':sev})
  logs.append({'case_id':cid,'baseline_documents':b0,'updated_documents':b1})
 if n%100==0:print('SCREEN',n,'/',len(pairs),flush=True)
with (OUT/'FULL_GUARD.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,audit[0].keys());w.writeheader();w.writerows(audit)
with (OUT/'ELIGIBLE_OWNER_ONLY.csv').open('w',encoding='utf8',newline='') as f:
 if eligible:
  w=csv.DictWriter(f,eligible[0].keys());w.writeheader();w.writerows(eligible)
with (OUT/'ELIGIBLE_RETRIEVAL.jsonl').open('w',encoding='utf8') as f:
 for r in logs:f.write(json.dumps(r,ensure_ascii=False)+'\n')
sev=collections.Counter(r['severity'] for r in eligible)
summary={'status':'DEVELOPMENT_BM25_GATE_NOT_CONFIRMATORY','source_docs':len(source),
'ddinter_pairs_with_source_mentions':len(pairs),'B0_chunks':len(arm0),'B1_chunks':len(arm1),
'excluded_pilot_pairs':len(excluded),'tested_pairs':len(audit),'both_name_mentioned':sum(r['both_drugs_B0'] and r['both_drugs_B1'] for r in audit),
'equal_proxy_score':sum(r['equal_proxy'] for r in audit),
'both_restrictive_warning_proxy':sum(r['warning_B0'] and r['warning_B1'] for r in audit),
'strictly_qualified_n':len(eligible),'strictly_qualified_by_severity':dict(sev),
'major_ge50_preinference':sev.get('Major',0)>=50,
'major_ge150_preinference':sev.get('Major',0)>=150,
'OSF_registered':False,'LLM_model_runs':0,'not_a_clinical_validation':True,
'source_sha256':{x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in ['evidence_corpus.jsonl','source_pair_coverage.jsonl']}}
(OUT/'GATE_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
print('SUMMARY',json.dumps(summary),flush=True)
print('HASHES',json.dumps({f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in OUT.iterdir() if f.is_file()}),flush=True)
