"""Format diagnostics use synthetic inputs; no claim of agent behavior or venue compliance."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'skills/resubmitting-papers/scripts/latex_format.py'

def module():
    assert SCRIPT.is_file(), 'Missing implementation: latex_format.py'
    spec=importlib.util.spec_from_file_location('latex_format',SCRIPT)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def signature(context='body',value='0.0pt',extra=''):
    return f'RSFMT-BEGIN:{context}\nRSFMT-parskip={value}\nRSFMT-fontsize=10\n{extra}RSFMT-END:{context}\n'

class SourceTests(unittest.TestCase):
    def codes(self, text): return {x['code'] for x in module().scan_text(text,'main.tex')}
    def test_multiline_spacing_assignment(self):
        self.assertIn('length-override',self.codes('\\setlength\n {\\textfloatsep}{2pt}'))
    def test_direct_length_assignment(self):
        self.assertIn('length-override',self.codes(r'\parskip=4pt plus 1pt'))
    def test_reading_dimension_is_not_assignment(self):
        self.assertNotIn('length-override',self.codes(r'\typeout{\the\parskip}'))
    def test_negative_spacing(self): self.assertIn('manual-spacing',self.codes(r'\vspace{-3mm}'))
    def test_legitimate_table_row_not_flagged_as_spacing(self):
        self.assertNotIn('manual-spacing',self.codes(r'A & B \\'))
    def test_explicit_row_spacing_is_reviewed(self): self.assertIn('manual-spacing',self.codes(r'A & B \\[3pt]'))
    def test_comments_ignored_preserving_line(self):
        text='% \\vspace{-3pt}\nA\n\\captionsetup{font=small}'
        findings=module().scan_text(text,'main.tex')
        self.assertNotIn('manual-spacing',{x['code'] for x in findings})
        self.assertEqual(next(x['line'] for x in findings if x['code']=='caption-override'),3)
    def test_escaped_percent_does_not_mask_command(self):
        self.assertIn('manual-spacing',self.codes(r'10\% \vspace{1pt}'))
    def test_verbatim_environments_ignored(self):
        for env in ['verbatim','verbatim*','Verbatim','lstlisting','minted','comment']:
            self.assertNotIn('manual-spacing',self.codes('\\begin{'+env+'}\n\\vspace{1pt}\n\\end{'+env+'}'))
    def test_inline_verb_with_percent(self):
        text=r'\verb|%\vspace{2pt}| \captionsetup{font=small}'
        self.assertNotIn('manual-spacing',self.codes(text)); self.assertIn('caption-override',self.codes(text))
    def test_scientific_macro_not_style_override(self):
        self.assertNotIn('style-definition',self.codes(r'\newcommand{\loss}{\mathcal{L}}'))
    def test_font_scope_site_is_flag_not_proven_error(self):
        fs=module().scan_text(r'{\small Table text}','table.tex')
        self.assertTrue(fs); self.assertTrue(all(x['severity']=='review' for x in fs))
    def test_caption_list_heading_and_font_packages(self):
        fs=self.codes(r'\usepackage{caption,enumitem,titlesec,times}')
        self.assertIn('style-package',fs)
    def test_arraystretch_definition(self):
        self.assertIn('style-definition',self.codes(r'\renewcommand{\arraystretch}{1.3}'))
    def test_float_forcing(self): self.assertIn('float-placement',self.codes(r'\begin{figure}[H]'))
    def test_center_environment(self): self.assertIn('center-environment',self.codes(r'\begin{center}x\end{center}'))
    def test_scan_does_not_modify_sources(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'main.tex'; p.write_text(r'\vspace{-1pt}'); before=p.read_bytes()
            result=module().scan_files(Path(d),['main.tex'])
            self.assertEqual(p.read_bytes(),before); self.assertTrue(result['findings'])
    def test_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): module().scan_files(Path(d),['../x.tex'])
    def test_duplicate_packages_across_files(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'a.tex').write_text(r'\usepackage{caption}')
            (p/'b.tex').write_text(r'\usepackage[small]{caption}')
            self.assertIn('repeated-package',{x['code'] for x in module().scan_files(p,['a.tex','b.tex'])['findings']})

class ProbeTests(unittest.TestCase):
    def test_identical_is_not_certification(self):
        r=module().compare_logs(signature(),signature())
        self.assertEqual(r['status'],'no-difference-detected'); self.assertFalse(r['certifies_compliance'])
    def test_spacing_drift_detected(self):
        r=module().compare_logs(signature(),signature(value='4.0pt'))
        self.assertEqual(r['differences'][0]['key'],'parskip'); self.assertEqual(r['status'],'review-required')
    def test_late_context_catches_local_difference(self):
        a=signature()+signature('after_table'); b=signature()+signature('after_table', '8.0pt')
        self.assertEqual(module().compare_logs(a,b)['differences'][0]['context'],'after_table')
    def test_missing_probe_unknown(self):
        self.assertEqual(module().compare_logs('normal log','normal log')['status'],'unknown')
    def test_missing_context_not_pass(self):
        self.assertEqual(module().compare_logs(signature()+signature('after_table'),signature())['status'],'incomplete')
    def test_missing_key_not_pass(self):
        r=module().compare_logs(signature(),signature().replace('RSFMT-fontsize=10\n',''))
        self.assertEqual(r['status'],'incomplete')
    def test_duplicate_context_rejected(self):
        with self.assertRaises(ValueError): module().parse_log(signature()+signature())
    def test_truncated_probe_rejected(self):
        with self.assertRaises(ValueError): module().parse_log(signature().replace('RSFMT-END:body\n',''))
    def test_duplicate_key_rejected(self):
        with self.assertRaises(ValueError): module().parse_log(signature(extra='RSFMT-fontsize=12\n'))
    def test_context_mismatch_rejected(self):
        with self.assertRaises(ValueError): module().parse_log(signature().replace('RSFMT-END:body','RSFMT-END:other'))
    def test_identical_absence_of_values_unknown(self):
        with self.assertRaises(ValueError): module().parse_log('RSFMT-BEGIN:body\nRSFMT-END:body\n')

class DependencyTests(unittest.TestCase):
    def graph(self):
        import json
        return json.loads((ROOT/'skills/resubmitting-papers/assets/workflow.json').read_text())
    def test_style_baseline_precedes_blueprint(self):
        g=self.graph()
        self.assertIn('style_baseline',g)
        self.assertIn('style_baseline',g['blueprint'])
        self.assertIn('venue',g['style_baseline'])
    def test_style_audit_is_required_for_release(self):
        g=self.graph()
        self.assertIn('style_audit',g)
        self.assertIn('compile',g['style_audit'])
        self.assertIn('style_audit',g['release'])

if __name__=='__main__': unittest.main()
