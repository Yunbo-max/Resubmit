#!/usr/bin/env python3
"""Compile synthetic one/two-column article fixtures. NOT official venue templates.
Needs latexmk/TeX Live with booktabs, graphicx, tikz; optional PyMuPDF for PNGs.
"""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'skills/resubmitting-papers'

def main():
    if not shutil.which('latexmk'): raise SystemExit('latexmk unavailable; no build claimed')
    sys.path.insert(0,str(S/'scripts'))
    from tables import render
    from qa import log_findings
    data=json.loads((ROOT/'tests/fixtures/results.json').read_text())
    para=('This is a synthetic software layout fixture, not a research manuscript. '
          'The table checks native numerical rendering and the diagram checks vector labels at the final page width. '
          'No scientific result, conference compliance or acceptance claim follows from this example. ')
    outputs=[]
    for columns in (1,2):
        out=ROOT/'build'/f'{columns}-column'; out.mkdir(parents=True,exist_ok=True)
        shutil.copy2(S/'assets/layout-probe.tex', out/'layout-probe.tex')
        (out/'results.tex').write_text(render(data,columns=columns,span='column').replace('[t]', '[htbp]', 1))
        (out/'full.tex').write_text(render(dict(data,id='tab:full'),columns=columns,span='full').replace('[t]', '[htbp]', 1))
        # Deliberately reflow the vector topology; do not just scale the old artwork.
        if columns==1:
            diagram=r'''\node (a) at (0,0) {Input}; \node (b) at (3,0) {Transform}; \node (c) at (6,0) {Inspect};
\draw[->] (a)--(b); \draw[->] (b)--(c);'''
        else:
            diagram=r'''\node (a) at (0,0) {Input}; \node (b) at (2.1,0) {Transform}; \node (c) at (2.1,-1.1) {Inspect};
\draw[->] (a)--(b); \draw[->] (b)--(c);'''
        tex=(r'\documentclass[10pt'+(',twocolumn' if columns==2 else '')+r''']{article}
\usepackage{booktabs,graphicx,tikz,flafter}
\input{'''+ 'layout-probe.tex' +r'''}
\title{Synthetic Layout Fixture}
\author{Software test only}
\date{}
\begin{document}
\maketitle
\begin{abstract}'''+para+r'''\end{abstract}
\section{Evidence objects}
The compact native table is Table~\ref{tab:fixture}. '''+para+r'''
\input{results.tex}
Figure~\ref{fig:flow} demonstrates an editable diagram with a topology-aware layout.
\begin{figure}[htbp]
\centering
\begin{tikzpicture}[every node/.style={draw,rounded corners,minimum height=0.55cm,font=\small},>=stealth]
'''+diagram+r'''
\end{tikzpicture}
\caption{Synthetic diagram; labels and arrows remain vector objects.}
\label{fig:flow}
\end{figure}
The full-width variant is Table~\ref{tab:full}.
\input{full.tex}
\section{Verification}
'''+para*7+r'''
\section{Scope}
'''+para*3+r'''
\clearpage
\section*{References (fixture)}
No research claims or citations are represented by the fixture values.
\clearpage
\appendix
\section{Additional checks}
'''+para+r'''
\end{document}
''')
        (out/'main.tex').write_text(tex)
        run=subprocess.run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-latexoption=-no-shell-escape','main.tex'],cwd=out,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
        (out/'build-output.txt').write_text(run.stdout)
        if run.returncode: raise SystemExit(f'Build failed: {out}; see build-output.txt')
        findings=log_findings((out/'main.log').read_text(errors='replace'))
        if findings: raise SystemExit(f'Build diagnostics: {findings}')
        if importlib.util.find_spec('fitz'):
            import fitz
            with fitz.open(out/'main.pdf') as doc:
                for i,p in enumerate(doc,1): p.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(out/f'page-{i:02}.png')
                print(f'{columns}-column: {len(doc)} PDF pages; rendered all pages; no flagged build diagnostics')
        # A source ZIP must compile after extraction, without the original workspace.
        from package import pack
        import zipfile
        pack(out, ['main.tex','results.tex','full.tex','layout-probe.tex'], out/'source.zip')
        clean=out/'clean'; clean.mkdir(exist_ok=True)
        with zipfile.ZipFile(out/'source.zip') as z: z.extractall(clean)
        check=subprocess.run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-latexoption=-no-shell-escape','main.tex'],cwd=clean,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
        if check.returncode: raise SystemExit(f'Clean ZIP rebuild failed: {clean}')
        print(f'{columns}-column: allowlisted source ZIP rebuilt in a clean directory')
        outputs.append(str(out/'main.pdf'))
    print('\n'.join(outputs))
if __name__=='__main__': main()
