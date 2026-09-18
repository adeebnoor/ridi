#!/usr/bin/env python3
from __future__ import annotations
import csv, json, pathlib
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parent/"primary_replay"
DATASETS=["nq","hotpotqa","fever","scifact"]
SEED=20260918
DRAWS=100000

rows={}
for d in DATASETS:
    p=ROOT/f"{d}_primary_records.jsonl"
    rows[d]=[json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows[d])==100

def mean(vals): return float(np.mean(np.asarray(vals,dtype=float)))
def pct(x): return 100.0*float(x)

dataset={}
for d in DATASETS:
    r=rows[d]
    changed=[x for x in r if x["delta_unconstrained"]>0]
    dataset[d]={
      "n":len(r),
      "updated_accuracy":mean([x["updated_correct"] for x in r]),
      "controlled_accuracy":mean([x["controlled_correct"] for x in r]),
      "paired_accuracy_difference":mean([x["correctness_difference"] for x in r]),
      "correctness_status_disagreement":mean([x["correctness_status_disagreement"] for x in r]),
      "answer_text_disagreement":mean([x["answer_text_disagreement"] for x in r]),
      "mean_changed_slots_unconstrained":mean([x["delta_unconstrained"] for x in r]),
      "mean_changed_slots_controlled":mean([x["j_eta"] for x in r]),
      "mean_changed_slots_reduction":mean([x["delta_unconstrained"]-x["j_eta"] for x in r]),
      "mean_avoidable_turnover_fraction_among_changed":mean([x["avoidable_turnover_fraction"] for x in changed]),
      "max_utility_regret":max(float(x["utility_regret"]) for x in r),
      "improved_correctness_n":sum(x["correctness_difference"]==1 for x in r),
      "worsened_correctness_n":sum(x["correctness_difference"]==-1 for x in r),
      "answer_changed_n":sum(x["answer_text_disagreement"] for x in r),
    }

metrics=[
 "paired_accuracy_difference",
 "correctness_status_disagreement",
 "answer_text_disagreement",
 "mean_changed_slots_reduction",
]
rng=np.random.default_rng(SEED)
boot={m:np.empty(DRAWS,dtype=float) for m in metrics}
boot_avoid=np.empty(DRAWS,dtype=float)
for b in range(DRAWS):
    dsvals={m:[] for m in metrics}
    av=[]
    for d in DATASETS:
        r=rows[d]
        idx=rng.integers(0,len(r),size=len(r))
        samp=[r[int(i)] for i in idx]
        dsvals["paired_accuracy_difference"].append(mean([x["correctness_difference"] for x in samp]))
        dsvals["correctness_status_disagreement"].append(mean([x["correctness_status_disagreement"] for x in samp]))
        dsvals["answer_text_disagreement"].append(mean([x["answer_text_disagreement"] for x in samp]))
        dsvals["mean_changed_slots_reduction"].append(mean([x["delta_unconstrained"]-x["j_eta"] for x in samp]))
        ch=[x["avoidable_turnover_fraction"] for x in samp if x["delta_unconstrained"]>0]
        av.append(mean(ch) if ch else 0.0)
    for m in metrics: boot[m][b]=mean(dsvals[m])
    boot_avoid[b]=mean(av)

macro={
 "updated_accuracy":mean([dataset[d]["updated_accuracy"] for d in DATASETS]),
 "controlled_accuracy":mean([dataset[d]["controlled_accuracy"] for d in DATASETS]),
 "paired_accuracy_difference":mean([dataset[d]["paired_accuracy_difference"] for d in DATASETS]),
 "correctness_status_disagreement":mean([dataset[d]["correctness_status_disagreement"] for d in DATASETS]),
 "answer_text_disagreement":mean([dataset[d]["answer_text_disagreement"] for d in DATASETS]),
 "mean_changed_slots_unconstrained":mean([dataset[d]["mean_changed_slots_unconstrained"] for d in DATASETS]),
 "mean_changed_slots_controlled":mean([dataset[d]["mean_changed_slots_controlled"] for d in DATASETS]),
 "mean_changed_slots_reduction":mean([dataset[d]["mean_changed_slots_reduction"] for d in DATASETS]),
 "mean_avoidable_turnover_fraction_among_changed":mean([dataset[d]["mean_avoidable_turnover_fraction_among_changed"] for d in DATASETS]),
 "improved_correctness_n":sum(dataset[d]["improved_correctness_n"] for d in DATASETS),
 "worsened_correctness_n":sum(dataset[d]["worsened_correctness_n"] for d in DATASETS),
 "answer_changed_n":sum(dataset[d]["answer_changed_n"] for d in DATASETS),
}
for m in metrics:
    macro[m+"_ci95"]=[float(np.quantile(boot[m],.025)),float(np.quantile(boot[m],.975))]
macro["mean_avoidable_turnover_fraction_among_changed_ci95"]=[float(np.quantile(boot_avoid,.025)),float(np.quantile(boot_avoid,.975))]

out={
 "protocol_id":"RIDI-NATURE-FRONTIER-DOWNSTREAM-v1",
 "primary_cell":{"k":10,"eta":0.001},
 "bootstrap":{"draws":DRAWS,"seed":SEED,"stratification":"dataset, resampling queries with replacement within each dataset"},
 "dataset":dataset,
 "equal_dataset_weight_macro":macro,
 "interpretation_boundary":"Finite 400-query common-retrievable panel; descriptive benchmark correctness. No non-inferiority claim and no universal eta claim."
}
(ROOT/"PRIMARY_AGGREGATE_RESULTS.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")

md=["# Frontier → downstream primary result","",
"Protocol: RIDI-NATURE-FRONTIER-DOWNSTREAM-v1  ",
"Primary cell: k=10, eta=0.001  ",
f"Bootstrap: {DRAWS:,} dataset-stratified query resamples; seed {SEED}.","",
"| Dataset | Updated acc. | Controlled acc. | Δ acc. | Correctness status changed | Answer text changed | Changed slots | Controlled slots | Slot reduction | Avoidable fraction |",
"|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
for d in DATASETS:
    x=dataset[d]
    md.append(f"| {d} | {pct(x['updated_accuracy']):.1f}% | {pct(x['controlled_accuracy']):.1f}% | {pct(x['paired_accuracy_difference']):+.1f} pp | {pct(x['correctness_status_disagreement']):.1f}% | {pct(x['answer_text_disagreement']):.1f}% | {x['mean_changed_slots_unconstrained']:.2f} | {x['mean_changed_slots_controlled']:.2f} | {x['mean_changed_slots_reduction']:.2f} | {pct(x['mean_avoidable_turnover_fraction_among_changed']):.2f}% |")
m=macro
md += ["",
"## Equal-dataset-weight macro","",
f"- Mean changed slots: {m['mean_changed_slots_unconstrained']:.4f} → {m['mean_changed_slots_controlled']:.4f}; reduction {m['mean_changed_slots_reduction']:.4f} (95% bootstrap interval {m['mean_changed_slots_reduction_ci95'][0]:.4f}–{m['mean_changed_slots_reduction_ci95'][1]:.4f}).",
f"- Query-mean avoidable-turnover fraction among changed queries: {pct(m['mean_avoidable_turnover_fraction_among_changed']):.2f}% (95% interval {pct(m['mean_avoidable_turnover_fraction_among_changed_ci95'][0]):.2f}–{pct(m['mean_avoidable_turnover_fraction_among_changed_ci95'][1]):.2f}%).",
f"- Updated vs controlled benchmark accuracy: {pct(m['updated_accuracy']):.2f}% vs {pct(m['controlled_accuracy']):.2f}%; paired difference {pct(m['paired_accuracy_difference']):+.2f} pp (95% interval {pct(m['paired_accuracy_difference_ci95'][0]):+.2f} to {pct(m['paired_accuracy_difference_ci95'][1]):+.2f} pp).",
f"- Correctness status changed in {pct(m['correctness_status_disagreement']):.2f}% of queries (95% interval {pct(m['correctness_status_disagreement_ci95'][0]):.2f}–{pct(m['correctness_status_disagreement_ci95'][1]):.2f}%).",
f"- Normalized answer text changed in {pct(m['answer_text_disagreement']):.2f}% (95% interval {pct(m['answer_text_disagreement_ci95'][0]):.2f}–{pct(m['answer_text_disagreement_ci95'][1]):.2f}%).",
f"- Directional correctness changes: {m['improved_correctness_n']} improved, {m['worsened_correctness_n']} worsened; answer text changed in {m['answer_changed_n']}/400 queries.",
"",
"These results do not establish non-inferiority or downstream benefit. They show the realized finite-panel trade-off under the locked rank-utility budget."
]
(ROOT/"PRIMARY_AGGREGATE_RESULTS.md").write_text("\n".join(md)+"\n",encoding="utf-8")
print(json.dumps(out,sort_keys=True))
