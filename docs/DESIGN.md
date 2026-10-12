# Design: evidence-led, layout-aware resubmission

## User goal

Make conference migration reliable when a single-column/double-column template change coincides with rebuttal evidence updates. The primary value is native tables, figure redraw, page-limit control, aesthetics and full-paper writing in the correct dependency order. Review diagnosis supports this objective; it is not the product's center.

## Selected architecture

One `resubmitting-papers` entry skill with six focused references, a per-revision JSON DAG and four small Python helpers. It is portable as one complete directory. No mandatory multi-agent hierarchy, database, cloud service or research controller. The user authorized creation in the new repository; implementation stays separate from the upstream Research Autopilot.

Evidence reconciliation and target-template verification run independently, then join in the blueprint. Table and figure specifications stabilize before full result prose. Compiling is the only source of actual pagination. A semantic audit and an all-page final-PDF visual audit both precede release. Change propagation uses a new revision rather than cyclic DAG edges.

## Differentiators as design goals, not proven novelty claims

- Treat template conversion as an asset and argument remapping problem, not style-file substitution.
- Treat rebuttal table changes as data updates propagating into rankings, plots, captions and prose.
- Use target-width structural variants before shrinking; typography and scientific completeness are not expendable.
- Preserve evidence and readable layout while controlling counted pages under exact target rules.
- Adapt Autopilot's evidence-first full-paper writing with compact specialist loading.

## Non-goals

No guaranteed acceptance; no claim of being first; no automatic experiments or submission; no arbitrary official-template compatibility claim; no fictional real-world revision benchmark. Existing reviewers and author replies are not ground truth. No AI-generated measured evidence.

## Verification boundary

Deterministic tests can prove helper behavior. Article-class one/two-column fixtures can demonstrate build/layout mechanics. Neither proves all conference styles work nor that arbitrary agents follow the skill. Behavioral evaluation and real-paper/official-template coverage are separate future validation tasks, not reported as complete.
