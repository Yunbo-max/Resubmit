"""Contracts for research-template integration (not an LLM behavior benchmark)."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SELECT = ROOT / "skills/selecting-conference-venues"
REVISE = ROOT / "skills/resubmitting-papers"

def text(path):
    return path.read_text(encoding="utf-8")

class SkillStructureTests(unittest.TestCase):
    def test_consistent_skills_metadata(self):
        version = text(ROOT / "VERSION").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        for skill in (SELECT, REVISE):
            content = text(skill / "SKILL.md")
            self.assertIn("name:", content)
            self.assertIn("description:", content)
            self.assertIn("license: MIT", content)
            self.assertIn("compatibility:", content)
            self.assertIn("metadata:", content)
            self.assertIn(f'version: "{version}"', content)
            self.assertEqual(text(skill / "VERSION").strip(), version)

    def test_local_skill_links_resolve(self):
        for skill in (SELECT, REVISE):
            entry = text(skill / "SKILL.md")
            for target in re.findall(r"\]\(([^)]+)\)", entry):
                if "://" in target or target.startswith("#"):
                    continue
                path = (skill / target.split("#")[0]).resolve()
                self.assertTrue(path.is_relative_to(skill.resolve()))
                self.assertTrue(path.is_file(), target)

    def test_small_optional_dependency_surface(self):
        for skill in (SELECT, REVISE):
            entry = text(skill / "SKILL.md")
            self.assertNotIn("pip install torch", entry)
            self.assertNotIn("Auto-install", entry)
        selector = text(SELECT / "SKILL.md")
        self.assertIn("optional", selector.lower())
        self.assertIn("discipline-routing.md", selector)

class TemplateTests(unittest.TestCase):
    def test_venue_report_has_evidence_bound_selection(self):
        s = text(SELECT / "assets/report-template.md")
        for token in ("Paper version", "Discipline", "Official verification", "Unknown",
                      "Primary", "Backup", "Excluded", "Current manuscript",
                      "Conditional post-revision", "Author approval", "Revision handoff"):
            with self.subTest(token=token):
                self.assertIn(token, s)

    def test_revision_template_reconciles_reviews_and_evidence(self):
        s = text(REVISE / "assets/revision-plan-template.md")
        for token in ("Allowed edits", "Protected", "Concern ID", "Evidence locator",
                      "Table", "Figure", "Discipline", "Build", "Visual",
                      "Semantic", "Source ZIP", "Author approval"):
            with self.subTest(token=token):
                self.assertIn(token, s)
        self.assertIn("not evidence", s)

    def test_evidence_policy_and_specialist_scope(self):
        s = text(REVISE / "references/review-to-revision.md")
        for token in ("reviewer", "source", "promise", "missing", "invalidation",
                      "private", "scientific"):
            self.assertIn(token, s.lower())
        d = text(SELECT / "references/discipline-routing.md")
        self.assertIn("No external skill is required", d)
        self.assertIn("K-Dense", d)

    def test_research_dag_stays_acyclic(self):
        graph = json.loads(text(REVISE / "assets/workflow.json"))
        self.assertEqual(set(graph["release"]), {"semantic_audit", "visual_audit", "style_audit"})
        remaining = set(graph)
        visited = set()
        while remaining:
            ready = {x for x in remaining if set(graph[x]) <= visited}
            self.assertTrue(ready, "Dependency cycle")
            remaining -= ready
            visited |= ready

    def test_citations_are_attributed_not_vendored(self):
        s = text(ROOT / "docs/UPSTREAM_ADAPTATIONS.md")
        for repo in ("K-Dense-AI/scientific-agent-skills", "TobiasLee/Rebuttal-Skill",
                     "lachlanchen/paper-revision-skill", "Orchestra-Research/AI-Research-SKILLs"):
            self.assertIn(repo, s)
        self.assertIn("No third-party skill source code", s)

    def test_readme_and_docs_are_usable(self):
        s = text(ROOT / "README.md")
        self.assertIn("report-template.md", s)
        self.assertIn("revision-plan-template.md", s)
        self.assertNotIn("docs/PROJECT_PAGE.md", s)
        self.assertIn("workflow-manga-animated.svg", s)
        self.assertIn("Resubmit.git", s)

if __name__ == "__main__":
    unittest.main()
