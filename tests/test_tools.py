"""Deterministic helper tests. Fixture values are synthetic, not research results."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/resubmitting-papers/scripts'

def load(name):
    path = SCRIPTS / (name + '.py')
    assert path.is_file(), f'Missing implementation: {path.name}'
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def table():
    return {'id': 'tab:fixture', 'caption': 'SYNTHETIC SOFTWARE FIXTURE.',
            'columns': [{'id': 'score', 'label': 'Score', 'direction': 'max', 'precision': 2}],
            'rows': [
              {'label': 'Base_A', 'group': 'protocol-A', 'cells': {'score': {'value': 1.25, 'source': 'fixture:row1', 'status': 'measured'}}},
              {'label': 'New', 'group': 'protocol-A', 'cells': {'score': {'value': 2.25, 'source': 'fixture:row2', 'status': 'measured'}}}]}

class GraphTests(unittest.TestCase):
    def test_topological_order(self):
        m = load('workflow')
        self.assertEqual(m.order({'a': [], 'b': ['a']}), ['a', 'b'])
    def test_cycle_rejected(self):
        with self.assertRaises(ValueError): load('workflow').order({'a':['b'], 'b':['a']})
    def test_missing_dependency(self):
        with self.assertRaises(ValueError): load('workflow').order({'a':['missing']})
    def test_selective_invalidation(self):
        m = load('workflow'); graph = {'venue':[], 'results':[], 'tables':['results','venue'], 'pdf':['tables'], 'qa':['pdf']}
        self.assertEqual(m.affected(graph, ['results']), ['results', 'tables', 'pdf', 'qa'])
    def test_unknown_change(self):
        with self.assertRaises(ValueError): load('workflow').affected({'a':[]}, ['bad'])
    def test_bundled_dag_is_acyclic(self):
        g = json.loads((SCRIPTS.parent/'assets/workflow.json').read_text())
        self.assertEqual(set(load('workflow').order(g)), set(g))

class TableTests(unittest.TestCase):
    def test_native_table_and_winner(self):
        text = load('tables').render(table(), span='column', columns=2)
        self.assertIn('\\begin{table}[t]', text)
        self.assertIn('\\textbf{2.25}', text)
        self.assertNotIn('resizebox', text)
        self.assertIn('Base\\_A', text)
    def test_full_width_double_column(self):
        self.assertIn('\\begin{table*}', load('tables').render(table(), span='full', columns=2))
    def test_full_width_single_column(self):
        self.assertNotIn('table*', load('tables').render(table(), span='full', columns=1))
    def test_rank_recomputed_after_rebuttal_update(self):
        t = table(); t['rows'][0]['cells']['score']['value'] = 3.25
        s = load('tables').render(t)
        self.assertIn('\\textbf{3.25}', s); self.assertNotIn('\\textbf{2.25}', s)
    def test_missing_not_zero_or_ranked(self):
        t = table(); t['rows'][1]['cells']['score'] = {'value':None, 'status':'missing', 'reason':'not run'}
        s = load('tables').render(t)
        self.assertIn('---', s); self.assertNotIn('0.00', s)
    def test_missing_value_needs_status(self):
        t=table(); t['rows'][0]['cells']['score']['value']=None
        with self.assertRaises(ValueError): load('tables').render(t)
    def test_provenance_required(self):
        t=table(); del t['rows'][0]['cells']['score']['source']
        with self.assertRaises(ValueError): load('tables').render(t)
    def test_nonfinite_rejected(self):
        for bad in [float('nan'), float('inf'), True]:
            t=table(); t['rows'][0]['cells']['score']['value']=bad
            with self.assertRaises(ValueError): load('tables').render(t)
    def test_protocols_rank_separately(self):
        t=table(); t['rows'][1]['group']='protocol-B'
        s=load('tables').render(t)
        self.assertIn('protocol-A', s); self.assertIn('protocol-B', s)
        self.assertIn('\\textbf{1.25}', s); self.assertIn('\\textbf{2.25}', s)
    def test_derived_requires_formula(self):
        t=table(); t['rows'][0]['cells']['score']['status']='derived'
        with self.assertRaises(ValueError): load('tables').render(t)
    def test_duplicate_columns_rejected(self):
        t=table(); t['columns']*=2
        with self.assertRaises(ValueError): load('tables').render(t)
    def test_min_direction(self):
        t=table(); t['columns'][0]['direction']='min'
        self.assertIn('\\textbf{1.25}', load('tables').render(t))
    def test_uncertainty_requires_type(self):
        t=table(); t['rows'][0]['cells']['score']['uncertainty']=0.1
        with self.assertRaises(ValueError): load('tables').render(t)

class QATests(unittest.TestCase):
    def test_missing_main_boundary_is_unknown(self):
        r=load('qa').page_budget(12, {'main_limit':8})
        self.assertEqual(r['status'], 'unknown')
    def test_main_pages_not_total_pages(self):
        r=load('qa').page_budget(12, {'main_limit':8,'main_start':1,'main_end':8})
        self.assertEqual(r['status'],'pass'); self.assertEqual(r['main_pages'],8)
    def test_overflow_fails(self):
        self.assertEqual(load('qa').page_budget(12, {'main_limit':8,'main_start':1,'main_end':9})['status'],'fail')
    def test_bad_page_range(self):
        with self.assertRaises(ValueError): load('qa').page_budget(4, {'main_limit':8,'main_start':1,'main_end':9})
    def test_stale_visual_receipt_fails(self):
        r={'pdf_sha256':'old','reviewed_pages':[1,2], 'findings':[], 'reviewer':'test'}
        self.assertFalse(load('qa').visual_ok(r, 'new',2))
    def test_all_pages_required(self):
        r={'pdf_sha256':'new','reviewed_pages':[1], 'findings':[], 'reviewer':'test'}
        self.assertFalse(load('qa').visual_ok(r, 'new',2))
    def test_visual_receipt_can_pass(self):
        r={'pdf_sha256':'new','reviewed_pages':[1,2], 'findings':[], 'reviewer':'test'}
        self.assertTrue(load('qa').visual_ok(r, 'new',2))
    def test_critical_findings_block(self):
        r={'pdf_sha256':'new','reviewed_pages':[1,2], 'findings':['clipped axis'], 'reviewer':'test'}
        self.assertFalse(load('qa').visual_ok(r, 'new',2))
    def test_failed_build_detected(self):
        self.assertTrue(load('qa').log_findings('! LaTeX Error: missing.\nOverfull \\hbox (4.0pt too wide)'))

class PackageTests(unittest.TestCase):
    def test_allowlist_archive(self):
        m=load('package');
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'main.tex').write_text('test'); (root/'reviews.md').write_text('private')
            out=root/'out.zip'; m.pack(root,['main.tex'],out)
            import zipfile
            with zipfile.ZipFile(out) as z: self.assertEqual(z.namelist(), ['main.tex'])
    def test_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): load('package').pack(Path(d), ['../secret'],Path(d)/'a.zip')
    def test_internal_paths_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'reviews.md').write_text('private')
            with self.assertRaises(ValueError): load('package').pack(p,['reviews.md'],p/'a.zip')
    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as other:
            p=Path(d); q=Path(other)/'data'; q.write_text('secret'); (p/'main.tex').symlink_to(q)
            with self.assertRaises(ValueError): load('package').pack(p,['main.tex'],p/'a.zip')

if __name__ == '__main__': unittest.main()

class BoundaryTests(unittest.TestCase):
    def test_none_visual_page_list_rejected(self):
        r={'pdf_sha256':'new','reviewed_pages':None,'findings':[],'reviewer':'test'}
        self.assertFalse(load('qa').visual_ok(r,'new',1))
    def test_bool_is_not_a_reviewed_page(self):
        r={'pdf_sha256':'new','reviewed_pages':[True],'findings':[],'reviewer':'test'}
        self.assertFalse(load('qa').visual_ok(r,'new',1))
    def test_cell_without_value_rejected(self):
        t=table(); t['rows'][0]['cells']['score']={'status':'missing','reason':'not run'}
        with self.assertRaises(ValueError): load('tables').render(t)
    def test_nonstr_source_rejected(self):
        t=table(); t['rows'][0]['cells']['score']['source']=['not a locator']
        with self.assertRaises(ValueError): load('tables').render(t)
    def test_font_file_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'font.ttf').write_bytes(b'dummy')
            with self.assertRaises(ValueError): load('package').pack(p,['font.ttf'],p/'a.zip')
