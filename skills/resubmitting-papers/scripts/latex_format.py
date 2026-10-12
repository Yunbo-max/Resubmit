#!/usr/bin/env python3
"""Read-only LaTeX style diagnostics; flags and parameter drift are not violations.

Does not expand TeX macros, execute TeX, repair sources, or certify venue compliance.
Explicitly supply the relevant input files. A file list is not the runtime load order.
"""
import argparse
import json
from pathlib import Path
import re

STYLE_PACKAGES = set('caption subcaption subfig subfigure enumitem titlesec titling parskip setspace geometry fullpage fancyhdr times mathptmx newtxtext newtxmath fontspec unicode-math sectsty savetrees balance flushend'.split())
LENGTHS = r'(?:parskip|parindent|baselineskip|textfloatsep|floatsep|intextsep|dbltextfloatsep|dblfloatsep|abovecaptionskip|belowcaptionskip|abovedisplayskip|belowdisplayskip|abovedisplayshortskip|belowdisplayshortskip|jot|topsep|partopsep|itemsep|parsep|tabcolsep|arraycolsep|extrarowheight|textwidth|textheight|columnsep|oddsidemargin|evensidemargin|topmargin)'
STYLE_MACROS = r'(?:arraystretch|baselinestretch|section|subsection|subsubsection|paragraph|maketitle|@makecaption|thebibliography|normalsize)'
PACKAGES = re.compile(r'\\(?:usepackage|RequirePackage)\s*(?:\[([^\]]*)\]\s*)?\{([^{}]+)\}')
VERBATIM = re.compile(r'\\begin\{(verbatim\*?|Verbatim|lstlisting|minted|comment)\}')


def masked_source(text: str) -> str:
    """Mask ordinary comments and common verbatim forms without changing line offsets."""
    chars = list(text)
    def mask(a, b):
        for k in range(a, b):
            if chars[k] not in '\r\n': chars[k] = ' '
    i = 0
    while i < len(text):
        if text[i] == '%':
            j = i - 1
            while j >= 0 and text[j] == '\\': j -= 1
            if (i-j-1) % 2 == 0:
                end = text.find('\n', i)
                end = len(text) if end < 0 else end
                mask(i, end); i = end; continue
        if text[i] == '\\':
            env = VERBATIM.match(text, i)
            if env:
                end_mark = '\\end{' + env[1] + '}'
                end = text.find(end_mark, env.end())
                end = len(text) if end < 0 else end + len(end_mark)
                mask(i, end); i = end; continue
            verb = re.match(r'\\verb\*?(?![A-Za-z])', text[i:])
            if verb:
                d = i + verb.end()
                if d < len(text) and not text[d].isspace():
                    end = text.find(text[d], d+1)
                    nl = text.find('\n', d+1)
                    if end < 0 or (nl >= 0 and nl < end): end = nl if nl >= 0 else len(text)
                    else: end += 1
                    mask(i, end); i = end; continue
            # A TeX control symbol (e.g. \\ or \%) is not a new command start.
            if i+1 < len(text) and not text[i+1].isalpha():
                i += 2; continue
        i += 1
    return ''.join(chars)


def scan_text(text: str, path: str = 'main.tex') -> list[dict]:
    clean = masked_source(text)
    findings = []
    def emit(code, match, why):
        findings.append({'code': code, 'severity': 'review', 'path': path,
                         'line': clean.count('\n', 0, match.start())+1,
                         'source': text[match.start():match.end()][:160], 'reason': why})
    checks = [
        ('length-override', rf'\\(?:setlength|addtolength)\s*\{{\s*\\{LENGTHS}\s*\}}', 'Compare the assigned length and its scope with the target kit.'),
        ('length-override', rf'\\{LENGTHS}(?![A-Za-z])\s*(?:=|[-+]?\d)', 'Direct dimension/glue assignment needs scope review.'),
        ('manual-spacing', r'\\(?:vspace|hspace)\*?\s*\{|\\(?:vskip|hskip|kern|vfill|smallskip|medskip|bigskip|enlargethispage)(?![A-Za-z])|\\\\\s*\[[^\]]+\]', 'Manual spacing may be legitimate; inspect its owner and rendered neighbors.'),
        ('caption-override', r'\\(?:captionsetup|captionof|subcaptionsetup)(?![A-Za-z])', 'Check caption ownership and local versus global settings.'),
        ('heading-list-override', r'\\(?:titleformat|titlespacing|setlist|setenumerate|setitemize)(?![A-Za-z])', 'Check whether the official kit permits this heading/list override.'),
        ('style-definition', rf'\\(?:newcommand|renewcommand|providecommand)\*?\s*(?:\{{\s*\\{STYLE_MACROS}\s*\}}|\\{STYLE_MACROS}(?![A-Za-z]))|\\(?:gdef|def)\s*\\{STYLE_MACROS}(?![A-Za-z])', 'A style-owning macro is defined; do not confuse it with a scientific macro.'),
        ('font-scope', r'\\(?:tiny|scriptsize|footnotesize|small|normalsize|large|Large|LARGE|huge|Huge|fontsize|selectfont|fontfamily|rmfamily|sffamily|ttfamily|setstretch|onehalfspacing|doublespacing|linespread)(?![A-Za-z])', 'Check permitted font/leading and whether the declaration leaks past its intended scope.'),
        ('float-placement', r'\\(?:FloatBarrier|clearpage|newpage|pagebreak|nopagebreak|flushbottom|raggedbottom)(?![A-Za-z])|\\begin\{(?:figure|table)\*?\}\s*\[[!Hh]+\]', 'Placement/page-building intervention needs rendered inspection, not blanket removal.'),
        ('center-environment', r'\\begin\{center\}', 'A center environment may introduce vertical space; compare with a scoped centering declaration when appropriate.')]
    for code, pattern, why in checks:
        for match in re.finditer(pattern, clean): emit(code, match, why)
    for match in PACKAGES.finditer(clean):
        if any(p.strip() in STYLE_PACKAGES for p in match[2].split(',')):
            emit('style-package', match, 'Potential style owner, not an automatic incompatibility. Check options, load order and the exact target kit.')
    return sorted(findings, key=lambda f: (f['line'], f['code']))


def scan_files(root: Path, files: list[str]) -> dict:
    root = root.resolve()
    if not files or len(files) != len(set(files)): raise ValueError('Supply a nonempty, unique file list')
    findings, packages = [], {}
    for name in files:
        rel = Path(name)
        path = (root/rel).resolve()
        if rel.is_absolute() or '..' in rel.parts or not path.is_relative_to(root) or not path.is_file():
            raise ValueError(f'Unsafe or missing source file: {name}')
        text = path.read_text(encoding='utf-8')
        findings += scan_text(text, name)
        clean = masked_source(text)
        for match in PACKAGES.finditer(clean):
            for package in match[2].split(','):
                packages.setdefault(package.strip(), []).append({'path': name, 'line': clean.count('\n', 0, match.start())+1, 'options': match[1] or ''})
    for package, sites in packages.items():
        if len(sites) > 1:
            findings.append({'code':'repeated-package', 'severity':'review', 'package':package, 'sites':sites,
                             'reason':'Repeated declaration; macro expansion, conditionals and actual load order are not evaluated.'})
    return {'status':'review-required' if findings else 'no-flags-detected', 'certifies_compliance':False,
            'files':files, 'findings':findings,
            'limitations':'Heuristic source scan only. No TeX expansion or automatic edits; source line numbers are not PDF page numbers.'}


def parse_log(text: str) -> dict:
    contexts = {}; current = None
    for line in text.splitlines():
        if line.startswith('RSFMT-BEGIN:'):
            label = line.split(':', 1)[1].strip()
            if current is not None or not label or label in contexts: raise ValueError('Nested, duplicate or empty probe context')
            current = label; contexts[label] = {}
        elif line.startswith('RSFMT-END:'):
            label = line.split(':', 1)[1].strip()
            if current != label or not contexts.get(label): raise ValueError('Mismatched or empty probe context')
            current = None
        elif line.startswith('RSFMT-'):
            if current is None or '=' not in line: raise ValueError('Malformed probe field')
            key, value = line[6:].split('=', 1)
            if not key or not value.strip() or key in contexts[current]: raise ValueError('Empty or duplicate probe field')
            contexts[current][key] = ' '.join(value.split())
        elif current is not None and line.strip():
            raise ValueError('Unexpected/wrapped output inside probe; use short fields and a complete log')
    if current is not None: raise ValueError('Truncated probe')
    return contexts


def compare_logs(reference: str, candidate: str) -> dict:
    a, b = parse_log(reference), parse_log(candidate)
    missing, differences = [], []
    if not a or not b:
        status = 'unknown'
    else:
        for context in sorted(set(a) | set(b)):
            if context not in a or context not in b:
                missing.append({'context':context, 'missing_from':'reference' if context not in a else 'candidate'}); continue
            for key in sorted(set(a[context]) | set(b[context])):
                if key not in a[context] or key not in b[context]:
                    missing.append({'context':context, 'key':key, 'missing_from':'reference' if key not in a[context] else 'candidate'})
                elif a[context][key] != b[context][key]:
                    differences.append({'context':context, 'key':key, 'reference':a[context][key], 'candidate':b[context][key]})
        status = 'incomplete' if missing else 'review-required' if differences else 'no-difference-detected'
    return {'status':status, 'certifies_compliance':False, 'differences':differences, 'missing':missing,
            'limitations':'Compare equivalent contexts with the same engine/packages. Nominal parameters do not measure stretched page glue or establish visual/style compliance.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    scan = sub.add_parser('scan'); scan.add_argument('root', type=Path); scan.add_argument('--files', nargs='+', required=True); scan.add_argument('--out', type=Path)
    compare = sub.add_parser('compare'); compare.add_argument('--reference', type=Path, required=True); compare.add_argument('--candidate', type=Path, required=True); compare.add_argument('--out', type=Path)
    a = p.parse_args()
    try:
        result = scan_files(a.root, a.files) if a.command == 'scan' else compare_logs(a.reference.read_text(errors='replace'), a.candidate.read_text(errors='replace'))
        output = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
        if a.out:
            inputs = [(a.root/f).resolve() for f in a.files] if a.command == 'scan' else [a.reference.resolve(), a.candidate.resolve()]
            if a.out.resolve() in inputs: raise ValueError('Report must not overwrite an input')
            a.out.parent.mkdir(parents=True, exist_ok=True); a.out.write_text(output, encoding='utf-8')
        print(output, end='')
        return 0 if result['status'] in ('no-flags-detected','no-difference-detected') else 1
    except (ValueError, OSError, TypeError) as e: p.exit(2, f'{e}\n')

if __name__ == '__main__': raise SystemExit(main())
