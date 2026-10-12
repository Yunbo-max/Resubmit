#!/usr/bin/env python3
"""Render every supplied cell into a native LaTeX table with provenance validation.
Requires booktabs. Never shrinks the table; resolve width structurally after compile.
"""
import argparse
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
import math
from pathlib import Path
import re

def esc(value):
    substitutions={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$',
                   '#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    return ''.join(substitutions.get(c,c) for c in str(value))

def number(v):
    if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):
        raise ValueError('Values must be finite numbers, not bool/string/NaN/Inf')
    return Decimal(str(v))

def validate(t):
    if not re.fullmatch(r'[A-Za-z0-9:_-]+',t.get('id','')): raise ValueError('Invalid table label')
    if not t.get('caption') or not t.get('columns') or not t.get('rows'): raise ValueError('Caption, columns and rows required')
    ids=[c['id'] for c in t['columns']]
    if len(set(ids))!=len(ids): raise ValueError('Duplicate column IDs')
    for c in t['columns']:
        if c.get('direction') not in ('min','max'): raise ValueError('Direction must be min/max')
        if type(c.get('precision')) is not int or not 0<=c['precision']<=8: raise ValueError('Precision must be 0..8')
        if not c.get('label'): raise ValueError('Column label required')
    labels=set()
    for r in t['rows']:
        if not r.get('label') or not r.get('group'): raise ValueError('Row label and comparable protocol group required')
        key=(r['group'],r['label'])
        if key in labels: raise ValueError('Duplicate method within protocol group')
        labels.add(key)
        if set(r.get('cells',{}))!=set(ids): raise ValueError('Every row needs every column; use explicit missingness')
        for cell in r['cells'].values():
            if 'value' not in cell: raise ValueError('Every cell needs an explicit value, including null')
            if cell.get('value') is None:
                if cell.get('status')!='missing' or not cell.get('reason'): raise ValueError('Missing cells need status and reason')
                continue
            number(cell['value'])
            if cell.get('status') not in ('measured','derived','reported') or not isinstance(cell.get('source'),str) or not cell['source'].strip():
                raise ValueError('Numeric cells need measured/derived/reported status and a source locator')
            if cell['status']=='derived' and not cell.get('formula'): raise ValueError('Derived cells need formula and input locators')
            if cell['status']=='derived' and not cell.get('inputs'): raise ValueError('Derived cells need input locators')
            if 'uncertainty' in cell:
                if number(cell['uncertainty'])<0: raise ValueError('Negative uncertainty')
                if cell.get('uncertainty_type') not in ('sd','se'): raise ValueError('Only explicit sd/se supported; intervals require a custom renderer')
                if type(cell.get('n')) is not int or cell['n']<1: raise ValueError('Uncertainty needs sample count and unit in notes')
            if 'eligible' in cell and type(cell['eligible']) is not bool: raise ValueError('eligible must be boolean')

def render(t, span='column', columns=2):
    validate(t)
    if span not in ('column','full') or columns not in (1,2): raise ValueError('Invalid layout variant')
    env='table*' if span=='full' and columns==2 else 'table'
    cs=t['columns']; groups=list(dict.fromkeys(r['group'] for r in t['rows']))
    best={}
    for g in groups:
        for c in cs:
            vals=[number(r['cells'][c['id']]['value']) for r in t['rows'] if r['group']==g
                  and r['cells'][c['id']]['value'] is not None and r['cells'][c['id']].get('eligible',True)]
            if vals: best[g,c['id']]=(max if c['direction']=='max' else min)(vals)
    lines=[r'\begin{'+env+'}[t]',r'\centering',r'\caption{'+esc(t['caption'])+'}',
           r'\label{'+t['id']+'}',r'\begin{tabular}{l'+'r'*len(cs)+'}',r'\toprule',
           'Method & '+' & '.join(esc(c['label'])+(' $\\uparrow$' if c['direction']=='max' else ' $\\downarrow$') for c in cs)+r' \\',r'\midrule']
    for gi,g in enumerate(groups):
        if len(groups)>1:
            if gi: lines.append(r'\midrule')
            lines.append(r'\multicolumn{'+str(len(cs)+1)+r'}{l}{\textit{'+esc(g)+r'}} \\')
        for r in (r for r in t['rows'] if r['group']==g):
            cells=[]
            for c in cs:
                x=r['cells'][c['id']]; v=x['value']
                if v is None: cells.append('---'); continue
                value=number(v); text=f"{value.quantize(Decimal(10)**-c['precision'],rounding=ROUND_HALF_UP):.{c['precision']}f}"
                if x.get('eligible',True) and value==best.get((g,c['id'])): text=r'\textbf{'+text+'}'
                if 'uncertainty' in x:
                    text+=r' $\pm$ '+f"{number(x['uncertainty']):.{c['precision']}f}"
                cells.append(text)
            lines.append(esc(r['label'])+' & '+' & '.join(cells)+r' \\')
    lines += [r'\bottomrule',r'\end{tabular}',r'\par\smallskip',r'\begin{minipage}{\linewidth}',
              r'\footnotesize Bold: best unrounded value within each comparable protocol group; not a significance test. Missing entries are not zero.']
    for note in t.get('notes',[]): lines.append(esc(note))
    lines += [r'\end{minipage}',r'\end{'+env+'}']
    return '\n'.join(lines)+'\n'

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('data',type=Path)
    p.add_argument('--out',type=Path,required=True); p.add_argument('--span',choices=['column','full'],default='column')
    p.add_argument('--columns',type=int,choices=[1,2],default=2); a=p.parse_args()
    try:
        raw=a.data.read_bytes(); t=json.loads(raw); text=render(t,a.span,a.columns)
        a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(text,encoding='utf-8')
        a.out.with_suffix('.provenance.json').write_text(json.dumps({'input':str(a.data),
            'input_sha256':hashlib.sha256(raw).hexdigest(),'output_sha256':hashlib.sha256(text.encode()).hexdigest(),
            'span':a.span,'columns':a.columns,'source_cells':t['rows']},indent=2)+'\n')
    except (ValueError,OSError,KeyError,TypeError) as e: p.exit(2,f'{e}\n')
if __name__=='__main__': main()
