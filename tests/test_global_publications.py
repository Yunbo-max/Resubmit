"""Contract tests for cross-region journals and conference recommendations.

These test instructions/templates and status semantics, not model predictions.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SELECT = ROOT/"skills/selecting-conference-venues"
REVISE = ROOT/"skills/resubmitting-papers"

class GlobalRoutingTests(unittest.TestCase):
    def test_venue_skill_supports_both_types(self):
        body=(SELECT/"SKILL.md").read_text()
        for token in ("journal", "conference", "institution", "special issue",
                      "journal-timing.md", "ranking-systems.md", "institution-profile.md"):
            with self.subTest(token=token): self.assertIn(token,body.lower())
    def test_cas_policy_is_versioned_and_discontinued(self):
        body=(SELECT/"references/ranking-systems.md").read_text()
        for token in ("2026", "discontinued", "2025", "las.cas.cn",
                      "JCR", "JIF", "AJG", "ABDC", "FT50", "Scopus", "2024", "2025"):
            with self.subTest(token=token): self.assertIn(token,body)
        self.assertNotIn("2026 CAS ranking official new",body)
    def test_region_not_nationality_and_institution_override(self):
        body=(SELECT/"references/institution-profile.md").read_text().lower()
        for token in ("affiliation", "institution", "nationality", "china", "united kingdom",
                      "australia", "business school", "institutional"):
            self.assertIn(token,body)
    def test_journal_submission_deadlines_are_different(self):
        body=(SELECT/"references/journal-timing.md").read_text()
        for token in ("regular", "Special Issue", "rolling", "deadline",
                      "conference", "first decision", "time-to-publication",
                      "unverified", "author"):
            self.assertIn(token,body)
    def test_paper_report_has_journal_and_conference_contract(self):
        report=(SELECT/"assets/report-template.md").read_text()
        for token in ("Paper version", "Discipline", "Official verification", "Unknown",
                      "Primary", "Backup", "Excluded", "Current manuscript",
                      "Conditional post-revision", "Author approval", "Revision handoff",
                      "Journal / Conference", "Evaluation context", "ISSN",
                      "AJG", "ABDC", "time-to-publication"):
            self.assertIn(token,report)
    def test_revision_skill_retains_small_edits(self):
        body=(REVISE/"SKILL.md").read_text()
        self.assertIn("journal",body.lower())
        self.assertIn("latex-edit",body)
        self.assertIn("journal", (REVISE/"references/layout.md").read_text().lower())
    def test_readme_public_entrypoint_stays_clear(self):
        body=(ROOT/"README.md").read_text()
        self.assertIn("journal",body.lower())
        self.assertIn("conference",body.lower())
        self.assertIn("cas",body.lower())
        self.assertIn("ft50",body.lower())
        self.assertIn("galaxy-journey.svg",body)
        self.assertIn("workflow-manga-animated.svg",body)
    def test_versions_consistent(self):
        expected="0.4.0"
        for path in [ROOT/"VERSION",SELECT/"VERSION",REVISE/"VERSION"]:
            self.assertEqual(path.read_text().strip(),expected)
    def test_no_new_runtime_dependency(self):
        self.assertFalse((SELECT/"scripts").exists())
        self.assertIn("no separate API", (SELECT/"SKILL.md").read_text())
if __name__=="__main__":unittest.main()
