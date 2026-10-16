# Visual design and animation notes

ReSubmit's README uses **two different illustrations**, not a before/after pair:

1. [Project introduction](assets/intro-manga.svg) — a manga-inspired researcher, an editable paper, a laptop and clear product positioning. This is an original vector illustration; it is not a screenshot, journal approval, or proof of venue acceptance.
2. [Workflow diagram](assets/workflow-manga-animated.svg) — six discrete stages, linked by directional arrows: Paper + Reviews → Discipline Routing → Verify Venue → Recommend Venues → Revise in LaTeX → Audit and Package. The dynamic highlighting indicates the sequence rather than a real scheduled agent execution.

Each animated SVG is **self-contained**, uses only SVG primitives and CSS, requires no JavaScript, third-party scripts, externally hosted images or fonts, and exposes a static counterpart ([intro](assets/intro-manga-still.svg), [flow](assets/workflow-manga-still.svg)) for reduced motion. The workflow remains legible even if a client does not play CSS animations.

## Why the process is drawn this way

- Reviewer history and verified evidence are read before making major scientific changes.
- Discipline-specific procedures are optional references, not mandatory installs or independent science certification.
- Official CFP, edition, rank, date and track verification occurs *before* subjective venue recommendation.
- The LLM supplies subjective fit judgments; it does not promise calibrated acceptance probabilities.
- Only the author's choice triggers substantial retargeting; a local LaTeX fix may bypass venue search.
- Revisions are source-preserving and must finish with compiled-page and scientific consistency checks.

## Technical caveats

The manga figure, paper sheets and process cards are **illustrations**, not actual compiled conference templates or research results. Official target styles must be checked for the selected edition and track. The images contain no real deadline, ranking, score or acceptance prediction. Read the [real skill specifications](../skills/selecting-conference-venues/SKILL.md) and [revision contracts](../skills/resubmitting-papers/SKILL.md) for operational limitations.

This release changes README presentation assets only. Existing skills, model selection, LaTeX helper scripts and research-evidence rules are preserved.
