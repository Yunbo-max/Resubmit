#!/usr/bin/env python3
"""PDF preflight. Heuristic flags are NOT scientific or aesthetic certification.
PDF physical page ranges and policy verification must be supplied explicitly.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

def page_budget(total, profile):
    limit=profile.get('main_limit'); start=profile.get('main_start'); end=profile.get('main_end')
    if any(x is None for x in (limit,start,end)):
        return {'status':'unknown','total_pages':total,'reason':'Supply verified physical main_start/main_end/main_limit'}
    if any(type(x) is not int for x in (limit,start,end)) or not (1<=start<=end<=total) or limit<1:
        raise ValueError('Invalid physical page range or limit')
    n=end-start+1
    return {'status':'pass' if n<=limit else 'fail','main_pages':n,'main_limit':limit,'total_pages':total}

def visual_ok(receipt, digest, pages):
    if not isinstance(receipt, dict): return False
    reviewed = receipt.get('reviewed_pages')
    if not isinstance(reviewed, list) or any(type(x) is not int for x in reviewed): return False
    return bool(receipt.get('pdf_sha256')==digest
        and isinstance(receipt.get('reviewer'),str) and receipt['reviewer'].strip()
        and receipt.get('findings')==[] and len(reviewed)==pages
        and set(reviewed)==set(range(1,pages+1)))

def log_findings(text):
    pats=[r'^!.*$',r'.*Overfull \\[hv]box.*$',r'.*(?:Citation|Reference).*undefined.*$',
          r'.*There were undefined references.*$',r'.*Label\(s\) may have changed.*$',
          r'.*Rerun to get.*$',r'.*multiply[- ]defined.*$',r'.*Float too large.*$',r'.*Too many unprocessed floats.*$']
    return list(dict.fromkeys(m.group(0) for p in pats for m in re.finditer(p,text,re.M|re.I)))

def inspect(pdf: Path, profile: dict, log: Path|None=None, receipt: dict|None=None):
    try: import fitz
    except ImportError as e: raise ValueError('Install PyMuPDF for PDF inspection; tests of pure helpers need no PDF library') from e
    digest=hashlib.sha256(pdf.read_bytes()).hexdigest(); doc=fitz.open(pdf)
    findings=[]; pages=[]
    minimum=profile.get('min_font_pt',7.0)
    if isinstance(minimum,bool) or not isinstance(minimum,(int,float)) or minimum<=0: raise ValueError('Invalid minimum font size')
    for idx,page in enumerate(doc,1):
        spans=[s for b in page.get_text('dict')['blocks'] if 'lines' in b for line in b['lines'] for s in line['spans'] if s['text'].strip()]
        small=[{'text':s['text'][:60],'pt':round(s['size'],2)} for s in spans if s['size']<minimum]
        outside=[s['text'][:60] for s in spans if not (page.rect+(-1,-1,1,1)).contains(fitz.Rect(s['bbox']))]
        if small: findings.append(f'Page {idx}: text below {minimum} PDF pt; review math, footnotes and figure labels separately')
        if outside: findings.append(f'Page {idx}: text outside page bounds')
        if not spans: findings.append(f'Page {idx}: no searchable text; raster/blank page needs manual review')
        pages.append({'page':idx,'width_pt':page.rect.width,'height_pt':page.rect.height,'small_text':small,'outside':outside})
    budget=page_budget(len(doc),profile)
    if budget['status']!='pass': findings.append('Page budget '+budget['status'])
    if profile.get('policy_verified') is not True or not profile.get('policy_source') or not profile.get('accessed') or any(not profile.get(k) for k in ('venue','year','track','stage')):
        findings.append('Target venue/year/track/stage policy not verified')
    if log is None: findings.append('Build log missing')
    else: findings.extend(log_findings(log.read_text(errors='replace')))
    approved=visual_ok(receipt,digest,len(doc))
    if not approved: findings.append('All-page visual review missing or stale')
    result={'pdf_sha256':digest,'budget':budget,'pages':pages,'findings':findings,
            'visual_approved':approved,'ready_for_author_review':not findings,
            'scope':'Heuristic preflight only; requires separate scientific, template-integrity and anonymity audits.'}
    doc.close(); return result

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('pdf',type=Path); p.add_argument('--profile',required=True,type=Path)
    p.add_argument('--log',type=Path); p.add_argument('--visual',type=Path); p.add_argument('--out',required=True,type=Path); a=p.parse_args()
    try:
        r=inspect(a.pdf,json.loads(a.profile.read_text()),a.log,json.loads(a.visual.read_text()) if a.visual else None)
        a.out.write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps({'findings':r['findings'],'ready_for_author_review':r['ready_for_author_review']}))
        return 0 if r['ready_for_author_review'] else 1
    except (ValueError,OSError,TypeError,KeyError) as e: p.exit(2,f'{e}\n')
if __name__=='__main__': raise SystemExit(main())
