"""Reader-facing README entry flow: source check, not agent-performance testing."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
DOC=(ROOT/"README.md").read_text(encoding="utf-8")

class ReadmeOnboardingTests(unittest.TestCase):
    def test_install_first(self):
        self.assertIn('id="quick-start"',DOC)
        self.assertLess(DOC.index('id="quick-start"'),DOC.index("docs/assets/workflow-manga-animated.svg"))
        self.assertLess(DOC.index('id="quick-start"'),DOC.index("## How ReSubmit compares"))
    def test_big_promise_and_clear_io(self):
        self.assertIn("# Every Thoughtful Paper Deserves the Right Venue.",DOC)
        self.assertIn("What you provide",DOC)
        self.assertIn("What you receive",DOC)
        self.assertIn("Example result",DOC)
        self.assertIn("hypothetical",DOC.lower())
    def test_actual_install_commands(self):
        self.assertIn("git clone https://github.com/Yunbo-max/Resubmit.git",DOC)
        self.assertIn("cd Resubmit",DOC)
        self.assertIn("python scripts/install_skill.py --agent codex --skill selecting-conference-venues",DOC)
        self.assertIn("python scripts/install_skill.py --agent codex --skill resubmitting-papers",DOC)
        self.assertIn("docs/INSTALL.md",DOC)
    def test_cleared_marketing_disclaimer_section(self):
        self.assertNotIn("## Evidence before promises",DOC)
        self.assertNotIn("Helper tests and synthetic LaTeX examples do not prove",DOC)
    def test_preserves_core_demos_comparison_and_templates(self):
        for target in ("galaxy-journey.svg","workflow-manga-animated.svg",
                       "report-template.md","revision-plan-template.md",
                       "docs/FEATURE_MATRIX.md", "CONTRIBUTING.md"):
            self.assertIn(target,DOC)
        self.assertNotIn("docs/PROJECT_PAGE.md",DOC)
    def test_explicit_prompt_and_outputs(self):
        self.assertIn("Copy this prompt",DOC)
        self.assertIn("Publication shortlist",DOC)
        self.assertIn("Revision plan",DOC)
        self.assertIn("Revised LaTeX",DOC)
if __name__=="__main__": unittest.main()
