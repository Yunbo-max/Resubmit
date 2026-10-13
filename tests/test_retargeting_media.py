"""Presentation checks, not a scientific or agent-performance benchmark."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load():
    spec = importlib.util.spec_from_file_location('retargeting_media', ROOT/'scripts/build_retargeting_media.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class RetargetingMediaTests(unittest.TestCase):
    def test_before_uses_two_columns(self):
        html = load().html_source('before')
        self.assertIn('ICML-style', html)
        self.assertIn('column-count:2', html)
        self.assertIn('Two-column source', html)
    def test_after_uses_one_column(self):
        html = load().html_source('after')
        self.assertIn('NeurIPS-style', html)
        self.assertIn('column-count:1', html)
        self.assertIn('One-column target', html)
    def test_same_paper_content(self):
        m = load()
        a, b = m.html_source('before'), m.html_source('after')
        self.assertIn(m.PAPER_BODY, a)
        self.assertIn(m.PAPER_BODY, b)
    def test_not_misrepresented_as_official_output(self):
        for state in ('before','after'):
            h = load().html_source(state)
            self.assertIn('Schematic illustration', h)
            self.assertIn('not an official template', h)
            self.assertNotIn('CIFAR', h)
            self.assertNotIn('2025', h)
    def test_no_links_scripts_or_upload(self):
        for state in ('before','after'):
            h = load().html_source(state)
            for token in ('<script','http://','https://','type="file"','Project page'):
                self.assertNotIn(token, h)
    def test_invalid_mode_rejected(self):
        with self.assertRaises(ValueError): load().html_source('other')

if __name__ == '__main__': unittest.main()
