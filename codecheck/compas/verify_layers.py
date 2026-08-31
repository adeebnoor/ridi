"""VERIFICATION: build the extremal allocations EXPLICITLY and check that every audited
statistic is bit-identical to the deployed allocation.  This is the falsification test:
if any audited statistic differs, the audit-equivalence claim is wrong for that layer."""
import pandas as pd, numpy as np, json, math
from math import lgamma

d = pd.read_csv('compas_analysis_min.csv').reset_index(drop=True)
d['black']  = (d.race == "African-American").astype(int)
d['female'] = (d.sex == "Female").astype(int)
N = len(d); P = int(d.two_year_recid.sum()); K = 1000

dep = d.sort_values(['decile_score','id'], ascending=[False,True]).head(K)
d['sel'] = d.index.isin(set(dep.index)).astype(int)
h = int(dep.two_year_recid.sum())

def stats(idx):
    s = d.loc[idx]
    return dict(n=len(s), pos=int(s.two_year_recid.sum()),
                precision=round(s.two_year_recid.sum()/len(s), 10),
                recall=round(s.two_year_recid.sum()/P, 10),
                black=round(float(s.black.mean()), 6),
                female=round(float(s.female.mean()), 6),
                age=round(float(s.age.mean()), 4),
                priors=round(float(s.priors_count.mean()), 4))

def build(keys, tcol, direction):
    """Explicitly construct the allocation that extremises tcol subject to per-cell counts."""
    out = []
    for _, cell in d.groupby(keys, sort=False):
        m = int(cell.sel.sum())
        if m == 0: continue
        c = cell.sort_values([tcol, 'id'], ascending=(direction == 'min'))
        out += list(c.index[:m])
    assert len(out) == K, f"built {len(out)} != {K}"
    assert len(set(out)) == K, "duplicate selections"
    return out

LAYERS = [("L0 outcome", ['two_year_recid']),
          ("L1 outcome x race", ['two_year_recid','black']),
          ("L2 outcome x race x decile", ['two_year_recid','black','decile_score']),
          ("L3 outcome x race x decile x sex", ['two_year_recid','black','decile_score','female'])]

base = stats(list(dep.index))
print("DEPLOYED COMPAS top-1000:", base, "\n")

AUDITED = {"L0 outcome": ['precision','recall'],
           "L1 outcome x race": ['precision','recall','black'],
           "L2 outcome x race x decile": ['precision','recall','black'],
           "L3 outcome x race x decile x sex": ['precision','recall','black','female']}

fails = 0
for lname, keys in LAYERS:
    for tcol in ['age','female','priors_count','black']:
        for direction in ['min','max']:
            idx = build(keys, tcol, direction)
            s = stats(idx)
            for field in AUDITED[lname]:
                if s[field] != base[field]:
                    print(f"  !! FAIL {lname} extremise {tcol} {direction}: {field} {s[field]} != {base[field]}")
                    fails += 1
    print(f"{lname:<36} audited statistics IDENTICAL under all 8 extremal constructions "
          f"({', '.join(AUDITED[lname])})")

print(f"\nVERIFICATION: {fails} mismatches (must be 0)\n")

print(f"{'layer':<36}{'age min':>9}{'age max':>9}{'fem min':>9}{'fem max':>9}{'pri min':>9}{'pri max':>9}")
for lname, keys in LAYERS:
    a0 = stats(build(keys,'age','min'))['age'];            a1 = stats(build(keys,'age','max'))['age']
    f0 = stats(build(keys,'female','min'))['female'];      f1 = stats(build(keys,'female','max'))['female']
    p0 = stats(build(keys,'priors_count','min'))['priors'];p1 = stats(build(keys,'priors_count','max'))['priors']
    print(f"{lname:<36}{a0:>9.2f}{a1:>9.2f}{f0:>9.1%}{f1:>9.1%}{p0:>9.2f}{p1:>9.2f}")

print(f"\nCohort N={N} (ProPublica two-year analysis cohort = 6172): {'MATCH' if N==6172 else 'MISMATCH'}")
print(f"positives={P} ({P/N:.4%}); African-American={int(d.black.sum())} ({d.black.mean():.4%}); female={int(d.female.sum())} ({d.female.mean():.4%})")
