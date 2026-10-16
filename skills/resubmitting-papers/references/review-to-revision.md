# Evidence-grounded rebuttal and resubmission changes

Use only for author-owned/authorized review history, responses and manuscripts. These are private artifacts. Check the target venue's current confidentiality and generative-AI use policies; do not act as a confidential third-party reviewer without permission.

## Why this reference exists

Prior projects supply complementary ideas:

- TobiasLee Rebuttal-Skill: diagnose the decision-critical concerns and prioritize evidence rather than restating every sentence.
- lachlanchen paper-revision-skill: plan-gated native LaTeX edits, immutable baselines, redlines and compiled-PDF verification.
- K-Dense peer-review/scientific-writing: source-bound scientific claims, method/ethics/statistical scrutiny, qualified human accountability and domain reporting standards.
- The existing ReSubmit DAG: integrate these actions with table/figure and final PDF updates.

This is a new contract, not vendored code or a mandatory third-party dependency.

## Intake and authority

Record manuscript version/hash, author-visible review sources, relevant rebuttal/discussion, author permissions, venue/year/stage, required disclosure policy and the current evidence inventory. Do not assume a reviewer allegation is true; independently audit it. Do not infer AC intent or reviewer agreement from silence.

## Convert criticism to testable changes

For each concern, create a stable Concern ID in the [revision-plan template](../assets/revision-plan-template.md):

1. **Identify the actual question.** Label possible failure mode: novelty/scope, claim evidence, counterfactual explanation, inadequate baseline, experimental protocol, theory assumption, statistics, computation, reproducibility, writing or format.
2. **Separate rebuttal promises from measurements.** Classify the old answer as clarification, existing reference, promised result, new verified result or contradicted result.
3. **Attach the source.** Every new quantitative claim needs a local evidence locator, experimental protocol, version and measurement status. A manuscript text change is not itself scientific proof.
4. **Choose the smallest useful remedy.** Existing-evidence clarification, new experiment proposal (only after approval), strengthened comparator, corrected proof, narrowed claim, appropriate citation, better table/figure or a genuine venue change.
5. **Define a falsifier.** When a new scientific mechanism is proposed, state assumptions, critical derivation, different prediction and what observation would count against it. Not required for a spacing or wording edit.
6. **Authorize and edit.** Match each remedy to target sections/assets, explicit allowed edits and an acceptance check before touching shared TeX.
7. **Verify from compiled pages.** Inspect numbers, equations, captions, section references, row labels, style and reported page anchors. Reconcile the author response (if requested) with the actual changes.

Do not generate reviewer-facing prose as final submission material without a venue policy check and explicit author approval.

## Updating and invalidation

A source change can invalidate earlier “resolved” status. If a baseline changes, results and relative deltas may change; retest table emphasis, figure legends, abstract, related claims and semantic audit. A reviewer reply that claims an experiment was run must stay pending until real artifacts are available. No reviewer response is not reviewer acceptance.

Report **evidence verified**, **manuscript updated** and **PDF checked** separately. Unknown and missing are not failed experiments. Record negative/contradicting results rather than dropping them.

## Domain-specific questions

For biology and clinical research, check cohort/case inclusion, leakage, sampling units, ethics and relevant reporting guidance. For chemistry or physical simulation, check units, method controls and validated predictions. For systems, verify workloads/hardware and fair accounting; for ML, baseline and compute parity; for theory, assumptions/proofs. Do not import clinical claims, chemical measurements or statistical significance from a general LLM's confidence.

If a K-Dense or comparable specialist skill is already installed and approved for the task, use it only for the narrow analysis. Respect skill dependencies, privacy rules and model/venue policies. Do not download a 177-skill collection or publish confidential materials merely to do one review.

## Deliverable

One private revision plan with Concern IDs, evidence map and testable change requests; a source/PDF before-and-after record; unresolved gaps; and a clean separate manuscript source ZIP when authorized. Do not serialize private reviewer text or provenance logs into the public package.
