"""Regression tests for native LaTeX editing; no scientific/venue claims."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'skills/resubmitting-papers'

def load(name):
    path = S/'scripts'/f'{name}.py'
    assert path.is_file(), f'Missing implementation: {name}'
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

class ScopeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ['main.tex', 'results.tex', 'kit.sty']:
            (self.root/name).write_text(name)
    def test_snapshot_has_content_hashes(self):
        r=load('revision_check').capture(self.root,['main.tex'])
        self.assertEqual(len(r['files']['main.tex']),64)
    def test_unchanged_scope(self):
        m=load('revision_check'); b=m.capture(self.root,['main.tex','kit.sty'])
        self.assertTrue(m.check(self.root,b,['main.tex'],['kit.sty'])['within_scope'])
    def test_allowed_edit(self):
        m=load('revision_check'); b=m.capture(self.root,['main.tex','kit.sty'])
        (self.root/'main.tex').write_text('new')
        r=m.check(self.root,b,['main.tex'],['kit.sty'])
        self.assertEqual(r['changed'],['main.tex']); self.assertTrue(r['within_scope'])
        self.assertFalse(r['certifies_semantics'])
    def test_unrelated_edit_blocked(self):
        m=load('revision_check'); b=m.capture(self.root,['main.tex','results.tex'])
        (self.root/'results.tex').write_text('changed number')
        r=m.check(self.root,b,['main.tex'],[])
        self.assertFalse(r['within_scope']); self.assertEqual(r['out_of_scope'],['results.tex'])
    def test_protected_style_edit_blocked(self):
        m=load('revision_check'); b=m.capture(self.root,['main.tex','kit.sty'])
        (self.root/'kit.sty').write_text('shrunken margins')
        self.assertEqual(m.check(self.root,b,['main.tex'],['kit.sty'])['protected_changes'],['kit.sty'])
    def test_allowed_and_protected_overlap_rejected(self):
        m=load('revision_check'); b=m.capture(self.root,['kit.sty'])
        with self.assertRaises(ValueError): m.check(self.root,b,['kit.sty'],['kit.sty'])
    def test_removed_file_detected(self):
        m=load('revision_check'); b=m.capture(self.root,['main.tex','results.tex'])
        (self.root/'results.tex').unlink()
        self.assertIn('results.tex',m.check(self.root,b,['main.tex'],[])['out_of_scope'])
    def test_new_allowed_file(self):
        m=load('revision_check'); b=m.capture(self.root,['main.tex'])
        (self.root/'figure.tex').write_text('new diagram')
        self.assertTrue(m.check(self.root,b,['figure.tex'],[])['within_scope'])
    def test_new_reported_unallowed_file(self):
        m=load('revision_check'); b=m.capture(self.root,['main.tex'])
        r=m.check(self.root,b,['main.tex'],[],['results.tex'])
        self.assertIn('results.tex',r['out_of_scope'])
    def test_cannot_protect_unrecorded_template(self):
        m=load('revision_check'); b=m.capture(self.root,['main.tex'])
        with self.assertRaises(ValueError): m.check(self.root,b,[],['kit.sty'])
    def test_escape_rejected(self):
        with self.assertRaises(ValueError): load('revision_check').capture(self.root,['../secret'])
    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            x=Path(d)/'x'; x.write_text('private'); (self.root/'link.tex').symlink_to(x)
            with self.assertRaises(ValueError): load('revision_check').capture(self.root,['link.tex'])
    def test_ambiguous_path_rejected(self):
        with self.assertRaises(ValueError): load('revision_check').capture(self.root,['./main.tex'])
    def test_empty_snapshot_rejected(self):
        with self.assertRaises(ValueError): load('revision_check').capture(self.root,[])
    def test_bad_digest_rejected(self):
        with self.assertRaises(ValueError): load('revision_check').check(self.root,{'schema_version':1,'files':{'main.tex':'yes'}},[],[])
    def test_no_source_changes_from_audit(self):
        m=load('revision_check'); b=m.capture(self.root,['main.tex']); m.check(self.root,b,[],[])
        self.assertEqual(m.capture(self.root,['main.tex']),b)

@unittest.skipUnless(importlib.util.find_spec('fitz'),'PyMuPDF is optional')
class PDFTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
    def pdf(self,name,words,width=400):
        import fitz
        p=self.root/name
        with fitz.open() as d:
            for word in words: d.new_page(width=width,height=400).insert_text((30,50),word)
            d.save(p)
        return p
    def test_identical_pages(self):
        a=self.pdf('a.pdf',['Fixture A','Fixture B'])
        r=load('pdf_revision_diff').compare(a,a)
        self.assertEqual(r['changed_pages'],[]); self.assertFalse(r['certifies_visual_quality'])
    def test_changed_page_and_neighbor(self):
        a=self.pdf('a.pdf',['A','B','C']); b=self.pdf('b.pdf',['A','changed','C'])
        r=load('pdf_revision_diff').compare(a,b)
        self.assertEqual(r['changed_pages'],[2]); self.assertEqual(r['review_candidate_pages'],[1,2,3])
    def test_added_page(self):
        a=self.pdf('a.pdf',['A']); b=self.pdf('b.pdf',['A','B'])
        r=load('pdf_revision_diff').compare(a,b)
        self.assertEqual(r['pages'][1]['change'],'added')
    def test_removed_page(self):
        a=self.pdf('a.pdf',['A','B']); b=self.pdf('b.pdf',['A'])
        r=load('pdf_revision_diff').compare(a,b)
        self.assertEqual(r['pages'][1]['change'],'removed'); self.assertEqual(r['review_candidate_pages'],[1])
    def test_page_size_change(self):
        a=self.pdf('a.pdf',['A']); b=self.pdf('b.pdf',['A'],450)
        self.assertEqual(load('pdf_revision_diff').compare(a,b)['pages'][0]['change'],'resized')
    def test_metadata_only_not_visual_change(self):
        import fitz
        a=self.pdf('a.pdf',['A']); b=self.root/'b.pdf'
        with fitz.open(a) as d: d.set_metadata({'title':'metadata only'}); d.save(b)
        r=load('pdf_revision_diff').compare(a,b)
        self.assertNotEqual(r['before_sha256'],r['after_sha256']); self.assertEqual(r['changed_pages'],[])
    def test_invalid_dpi_rejected(self):
        a=self.pdf('a.pdf',['A'])
        for dpi in [True,0,1000]:
            with self.assertRaises(ValueError): load('pdf_revision_diff').compare(a,a,dpi=dpi)
    def test_render_does_not_overwrite_directory(self):
        a=self.pdf('a.pdf',['A'])
        with self.assertRaises(ValueError): load('pdf_revision_diff').compare(a,a,render_dir=self.root)
    def test_render_all_pages_and_preserve_pdf(self):
        a=self.pdf('a.pdf',['A']); old=a.read_bytes(); out=self.root/'renders'
        load('pdf_revision_diff').compare(a,a,render_dir=out)
        self.assertTrue((out/'after-001.png').is_file()); self.assertEqual(a.read_bytes(),old)

class RoutingTests(unittest.TestCase):
    def test_local_dag_does_not_require_research_or_full_draft(self):
        p=S/'assets/latex-edit-workflow.json'
        self.assertTrue(p.is_file(),'Local LaTeX DAG not implemented')
        g=json.loads(p.read_text()); order=load('workflow').order(g)
        self.assertNotIn('evidence',g); self.assertNotIn('framing',g)
        self.assertLess(order.index('baseline_render'),order.index('edit'))
        self.assertIn('change_audit',g['release'])
    def test_local_operation_cli(self):
        import subprocess
        r=subprocess.run([sys.executable,str(S/'scripts/workflow.py'),'--operation','latex-edit'],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertIn('change_audit',json.loads(r.stdout)['nodes'])

if __name__=='__main__': unittest.main()
