#!/usr/bin/env python3
"""Compare actual PDF page renders at identical DPI; do not judge beauty or meaning.
Requires PyMuPDF. Compares physical indices, not semantic page correspondence.
"""
import argparse
import hashlib
import json
from pathlib import Path


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()


def compare(before: Path, after: Path, dpi: int = 120,
            render_dir: Path | None = None) -> dict:
    if type(dpi) is not int or not 36 <= dpi <= 300:
        raise ValueError('DPI must be an integer between 36 and 300')
    try:
        import fitz
    except ImportError as e:
        raise ValueError('PyMuPDF is required for rendered comparison') from e
    bh, ah = sha(before), sha(after)
    if render_dir is not None:
        if render_dir.exists(): raise ValueError('Render directory must be new; never overwrite prior evidence')
        render_dir.mkdir(parents=True)
    with fitz.open(before) as a, fitz.open(after) as b:
        if not a.is_pdf or not b.is_pdf or a.needs_pass or b.needs_pass:
            raise ValueError('Use readable, unencrypted PDFs')
        pages = []
        for i in range(max(len(a), len(b))):
            keys, sizes = [], []
            for label, doc in [('before', a), ('after', b)]:
                if i >= len(doc):
                    keys.append(None); sizes.append(None); continue
                page = doc[i]
                w, h = page.rect.width, page.rect.height
                if w*h*(dpi/72)**2 > 40_000_000:
                    raise ValueError('Page exceeds 40M-pixel render budget; reduce DPI and review separately')
                pix = page.get_pixmap(dpi=dpi, colorspace=fitz.csRGB, alpha=False, annots=True)
                keys.append(hashlib.sha256(pix.samples).hexdigest())
                sizes.append([pix.width, pix.height, w, h, page.rotation])
                if render_dir is not None: pix.save(render_dir/f'{label}-{i+1:03}.png')
                del pix
            if keys[0] is None: change = 'added'
            elif keys[1] is None: change = 'removed'
            elif sizes[0] != sizes[1]: change = 'resized'
            elif keys[0] != keys[1]: change = 'changed'
            else: change = 'unchanged'
            pages.append({'page': i+1, 'change': change, 'before_render_sha256': keys[0],
                          'after_render_sha256': keys[1]})
        changed = [r['page'] for r in pages if r['change'] != 'unchanged']
        review = set()
        for n in changed:
            anchor = min(n, len(b))
            review.update(x for x in (anchor-1, anchor, anchor+1) if 1 <= x <= len(b))
        report = {'schema_version': 1, 'before_sha256': bh, 'after_sha256': ah,
                  'dpi': dpi, 'renderer': 'PyMuPDF '+fitz.VersionBind,
                  'before_pages': len(a), 'after_pages': len(b), 'pages': pages,
                  'changed_pages': changed, 'review_candidate_pages': sorted(review),
                  'certifies_visual_quality': False,
                  'limitations': 'Same-index RGB raster comparison only. Insertions may flag every later page. '
                                'Inspect all changed pages and neighbors; final approval still needs every page. '
                                'Equal pixels do not certify metadata, annotations, links, fonts or scientific meaning.'}
    if sha(before) != bh or sha(after) != ah:
        raise ValueError('PDF changed during comparison; rerun on frozen candidates')
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('before', type=Path); p.add_argument('after', type=Path)
    p.add_argument('--dpi', type=int, default=120)
    p.add_argument('--render-dir', type=Path); p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    try:
        if a.out.exists() or a.out.resolve() in (a.before.resolve(), a.after.resolve()):
            raise ValueError('Output must be a new report path, not a PDF input')
        r = compare(a.before, a.after, a.dpi, a.render_dir)
        a.out.parent.mkdir(parents=True, exist_ok=True)
        with a.out.open('x', encoding='utf-8') as f: json.dump(r, f, indent=2); f.write('\n')
        print(json.dumps({'changed_pages': r['changed_pages'], 'review_candidate_pages': r['review_candidate_pages'],
                          'certifies_visual_quality': False}))
    except (ValueError, OSError, TypeError, RuntimeError) as e:
        p.exit(2, f'{e}\n')

if __name__ == '__main__': main()
