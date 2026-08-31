import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

R = json.load(open('layered_results.json'))
L = R['layers']
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "font.family": "DejaVu Sans"})
INK = "#14345f"; ACC = "#b3261e"; GREY = "#8a8f98"; GREEN = "#1a7f4b"; PIN = "#c9ced6"

labels = ["performance\nonly", "+ race\nparity", "+ risk-decile\ncalibration", "+ sex\nparity"]
cls  = [r['log10class'] for r in L]
age  = [r['ranges']["mean age"] for r in L]
fem  = [r['ranges']["female share"] for r in L]
obs_age = L[0]['observed']["mean age"]; obs_fem = L[0]['observed']["female share"]

fig, ax = plt.subplots(1, 3, figsize=(13, 3.9))

a = ax[0]
a.bar(range(4), cls, color=[INK, INK, GREY, GREY], width=.62)
for i, v in enumerate(cls):
    a.text(i, v + 26, f"10$^{{{v:.0f}}}$", ha="center", fontsize=9, fontweight="bold",
           color=INK if i < 2 else "#444")
a.axhline(80, color=ACC, ls="--", lw=1.2)
a.text(3.62, 96, "atoms in the\nobservable\nuniverse", ha="left", fontsize=7.2, color=ACC)
a.set_xticks(range(4)); a.set_xticklabels(labels, fontsize=7.8); a.set_xlim(-.62, 4.55)
a.set_ylabel("audit-equivalent cohorts (log$_{10}$)"); a.set_ylim(0, 1290)
a.set_title("a  No audit closes the class", loc="left", fontweight="bold", fontsize=10.5)

b = ax[1]
for i, (lo, hi) in enumerate(age):
    b.add_patch(Rectangle((i - .28, lo), .56, hi - lo, color=GREEN, alpha=.30, lw=0))
    b.plot([i - .28, i + .28], [lo, lo], color=GREEN, lw=2)
    b.plot([i - .28, i + .28], [hi, hi], color=GREEN, lw=2)
    b.text(i, hi + 1.2, f"{hi-lo:.1f} yr", ha="center", fontsize=8.2, fontweight="bold", color="#155f38")
b.axhline(obs_age, color=INK, lw=1.4, ls=":")
b.text(3.46, obs_age - 3.0, f"deployed {obs_age:.1f} yr", ha="right", fontsize=7.4, color=INK)
b.set_xticks(range(4)); b.set_xticklabels(labels, fontsize=7.8); b.set_xlim(-.6, 3.6)
b.set_ylabel("mean age of supervised cohort (yr)"); b.set_ylim(18, 56)
b.set_title("b  Age stays free at every layer", loc="left", fontweight="bold", fontsize=10.5)

c = ax[2]
for i, (lo, hi) in enumerate(fem):
    if hi - lo < 1e-9:
        c.plot([i], [lo * 100], marker="o", ms=7, color=PIN, mec=INK, mew=1.4, zorder=3)
        c.text(i, lo * 100 + 7.5, "pinned\nby the audit", ha="center", fontsize=7.6, color=INK)
    else:
        c.add_patch(Rectangle((i - .28, lo * 100), .56, (hi - lo) * 100, color=ACC, alpha=.26, lw=0))
        c.plot([i - .28, i + .28], [lo * 100, lo * 100], color=ACC, lw=2)
        c.plot([i - .28, i + .28], [hi * 100, hi * 100], color=ACC, lw=2)
        c.text(i, hi * 100 + 2.4, f"{(hi-lo)*100:.0f} pp", ha="center", fontsize=8.2,
               fontweight="bold", color=ACC)
c.axhline(obs_fem * 100, color=INK, lw=1.4, ls=":")
c.text(3.46, obs_fem * 100 - 5.5, f"deployed {obs_fem*100:.1f}%", ha="right", fontsize=7.4, color=INK)
c.set_xticks(range(4)); c.set_xticklabels(labels, fontsize=7.8); c.set_xlim(-.6, 3.6)
c.set_ylabel("female share of supervised cohort (%)"); c.set_ylim(-6, 82)
c.set_title("c  One protected axis does not constrain another",
            loc="left", fontweight="bold", fontsize=10.5)

fig.suptitle("An exact group-fairness audit leaves the supervised cohort undetermined — COMPAS, "
             "real two-year cohort (n = 6,172), deployed top-1,000",
             fontsize=10.6, fontweight="bold", y=1.03)
fig.text(0.5, -0.07,
         "Every cohort shown reproduces the deployed allocation's audited statistics exactly — precision@1,000 = 0.745, recall = 0.265, and, from panel b onward, an African-American share "
         "identical to the deployed 74.7% at every outcome level. Each is realisable by a deployable scorer. Verified by explicit construction (0/32 mismatches).",
         ha="center", fontsize=7.5, color=GREY)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig("fig_compas_audit_equivalence.png", dpi=200, bbox_inches="tight")
print("wrote fig_compas_audit_equivalence.png")
