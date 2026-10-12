#!/usr/bin/env python3
"""Create a source ZIP from an explicit allowlist, never by archiving a workspace.
Does not check authorship, venue compliance, or scientific claims; never submits.
"""
import argparse
import json
from pathlib import Path
import re
import zipfile

def pack(root:Path, files:list[str], out:Path):
    root=root.resolve(); out=out.resolve(); checked=[]
    if not files or len(files)!=len(set(files)): raise ValueError('Nonempty, duplicate-free file allowlist required')
    for name in files:
        rel=Path(name)
        if rel.is_absolute() or '..' in rel.parts or '\\' in name: raise ValueError('Unsafe package path')
        if any(p.startswith('.') for p in rel.parts) or re.search(r'(^|[/_.-])(reviews?|rebuttal|internal|prompts?|state|audits?|receipts?|credentials?|secrets?)([/_.-]|$)',name,re.I):
            raise ValueError(f'Internal or review material excluded from source package: {name}')
        p=(root/rel).resolve()
        if not p.is_relative_to(root) or not p.is_file() or p==out: raise ValueError(f'Invalid, escaping or self-referential file: {name}')
        if p.suffix.lower() not in {'.tex','.bib','.sty','.cls','.bst','.pdf','.png','.jpg','.jpeg','.svg','.eps','.ttf','.otf'}:
            raise ValueError(f'Unsupported source-package extension: {name}')
        if p.suffix.lower() in {'.ttf','.otf'}: raise ValueError('Do not distribute font files')
        checked.append((p,rel.as_posix()))
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for p,name in checked: z.write(p,name)

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('root',type=Path); p.add_argument('--allowlist',type=Path,required=True); p.add_argument('--out',type=Path,required=True); a=p.parse_args()
    try: pack(a.root,json.loads(a.allowlist.read_text()),a.out)
    except (ValueError,OSError,TypeError) as e: p.exit(2,f'{e}\n')
if __name__=='__main__': main()
