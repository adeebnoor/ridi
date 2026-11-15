#!/usr/bin/env python3
"""Rebuild the archived primary-exchange figure from its original chart source and supplied case data."""
from pathlib import Path
import json,csv,math,hashlib,collections,re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score,roc_curve
from scipy.stats import beta
from textwrap import fill

ROOT=Path(__file__).resolve().parent
SRC=ROOT.parent/'figure_data'
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out',type=Path,required=True)
OUT=parser.parse_args().out
OUT.mkdir(exist_ok=True)
NAVY='#163D57'; BLUE='#2C7799'; ORANGE='#BA692F'; GREEN='#3E8D77'; GREY='#87929A'; LIGHT='#D2DFE4'; BG='white'; DARK='#202B34'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':9.5,'axes.titlesize':10,'xtick.labelsize':8.5,'ytick.labelsize':8.5,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none','figure.facecolor':'white','axes.facecolor':'white'})
def rows(name):return list(csv.DictReader(open(SRC/name,newline='',encoding='utf8')))
def jj(name):return json.load(open(SRC/name,encoding='utf8'))
def panel(ax,letter,title):
 ax.set_title(f'{letter}  {title}',fontweight='bold',loc='left',pad=12,color=NAVY)
def style(ax,axis='y'):
 ax.grid(axis=axis,color='#E2E7EA',lw=.7);ax.set_axisbelow(True)
def save(fig,name):
 for ext in ('png','svg','pdf'):
  fig.savefig(OUT/(name+'.'+ext),dpi=240,bbox_inches='tight',pad_inches=.18)
 plt.close(fig)

def xerr_fmt(ax,v,lo,hi,y,fmt='o',color=BLUE):
 ax.errorbar([v],[y],xerr=[[max(0,v-lo)],[max(0,hi-v)]],fmt=fmt,capsize=3,ms=5,elinewidth=1.3,color=color)

primary=rows('Primary_800_paired_outcomes.csv');scale=rows('Scale_4800_paired_correctness.csv')
transfer=rows('Transfer_800_paired_correctness.csv')
assert len(primary)==800 and len(scale)==4800 and len(transfer)==800
for x in primary:assert x['retrieval_metrics_identical']=='True'
assert sum(int(x['reference_correct'])!=int(x['exchange_correct']) for x in primary)==134
assert sum(int(x['reference_correct'])==1 and int(x['exchange_correct'])==0 for x in primary)==60
assert sum(int(x['reference_correct'])==0 and int(x['exchange_correct'])==1 for x in primary)==74
case275=next(x for x in primary if x['dataset']=='scifact' and x['query_id']=='275')
assert case275['reference_canonical']=='SUPPORTS' and case275['exchange_canonical']=='REFUTES'
scale_reg=jj('SCALE_REGISTERED_REPLAY_COMPACT_VERIFIED.json')['results']
# Figure 2: controlled same-grade observations + registered replication.
fig=plt.figure(figsize=(11.6,12.3))
g=fig.add_gridspec(3,2,height_ratios=[1.0,1.03,1.12],hspace=.55,wspace=.37)
a=fig.add_subplot(g[0,0]);panel(a,'a','Example: identical graded ranks, reversed verdict')
a.axis('off');a.text(0,.96,'SciFact claim 275 (released label: SUPPORTS)',weight='bold',color=NAVY,transform=a.transAxes,va='top',fontsize=9)
a.text(0,.85,fill('Combining phosphatidylinositide 3-kinase and MEK 1/2 inhibitors is effective at treating KRAS mutant tumors.',62),transform=a.transAxes,va='top',fontsize=8.3)
for y,title,color,ans in [(.53,'Original context (A)',GREEN,'SUPPORTS'),(.27,'Exchanged uncredited passages (B)',ORANGE,'REFUTES')]:
 a.text(.01,y+.085,title,transform=a.transAxes,color=color,weight='bold',fontsize=8.4)
 for j in range(10):
  a.scatter(.035+j*.06,y,s=95,marker='s',color=GREEN if j==0 else color,transform=a.transAxes,zorder=3)
  a.text(.035+j*.06,y,'R' if j==0 else 'U',transform=a.transAxes,color='white',ha='center',va='center',fontsize=6.5)
 a.text(.66,y,ans,transform=a.transAxes,va='center',weight='bold',color=color,fontsize=9.2)
a.text(.01,.06,'Same relevance grades at each rank; nine uncredited passages differ.\nVerdict strings: original primary 800-case records, not a clinical claim.',transform=a.transAxes,fontsize=7.7,color=DARK)

b=fig.add_subplot(g[0,1]);panel(b,'b','Primary exchange versus execution floor')
vals=[17.2666667,1.23333333];ci=[[14.6,20.0333333],[.4666667,2.1333333]]
y=np.arange(2)[::-1];b.barh(y,vals,color=[BLUE,GREY],height=.43)
for i,(v,(lo,hi)) in enumerate(zip(vals,ci)):
 xerr_fmt(b,v,lo,hi,y[i],fmt='none',color=DARK);b.text(max(v+.6,hi+.65),y[i],f'{v:.2f}%',va='center',fontsize=8.8)
b.set_yticks(y,['Exchanged context','Same-context rerun']);b.set_xlim(0,26);b.set_xlabel('Changed correctness (%)');style(b,'x')
b.text(.03,-.22,'Paired excess: 16.03 pp (95% CI 13.27–18.87)',transform=b.transAxes,fontsize=8.2)

c=fig.add_subplot(g[1,0]);panel(c,'c','Credited-evidence and family sensitivity')
names=['All 800','Credited present\n(n=591)','Mistral 7B\n(transfer)','OLMo-2 7B\n(transfer)']
vals=[17.2666667,13.4496393,13.6333333,13.6333333]
lo=[14.6,10.6752,11.2333333,11.1666667];hi=[20.0333,16.33794,16.1333333,16.2]
xx=np.arange(4);c.bar(xx,vals,color=[BLUE,GREEN,ORANGE,ORANGE],width=.56,alpha=.9)
for i,v in enumerate(vals):c.errorbar(i,v,yerr=[[v-lo[i]],[hi[i]-v]],fmt='none',color=DARK,capsize=3)
c.set_ylim(0,30);c.set_ylabel('Changed correctness (%)');c.set_xticks(xx,names,fontsize=8);style(c)

d=fig.add_subplot(g[1,1]);panel(d,'d','Model scale: exchange and same-context rerun')
order=['qwen3-0.6b','qwen3-1.7b','qwen3-4b','qwen3-8b','qwen3-14b','qwen3-32b']
params=np.array([scale_reg[k]['params_b'] for k in order]);ii=np.array([100*scale_reg[k]['macro_intervention'] for k in order]);ff=np.array([100*scale_reg[k]['macro_floor'] for k in order]);bnd=np.array([np.array(scale_reg[k]['macro_intervention_ci95'])*100 for k in order]);
d.errorbar(params,ii,yerr=[ii-bnd[:,0],bnd[:,1]-ii],fmt='o-',color=BLUE,label='Exchange',capsize=3)
d.plot(params,ff,'s-',color=GREY,label='Batch floor',ms=5);d.set_xscale('log');d.set_xticks(params,[f'{z:g}' for z in params]);d.minorticks_off();d.set_xlabel('Model parameters (billions)');d.set_ylabel('Changed correctness (%)');d.legend(frameon=False,fontsize=8,loc='upper left');style(d)

e=fig.add_subplot(g[2,:]);panel(e,'e','Registered scale: exchange minus measured execution floor')
exc=np.array([scale_reg[k]['macro_excess']*100 for k in order]);eci=np.array([np.array(scale_reg[k]['macro_excess_ci95'])*100 for k in order]);e.errorbar(params,exc,yerr=[exc-eci[:,0],eci[:,1]-exc],fmt='o-',color=BLUE,capsize=3,lw=1.7,markersize=6)
e.axhline(2,color=ORANGE,lw=1.3,ls='--',label='Preregistered lower-bound criterion: >2 pp')
e.set_xscale('log');e.set_xticks(params,[f'{z:g}B' for z in params]);e.minorticks_off();e.set_xlim(.48,45);e.set_ylim(0,22);e.set_xlabel('Qwen3 model size');e.set_ylabel('Excess changed correctness (percentage points)');style(e);e.legend(frameon=False,loc='upper left',fontsize=9)
save(fig,'Figure_2')
