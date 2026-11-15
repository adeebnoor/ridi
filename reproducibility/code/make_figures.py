"""Generate Figures 1, 3, 4 and Supplementary Figure 1 using the accompanying source tables."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.stats import binomtest
from sklearn.metrics import roc_auc_score, roc_curve

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'figure_data'
HOLD = ROOT / 'holdout'
ORDER = ['0.6','1.7','4','8','14','32']
BLUE, TEAL, RUST, GRAY, LIGHT, INK = '#1F507B','#14786C','#A84F24','#71808D','#D1DBDF','#172C3B'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':11,
                    'axes.titleweight':'bold','axes.titlecolor':INK,'axes.spines.top':False,
                    'axes.spines.right':False,'axes.labelcolor':INK,'pdf.fonttype':42})
def panel(ax, letter, title, ygrid=True):
    ax.set_title(letter+'   '+title,loc='left',pad=10)
    if ygrid:
        ax.grid(axis='y',color='#E2E8EB',linewidth=.65)
        ax.set_axisbelow(True)
def save(fig, name, dest):
    dest.mkdir(parents=True,exist_ok=True)
    fig.savefig(dest/(name+'.pdf'),bbox_inches='tight',pad_inches=.14)
    fig.savefig(dest/(name+'.png'),dpi=190,bbox_inches='tight',pad_inches=.14)
    plt.close(fig)
def pct(x): return np.array(x)*100
def transfer_vars():
    table = pd.read_csv(DATA/'Transfer_800_paired_correctness.csv')
    probes = ['predictor_1_7b','predictor_4b','predictor_8b']
    fragility = sum((table[p+'_reference']!=table[p+'_exchange']).astype(int) for p in probes)
    difficulty = sum(1-table[p+'_reference'] for p in probes)
    return table, fragility, difficulty
def figure1(out):
    data=json.loads((DATA/'Figure_1_historical.json').read_text())
    fig,axes=plt.subplots(2,1,figsize=(8,6.1),layout='constrained',height_ratios=[1,1.55])
    ax=axes[0];panel(ax,'a','What rank-by-rank relevance grades fix',False);ax.set_axis_off()
    for y,txt,vals in [(0.56,'Reference',['R']+['U']*9),(0.28,'Controlled exchange',['R']+['V']*9)]:
        ax.text(.005,y+.073,txt,transform=ax.transAxes,va='center',fontsize=9)
        for k,val in enumerate(vals):
            x=.225+k*.075;c=TEAL if val=='R' else BLUE if val=='U' else RUST
            ax.add_patch(Rectangle((x,y),.061,.145,facecolor=c,transform=ax.transAxes))
            ax.text(x+.0305,y+.073,('R' if val=='R' else val+str(k)),transform=ax.transAxes,color='white',ha='center',va='center',fontsize=8.1)
    ax.text(.005,.035,'One credited document at rank 1 in this example. U and V denote distinct uncredited documents.',transform=ax.transAxes,fontsize=8.1)
    ax=axes[1];panel(ax,'b','Paired correctness changes and net accuracy')
    x=np.arange(6);ax.bar(x,data['changed_pct'],width=.55,color=BLUE,label='Correctness changed')
    ax.plot(x,data['net_pct'],'o-',color=RUST,label='Net accuracy change',lw=1.5)
    ax.axhline(0,color=GRAY,lw=.8);ax.set_xticks(x,data['sizes']);ax.set_ylim(-4,21);ax.set_xlabel('Qwen3 size (parameters)');ax.set_ylabel('Pooled percentage points')
    ax.legend(frameon=False,ncol=2,loc='upper left');save(fig,'Figure_1',out)
def figure3(out):
    fig,axes=plt.subplots(3,2,figsize=(10.7,10.8),layout='constrained')
    a,b,c,d,e,f=axes.flat
    cells=pd.read_csv(DATA/'Figure5_factorial_cells_v28.csv')
    panel(a,'a','Context change across execution settings')
    x=np.arange(len(cells));mid=pct(cells.turnover)
    a.errorbar(x,mid,yerr=[mid-pct(cells.ci95_lower),pct(cells.ci95_upper)-mid],fmt='o',capsize=2.5,color=BLUE)
    a.axhline(1.5,ls='--',lw=1.2,color=RUST,label='Largest execution difference');a.set_ylim(0,28)
    a.set_xticks(x,[('HF' if t.backend=='hf' else 'vLLM')+'\n'+str(t.batch_size)+' / '+str(t.repeat) for t in cells.itertuples()],fontsize=7)
    a.set_xlabel('Backend / batch size and repeat');a.set_ylabel('Correctness changed (%)');a.legend(loc='upper right',fontsize=7.4,frameon=False)
    comp=pd.read_csv(DATA/'Figure5_factorial_components_v28.csv').set_index('term').contribution
    total=comp.sum();vals=[comp['context'],comp.reindex(['backend','batch_size','repeat']).sum()];vals.append(total-sum(vals)); vals=pct(vals)/total
    panel(b,'b','Within-question variance in the factorial',False)
    b.barh([2,1,0],vals,color=[BLUE,TEAL,GRAY],height=.5);b.set_yticks([2,1,0],['Context','Other main terms','Interactions']);b.set_xlim(0,110);b.set_xlabel('Share of measured variance (%)')
    for y,v in zip([2,1,0],vals): b.text(v+1.3,y,f'{v:.1f}%',va='center',fontsize=8)
    natural=pd.read_csv(DATA/'Figure5_natural_transitions_v28.csv').set_index('stratum')
    panel(c,'c','Nested exact-record SciFact groups',False)
    keys=['exact_grade_vector','exact_with_both_credited','strict_uncredited_membership_change_with_credited_evidence']
    for yi,key in zip([2,1,0],keys):
        t=natural.loc[key];v=100*t.turnover
        c.errorbar(v,yi,xerr=[[v-100*t.ci95_lower],[100*t.ci95_upper-v]],fmt='o',color=BLUE,capsize=3)
        c.text(10.6,yi,f'{int(t.changes)}/{int(t.pairs)}',va='center',fontsize=8)
    c.set_yticks([2,1,0],['Identical grades','Credited in both','Credited text held']);c.set_ylim(-.5,2.5);c.set_xlim(0,15);c.set_xlabel('Correctness changed (%)')
    panel(d,'d','BM25 segmentation across three corpora')
    counts=json.loads((DATA/'Natural_segmentation_561_summary.json').read_text())
    eligible=counts['eligible']
    vals=np.array([counts['qwen_changed'],counts['mistral_changed'],counts['either_changed']])
    x=np.arange(3);rates=pct(vals/eligible)
    cis=np.array([binomtest(int(n),eligible).proportion_ci(method='exact') for n in vals])*100
    d.bar(x,rates,width=.5,color=[BLUE,RUST,TEAL]);d.errorbar(x,rates,yerr=[rates-cis[:,0],cis[:,1]-rates],fmt='none',capsize=3,color=INK)
    d.set(xticks=x,xticklabels=['Qwen3-8B','Mistral-7B','Either model'],ylim=(0,14),ylabel='Correctness changed (%)')
    panel(e,'e','Overlap on the 561 eligible questions',False)
    qwen,mistral,either=vals
    both=qwen+mistral-either
    overlap=[qwen-both,both,mistral-both,eligible-either]
    e.barh([3,2,1,0],overlap,color=[BLUE,TEAL,RUST,LIGHT]);e.set_yticks([3,2,1,0],['Qwen only','Both','Mistral only','Neither'])
    for y,v in zip([3,2,1,0],overlap):e.text(v+4,y,str(v),va='center',fontsize=8)
    e.set_xlabel('Questions');e.set_xlim(0,565)
    report=json.loads((HOLD/'Holdout_Frozen_Analysis.json').read_text())['frozen']
    panel(f,'f','Held-out change above re-execution',False)
    tick=[];names=[]
    for i,(h,m,label) in enumerate([('H1','qwen3','W  ·  Qwen'),('H1','mistral','W  ·  Mistral'),('H3','qwen3','D  ·  Qwen'),('H3','mistral','D  ·  Mistral')]):
        t=report[h][m] if h=='H1' else report[h][m]['all'];v=100*t['excess_eqw'];lo,hi=pct(t['excess_95ci']);y=[3.4,2.4,1,0][i]
        f.errorbar(v,y,xerr=[[v-lo],[hi-v]],fmt='o' if h=='H1' else 's',color=BLUE if m=='qwen3' else RUST,capsize=3);tick.append(y);names.append(label)
        f.text(17.4,y,f"{t['changes']} / {t['control_changes']}",va='center',fontsize=7.5)
    f.axvline(2,ls='--',lw=.85,color=GRAY);f.set_yticks(tick,names);f.set_ylim(-.55,4.08);f.set_xlim(-.4,21.8);f.set_xlabel('Excess (percentage points), 95% interval')
    f.text(17.4,3.95,'Changed / ctrl',fontsize=7.1)
    save(fig,'Figure_3',out)
def figure4(out):
    t,frag,_=transfer_vars();scale=pd.read_csv(DATA/'Scale_4800_paired_correctness.csv')
    n_sizes=(scale.reference!=scale.exchange).groupby([scale.dataset,scale.query_id]).sum()
    counts=np.bincount(n_sizes,minlength=7);assert sum(counts[1:])==293 and sum(counts[2:])==151
    fig,axes=plt.subplots(1,3,figsize=(12,3.9),layout='constrained');a,b,c=axes
    panel(a,'a','Recurrence across model sizes');a.bar(range(7),counts,color=BLUE)
    for i,v in enumerate(counts):a.text(i,v+6,str(v),ha='center',fontsize=7.4)
    a.set(xticks=range(7),ylim=(0,565),xlabel='Number of sizes changing',ylabel='Questions')
    panel(b,'b','Transitions by small-probe score')
    panel(c,'c','Prediction of any target change',False)
    for j,(m,label,col,band) in enumerate([('qwen3_32b','Qwen3',BLUE,'0.621–0.736'),('olmo2_32b','OLMo-2',RUST,'0.620–0.720')]):
        ref=t[m+'_reference'];ex=t[m+'_exchange'];change=(ref!=ex)
        for j2,(baseline,marker,ls,name) in enumerate([(1,'o','-','regression'),(0,'s','--','gain')]):
            vals=[];bottom=[];top=[]
            for z in range(4):
                keep=(ref==baseline)&(frag==z);k=int(change[keep].sum());n=int(keep.sum());val=k/n
                lo,hi=binomtest(k,n).proportion_ci(method='wilson');vals.append(100*val);bottom.append(100*(val-lo));top.append(100*(hi-val))
            b.errorbar(np.arange(4)-.12+.08*(2*j+j2),vals,yerr=[np.maximum(bottom,0),np.maximum(top,0)],fmt=marker+ls,color=col,lw=.8,ms=3,capsize=1.3,label=label+' '+name)
        fx,ty,_=roc_curve(change,frag);auc=roc_auc_score(change,frag)
        c.plot(fx,ty,'o-',ms=3,color=col,label=f'{label}  {auc:.3f}\n({band})')
    b.set(xticks=range(4),ylim=(-3,105),xlabel='Probe fragility (0–3)',ylabel='Conditional transition rate (%)')
    b.legend(loc='upper left',fontsize=6,frameon=False);c.plot([0,1],[0,1],'--',color=GRAY,lw=.8)
    c.set(xlabel='False-positive rate',ylabel='True-positive rate',xlim=(0,1),ylim=(0,1.025));c.legend(frameon=False,loc='lower right',fontsize=6.7)
    save(fig,'Figure_4',out)
def supplement(out):
    fig,axes=plt.subplots(2,2,figsize=(9.7,7.5),layout='constrained');a,b,c,d=axes.flat
    summ=json.loads((DATA/'Source_Reconciliation.json').read_text())['summary']
    vals=[summ['qwen3-'+m+'b'] for m in ORDER];xx=np.arange(6)
    panel(a,'a','Answers carrying an insufficiency marker')
    for offset,key,col,label in [(-.18,'ref',BLUE,'Reference'),(.18,'exchange',RUST,'Exchange')]:
        a.bar(xx+offset,[100*v[key]/v['n'] for v in vals],width=.36,color=col,label=label)
    a.set_xticks(xx,[m+'B' for m in ORDER]);a.set_ylim(0,32);a.set_ylabel('Marker present (%)');a.legend(frameon=False,fontsize=7)
    for i,v in enumerate(vals):
        p=binomtest(v['stopped'],v['stopped']+v['started'],.5).pvalue
        a.text(i,100*v['exchange']/v['n']+1.6,format(p,'.2g') if p>=.01 else format(p,'.1e').replace('e-0','e−'),ha='center',fontsize=6.5)
    panel(b,'b','Rule-based composition of transitions')
    base=np.zeros(6)
    for key,label,col in [('abstention','Incorrect-side marker',RUST),('containment','Containment',TEAL),('other','Other',BLUE)]:
        v=np.array([row.get(key,0) for row in vals]);b.bar(xx,v,bottom=base,color=col,width=.55,label=label);base+=v
    for i,v in enumerate(base):b.text(i,v+2,str(int(v)),ha='center',fontsize=7)
    b.set_xticks(xx,[m+'B' for m in ORDER]);b.set(ylabel='Correctness transitions',ylim=(0,181));b.legend(frameon=False,fontsize=7,ncol=2,loc='upper left')
    t,frag,diff=transfer_vars()
    for ax,key,letter,model,want in [(c,'qwen3_32b','c','Qwen3-32B',(407,50)),(d,'olmo2_32b','d','OLMo-2-32B',(424,68))]:
        keep=t[key+'_reference']==1;event=t.loc[keep,key+'_exchange']==0
        assert (int(keep.sum()),int(event.sum()))==want
        panel(ax,letter,model+' regression ('+str(want[1])+'/'+str(want[0])+')',False)
        for predictor,label,col in [(diff,'Difficulty',GRAY),(frag,'Fragility',TEAL),(diff+frag,'Sum',RUST)]:
            fx,ty,_=roc_curve(event,predictor.loc[keep]);auc=roc_auc_score(event,predictor.loc[keep]);ax.plot(fx,ty,'o-',color=col,ms=3,label=f'{label}  {auc:.3f}')
        ax.plot([0,1],[0,1],'--',color=LIGHT);ax.set(xlabel='False-positive rate',ylabel='True-positive rate',xlim=(0,1),ylim=(0,1.025));ax.legend(frameon=False,loc='lower right',fontsize=7.5)
    save(fig,'Supplementary_Figure_1',out)
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    for fn in (figure1,figure3,figure4,supplement):fn(args.out)
