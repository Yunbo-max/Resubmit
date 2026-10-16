"""Presentation contract tests: not a scientific or performance benchmark."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]

class WorkflowTests(unittest.TestCase):
    def test_svg_syntax_and_stage_names(self):
        for asset in ("workflow-animated.svg","workflow-still.svg"):
            data=(ROOT/"docs/assets"/asset).read_text(encoding="utf-8")
            tree=ET.fromstring(data)
            self.assertTrue(tree.tag.endswith("svg"))
            for label in ("PAPER + REVIEWS","DISCIPLINE ROUTING","VERIFY THE VENUE",
                          "RECOMMEND VENUES","REVISE IN LATEX","AUDIT AND PACKAGE"):
                self.assertIn(label,data)
            self.assertNotIn("May 2025",data)
            self.assertNotIn("https://",data)
    def test_animation_and_fallback(self):
        main=(ROOT/"README.md").read_text()
        animated=(ROOT/"docs/assets/workflow-animated.svg").read_text()
        still=(ROOT/"docs/assets/workflow-still.svg").read_text()
        self.assertIn("workflow-animated.svg",main)
        self.assertIn("workflow-still.svg",main)
        self.assertIn("prefers-reduced-motion: reduce",main)
        self.assertIn("prefers-reduced-motion:reduce",animated)
        self.assertIn("@keyframes act0",animated)
        self.assertNotIn("@keyframes",still)
    def test_comparison_is_qualified(self):
        readme=(ROOT/"README.md").read_text()
        self.assertIn("not a head-to-head benchmark",readme.lower())
        self.assertIn("K-Dense",readme)
        self.assertIn("FEATURE_MATRIX.md",readme)
        self.assertNotIn("docs/PROJECT_PAGE.md",readme)
    def test_optional_domain_reference_resolves(self):
        s=(ROOT/"skills/selecting-conference-venues/SKILL.md").read_text()
        self.assertIn("discipline-routing.md",s)
        path=ROOT/"skills/selecting-conference-venues/references/discipline-routing.md"
        self.assertTrue(path.exists())
        self.assertIn("No external skill is required",path.read_text())
    def test_new_repository_clone(self):
        for p in ("README.md","docs/INSTALL.md"):
            content=(ROOT/p).read_text()
            self.assertIn("https://github.com/Yunbo-max/Resubmit.git",content)
            self.assertNotIn("Resubmit-to-a-different-conference",content)
    def test_version_consistency(self):
        expected=(ROOT/"VERSION").read_text().strip()
        self.assertRegex(expected,r"^\d+\.\d+\.\d+$")
        for p in ("skills/selecting-conference-venues/VERSION",
                  "skills/resubmitting-papers/VERSION"):
            self.assertEqual((ROOT/p).read_text().strip(),expected)
if __name__=="__main__":unittest.main()
