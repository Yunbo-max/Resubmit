# Open-source capability comparison

**Reviewed 2026-10-16.** This comparison is based on publicly available repository READMEs and skills, not a side-by-side execution benchmark. It compares documented workflow *scope*, not what other agents are technically able to achieve.

**Legend:** ✓ explicitly documented; ◐ related/partial capability or another skill in the collection; — not a primary documented feature. A dash never means “impossible”.

| Project | Relevant strengths | Relationship to ReSubmit |
|---|---|---|
| [CCF-Deadlines](https://github.com/ccfddl/ccf-deadlines) | CORE/CCF data, multiple deadline stages, public catalog and MCP | Venue data; does not present a paper-specific review-to-LaTeX-edit package |
| [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Broad domain-specific research, biology/chemistry/physics methods, scientific writing and peer-review skills | Deeper domain expertise; optionally complements ReSubmit's discipline-aware venue analysis |
| [VibeResearch publish-venue-targeting](https://github.com/lengmo1996/VibeResearch-skills/blob/main/skills/global/publish-venue-targeting/SKILL.md) | Paper fit, current source checks, primary and backups, switch triggers | Strong conceptual overlap in venue recommendation; its main skill does not perform source-aware TeX layout repair |
| [TobiasLee Rebuttal-Skill](https://github.com/TobiasLee/Rebuttal-Skill/blob/main/SKILL.md) | Review concern diagnosis, evidence-first experiments and rebuttal/resubmission planning | Overlaps in review triage; not primarily conference discovery and LaTeX/PDF editing |
| [lachlanchen paper-revision-skill](https://github.com/lachlanchen/paper-revision-skill/blob/main/SKILL.md) | Controlled LaTeX edits, response trace, redlines, compiled PDF verification | Strong native revision overlap; current rank/deadline-based primary/backup choices are not its main scope |
| [Orchestra ML Paper Writing](https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/main/20-ml-paper-writing/ml-paper-writing) | ML paper writing, template preparation and citation verification | Writing and retargeting overlap, not principally a current CORE/CCF opportunity finder |

## How to interpret the README table

The comparison focuses on seven workflow interfaces: venue facts, specialist science, paper-specific venue choice, reviews-to-manuscript changes, native TeX layout edits, compiled-PDF QA, and combined decision-to-revision handoff.

The combination offered by ReSubmit is a documented **eligibility / judgment → author-approved target → evidence-linked LaTeX revision → PDF inspection** workflow with two installable skills. This is a packaging/integration distinction among these inspected examples, **not proof of unique components or superior execution quality**. Other agents can combine multiple libraries to achieve similar results.

ReSubmit does not replace discipline-specialist workflows and it has no validated acceptance-probability predictor, full automatic submission service or end-to-end performance comparison. We encourage rigorous matched-task benchmarks instead of categorical “other repos cannot do X” claims.

See the source skills: [venue selection](../skills/selecting-conference-venues/SKILL.md) and [LaTeX revision](../skills/resubmitting-papers/SKILL.md).
