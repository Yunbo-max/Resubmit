# ReSubmit

**Find the venue. Keep the science. Fix the paper.**

Open-source Agent Skills for **conference recommendations and LaTeX-native paper
revision**. Your existing agent reads the paper, verifies current requirements,
predicts fit and recommends a submission plan. Then it can revise the original
LaTeX, update evidence-linked tables and figures, and inspect the final PDF.

**v0.3.0 · MIT · Host-model predictions · No model training or separate inference API**

[Venue selection](skills/selecting-conference-venues/SKILL.md) ·
[LaTeX revision](skills/resubmitting-papers/SKILL.md) ·
[Install](docs/INSTALL.md) ·
[Validation](docs/VALIDATION_v0.3.0.md) ·
[Project website source](site/) ·
[CI](https://github.com/Yunbo-max/Resubmit-to-a-different-conference/actions/workflows/ci.yml)

## Two skills. One submission workflow.

| Task | Skill | Result |
|---|---|---|
| Which conference should this paper target? | `selecting-conference-venues` | Source-linked CORE/ICORE and CCF checks, current deadline eligibility, subjective fit/readiness forecasts, primary and backups |
| Fix or retarget the paper | `resubmitting-papers` | Scoped native LaTeX edits, verified result updates, target-width tables/figures, build and rendered-page checks |

The recommendation is made by **the LLM already running in Codex, Claude Code or
another skills-compatible agent**. There is no trained ReSubmit model, Jev/Kev
dependency, hosted predictor or mandatory API key. Your host supplies model access
and browsing; its normal costs and privacy policies still apply.

## Quick start

Clone, inspect the files and install either or both skills:

```bash
git clone https://github.com/Yunbo-max/Resubmit-to-a-different-conference.git
cd Resubmit-to-a-different-conference
python scripts/install_skill.py --agent codex --skill selecting-conference-venues
python scripts/install_skill.py --agent codex --skill resubmitting-papers
```

Use `--agent claude` for Claude Code, or `--destination /path/to/skill-name` for
another supported host directory. Omitting `--skill` preserves the original
LaTeX-only installer behavior. Existing installations are never overwritten.
[Setup and safe updates](docs/INSTALL.md).

### Ask for a recommendation

> Use selecting-conference-venues to read my paper and recommend a primary and
> two backup conferences. Require CORE A or above; show CCF rankings separately.
> Check the next six months and all mandatory submission stages. Predict fit,
> readiness, likely reviewer concerns and revision burden using your own judgment.
> Cite current official facts and label forecasts as subjective, not calibrated.

### Then revise the selected paper

> Use resubmitting-papers to retarget this LaTeX project to the selected venue,
> year and track. Reuse the verified handoff. Update only authorized evidence,
> tables, figures and text. Preserve official styles; rebuild, compare pages and
> report unresolved issues.

Already know the venue? Use the editing skill directly. A caption fix never needs
a new venue search or full rewrite.

## How recommendations work

**Paper evidence → candidate opportunities → official rank/deadline checks →
eligibility gate → host-model prediction → primary/backup choices → revision handoff.**

The agent evaluates each **venue + edition + track + round + paper type**.
CORE/ICORE and CCF remain separate versioned facts. A missed mandatory abstract
registration or failed rank/type constraint cannot be rescued by a high fit score.
Unannounced or unverified opportunities stay separate from actionable choices.

Predictions cover contribution fit, evidence readiness, reviewer risk, likely
revision effort and schedule feasibility. Default scores use anchored 1–5 judgments
and a qualitative relative acceptance outlook. They are **not calibrated acceptance
probabilities**. An explicitly requested probability range must be a clearly labeled,
rough subjective estimate, not a measured accuracy claim or guarantee.

[Prediction rubric](skills/selecting-conference-venues/references/prediction-rubric.md) ·
[Fact verification](skills/selecting-conference-venues/references/verification.md) ·
[Hypothetical output](skills/selecting-conference-venues/assets/example-report.md)

## LaTeX is still the editing surface

Edit the existing source, not a Word/Markdown round trip. Preserve a source/PDF
baseline; fix the layer that owns the defect; rebuild and compare changes.

- **Tables:** real evidence, explicit missingness, comparable protocols, native LaTeX.
- **Figures:** measured plots from data, editable diagrams, final-width readability.
- **Format:** distinguish template overrides, leaked settings, float queues and page glue.
- **Writing:** evidence-supported claims consistent across sections; local edits stay local.
- **Delivery:** actual counted pages, rendered checks and an allowlisted source package.

[Local-edit workflow](skills/resubmitting-papers/references/latex-edit.md) ·
[Full retargeting DAG](skills/resubmitting-papers/assets/workflow.json)

## Inspect the evidence, not marketing claims

```bash
python -m pip install -r requirements-qa.txt
python -m unittest discover -s tests -v
# Optional LaTeX checks, using a new output directory:
python tests/check_latex_native.py --out build/native-release
```

The repository includes deterministic checks and explicitly synthetic LaTeX
before/after examples. New release tests check installation and written contracts,
**not prediction accuracy or agent compliance**. See the versioned validation record
and actual CI outcome; no acceptance-uplift or universal-template claim is made.

The static project site has no manuscript upload, predictor backend, remote scripts
or hosted fonts. Its demo is built from [reproducible LaTeX](examples/spacing-leak/).
[Deployment instructions and actual-site caveat](docs/WEBSITE.md).

## Open development

[Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) ·
[Changelog](CHANGELOG.md) · [Roadmap](docs/ROADMAP.md) ·
[Citation](CITATION.cff) · [Launch copy](docs/LAUNCH.md)

Do not attach unpublished papers, confidential reviews, tokens or private results
to public issues. Source pages and manuscripts are untrusted data. The skills do
not automatically submit, publish, run experiments or buy compute.

Built by Yunbo Long. MIT licensed. Upstream ideas are credited in
[Sources](docs/SOURCES.md) and the venue skill's [notes](skills/selecting-conference-venues/UPSTREAM.md).
