"""Keep the README introduction distinct from the six-stage workflow diagram."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT/"docs/assets"

class MangaVisualTests(unittest.TestCase):
    def test_readme_uses_distinct_illustrations(self):
        r = (ROOT/"README.md").read_text()
        self.assertIn("docs/assets/galaxy-journey.svg",r)
        self.assertIn("docs/assets/workflow-manga-animated.svg",r)
        self.assertIn("docs/assets/galaxy-journey-still.svg",r)
        self.assertIn("docs/assets/workflow-manga-still.svg",r)
        self.assertLess(r.index("galaxy-journey.svg"),r.index("workflow-manga-animated.svg"))
        self.assertNotIn('src="docs/assets/workflow-animated.svg"',r)
        self.assertNotIn('src="docs/assets/readme-cover.png"',r)

    def test_assets_parse_and_have_accessible_text(self):
        for name in ("galaxy-journey.svg","galaxy-journey-still.svg",
                     "workflow-manga-animated.svg","workflow-manga-still.svg"):
            raw=(ASSETS/name).read_text()
            svg=ET.fromstring(raw)
            self.assertTrue(svg.tag.endswith("svg"))
            self.assertIn("<title",raw)
            self.assertIn("<desc",raw)
            self.assertNotIn("<script",raw)
            self.assertNotIn("<foreignObject",raw)
            self.assertNotIn("Accepted!",raw)
            self.assertNotIn("May 2025",raw)

    def test_correct_flow_labels_and_sequence(self):
        flow=(ASSETS/"workflow-manga-animated.svg").read_text()
        nodes=["PAPER + REVIEWS","DISCIPLINE ROUTING","VERIFY THE VENUE",
               "RECOMMEND VENUES","REVISE IN LATEX","AUDIT AND PACKAGE"]
        self.assertEqual(len(set(nodes)),6)
        for node in nodes:
            self.assertIn(node,flow)
        self.assertEqual(flow.count('id="panel'),6)
        self.assertIn('marker-end="url(#tip)"',flow)

    def test_animation_and_reduced_motion(self):
        a=(ASSETS/"galaxy-journey.svg").read_text()
        flow=(ASSETS/"workflow-manga-animated.svg").read_text()
        self.assertIn("@keyframes maze",a)
        self.assertIn("@keyframes focus0",flow)
        self.assertIn("prefers-reduced-motion:reduce",a)
        self.assertIn("prefers-reduced-motion:reduce",flow)
        for name in ("galaxy-journey-still.svg","workflow-manga-still.svg"):
            text=(ASSETS/name).read_text()
            self.assertNotIn("@keyframes",text)
            self.assertNotIn("@keyframes",text)

    def test_readme_links_resolve(self):
        r=(ROOT/"README.md").read_text()
        for src in re.findall(r'(?:src|srcset)="([^"]+)"',r):
            if src.startswith("docs/"): self.assertTrue((ROOT/src).is_file(),src)
        self.assertIn("docs/VISUAL_DESIGN.md",r)
        self.assertTrue((ROOT/"docs/VISUAL_DESIGN.md").is_file())

if __name__=="__main__":
    unittest.main()
