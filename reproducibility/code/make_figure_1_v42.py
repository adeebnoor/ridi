"""Figure 1 (v42): a, schematic; b, identical record, mean accuracy and paired flips (Primary 800 + Scale 8B floor);
c, six sizes (unchanged data). Writes figure_data/Figure1b_v42_source.csv. Usage: python code/make_figure_1_v42.py --out rendered"""
import argparse, json
from pathlib import Path
import pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
ROOT = Path(__file__).resolve().parents[1]; DATA = ROOT/'figure_data'
BLUE, TEAL, RUST, GRAY, LIGHT, INK = '#1F507B','#14786C','#A84F24','#71808D','#D1DBDF','#172C3B'
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Liberation Sans','Arial','DejaVu Sans'],'font.size':7,
  'axes.titlesize':8,'axes.labelsize':7,'xtick.labelsize':6.5,'ytick.labelsize':6.5,'axes.spines.top':False,'axes.spines.right':False,
  'axes.linewidth':.6,'pdf.fonttype':42,'axes.labelcolor':INK})
def counts():
    p = pd.read_csv(DATA/'Primary_800_paired_outcomes.csv'); s = pd.read_csv(DATA/'Scale_4800_paired_correctness.csv')
    q = s[s.model=='qwen3-8b'].merge(p, on=['dataset','query_id'])
    assert (q.reference==q.reference_correct).all() and (q.exchange==q.exchange_correct).all() and p.retrieval_metrics_identical.all()
    n=len(p); k0=int(p.reference_correct.sum()); k1=int(p.exchange_correct.sum())
    R=int(((p.reference_correct==1)&(p.exchange_correct==0)).sum()); I=int(((p.reference_correct==0)&(p.exchange_correct==1)).sum())
    fR=int(((q.reference==1)&(q.batched_reference==0)).sum()); fI=int(((q.reference==0)&(q.batched_reference==1)).sum())
    return dict(n=n,grades_identical=int(p.retrieval_metrics_identical.sum()),k0=k0,k1=k1,R=R,I=I,floor_R=fR,floor_I=fI,
                feasible_min=abs(k1-k0),feasible_max=min(k0+k1,2*n-k0-k1),cancelled=2*min(R,I),visible=abs(I-R))
def main(out):
    c = counts(); n = c['n']
    pd.DataFrame([dict(quantity=k,value=v) for k,v in c.items()]).to_csv(DATA/'Figure1b_v42_source.csv',index=False)
    hist = json.loads((DATA/'Figure_1_historical.json').read_text())
    fig = plt.figure(figsize=(183/25.4, 4.3)); gs = fig.add_gridspec(2,2,height_ratios=[.62,1],width_ratios=[1.15,1],hspace=.55,wspace=.28,left=.105,right=.985,top=.95,bottom=.1)
    ax = fig.add_subplot(gs[0,:]); ax.set_axis_off(); ax.set_xlim(0,1); ax.set_ylim(0,1)
    ax.text(0,1,'a',fontsize=8,fontweight='bold',va='top'); ax.text(.025,1,'What rank-by-rank relevance grades fix',fontsize=7.5,va='top')
    for y,txt,vals in [(.5,'Reference',['R']+['U']*9),(.18,'Controlled exchange',['R']+['V']*9)]:
        ax.text(.02,y+.11,txt,va='center')
        for k,v in enumerate(vals):
            x=.2+k*.06; col=TEAL if v=='R' else BLUE if v=='U' else RUST
            ax.add_patch(Rectangle((x,y),.05,.22,facecolor=col,lw=0)); ax.text(x+.025,y+.11,'R' if v=='R' else v+str(k),color='white',ha='center',va='center',fontsize=6)
    ax.text(.82,.61,'grade vector\n(1,0,0,0,0,0,0,0,0,0)',ha='left',va='center',fontsize=6.3,color=INK)
    ax.text(.82,.29,'grade vector\n(1,0,0,0,0,0,0,0,0,0)',ha='left',va='center',fontsize=6.3,color=INK)
    ax.text(.02,-.02,'One credited document at rank 1 in this example. U and V denote distinct uncredited documents.',fontsize=6.3,color=GRAY)
    # b
    gb = gs[1,0].subgridspec(3,1,height_ratios=[.5,.75,1.1],hspace=1.15)
    a0=fig.add_subplot(gb[0]); a0.set_axis_off(); a0.set_xlim(0,1); a0.set_ylim(0,1)
    fig.text(.012,.555,'b',fontsize=8,fontweight='bold',va='top'); fig.text(.03,.555,'Identical record, almost unchanged mean, many flipped answers',fontsize=7.5,va='top')
    a0.add_patch(Rectangle((0,.05),1,.9,facecolor=LIGHT,lw=0))
    a0.text(.5,.5,f"Relevance record identical for {c['grades_identical']}/{n} questions",ha='center',va='center',fontsize=6.5)
    a1=fig.add_subplot(gb[1]); 
    for y,(lab,k) in enumerate([('Exchange',c['k1']),('Reference',c['k0'])]):
        a1.barh(y,100*k/n,color=BLUE if y else RUST,height=.6); a1.text(100*k/n+1,y,f'{100*k/n:.1f}% ({k}/{n})',va='center',fontsize=6.5)
    a1.set_yticks([0,1],['Exchange','Reference']); a1.set_xlim(0,100); a1.set_title('Mean accuracy (%)',loc='left',fontsize=6.5,pad=2); a1.tick_params(length=2)
    a2=fig.add_subplot(gb[2])
    rows=[('Re-execution\n(batch of 16)',c['floor_R'],c['floor_I']),('Context\nexchange',c['R'],c['I'])]
    for y,(lab,r,i) in enumerate(rows):
        a2.barh(y,-r,color=RUST,height=.6); a2.barh(y,i,color=TEAL,height=.6)
        a2.text(-r-2,y,f'{r} regressions',ha='right',va='center',fontsize=6.3); a2.text(i+2,y,f'{i} improvements',ha='left',va='center',fontsize=6.3)
    a2.axvline(0,color=INK,lw=.6); a2.set_yticks([0,1],[r[0] for r in rows]); a2.set_xlim(-150,150)
    a2.set_xticks([-100,-50,0,50,100],['100','50','0','50','100']); a2.set_xlabel('Questions changing scored correctness (n = 800)',labelpad=1); a2.tick_params(length=2)
    a2.text(0.5,1.22,f"Net change {c['visible']} questions (+1.75 points); {c['cancelled']} of {c['R']+c['I']} changes cancel in the mean.\nCompatible with the two accuracies: {c['feasible_min']}–{c['feasible_max']} changed ({100*c['feasible_min']/n:.2f}–{100*c['feasible_max']/n:.1f}%; Proposition 1b).",ha='center',va='center',fontsize=6.2,color=INK,transform=a2.transAxes)
    # c
    ax=fig.add_subplot(gs[1,1]); fig.text(.545,.555,'c',fontsize=8,fontweight='bold',va='top'); fig.text(.563,.555,'Paired correctness changes and net accuracy',fontsize=7.5,va='top')
    x=range(6); ax.bar(x,hist['changed_pct'],width=.55,color=BLUE,label='Correctness changed')
    ax.plot(x,hist['net_pct'],'o-',color=RUST,label='Net accuracy change',lw=1,ms=3)
    ax.axhline(0,color=GRAY,lw=.6); ax.set_xticks(list(x),hist['sizes']); ax.set_ylim(-4,21); ax.set_xlabel('Qwen3 size (parameters)',labelpad=1); ax.set_ylabel('Pooled percentage points')
    ax.grid(axis='y',color='#E2E8EB',lw=.5); ax.set_axisbelow(True); ax.legend(frameon=False,ncol=2,loc='upper left',fontsize=6.3); ax.tick_params(length=2)
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    fig.savefig(out/'Figure_1.pdf'); fig.savefig(out/'Figure_1.png',dpi=220)
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--out',default='rendered'); main(ap.parse_args().out)
