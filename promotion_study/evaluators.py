#!/usr/bin/env python3
from __future__ import annotations
import re,unicodedata

def _norm(s):
    s=unicodedata.normalize("NFKC",s).casefold()
    s=re.sub(r"[`*_#]+","",s)
    s=re.sub(r"\s+"," ",s).strip()
    return s

def _valid_set(task,labels):
    return {"yes","no"} if task=="bool" else {x.upper() for x in labels}

def e1_anchored_final(text,task,labels,option_texts):
    valid=_valid_set(task,labels);found=None
    for line in text.splitlines():
        m=re.fullmatch(r"\s*FINAL\s*:\s*(.*?)\s*",line,re.I)
        if not m:continue
        payload=m.group(1).strip()
        if task=="bool":
            if payload.casefold() in valid:found=payload.casefold()
        else:
            mm=re.fullmatch(r"[\(\[\{]?\s*([A-Z])\s*[\)\]\}\.\!\?]?",payload,re.I)
            if mm and mm.group(1).upper() in valid:found=mm.group(1).upper()
    return found

def _symbol_mentions(text,task,labels):
    hits=[]
    if task=="bool":
        for m in re.finditer(r"(?<![A-Za-z])(yes|no)(?![A-Za-z])",text,re.I):
            hits.append((m.start(),m.group(1).casefold()))
        return hits
    labs="".join(re.escape(x.upper()) for x in labels)
    patterns=[
      rf"(?i)\b(?:answer|option|choice)\s*(?:is|:|=|-)?\s*[\(\[]?([{labs}])[\)\]]?(?![A-Za-z])",
      rf"(?im)^\s*([{labs}])\s*[\.\)\]:-]\s+",
      rf"(?im)^\s*FINAL\s*:\s*[\(\[]?([{labs}])[\)\]]?\s*$",
    ]
    for pat in patterns:
        for m in re.finditer(pat,text):
            hits.append((m.start(),m.group(1).upper()))
    return sorted(set(hits),key=lambda z:(z[0],z[1]))

def e2_first_valid(text,task,labels,option_texts):
    h=_symbol_mentions(text,task,labels);return h[0][1] if h else None

def e3_last_valid(text,task,labels,option_texts):
    h=_symbol_mentions(text,task,labels);return h[-1][1] if h else None

def e4_wrapper_tolerant(text,task,labels,option_texts):
    valid=_valid_set(task,labels);found=None
    pat=r"(?im)^\s*(?:\*\*|__|`)?\s*FINAL\s*(?:ANSWER)?\s*[:=\-]\s*(.+?)\s*(?:\*\*|__|`)?\s*$"
    for m in re.finditer(pat,text):
        p=m.group(1).strip().strip("`*_[](){}<> \t\r\n.!?")
        if task=="bool":
            mm=re.search(r"(?i)\b(yes|no)\b",p)
            if mm:found=mm.group(1).casefold()
        else:
            mm=re.search(r"(?i)(?:answer|option|choice)?\s*[\(\[]?([A-Z])[\)\]]?",p)
            if mm and mm.group(1).upper() in valid:found=mm.group(1).upper()
    return found

def e5_option_text(text,task,labels,option_texts):
    anchored=e1_anchored_final(text,task,labels,option_texts)
    if anchored is not None:return anchored
    lines=[x.strip() for x in text.splitlines() if x.strip()]
    candidates=[]
    for line in lines[::-1]:
        m=re.match(r"(?i)^\s*FINAL\s*:\s*(.+)$",line)
        if m:candidates.append(m.group(1));break
    if lines:candidates.append(lines[-1])
    if task=="bool":
        for c in candidates:
            n=_norm(c).strip(".!? ")
            if n in ("yes","no"):return n
        return None
    matches=[]
    for c in candidates:
        nc=_norm(c).strip(".!? ")
        for lab,opt in zip(labels,option_texts):
            if nc==_norm(str(opt)).strip(".!? "):matches.append(lab.upper())
    uniq=sorted(set(matches))
    return uniq[0] if len(uniq)==1 else None

EVALUATORS={"E1":e1_anchored_final,"E2":e2_first_valid,"E3":e3_last_valid,"E4":e4_wrapper_tolerant,"E5":e5_option_text}
