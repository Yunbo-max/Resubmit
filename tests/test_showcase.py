"""README presentation contracts; not paper-quality or recommendation benchmarks."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ShowcaseSourceTests(unittest.TestCase):
    def test_readme_has_committed_visuals(self):
        text = (ROOT / 'README.md').read_text()
        for name in ('galaxy-journey.svg', 'galaxy-journey-still.svg', 'workflow-manga-animated.svg', 'workflow-manga-still.svg', 'after-neurips-one-column.png'):
            self.assertIn(name, text)
    def test_readme_has_no_unavailable_project_page_and_has_install(self):
        text = (ROOT / 'README.md').read_text()
        self.assertNotIn('docs/PROJECT_PAGE.md', text)
        self.assertNotIn('yunbo-max.github.io', text)
        self.assertIn('scripts/install_skill.py --agent codex --skill selecting-conference-venues', text)
        self.assertIn('scripts/install_skill.py --agent codex --skill resubmitting-papers', text)
    def test_readme_static_motion_fallback(self):
        text = (ROOT / 'README.md').read_text()
        self.assertIn('prefers-reduced-motion: reduce', text)
        self.assertIn('Additional example', text)
    def test_readme_no_active_embed_or_claimed_live_service(self):
        text = (ROOT / 'README.md').read_text()
        self.assertNotIn('<iframe', text)
        self.assertNotIn('<script', text)
        self.assertIn('subjective', text.lower())
    def test_press_page_accessible(self):
        text = (ROOT / 'site/press.html').read_text()
        for token in ('lang="en"', '<main', 'id="cover"', 'id="revision"', 'Synthetic', 'aria-pressed'):
            self.assertIn(token, text)
        self.assertNotIn('2025', text)
        self.assertNotIn('Never miss', text)
    def test_motion_is_opt_in(self):
        text = (ROOT / 'site/press.js').read_text()
        self.assertIn('prefers-reduced-motion', text)
        self.assertIn('clearInterval', text)
    def test_no_remote_fonts_or_scripts(self):
        for name in ('site/press.html', 'site/press.css'):
            text = (ROOT / name).read_text()
            self.assertNotIn('fonts.googleapis', text)
            self.assertNotRegex(text, r'<script[^>]+src=[\"\']https?://')
    def test_generator_exists_and_is_not_predictor(self):
        path = ROOT / 'scripts/build_readme_media.py'
        self.assertTrue(path.is_file())
        text = path.read_text()
        self.assertNotIn('api_key', text.lower())
        self.assertIn('demo.json', text)
        self.assertIn('is_animated', text)
    def test_renderer_uses_local_content_not_network(self):
        text = (ROOT / 'scripts/build_readme_media.py').read_text()
        self.assertIn('page.set_content', text)
        self.assertNotIn('page.goto(', text)
    def test_demo_has_explicit_source_mapping(self):
        text = (ROOT / 'site/press.html').read_text()
        self.assertIn('data-before-src=', text)
        self.assertIn('data-after-src=', text)
    def test_project_page_explains_preview(self):
        text = (ROOT / 'docs/PROJECT_PAGE.md').read_text()
        self.assertIn('preview', text.lower())
        self.assertIn('assets/project-desktop.png', text)
        self.assertIn('assets/project-mobile.png', text)
    def test_css_has_responsive_and_motion_rules(self):
        text = (ROOT / 'site/press.css').read_text()
        self.assertIn('@media', text)
        self.assertIn('prefers-reduced-motion', text)
    def test_media_workflow_is_scoped(self):
        text = (ROOT / '.github/workflows/readme-media.yml').read_text()
        self.assertIn('design/readme-showcase', text)
        self.assertNotIn('pull_request_target', text)
        self.assertNotIn('git add .', text)
        self.assertIn('git add -- docs/assets/', text)
    def test_readme_has_no_unverified_deadlines(self):
        text = (ROOT / 'README.md').read_text()
        self.assertNotIn('May 2025', text)
        self.assertNotIn('100% acceptance', text)
        self.assertIn('schematic', text.lower())

if __name__ == '__main__':
    unittest.main()
