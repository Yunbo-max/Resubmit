"""Release contract and installer tests, NOT prediction accuracy evaluation."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/selecting-conference-venues"


class VenueSkillTests(unittest.TestCase):
    def read(self, name):
        path = SKILL / name
        self.assertTrue(path.is_file(), str(path))
        return path.read_text(encoding="utf-8")

    def test_entry_and_description(self):
        text = self.read("SKILL.md")
        self.assertTrue(text.startswith("---\nname: selecting-conference-venues\n"))
        self.assertIn("description: Use when", text)

    def test_host_model_not_training(self):
        text = self.read("SKILL.md")
        for token in ("host model", "No training", "no separate API", "subjective"):
            self.assertIn(token, text)

    def test_facts_and_predictions_separated(self):
        text = self.read("references/prediction-rubric.md")
        for token in ("NOT an acceptance probability", "unknown", "current manuscript", "conditional"):
            self.assertIn(token, text)

    def test_official_rules_and_prerequisites(self):
        text = self.read("references/verification.md")
        for token in ("CORE", "CCF", "OR", "AND", "abstract", "timezone", "Findings", "unverified"):
            self.assertIn(token, text)

    def test_no_requirement_for_external_model_service(self):
        all_text = "\n".join(p.read_text() for p in SKILL.rglob("*.md"))
        self.assertTrue(all_text)
        self.assertNotIn("modal run", all_text)
        self.assertNotIn("pip install torch", all_text)

    def test_standalone_reference_links_resolve(self):
        self.read("SKILL.md")
        for p in SKILL.rglob("*.md"):
            for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", p.read_text()):
                if "://" in target or target.startswith("mailto:"):
                    continue
                resolved = (p.parent / target).resolve()
                self.assertTrue(resolved.is_relative_to(SKILL.resolve()), (p, target))
                self.assertTrue(resolved.exists(), (p, target))

    def test_example_is_hypothetical_not_live_prediction(self):
        text = self.read("assets/example-report.md")
        for token in ("Hypothetical", "not a live recommendation", "not calibrated", "missed"):
            self.assertIn(token, text)

    def test_template_has_recommendation_and_exclusions(self):
        text = self.read("assets/report-template.md")
        for token in ("Primary", "Backup", "Excluded", "source", "LaTeX", "subjective"):
            self.assertIn(token, text)

    def test_versions_match(self):
        version = self.read("VERSION")
        self.assertEqual(version, (ROOT/"VERSION").read_text())
        self.assertEqual(version, (ROOT/"skills/resubmitting-papers/VERSION").read_text())

    def test_runtime_needs_no_prediction_script(self):
        self.read("SKILL.md")
        self.assertFalse((SKILL/"scripts").exists())


class SelectedInstallerTests(unittest.TestCase):
    def command(self, *args):
        return subprocess.run([sys.executable, str(ROOT/"scripts/install_skill.py"), *args],
                              text=True, capture_output=True, timeout=15)

    def test_explicit_venue_skill_install(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"selection"
            run=self.command("--skill", "selecting-conference-venues", "--destination", str(out))
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertTrue((out/"references/verification.md").is_file())
            self.assertIn("selecting-conference-venues",run.stdout)

    def test_default_still_installs_latex(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"editing"
            run=self.command("--destination",str(out))
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertIn("name: resubmitting-papers", (out/"SKILL.md").read_text())

    def test_unknown_skill_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"bad"
            run=self.command("--skill","../../bad","--destination",str(out))
            self.assertNotEqual(run.returncode,0)
            self.assertFalse(out.exists())

    def test_venue_install_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"existing"; out.mkdir(); (out/"mine").write_text("keep")
            run=self.command("--skill","selecting-conference-venues","--destination",str(out))
            self.assertNotEqual(run.returncode,0)
            self.assertEqual((out/"mine").read_text(),"keep")
            self.assertFalse((out/"SKILL.md").exists())


class PublicVenueEntryTests(unittest.TestCase):
    def test_english_venue_entry(self):
        self.assertTrue((SKILL/"SKILL.md").exists())
        for p in SKILL.rglob("*.md"):
            self.assertNotRegex(p.read_text(),r"[\u4e00-\u9fff]")

    def test_site_advertises_both_not_an_online_predictor(self):
        text=(ROOT/"site/index.html").read_text()
        for token in ('id="venues"', "selecting-conference-venues", "host model", "No model training"):
            self.assertIn(token,text)
        self.assertNotIn('type="file"',text)

    def test_install_switch_has_both_commands(self):
        text=(ROOT/"site/app.js").read_text()
        self.assertIn("--skill selecting-conference-venues",text)
        self.assertIn("--skill resubmitting-papers",text)

    def test_launch_copy_and_validation_exist(self):
        for name in ("docs/LAUNCH.md","docs/VALIDATION_v0.3.0.md"):
            self.assertTrue((ROOT/name).is_file(),name)


if __name__=="__main__":
    unittest.main()
