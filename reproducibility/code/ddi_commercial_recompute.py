#!/usr/bin/env python3
"""Recompute the commercial-model drug-interaction results from the raw outputs.

Inputs (case-level files held by the author; see the Data availability statement):
  --raw       raw_outputs_frozen_order.jsonl  one record per call: case_id, arm (B0, R0 or B1), label, status,
                                              actual_model, started_utc, ended_utc, prompt_sha256, context_sha256
  --cases     PER_CASE.csv                    case_id, drug_a, drug_b, gold (DDInter class)
  --qwen8     RIDI_DDI_v38_8_MAJOR_DOWNGRADES.csv  (optional) the eight pairs downgraded by Qwen3-8B
Output: JSON summary to stdout (and --out).

Registered primary analysis (OSF t9wvh): among DDInter-Major pairs labelled Major at B0, a Moderate or Minor label
at B1 versus at R0; two-sided exact McNemar test; paired percentile bootstrap of the risk difference.
Intervals here are the exact percentiles of the paired bootstrap distribution (multinomial enumeration), so they do
not depend on a random seed. Contrasts marked post hoc were not listed in the frozen pre-outcome manifest.
"""
import argparse, collections, csv, hashlib, json
from math import comb
from scipy.stats import binom

LOW = {'Moderate', 'Minor'}

def mcnemar(b, c):
    n = b + c
    return 1.0 if n == 0 else min(1.0, 2 * sum(comb(n, k) for k in range(0, min(b, c) + 1)) / 2 ** n)

def boot_exact(npos, nneg, n, alpha=0.05):
    """Exact percentile interval (in percentage points) for the bootstrap mean of paired differences in {+1, -1, 0}."""
    pp, pn = npos / n, nneg / n
    pmf = collections.defaultdict(float)
    for x in range(n + 1):
        px = binom.pmf(x, n, pp)
        if px < 1e-16: continue
        for y in range(n - x + 1):
            py = binom.pmf(y, n - x, pn / (1 - pp)) if pn > 0 else float(y == 0)
            if py < 1e-16: continue
            pmf[x - y] += px * py
    ks = sorted(pmf); acc = 0.0; lo = hi = None
    for k in ks:
        acc += pmf[k]
        if lo is None and acc >= alpha / 2: lo = k
        if hi is None and acc >= 1 - alpha / 2: hi = k
    return [round(100 * lo / n, 2), round(100 * hi / n, 2)]

def contrast(x, y, alpha=0.05):
    b = sum(1 for i, j in zip(x, y) if i and not j); c = sum(1 for i, j in zip(x, y) if j and not i)
    both = sum(1 for i, j in zip(x, y) if i and j); n = len(x)
    return {'update': sum(x), 'repeat': sum(y), 'n': n, 'update_only': b, 'repeat_only': c, 'both': both, 'neither': n - b - c - both,
            'difference_pp': round(100 * (sum(x) - sum(y)) / n, 4), 'exact_mcnemar_two_sided_p': mcnemar(b, c),
            'bootstrap_%d_interval_pp' % round(100 * (1 - alpha)): boot_exact(b, c, n, alpha)}

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--raw', required=True); ap.add_argument('--cases', required=True); ap.add_argument('--qwen8'); ap.add_argument('--out')
    a = ap.parse_args()
    raw = [json.loads(l) for l in open(a.raw, encoding='utf8') if l.strip()]
    cases = {r['case_id']: r for r in csv.DictReader(open(a.cases, encoding='utf8'))}
    by = collections.defaultdict(dict)
    for r in raw:
        assert r['arm'] not in by[r['case_id']], 'duplicate call'
        by[r['case_id']][r['arm']] = r
    assert set(by) == set(cases) and all(set(v) == {'B0', 'R0', 'B1'} for v in by.values())
    L = {c: {k: by[c][k]['label'] for k in ('B0', 'R0', 'B1')} for c in by}; G = {c: cases[c]['gold'] for c in by}
    ids = sorted(by)
    prim = [c for c in ids if G[c] == 'Major' and L[c]['B0'] == 'Major']
    res = {
        'registration': 'https://osf.io/t9wvh/', 'model_reported_by_api': sorted({r['actual_model'] for r in raw}),
        'calls': len(raw), 'completed': sum(r['status'] == 'COMPLETED' for r in raw), 'cases': len(ids),
        'first_call_started_utc': min(r['started_utc'] for r in raw), 'last_call_ended_utc': max(r['ended_utc'] for r in raw),
        'labels_returned': dict(collections.Counter(r['label'] for r in raw)),
        'identical_prompt_B0_R0': sum(by[c]['B0']['prompt_sha256'] == by[c]['R0']['prompt_sha256'] for c in ids),
        'different_context_B0_B1': sum(by[c]['B0']['context_sha256'] != by[c]['B1']['context_sha256'] for c in ids),
        'input_tokens': sum(r.get('input_tokens', 0) for r in raw), 'cached_input_tokens': sum(r.get('cached_input_tokens', 0) for r in raw),
        'raw_outputs_sha256': hashlib.sha256(open(a.raw, 'rb').read()).hexdigest(),
        'reference_classes': dict(collections.Counter(G.values())),
        'registered_primary': dict(contrast([int(L[c]['B1'] in LOW) for c in prim], [int(L[c]['R0'] in LOW) for c in prim]),
                                   endpoint='Major pairs labelled Major at B0: Moderate or Minor label at B1 versus at R0',
                                   criterion='all 519 records; n >= 50; excess > 0; exact P < 0.05; 95% interval above zero'),
        'registered_secondary_accuracy': {k: [sum(L[c][k] == G[c] for c in ids), len(ids)] for k in ('B0', 'R0', 'B1')},
    }
    p = res['registered_primary']
    p['criterion_met'] = bool(res['completed'] == 519 and p['n'] >= 50 and p['difference_pp'] > 0 and p['exact_mcnemar_two_sided_p'] < 0.05 and p['bootstrap_95_interval_pp'][0] > 0)
    gains = sum(1 for c in ids if L[c]['B1'] == G[c] and L[c]['B0'] != G[c]); losses = sum(1 for c in ids if L[c]['B1'] != G[c] and L[c]['B0'] == G[c])
    ci90 = boot_exact(gains, losses, len(ids), alpha=0.10)
    res['registered_secondary_accuracy_change'] = {'gains': gains, 'losses': losses, 'difference_pp': round(100 * (gains - losses) / len(ids), 4),
                                                   'bootstrap_90_interval_pp': ci90, 'equivalent_within_2pp': bool(ci90[0] > -2 and ci90[1] < 2)}
    res['post_hoc_label_change_vs_B0'] = contrast([int(L[c]['B1'] != L[c]['B0']) for c in ids], [int(L[c]['R0'] != L[c]['B0']) for c in ids])
    res['post_hoc_correctness_change_vs_B0'] = contrast([int((L[c]['B1'] == G[c]) != (L[c]['B0'] == G[c])) for c in ids],
                                                        [int((L[c]['R0'] == G[c]) != (L[c]['B0'] == G[c])) for c in ids])
    for k in ('post_hoc_label_change_vs_B0', 'post_hoc_correctness_change_vs_B0'):
        res[k]['status'] = 'post hoc: not listed in the frozen pre-outcome manifest'
    res['label_transitions_B0_to_B1'] = {'%s -> %s' % k: v for k, v in collections.Counter((L[c]['B0'], L[c]['B1']) for c in ids if L[c]['B0'] != L[c]['B1']).most_common()}
    res['label_transitions_B0_to_R0'] = {'%s -> %s' % k: v for k, v in collections.Counter((L[c]['B0'], L[c]['R0']) for c in ids if L[c]['B0'] != L[c]['R0']).most_common()}
    if a.qwen8:
        q8 = [frozenset((r['drug_a'], r['drug_b'])) for r in csv.DictReader(open(a.qwen8, encoding='utf8'))]
        pair = {c: frozenset((cases[c]['drug_a'], cases[c]['drug_b'])) for c in ids}
        sel = [c for c in ids if pair[c] in q8]
        res['qwen3_eight_downgraded_pairs_in_commercial_model'] = {
            'found': len(sel), 'labelled_major_at_B0': sum(L[c]['B0'] == 'Major' for c in sel),
            'downgraded_at_B1': sum(L[c]['B0'] == 'Major' and L[c]['B1'] in LOW for c in sel),
            'downgraded_at_R0': sum(L[c]['B0'] == 'Major' and L[c]['R0'] in LOW for c in sel)}
    txt = json.dumps(res, indent=1)
    print(txt)
    if a.out: open(a.out, 'w', encoding='utf8').write(txt + '\n')

if __name__ == '__main__':
    main()
