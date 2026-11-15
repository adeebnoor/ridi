#!/usr/bin/env python3
"""Run the pre-registered analysis (score_and_analyze.py -> frozen holdout_analysis.py, unmodified) and write RESULTS/.
Usage: make_results.py [ROOT]   (ROOT defaults to the study folder; used only for testing on synthetic data)"""
import json, subprocess, sys, shutil, glob, datetime, hashlib
from pathlib import Path
ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/workspace/COMMERCIAL_v45')
MODELS = ['gpt-5.4-mini', 'claude-sonnet-5.5', 'gemini-3.8-flash']
subprocess.run([sys.executable, str(ROOT/'code'/'score_and_analyze.py'), '--gold', str(ROOT/'frozen_inputs'/'holdout_1500_gold.jsonl')], check=True, cwd=str(ROOT))
rep = json.load(open(ROOT/'analysis'/'H1_H4_commercial.json'))
res = ROOT/'RESULTS'; res.mkdir(exist_ok=True)
L = json.load(open(ROOT/'SPEND_LEDGER.json'))
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
# ---- operational stats from raw outputs
ops = {}
for m in MODELS:
    rows = [json.loads(l) for l in open(ROOT/'runs'/m/'raw_outputs.jsonl')]
    ok = [r for r in rows if 'error' not in r]
    ops[m] = {'calls_recorded': len(rows), 'completed_pct': round(100 * len(rows) / 7500, 2), 'errors': len(rows) - len(ok),
        'empty': sum(1 for r in ok if not (r.get('text') or '').strip()), 'truncated': sum(1 for r in ok if r.get('finish') in ('length', 'max_tokens')),
        'spend_usd': round(L['by_model'].get(m, 0), 4), 'by_arm': {}}
    o = ops[m]; o['empty_pct'] = round(100 * o['empty'] / max(1, len(ok)), 3); o['truncated_pct'] = round(100 * o['truncated'] / max(1, len(ok)), 3)
    for r in rows: o['by_arm'][r['arm']] = o['by_arm'].get(r['arm'], 0) + 1
    done = ROOT/'logs'/f'DONE_{m}.json'; o['supervisor'] = json.load(open(done)) if done.exists() else None
total_spend = L['total']
f = lambda x, d=4: 'NA' if x is None else (f'{x:.{d}f}' if isinstance(x, (int, float)) else str(x))
ci = lambda c: 'NA' if not c or c[0] is None else f'[{c[0]:.4f}, {c[1]:.4f}]'
R = rep['frozen']; FM = rep['format']
passed = [m for m in MODELS if R['H1'][m].get('H1_supported_holm')]
if len(passed) >= 2: verdict = 'MET'; verdict_txt = 'Replication criterion MET: H1c passes (Holm-adjusted) for at least two of the three models.'
elif len(passed) == 1: verdict = 'NOT MET (supported in one model)'; verdict_txt = f'Replication criterion NOT MET; supported in one model ({passed[0]}).'
else: verdict = 'NOT MET'; verdict_txt = 'Replication criterion NOT MET: H1c passes for none of the three models.'
inc = [m for m in MODELS if ops[m]['completed_pct'] < 100]
def h_table(H, title):
    s = f'### {title}\n| Model | n eligible | excluded (missing arm) | change rate (eq. wt) | re-execution rate (eq. wt) | excess (eq. wt) | 95% CI of excess | one-sided P(excess ≤ 0.02) | Holm-supported |\n|---|---|---|---|---|---|---|---|---|\n'
    for m in MODELS:
        h = H[m]; s += f"| {m} | {h['n']} | {h['excluded_missing_arm']} | {f(h.get('change_rate_eqw'))} | {f(h.get('control_rate_eqw'))} | {f(h.get('excess_eqw'))} | {ci(h.get('excess_95ci'))} | {f(h.get('p_one_sided_excess_le_margin'))} | {h.get('H1_supported_holm','n/a')} |\n"
    return s
md = f"""# RIDI-CONFIRM-C: confirmatory results (commercial-model replication)
Registration: https://osf.io/anbjd/ (DOI 10.17605/OSF.IO/ANBJD). Generated {datetime.datetime.now().astimezone().isoformat()} (Asia/Riyadh) by code/make_results.py from the frozen analysis script (unmodified). Analysis report: analysis/H1_H4_commercial.json (SHA-256 {sha(ROOT/'analysis'/'H1_H4_commercial.json')}), scores: analysis/scores_commercial.csv.

## Verdict
**{verdict_txt}**
Study-level criterion: H1c must pass (Holm-adjusted, one-sided alpha 0.025) for at least two of three models. Passing models: {', '.join(passed) or 'none'}.
{('**Incomplete runs:** ' + ', '.join(inc) + ' (see completion table).') if inc else 'All three runs completed all 7,500 calls.'}

## Completion, empty and truncated answers, spend
| Model | calls recorded | completed | errors (missing arms) | empty | truncated | spend (USD) | restarts |
|---|---|---|---|---|---|---|---|
""" + ''.join(f"| {m} | {ops[m]['calls_recorded']} | {ops[m]['completed_pct']}% | {ops[m]['errors']} | {ops[m]['empty']} ({ops[m]['empty_pct']}%) | {ops[m]['truncated']} ({ops[m]['truncated_pct']}%) | {ops[m]['spend_usd']} | {(ops[m]['supervisor'] or {}).get('restarts','?')} |\n" for m in MODELS) + f"""
Total ledger spend including technical checks: USD {total_spend:.4f} (hard cap 200; Gemini cap 18).

## H1c (primary), E1_win, frozen scorer
{h_table(R['H1'], 'H1c: bm25_whole vs bm25_window, excess over re-execution')}
## H2c, strict E3_win (descriptive if fewer than 100 questions)
{h_table(R['H2'], 'H2c')}
Descriptive only: {', '.join(m + '=' + str(R['H2'][m].get('descriptive_only')) for m in MODELS)}.

## H3c, contriever vs bm25_whole, E1_dense (nominal)
| Model | stratum | n | change rate (eq. wt) | re-execution rate (eq. wt) | excess | 95% CI | one-sided P(excess ≤ 0.02) |
|---|---|---|---|---|---|---|---|
""" + ''.join(f"| {m} | {k} | {v['n']} | {f(v.get('change_rate_eqw'))} | {f(v.get('control_rate_eqw'))} | {f(v.get('excess_eqw'))} | {ci(v.get('excess_95ci'))} | {f(v.get('p_one_sided_excess_le_margin'))} |\n" for m in MODELS for k, v in R['H3'][m].items()) + f"""
## H4c (descriptive): overlap of changed E1_win questions
n E1_win = {R['H4']['n_E1']}; changed in either model = {R['H4']['either']} (exact 95% CI {ci(R['H4']['either_exact95'])}); in all three = {R['H4']['both']}; only in one model: {json.dumps(R['H4']['only'])}.

## Sensitivity: format-scorer variant (not confirmatory)
{h_table(FM['H1'], 'H1c with the format scorer')}
## Deviations and operational notes
- Settings, prompts, scorer, call order and analysis are exactly those of addendum v1.3 (osf.io/anbjd); runner and analysis code are unmodified (hashes in MANIFEST_SHA256.txt).
- Operational interruptions (see runs/RUN_LOG.md): a runner crash caused by the runner's ledger file being read while another process was writing it, and two hung HTTP calls; the runner was resumed from its saved outputs, and an in-flight call may have been repeated (possible extra billed calls not in the ledger). The runner was supervised by code/supervisor.py (restart after a crash or a 10-minute stall; stop rules for >2% empty answers, repeated failures and near-cap spend).
- Missing arms (errors) are excluded under the registered rule and counted in the tables above.
- The 'whole_rep_b1' / 'whole_rep_b16' labels denote independent repeat calls (declared in the addendum).
- Gemini max_tokens 640 and GPT/Claude 128 as pre-registered.
"""
(res/'RESULTS.md').write_text(md)
json.dump({'verdict': verdict, 'passed_models': passed, 'ops': ops, 'total_spend_usd': total_spend, 'report': rep}, open(res/'results_summary.json', 'w'), indent=1, default=float)
shutil.copy(ROOT/'analysis'/'H1_H4_commercial.json', res/'H1_H4_commercial.json'); shutil.copy(ROOT/'SPEND_LEDGER.json', res/'SPEND_LEDGER_final.json')
ar_v = {'MET': 'تحقق معيار التكرار', 'NOT MET': 'لم يتحقق معيار التكرار', 'NOT MET (supported in one model)': 'لم يتحقق معيار التكرار (مدعوم في نموذج واحد فقط)'}[verdict]
ar = f"""# ملخص النتائج (RIDI-CONFIRM-C) — التكرار على النماذج التجارية
التسجيل: https://osf.io/anbjd/ (DOI 10.17605/OSF.IO/ANBJD)

## الحكم: {ar_v}
المعيار المسجَّل: أن تنجح الفرضية H1c (بعد تصحيح Holm، ألفا أحادي الطرف 0.025) في نموذجين على الأقل من ثلاثة. النماذج الناجحة: {('، '.join(passed)) if passed else 'لا يوجد'}.

## H1c (الأساسية)
| النموذج | عدد الأسئلة | الفائض عن حد إعادة التنفيذ | فترة الثقة 95% | P أحادي الطرف | Holm |
|---|---|---|---|---|---|
""" + ''.join(f"| {m} | {R['H1'][m]['n']} | {f(R['H1'][m].get('excess_eqw'))} | {ci(R['H1'][m].get('excess_95ci'))} | {f(R['H1'][m].get('p_one_sided_excess_le_margin'))} | {'نجح' if R['H1'][m].get('H1_supported_holm') else 'لم ينجح'} |\n" for m in MODELS) + f"""
## الاكتمال والتكلفة
""" + ''.join(f"- {m}: اكتمل {ops[m]['completed_pct']}% ({ops[m]['calls_recorded']} من 7500)، أخطاء {ops[m]['errors']}، إجابات فارغة {ops[m]['empty_pct']}%، مقتطعة {ops[m]['truncated_pct']}%، التكلفة {ops[m]['spend_usd']} دولار.\n" for m in MODELS) + f"""- إجمالي الإنفاق (مع الفحوصات التقنية): {total_spend:.2f} دولار من سقف 200 دولار.

## ملاحظات
- لم يتغير أي إعداد عن الإضافة المسجَّلة (v1.3). التحليل هو النص المجمّد دون تعديل.
- توقفات تشغيلية: انهيار واحد بسبب قراءة ملف السجل المالي أثناء الكتابة وتعليق طلبَين؛ استؤنف التشغيل من الملفات المحفوظة (قد تتكرر مكالمة واحدة مدفوعة غير مسجّلة في السجل).
- التفاصيل الكاملة في RESULTS.md، وفرضيات H2c وH3c وH4c فيه أيضاً.
"""
(res/'SUMMARY_AR.md').write_text(ar)
print('RESULTS written', verdict)
