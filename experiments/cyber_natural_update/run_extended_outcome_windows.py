#!/usr/bin/env python3
"""Post hoc EPSS delayed-outcome sensitivity.

Requires the same pinned inputs already described by inputs/input_manifest.json.
The locked 365-day headline is a hard guardrail before 2/3-year results are written.
"""
import csv, gzip, json
from datetime import date
from pathlib import Path
import numpy as np
from scipy.stats import rankdata

DATES=["2023_03_05","2023_03_06","2023_03_07","2023_03_08"]
K=1000
START=date(2023,3,8)
WINDOWS={"365":date(2024,3,7),"2_year":date(2025,3,7),"3_year":date(2026,3,7)}
EXPECT={"n_candidates":195886,"v2_hits":8,"v3_hits":12}
ROOT=Path(__file__).resolve().parent
INPUTS=ROOT/"inputs"

def load_epss(path):
    out={}
    with gzip.open(path,"rt",encoding="utf-8",newline="") as h:
        rd=csv.DictReader(line for line in h if not line.startswith("#"))
        for r in rd:
            out[r["cve"].strip()]=float(r["epss"])
    return out

def load_kev(path):
    out={}
    with path.open(encoding="utf-8-sig",newline="") as h:
        for r in csv.DictReader(h):
            out[r["cveID"].strip()]=date.fromisoformat(r["dateAdded"].strip())
    return out

def topk(ids,scores):
    order=np.lexsort((ids.astype(str),-scores))
    return set(map(str,ids[order[:K]]))

def auc(labels,scores):
    pos=int(labels.sum()); neg=len(labels)-pos
    ranks=rankdata(scores,method="average")
    return float((ranks[labels].sum()-pos*(pos+1)/2)/(pos*neg)) if pos and neg else None

def average_precision(labels,scores,ids):
    pos=int(labels.sum())
    if not pos: return None
    order=np.lexsort((ids.astype(str),-scores)); y=labels[order].astype(int)
    precision=np.cumsum(y)/np.arange(1,len(y)+1)
    return float(precision[y==1].sum()/pos)

scores_by_day={d:load_epss(INPUTS/f"epss_{d}.csv.gz") for d in DATES}
kev=load_kev(INPUTS/"known_exploited_vulnerabilities.csv")
common=set.intersection(*(set(x) for x in scores_by_day.values()))
prior={c for c,d in kev.items() if d<=date(2023,3,6)}
ids=np.asarray(sorted(common-prior),dtype=object)
scores={d:np.asarray([scores_by_day[d][str(c)] for c in ids],dtype=float) for d in DATES}
v2=scores["2023_03_06"]; v3=scores["2023_03_07"]
t2=topk(ids,v2); t3=topk(ids,v3); universe=set(map(str,ids))
out={"study":"RIDI-EPSS-EXTENDED-OUTCOME-WINDOWS-v1","status":"post_hoc_sensitivity","primary_window_days":365,"n_candidates":len(ids),"windows":{}}

for label,end in WINDOWS.items():
    positive={c for c,d in kev.items() if START<=d<=end} & universe
    y=np.asarray([str(c) in positive for c in ids],dtype=bool)
    out["windows"][label]={
        "window_end":end.isoformat(),
        "n_future_kev_universe":len(positive),
        "v2_top1000_future_kev":len(t2&positive),
        "v3_top1000_future_kev":len(t3&positive),
        "difference_v3_minus_v2":len(t3&positive)-len(t2&positive),
        "v2_full_universe_auroc":auc(y,v2),
        "v3_full_universe_auroc":auc(y,v3),
        "v2_full_universe_average_precision":average_precision(y,v2,ids),
        "v3_full_universe_average_precision":average_precision(y,v3,ids),
    }

p=out["windows"]["365"]
if len(ids)!=EXPECT["n_candidates"] or p["v2_top1000_future_kev"]!=EXPECT["v2_hits"] or p["v3_top1000_future_kev"]!=EXPECT["v3_hits"]:
    raise RuntimeError("locked 365-day headline did not reproduce")

out_path=ROOT/"results"/"extended_outcome_windows.json"
out_path.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(out,indent=2))
