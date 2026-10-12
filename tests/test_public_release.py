"""Public distribution tests; never install into a real user skill directory."""
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

def installer():
    path = ROOT / 'scripts/install_skill.py'
    assert path.is_file(), 'Installer implementation is missing'
    spec = importlib.util.spec_from_file_location('install_skill', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class InstallerTests(unittest.TestCase):
    def source(self, root):
        p = root/'source'; p.mkdir(); (p/'SKILL.md').write_text('---\nname: example\n---\n')
        (p/'references').mkdir(); (p/'references/a.md').write_text('reference')
        return p
    def test_install_copies_references(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); s=self.source(p); target=p/'dest/example'
            installer().install(s,target)
            self.assertEqual((target/'references/a.md').read_text(),'reference')
    def test_existing_install_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); s=self.source(p); t=p/'dest'; t.mkdir(); (t/'mine').write_text('keep')
            with self.assertRaises(FileExistsError): installer().install(s,t)
            self.assertEqual((t/'mine').read_text(),'keep')
    def test_missing_entry_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); s=p/'source'; s.mkdir()
            with self.assertRaises(ValueError): installer().install(s,p/'dest')
    def test_symlink_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); s=self.source(p); (s/'outside').symlink_to(p)
            with self.assertRaises(ValueError): installer().install(s,p/'dest')
    def test_destination_inside_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); s=self.source(p)
            with self.assertRaises(ValueError): installer().install(s,s/'dest')
    def test_cache_not_distributed(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); s=self.source(p); (s/'__pycache__').mkdir(); (s/'__pycache__/bad.pyc').write_bytes(b'x')
            installer().install(s,p/'dest')
            self.assertFalse((p/'dest/__pycache__').exists())

class DistributionTests(unittest.TestCase):
    def test_versions_agree(self):
        self.assertEqual((ROOT/'VERSION').read_text(),(ROOT/'skills/resubmitting-papers/VERSION').read_text())
    def test_public_entry_is_english(self):
        for name in ('README.md','docs/LATEX_NATIVE.md','site/index.html'):
            self.assertNotRegex((ROOT/name).read_text(),r'[\u4e00-\u9fff]')
    def test_site_has_no_remote_scripts_or_fonts(self):
        page=(ROOT/'site/index.html').read_text(); css=(ROOT/'site/styles.css').read_text()
        self.assertNotRegex(page,r'<script[^>]+src=["\']https?://')
        self.assertNotIn('fonts.googleapis',css)
        self.assertNotIn('<input type="file"',page)
    def test_website_has_landmarks_and_accessible_demo(self):
        s=(ROOT/'site/index.html').read_text()
        for token in ('lang="en"','<main','<nav','<footer','aria-pressed','id="install"','Synthetic'):
            self.assertIn(token,s)
    def test_public_health_files_exist(self):
        for name in ('CONTRIBUTING.md','SECURITY.md','CHANGELOG.md','CITATION.cff','LICENSE','.github/workflows/ci.yml','.github/workflows/pages.yml'):
            self.assertTrue((ROOT/name).is_file(),name)
    def test_no_style_or_font_files_in_website_source(self):
        self.assertFalse([p for p in (ROOT/'site').rglob('*') if p.suffix in ('.sty','.cls','.ttf','.otf','.woff','.woff2')])
    def test_demo_sources_differ_only_in_scope(self):
        a=(ROOT/'examples/spacing-leak/before.tex').read_text()
        b=(ROOT/'examples/spacing-leak/after.tex').read_text()
        self.assertEqual(a.replace(r'\input{table}',r'{\input{table}}'),b)
    def test_demo_is_explicitly_synthetic(self):
        self.assertIn('Synthetic',(ROOT/'examples/spacing-leak/content.tex').read_text())
    def test_install_has_no_network_or_shell(self):
        s=(ROOT/'scripts/install_skill.py').read_text()
        self.assertNotIn('subprocess',s); self.assertNotIn('requests',s)
    def test_local_resource_links_resolve(self):
        from html.parser import HTMLParser
        from urllib.parse import urlsplit,unquote
        class Links(HTMLParser):
            def __init__(self): super().__init__(); self.links=[]
            def handle_starttag(self,tag,attrs):
                if tag in ('script','link','img'):
                    self.links.extend(v for k,v in attrs if k in ('src','href'))
        p=Links(); p.feed((ROOT/'site/index.html').read_text())
        generated={'assets/demo-before.webp','assets/demo-after.webp'}
        for href in p.links:
            if urlsplit(href).scheme or href.startswith('#'): continue
            if href not in generated:self.assertTrue((ROOT/'site'/unquote(href)).is_file(),href)

if __name__=='__main__': unittest.main()
