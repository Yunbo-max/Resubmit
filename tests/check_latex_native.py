#!/usr/bin/env python3
"""Compile actual before/after article fixtures. NOT official conference validation."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
S = ROOT/'skills/resubmitting-papers'
sys.path.insert(0, str(S/'scripts'))
from revision_check import capture, check
from pdf_revision_diff import compare
from latex_format import compare_logs, parse_log
from qa import log_findings


def run(out: Path):
    if not shutil.which('latexmk'): raise RuntimeError('latexmk unavailable; no build claimed')
    if out.exists(): raise ValueError('Use a new output directory to preserve earlier evidence')
    out.mkdir(parents=True)
    para = ('This is a software fixture, not a scientific result. The body must keep '
            'its normal font size and paragraph spacing after the local note. '
            'The note has exactly the same words in both versions. ')
    notes = 'Local note for the scope test. This note may use smaller type. '
    summary = []
    for columns in (1,2):
        parent = out/f'{columns}-column'; parent.mkdir()
        main = (r'\documentclass[10pt'+(',twocolumn' if columns==2 else '')+r''']{article}
\usepackage{fixture-style}
\input{probe.tex}
\title{LaTeX Revision Fixture}
\author{Synthetic software test}
\date{}
\begin{document}
\maketitle
\section{Local edit}
'''+para+r'''
\par
\input{note.tex}
\ResubmitStyleProbe{after_note}
\section{Body retained}
'''+('\n\n'.join([para]*8))+r'''
\clearpage
\section{Following page}
'''+('\n\n'.join([para]*8))+r'''
\end{document}
''')
        for version in ('before','after'):
            project=parent/version; project.mkdir()
            (project/'main.tex').write_text(main)
            (project/'fixture-style.sty').write_text('% Test-only local style; not an official kit.\n\\ProvidesPackage{fixture-style}\n')
            shutil.copy2(S/'assets/latex-style-probe.tex',project/'probe.tex')
            local=r'\small\setlength{\parskip}{7pt} '+notes+r'\par'
            (project/'note.tex').write_text((local if version=='before' else '{'+local+'}')+'\n')
            cmd=['latexmk','-norc','-pdf','-interaction=nonstopmode','-halt-on-error','-latexoption=-no-shell-escape','main.tex']
            result=subprocess.run(cmd,cwd=project,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=90)
            (project/'build.stdout').write_text(result.stdout)
            if result.returncode: raise RuntimeError(f'{version} build failed; inspect {project}/build.stdout')
            findings=log_findings((project/'main.log').read_text(errors='replace'))
            if findings: raise RuntimeError(f'{version} log findings: {findings}')
            receipt={'command':cmd,'exit_code':result.returncode,'engine':'pdfLaTeX via latexmk',
                     'source':capture(project,['main.tex','fixture-style.sty','probe.tex','note.tex']),
                     'pdf_sha256':hashlib.sha256((project/'main.pdf').read_bytes()).hexdigest()}
            (project/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
        before,after=parent/'before',parent/'after'
        baseline=capture(before,['main.tex','fixture-style.sty','probe.tex','note.tex'])
        scope=check(after,baseline,['note.tex'],['fixture-style.sty'])
        assert scope['within_scope'] and scope['changed']==['note.tex'],scope
        # The rendered difference must be detected, not guessed from the source.
        difference=compare(before/'main.pdf',after/'main.pdf',render_dir=parent/'renders')
        assert difference['changed_pages'],difference
        drift=compare_logs((before/'main.log').read_text(),(after/'main.log').read_text())
        assert any(d['key']=='fontsize' for d in drift['differences']),drift
        fixed=parse_log((after/'main.log').read_text())['after_note']
        assert fixed['fontsize']=='10' and fixed['parskip'].startswith('0.0pt'),fixed
        (parent/'scope.json').write_text(json.dumps(scope,indent=2)+'\n')
        (parent/'pdf-diff.json').write_text(json.dumps(difference,indent=2)+'\n')
        (parent/'style-diff.json').write_text(json.dumps(drift,indent=2)+'\n')
        # A separate unrelated source change must fail the scope gate.
        original=(after/'main.tex').read_text(); (after/'main.tex').write_text(original+'% unrelated edit\n')
        assert not check(after,baseline,['note.tex'],['fixture-style.sty'])['within_scope']
        (after/'main.tex').write_text(original)
        summary.append({'columns':columns,'changed_pages':difference['changed_pages'],
                        'before_pages':difference['before_pages'],'after_pages':difference['after_pages'],
                        'within_scope':scope['within_scope'],'fixed_fontsize':fixed['fontsize']})
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--out',type=Path,required=True)
    run(p.parse_args().out)
