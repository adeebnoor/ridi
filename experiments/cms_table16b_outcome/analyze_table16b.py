#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, statistics
from decimal import Decimal, InvalidOperation
from pathlib import Path

K = 500
ETA = 0.001
CONTRASTS = [
    {"label":"FY2024_to_FY2025","old_snapshot":"2024-10-30","old_fy":2024,"new_snapshot":"2025-02-19","new_fy":2025,"expected_n":2377,"expected_delta":195,"expected_j":174},
    {"label":"FY2025_to_FY2026","old_snapshot":"2025-11-26","old_fy":2025,"new_snapshot":"2026-02-25","new_fy":2026,"expected_n":2349,"expected_delta":202,"expected_j":181},
]

def dec(x:str)->Decimal:
    try: return Decimal(x.strip())
    except InvalidOperation as e: raise ValueError(f"nonnumeric decimal: {x!r}") from e

def ccn(x:str)->str:
    s=x.strip()
    if s.endswith('.0') and s[:-2].isdigit(): s=s[:-2]
    if not s.isdigit(): raise ValueError(f"invalid CCN {x!r}")
    if len(s)>6: raise ValueError(f"CCN too long {x!r}")
    return s.zfill(6)

def read_tps(path:Path):
    out={}
    with path.open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            key=(r['snapshot_date'].strip(),int(r['fiscal_year']),ccn(r['ccn']))
            if key in out: raise ValueError(f"duplicate TPS key {key}")
            out[key]=dec(r['tps'])
    return out

def read_factors(path:Path):
    out={}
    with path.open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            key=(int(r['fiscal_year']),ccn(r['ccn']))
            if key in out: raise ValueError(f"duplicate factor key {key}")
            v=r['actual_vbp_factor'].strip()
            out[key]=None if v=='' else dec(v)
    return out

def topk(ids, score, k):
    return [i for i in sorted(ids,key=lambda i:(-score[i],i))[:k]]

def percentiles(ids, scores):
    order=sorted(ids,key=lambda i:(-scores[i],i)); n=len(order)
    return {i:(Decimal(1) if n==1 else Decimal(1)-Decimal(rank)/Decimal(n-1)) for rank,i in enumerate(order)}

def frontier_control(ids, old, new, k, eta):
    oldset=set(topk(ids,old,k)); newtop=set(topk(ids,new,k)); delta=k-len(oldset & newtop)
    u=percentiles(ids,new)
    inside=sorted(oldset,key=lambda i:(-u[i],i)); outside=sorted(set(ids)-oldset,key=lambda i:(-u[i],i))
    utility_star=sum(sorted(u.values(),reverse=True)[:k],Decimal(0))
    chosen=None
    for j in range(0,min(k,len(outside))+1):
        sel=inside[:k-j]+outside[:j]
        util=sum((u[i] for i in sel),Decimal(0)); regret=(utility_star-util)/utility_star
        if regret <= Decimal(str(eta)):
            chosen=(j,set(sel),regret); break
    if chosen is None: raise RuntimeError('no frontier point meets eta')
    return delta,chosen[0],chosen[1],chosen[2]

def qtile(vals,p):
    if not vals: return None
    x=sorted(vals); pos=(len(x)-1)*p; lo=int(pos); hi=min(lo+1,len(x)-1); frac=Decimal(str(pos-lo))
    return x[lo]*(Decimal(1)-frac)+x[hi]*frac

def summarize_factor_changes(ids, oldfy, newfy, factors):
    deltas=[]; absd=[]; unchanged=0; cross_up=0; cross_down=0; missing=0; oldvals=[]; newvals=[]
    for i in ids:
        a=factors.get((oldfy,i)); b=factors.get((newfy,i))
        if a is None or b is None: missing+=1; continue
        oldvals.append(a); newvals.append(b); d=b-a; deltas.append(d); absd.append(abs(d))
        if d==0: unchanged+=1
        if a < Decimal('1') and b >= Decimal('1'): cross_up+=1
        if a >= Decimal('1') and b < Decimal('1'): cross_down+=1
    def med(v): return statistics.median(v) if v else None
    return {
        'n_group':len(ids),'n_complete':len(deltas),'n_missing_factor':missing,
        'old_factor_median':str(med(oldvals)) if oldvals else None,
        'new_factor_median':str(med(newvals)) if newvals else None,
        'delta_factor_median':str(med(deltas)) if deltas else None,
        'delta_factor_q1':str(qtile(deltas,.25)) if deltas else None,
        'delta_factor_q3':str(qtile(deltas,.75)) if deltas else None,
        'delta_factor_min':str(min(deltas)) if deltas else None,
        'delta_factor_max':str(max(deltas)) if deltas else None,
        'delta_factor_median_abs':str(med(absd)) if absd else None,
        'delta_factor_bps_median':str(med(deltas)*Decimal(10000)) if deltas else None,
        'exact_factor_unchanged':unchanged,
        'factor_changed':len(deltas)-unchanged,
        'cross_below1_to_ge1':cross_up,'cross_ge1_to_below1':cross_down,
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--tps',type=Path,required=True); ap.add_argument('--factors',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
    tps=read_tps(a.tps); factors=read_factors(a.factors); result={'analysis_id':'RIDI-CMS-TABLE16B-OUTCOME-v1','k':K,'eta':ETA,'contrasts':{}}
    for c in CONTRASTS:
        old={i:v for (d,fy,i),v in tps.items() if d==c['old_snapshot'] and fy==c['old_fy']}; new={i:v for (d,fy,i),v in tps.items() if d==c['new_snapshot'] and fy==c['new_fy']}; ids=set(old)&set(new)
        if len(ids)!=c['expected_n']: raise RuntimeError(f"{c['label']} locked universe {len(ids)} != {c['expected_n']}")
        oldtop=set(topk(ids,old,K)); newtop=set(topk(ids,new,K)); delta=K-len(oldtop&newtop)
        fd,j,ctrl,regret=frontier_control(ids,old,new,K,ETA)
        if delta!=c['expected_delta'] or fd!=delta or j!=c['expected_j']: raise RuntimeError(f"{c['label']} locked result mismatch delta={delta}, frontier_delta={fd}, j={j}")
        groups={'retained':oldtop&newtop,'entrant':newtop-oldtop,'leaver':oldtop-newtop,'outside':ids-(oldtop|newtop),'all_locked_universe':ids}
        same={i for i in ids if old[i]==new[i]}
        observed_entrants=newtop-oldtop; controlled_entrants=ctrl-oldtop
        groups['frontier_entrant_retained']=observed_entrants & controlled_entrants
        groups['frontier_entrant_avoidable']=observed_entrants-controlled_entrants
        groups['frontier_old_member_preserved_only']=ctrl-newtop
        row={'n_locked_universe':len(ids),'delta_unconstrained':delta,'j_eta':j,'utility_regret':str(regret),'groups':{g:summarize_factor_changes(s,c['old_fy'],c['new_fy'],factors) for g,s in groups.items()}}
        same_sum=summarize_factor_changes(same,c['old_fy'],c['new_fy'],factors); same_sum['n_exact_same_reported_tps']=len(same); same_sum['factor_changed_fraction_complete']=None if same_sum['n_complete']==0 else same_sum['factor_changed']/same_sum['n_complete']; row['same_reported_tps']=same_sum
        result['contrasts'][c['label']]=row
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__': main()
