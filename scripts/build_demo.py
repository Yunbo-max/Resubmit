#!/usr/bin/env python3
"""Compile fixed synthetic sources and export actual rendered previews for the site."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,default=ROOT/'build/public-demo')
    args=p.parse_args()
    if not shutil.which('latexmk'):
        p.exit(2,'latexmk is required; no preview has been generated.\n')
    import fitz
    from PIL import Image
    assets=ROOT/'site/assets'; assets.mkdir(parents=True,exist_ok=True)
    records={}
    texts=[]
    for mode in ('before','after'):
        work=args.out/mode; work.mkdir(parents=True,exist_ok=True)
        for src in (ROOT/'examples/spacing-leak').glob('*.tex'): shutil.copy2(src,work/src.name)
        result=subprocess.run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-latexoption=-no-shell-escape',mode+'.tex'],cwd=work,capture_output=True,text=True,timeout=90)
        (work/'build.txt').write_text(result.stdout+result.stderr)
        if result.returncode: p.exit(2,f'Build failed: {work}/build.txt\n')
        pdf=work/(mode+'.pdf')
        with fitz.open(pdf) as doc:
            if len(doc)!=1: p.exit(2,'Demo must have one page; review the fixture before publishing.\n')
            page=doc[0]; text=page.get_text(); texts.append(' '.join(text.split()))
            blocks=[b for b in page.get_text('blocks') if b[4].strip()]
            clip=fitz.Rect(min(b[0] for b in blocks)-14,min(b[1] for b in blocks)-14,max(b[2] for b in blocks)+14,max(b[3] for b in blocks)+14)
            pix=page.get_pixmap(matrix=fitz.Matrix(1.65,1.65),clip=clip,alpha=False)
            Image.frombytes('RGB',(pix.width,pix.height),pix.samples).save(assets/f'demo-{mode}.webp',quality=85,method=6)
            records[mode]={'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':len(doc),'preview':f'assets/demo-{mode}.webp','cropped_preview':True,'crop_pdf_points':list(clip)}
    # Line reflow changes hyphenation; this fixture avoids comparing pixels as semantics.
    records['synthetic']=True
    records['note']='Actual LaTeX renders of a controlled scope change; not a conference-template or agent benchmark.'
    (assets/'demo.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))

if __name__=='__main__': main()
