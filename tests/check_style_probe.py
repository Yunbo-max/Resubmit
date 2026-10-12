#!/usr/bin/env python3
"""Optional real-TeX probe smoke test; generic article, NOT a conference kit.
Six variants (reference/scoped/leaked, each in one and two columns) demonstrate
runtime parameter drift and scope restoration. Fixture text contains no science.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT/'skills/resubmitting-papers'

def main():
    if not shutil.which('pdflatex'): raise SystemExit('pdflatex unavailable; no compile validation performed')
    sys.path.insert(0, str(SKILL/'scripts'))
    from latex_format import compare_logs
    summary = {}
    para = ('This is a software test of nominal LaTeX spacing and font parameters. '
            'It is not a research result or a conference-compliance example. ')
    for cols in (1,2):
        logs = {}
        for variant in ('reference','scoped','leaked'):
            folder = ROOT/'build'/'style-probe'/f'{cols}-{variant}'
            folder.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SKILL/'assets/latex-style-probe.tex',folder/'probe.tex')
            start = r'{\small\setlength{\parskip}{5pt}' if variant=='scoped' else r'\small\setlength{\parskip}{5pt}' if variant=='leaked' else '{'
            end = '' if variant=='leaked' else '}'
            tex = ('\\documentclass[10pt'+(',twocolumn' if cols==2 else '')+']{article}\n'
                   '\\input{probe.tex}\n\\begin{document}\n'
                   '\\section*{Style probe: synthetic fixture}\n'
                   '\\ResubmitStyleProbe{body}\n'+para*2+'\n\n'
                   +start+'\n\\ResubmitStyleProbe{local-block}\n'+para*2+'\\par\n'+end+'\n'
                   '\\ResubmitStyleProbe{after-block}\n'+para*2+'\n\n'+para+'\n\\end{document}\n')
            (folder/'main.tex').write_text(tex)
            run = subprocess.run(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','main.tex'],cwd=folder,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=40)
            (folder/'build-output.txt').write_bytes(run.stdout)
            if run.returncode: raise RuntimeError(f'Failed fixture: {folder}')
            logs[variant] = (folder/'main.log').read_text(errors='replace')
        same = compare_logs(logs['reference'], logs['reference'])
        scoped = compare_logs(logs['reference'], logs['scoped'])
        leaked = compare_logs(logs['reference'], logs['leaked'])
        assert same['status']=='no-difference-detected'
        assert {d['context'] for d in scoped['differences']}=={'local-block'}
        assert {d['context'] for d in leaked['differences']}=={'local-block','after-block'}
        assert all(not r['certifies_compliance'] for r in (same,scoped,leaked))
        summary[str(cols)] = {'reference':same, 'scoped':scoped, 'leaked':leaked}
        print(f'{cols} columns: all three builds passed; scoped change restored; leaked change detected after block.')
    p=ROOT/'build/style-probe/results.json'; p.write_text(json.dumps(summary,indent=2)+'\n')
    print(p)

if __name__=='__main__': main()
