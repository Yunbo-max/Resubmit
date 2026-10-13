# Host-model prediction rubric

The host LLM makes the predictions; this document is the rubric, not a trained model.
Use the same rubric across candidates, anchored to evidence. Do not ask for a new
model endpoint, synthetic training set, fine-tune or local GPU.

## Separate facts, judgments and plans

Facts: quoted/located requirements, observed paper contents, actual results.
Judgments: fit, readiness, likely reviewer concern, effort and outlook.
Plans: modifications not yet carried out. A plan is not evidence and does not imply a
favorable future experimental result.

Start with the current manuscript. Give conditional forecasts separately:
"If the matched-budget comparison supports the claimed mechanism..." is legitimate.
"The new comparison will show an improvement..." is not.

## Independent axes (1–5; unknown is separate)

| Axis | 1 | 3 | 5 |
|---|---|---|---|
| Contribution/community fit | Outside scope or wrong contribution form | Relevant but substantial audience/framing mismatch | Direct scope, contribution and evidence-form match |
| Evidence readiness | Central claim unsupported or contradicted | Plausible case with material remaining checks | Main claims supported by the supplied appropriate evidence |
| Schedule feasibility | Required work plainly infeasible in the stated window | Tight or dependent on uncertain tasks | Required work plausibly fits with room for verification |
| Revision burden | Minimal local updates | Significant prose/assets restructuring | New evidence, substantial analysis or method redesign |

Scores 2 and 4 represent intermediate cases. High burden means more work, not a better
candidate. Unknown has no numerical substitute. State what artifact supports each axis:
CFP passage, paper section, table, proof, review or inspected LaTeX source.
Without enough information, leave the axis unknown and give a provisional recommendation.

A score is **NOT an acceptance probability**. Do not add the axes into an unexplained
total. Do not sum paper/venue fits to 100%; several venues can all fit, or none can.
Do not recommend an ineligible candidate because it scores well on soft dimensions.

Review risks: identify the strongest specific objection (e.g. unmatched compute,
unclear novelty, missing proof condition, mismatch with track scope). Preserve uncertainty
about reviewer intent. Previous reviews are evidence about expressed concerns, not a
guarantee the next reviewers will agree.

## Relative acceptance outlook

Give a qualitative forecast for the current version: weak, plausible, competitive or
insufficient-evidence. This is a subjective host-model judgment, not an official verdict
or guarantee. A "competitive" paper can still be rejected.

If explicitly requested and enough material exists, a broad acceptance-probability range
may be added, labeled "rough subjective estimate; not calibrated; not a statistical
confidence interval." Name the event (e.g. acceptance to this main track), version,
assumptions and evidence gaps. Do not invent a range when the manuscript or venue evidence
is too sparse. Prefer rounded ranges; do not display spurious decimal precision.
Never call model self-confidence, repeated model agreement, a fit score or the historical
venue acceptance rate a calibrated paper-specific probability.

Host temperature, model identity, token usage and settings are reported only if actually
exposed. No accuracy, Brier score, calibration or acceptance-uplift claims without evaluation.

## Rank and stress-test

Apply the hard gate first, then compare viable candidates jointly. Normally offer one
primary and two backups, with a stretch/conditional option only when useful. Fewer are
better than invented suitable alternatives. Let the author's rank/time preferences
control trade-offs; do not optimize only for fame or easiest perceived acceptance.

For the top candidate, briefly state the strongest counterargument and compare the
runner-up. Avoid anchoring on the first venue mentioned. Use a specialist venue when the
actual contribution supports it. Consult a few relevant recent papers for top candidates
when available; no fixed requirement to collect five years of every conference's rates.

Estimate LaTeX burden from actual files when supplied: current main-body length, target
counting rules, column widths, widest native tables, equation/algorithm overflow, figure
source availability, bibliography and declarations. Otherwise mark it estimated/unknown.
Do not infer exact page savings from a paragraph count.

State what would change the recommendation: completed evidence, an extension verified on
the official site, a confirmed registration, a narrowed claim or an author scope decision.
Do not auto-edit the manuscript to make your preferred recommendation appear correct.

## Practical output

Lead with an actual choice and concise evidence-backed reasons. Then show the independent
axes, current eligibility, relative outlook, source-linked facts, main objections,
required work and exclusions. Keep the detailed report optional when the user requests
only a short answer. No mandatory JSON, training data, services or helper scripts.
