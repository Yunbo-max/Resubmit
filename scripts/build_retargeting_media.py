#!/usr/bin/env python3
"""Rebuild schematic ICML-to-NeurIPS README images; NOT official TeX output.

Uses identical HTML paper content in both layouts. No model calls, fake research
results, remote assets, project-page links, or manuscript uploads.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER_BODY = '''<section><h3>Abstract</h3><p>Changing the submission venue changes the layout, not the evidence. This synthetic document illustrates how the same content can flow from two columns into one.</p></section>
<section><h3>1 &nbsp; Introduction</h3><p>A new template changes the space available to text, tables and figures. Retargeting must preserve their meaning while adapting their arrangement.</p></section>
<section><h3>2 &nbsp; Preserve the evidence</h3><p>The table lists revision responsibilities, not experimental measurements. Both versions use the same entries.</p>
<table><caption>Table 1. Revision checklist (illustrative).</caption><thead><tr><th>Object</th><th>Preserve</th><th>Adapt</th></tr></thead><tbody><tr><td>Text</td><td>Claims</td><td>Flow</td></tr><tr><td>Table</td><td>Values</td><td>Width</td></tr><tr><td>Figure</td><td>Meaning</td><td>Layout</td></tr></tbody></table></section>
<section><h3>3 &nbsp; Reflow the layout</h3><p>The available width changes the table footprint and the figure arrangement. Avoid shrinking everything to fit. Inspect each object at its final printed size.</p>
<figure><div class="mini-flow"><span>Source</span><i>→</i><span>Layout</span><i>→</i><span>Check</span></div><figcaption>Figure 1. Revision flow; not measured data.</figcaption></figure></section>'''

CSS = '''*{box-sizing:border-box}body{margin:0;background:#f5f6ef;color:#143d32;font-family:Arial,sans-serif}main{width:1200px;height:850px;position:relative;overflow:hidden;border:1px solid #d8dfd1;border-top:6px solid #174d3b;border-radius:16px;background:radial-gradient(ellipse at 100% 0%,#e2eadb 0%,#f8f8f2 64%)}.left{position:absolute;left:48px;top:58px;width:424px}.badge{display:inline-block;padding:11px 20px;background:#e4ecdc;border-radius:24px;font-size:14px;letter-spacing:3px;font-weight:700}.eyebrow{font-size:12px;letter-spacing:2px;color:#64786b;margin:35px 0 14px}h1{font-family:Georgia,'Liberation Serif',serif;font-size:61px;font-weight:400;line-height:1.01;margin:0 0 10px;letter-spacing:-2px}.subtitle{font-family:Georgia,'Liberation Serif',serif;font-size:34px;line-height:1.1;margin:0 0 26px;letter-spacing:-.8px}.intro{font-family:Georgia,'Liberation Serif',serif;color:#5a7067;font-size:25px;line-height:1.28;margin:0 0 30px}.items{display:grid;gap:22px}.item{display:flex;align-items:start;gap:15px}.icon{border:1px solid #d2ddcb;border-radius:50%;background:#e7eedf;width:29px;height:29px;display:grid;place-items:center;flex-shrink:0;font-size:15px}.item strong{display:block;font-family:Georgia,'Liberation Serif',serif;font-size:20px;font-weight:400;line-height:1.2;margin-bottom:6px}.item p{margin:0;font-size:14px;color:#687d72;line-height:1.5}.closing{margin-top:36px;border-top:1px solid #cbd7c6;padding-top:20px;font-family:Georgia,'Liberation Serif',serif;font-style:italic;font-size:23px;line-height:1.28;color:#5a7067}.paper{position:absolute;right:40px;top:39px;width:630px;height:733px;padding:29px 32px 26px;background:white;border:1px solid #d6dfd0;border-radius:9px;box-shadow:0 16px 34px #153e3020;color:#19251f}.paper::before{content:'';position:absolute;inset:-12px 7px 12px -7px;border:1px solid #d5dfcc;border-radius:10px;background:#e5ecdf;z-index:-1;transform:rotate(1.5deg)}.paper-label{font-size:10px;letter-spacing:1.5px;display:flex;justify-content:space-between;border-bottom:1px solid #335e4b;padding-bottom:10px;color:#607366}.paper h2{font-family:Georgia,'Liberation Serif',serif;font-size:24px;line-height:1.18;text-align:center;color:#19251f;margin:24px 0 8px}.paper-note{text-align:center;font-size:10px;color:#728173;margin:0 0 24px}.paper-body{font-family:Georgia,'Liberation Serif',serif;font-size:13px;line-height:1.38;column-gap:25px;column-fill:balance}.paper-body section{break-inside:auto}.paper-body h3{font-size:15px;line-height:1.2;break-after:avoid;margin:15px 0 7px}.paper-body section:first-child h3{margin-top:0}.paper-body p{margin:0 0 8px;text-align:justify}.paper table{width:100%;border-collapse:collapse;margin:12px 0 15px;font-size:11px;break-inside:avoid}.paper caption{text-align:left;font-style:italic;font-size:11px;padding-bottom:6px}.paper th{text-align:left;padding:5px 4px;border-top:1px solid #445b4e;border-bottom:1px solid #8b9c8e}.paper td{padding:5px 4px}.paper tr:last-child td{border-bottom:1px solid #445b4e}.paper figure{margin:12px 0 15px;break-inside:avoid}.mini-flow{display:flex;align-items:center;justify-content:space-between;gap:5px;padding:18px 10px;background:#eff3e9;border:1px solid #dae2d2;border-radius:5px;font-family:Arial,sans-serif;font-size:10px}.mini-flow span{border:1px solid #c6d6c0;padding:8px 6px;border-radius:3px;background:#fff}.mini-flow i{font-style:normal;color:#326951}.paper figcaption{font-size:10px;font-style:italic;text-align:center;padding-top:6px}.paper-footer{position:absolute;bottom:18px;left:32px;right:32px;padding-top:10px;border-top:1px solid #dce3d6;display:flex;justify-content:space-between;font-size:9px;letter-spacing:1px;color:#708071}.footer{position:absolute;bottom:0;left:0;width:100%;height:52px;display:flex;align-items:center;justify-content:center;gap:16px;border-top:1px solid #d7dfcf;background:#f4f6ee;font-size:13px;color:#5b7265}.footer strong{font-weight:400;color:#174d3b}.after .paper-body{font-size:13px;line-height:1.36}.after .paper h2{margin-top:21px}.after .paper-note{margin-bottom:18px}.after .paper-body h3{margin:12px 0 6px}.after .paper-body section:first-child h3{margin-top:0}.after .paper table{margin:9px 0 11px}.after .paper figure{margin:9px 0 10px}.after .mini-flow{padding:12px 45px}.after .mini-flow span{min-width:95px;text-align:center}.after .paper-body p{margin-bottom:7px}'''


def html_source(state: str) -> str:
    if state not in ('before', 'after'):
        raise ValueError('state must be before or after')
    before = state == 'before'
    venue = 'ICML-style' if before else 'NeurIPS-style'
    layout = 'Two-column source' if before else 'One-column target'
    columns = 2 if before else 1
    items = ([('Two-column reading flow', 'Text and objects occupy narrower columns.'),
              ('Compact table footprint', 'Labels and values fit the original column.'),
              ('Original venue arrangement', 'Retarget the layout, not the research claim.')]
             if before else [('One continuous reading flow', 'Shared content reflows into the new width.'),
                              ('A wider native table', 'The same entries; a different footprint.'),
                              ('Figure layout adapted', 'Keep the meaning; inspect the new arrangement.')])
    checks = ''.join('<div class="item"><span class="icon">'+('↗' if before else '✓')+'</span><div><strong>'+title+'</strong><p>'+body+'</p></div></div>' for title,body in items)
    intro = 'The original venue layout.<br>Ready for a different destination.' if before else 'The same content.<br>Reflowed for a new venue.'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{CSS}.paper-body{{column-count:{columns}}}</style></head><body class="{state}"><main>
<div class="left"><span class="badge">● &nbsp; {state.upper()}</span><p class="eyebrow">RESUBMIT / TEMPLATE RETARGETING</p><h1>{venue}</h1><p class="subtitle">{layout}</p><p class="intro">{intro}</p><div class="items">{checks}</div><p class="closing">Keep the content.<br>Change the layout.</p></div>
<article class="paper"><div class="paper-label"><span>{venue.upper()} / LAYOUT SCHEMATIC</span><span>{columns} COLUMN{'S' if before else ''}</span></div><h2>Retargeting a Paper<br>Without Changing Its Evidence</h2><p class="paper-note">Synthetic document · shared text, table entries and figure labels</p><div class="paper-body">{PAPER_BODY}</div><div class="paper-footer"><span>CONTENT PRESERVED / LAYOUT CHANGED</span><span>01</span></div></article>
<div class="footer"><strong>Schematic illustration</strong><span>·</span><span>not an official template or a compiled paper</span><span>·</span><span>No research results</span></div></main></body></html>'''


def build(output: Path, browser: str | None = None) -> dict:
    from PIL import Image
    from playwright.sync_api import sync_playwright
    output.mkdir(parents=True, exist_ok=True)
    names = {'before': 'before-icml-two-column.png', 'after': 'after-neurips-one-column.png'}
    shared_text = []
    with sync_playwright() as p:
        options = {'headless': True, 'args': ['--no-sandbox']}
        if browser:
            options['executable_path'] = browser
        runner = p.chromium.launch(**options)
        try:
            page = runner.new_page(viewport={'width':1200, 'height':850}, device_scale_factor=1)
            page.route('**/*', lambda route: route.abort())
            for state,name in names.items():
                page.set_content(html_source(state), wait_until='load')
                page.evaluate('document.fonts.ready')
                shared_text.append(page.locator('.paper-body').inner_text())
                boxes = page.evaluate('''() => {const b=document.querySelector('.paper-body').getBoundingClientRect(); const f=document.querySelector('.paper-footer').getBoundingClientRect(); return {bodyBottom:b.bottom, footerTop:f.top, scroll:document.documentElement.scrollWidth};}''')
                if boxes['bodyBottom'] > boxes['footerTop'] - 6 or boxes['scroll'] > 1200:
                    raise ValueError(f'{state}: illustration overflow: {boxes}')
                page.locator('main').screenshot(path=str(output/name))
        finally:
            runner.close()
    if shared_text[0] != shared_text[1]:
        raise ValueError('The paper text differs between the two illustrations')
    images = [Image.open(output/n).convert('RGB') for n in names.values()]
    frames = [im.quantize(colors=128) for im in images]
    gif = output/'icml-to-neurips.gif'
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=[3500,3500], loop=0, disposal=2, optimize=False)
    with Image.open(gif) as animation:
        if animation.n_frames != 2:
            raise ValueError('Expected exactly two GIF frames')
        for i in range(2):
            animation.seek(i)
            if animation.info.get('duration') != 3500:
                raise ValueError('Unexpected GIF hold duration')
    manifest = {'kind':'source-rendered-layout-illustration', 'not_actual_compilation':True,
                'not_scientific_evidence':True, 'canvas':[1200,850], 'same_paper_text':True,
                'checks':['two-column-before','one-column-after','identical-paper-text','no-overflow','two-GIF-frames-3500ms'],
                'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'paper_body_sha256':hashlib.sha256(PAPER_BODY.encode()).hexdigest(), 'assets':{}}
    for name in list(names.values()) + [gif.name]:
        data=(output/name).read_bytes()
        manifest['assets'][name]={'sha256':hashlib.sha256(data).hexdigest(), 'bytes':len(data)}
    (output/'retargeting-illustration-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT/'docs/assets')
    parser.add_argument('--browser', help='Optional Chromium executable path')
    args=parser.parse_args()
    print(json.dumps(build(args.out,args.browser),indent=2))

if __name__ == '__main__': main()
