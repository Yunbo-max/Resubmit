#!/usr/bin/env python3
"""Build README media from an HTML cover and actual, explicitly synthetic LaTeX renders.

Run scripts/build_demo.py first in a complete checkout. This builder never calls a
model, downloads assets, modifies paper evidence, or publishes to GitHub.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build(browser_path=None):
    from PIL import Image
    from playwright.sync_api import sync_playwright
    site = ROOT / 'site'
    out = ROOT / 'docs/assets'
    source = site / 'assets/demo.json'
    if not source.is_file() or json.loads(source.read_text()).get('synthetic') is not True:
        raise ValueError('Run scripts/build_demo.py first; synthetic demo.json is required.')
    for mode in ('before', 'after'):
        if not (site / f'assets/demo-{mode}.webp').is_file():
            raise ValueError(f'Missing real demo-{mode}.webp render')
    out.mkdir(parents=True, exist_ok=True)
    checks = []
    errors = []
    blocked = []
    # Render a faithful in-memory copy of local public assets. No network or
    # loopback access is needed, including in restricted document sandboxes.
    html = (site / 'press.html').read_text()
    html = html.replace('<link rel="stylesheet" href="press.css">', '<style>' + (site / 'press.css').read_text() + '</style>')
    html = html.replace('<script src="press.js" defer></script>', '')
    for name, mime in [('demo-before.webp', 'image/webp'), ('demo-after.webp', 'image/webp'), ('favicon.svg', 'image/svg+xml')]:
        data = base64.b64encode((site / 'assets' / name).read_bytes()).decode('ascii')
        html = html.replace('assets/' + name, 'data:' + mime + ';base64,' + data)
    with sync_playwright() as p:
        opts = {'headless': True, 'args': ['--no-sandbox', '--disable-dev-shm-usage']}
        if browser_path:
            opts['executable_path'] = browser_path
        browser = p.chromium.launch(**opts)
        context = browser.new_context(viewport={'width': 1280, 'height': 1000}, device_scale_factor=1)
        def no_network(route):
            blocked.append(route.request.url)
            route.abort()
        context.route('**/*', no_network)
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.set_content(html, wait_until='load')
        page.add_script_tag(content=(site / 'press.js').read_text())
        page.evaluate('document.fonts.ready')
        page.wait_for_function('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Desktop overflow'
        page.locator('#cover').screenshot(path=str(out / 'readme-cover.png'), animations='disabled')
        frames = []
        for mode in ('before', 'after'):
            page.locator(f'#revision button[data-mode="{mode}"]').click()
            page.wait_for_function('(m) => document.querySelector("#revision-image").src === document.querySelector("#revision-image").dataset[m + "Src"] && document.querySelector("#revision-image").complete', arg=mode)
            page.locator('#revision').screenshot(path=str(out / f'latex-revision-{mode}.png'), animations='disabled')
            frames.append(Image.open(out / f'latex-revision-{mode}.png').convert('RGB'))
            assert page.locator(f'#revision button[data-mode="{mode}"]').get_attribute('aria-pressed') == 'true'
        assert frames[0].size == frames[1].size, 'Comparison panels must have equal geometry'
        assert frames[0].tobytes() != frames[1].tobytes(), 'Animation must show a real change'
        # Long-held frames: no flashing or invented intermediate PDF content.
        quantized = [frame.quantize(colors=128, method=Image.Quantize.MEDIANCUT) for frame in frames]
        quantized[0].save(out / 'latex-revision.gif', save_all=True, append_images=quantized[1:],
            duration=[2800, 2800], loop=0, disposal=2, optimize=True)
        shutil.copy2(out / 'latex-revision-after.png', out / 'latex-revision-still.png')
        with Image.open(out / 'latex-revision.gif') as gif:
            assert gif.is_animated and gif.n_frames == 2
        page.evaluate('window.scrollTo(0, 0)')
        page.screenshot(path=str(out / 'project-desktop.png'), full_page=True, animations='disabled')
        page.locator('#play-demo').click()
        assert page.locator('#play-demo').get_attribute('aria-pressed') == 'true'
        page.locator('#play-demo').click()
        assert page.locator('#play-demo').get_attribute('aria-pressed') == 'false'
        checks.extend(['desktop-no-horizontal-overflow', 'before-after-buttons', 'explicit-play-pause'])
        page.emulate_media(reduced_motion='reduce')
        page.locator('#play-demo').click()
        assert page.locator('#play-demo').get_attribute('aria-pressed') == 'false'
        assert page.evaluate('getComputedStyle(document.documentElement).scrollBehavior') == 'auto'
        checks.append('reduced-motion-no-autoplay')
        page.set_viewport_size({'width': 390, 'height': 844})
        page.evaluate('window.scrollTo(0, 0)')
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Mobile overflow'
        page.screenshot(path=str(out / 'project-mobile.png'), full_page=True, animations='disabled')
        checks.append('mobile-390px-no-horizontal-overflow')
        browser.close()
    if errors or blocked:
        raise ValueError(f'Browser errors or external asset requests: {errors!r}, {blocked!r}')
    names = ['readme-cover.png', 'latex-revision-before.png', 'latex-revision-after.png',
             'latex-revision-still.png', 'latex-revision.gif', 'project-desktop.png', 'project-mobile.png']
    for name in names:
        assert (out / name).stat().st_size < 1500000, f'Media budget exceeded: {name}'
    report = {
        'kind': 'readme-presentation-checks', 'synthetic': True,
        'browser_input': 'In-memory local HTML/CSS/JS and compiled previews; not a public HTTP endpoint test',
        'note': 'Browser checks and controlled LaTeX renders, not scientific or agent-performance validation.',
        'checks': checks, 'browser_errors': errors, 'external_asset_requests': blocked,
        'inputs': {str(path.relative_to(ROOT)): digest(path) for path in [source, site/'press.html', site/'press.css', site/'press.js', Path(__file__)]},
        'assets': {name: {'sha256': digest(out/name), 'bytes': (out/name).stat().st_size} for name in names},
        'demo': json.loads(source.read_text())
    }
    (out/'media-manifest.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser', help='Optional installed Chromium executable; defaults to Playwright Chromium')
    args = parser.parse_args()
    try:
        build(args.browser)
    except (OSError, ValueError, AssertionError) as exc:
        parser.exit(2, f'{exc}\n')

if __name__ == '__main__':
    main()
