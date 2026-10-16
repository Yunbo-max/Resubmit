# ReSubmit revision plan — [private manuscript version]

> Working template, **not submission-ready**. Protect confidential reviews and unpublished data. This file is a private work product; package only the approved manuscript sources, not this plan, in the final source ZIP.

## A. Scope, author approval and provenance

- **Revision mode:** [latex-edit / layout-only / rebuttal-update / retarget / full-revision]
- **Paper version and immutable baseline:** [main file, commit/hash, baseline PDF hash and date]
- **Target:** [venue, edition, track, article type; approved or still provisional]
- **Verified official kit:** [source URL and checked date; template hash; or Unknown]
- **Discipline:** [contribution type, intended audience, relevant reporting norms; optional specialist consultation if authorized]
- **Allowed edits:** [exact files/sections/figures/tables and rationale]
- **Protected:** [official class/style, untouched experiments and results, unrelated text, private review documents]
- **Author approval:** [who approved which changes; pending otherwise]
- **Privacy / AI-assistance boundary:** [permission for external model processing, venue policy, prohibited materials; Unknown blocks affected work]

## B. Review-to-change trace (rebuttal or resubmission tasks)

A reviewer opinion is not scientific ground truth. Reviewer's silence is not agreement. A promise is not evidence.

| Concern ID | Specific reviewer/AC concern | Old rebuttal answer (if any) | Evidence locator + status | What is unresolved | Intended revision and target | Completion test |
|---|---|---|---|---|---|---|
| [R1-C1] | [literal, bounded issue] | [answer or none] | [table/proof/raw result/hash; measured/reported/missing/contradicted] | [gap] | [section/figure/table and edit scope] | [scientific plus PDF check] |

**Status per concern:** reply drafted / verified evidence available / manuscript implemented / independently audited. These are independent states, not one resolved flag.

## C. Claim/evidence registry

| Claim ID | Exact versioned claim | Evidence locator | Design/method assumptions | Uncertainty, counterexample or negative result | Dependent paragraph/Table/Figure |
|---|---|---|---|---|---|
| [C1] | [supported proposition] | [source/hash, or missing] | [assumptions] | [limits] | [targets] |

Citations require correct metadata **and** passage-level support. Missing or promised experiments are **not evidence**. Statistical tests must match the actual sampling/experimental design; do not derive significance from highlighted means.

## D. Table and Figure changes (native, traceable)

| Artifact | Source/protocol snapshot | Scientific role | Required edit and target width | Editable source | Caption/callout location | Visual/scientific QA |
|---|---|---|---|---|---|---|
| Table [ID] | [dataset, method, metric, seeds, uncertainty, raw source] | [decisive comparison] | [group/split/transpose/one- or two-column variant] | [TeX or renderer] | [section] | [all cells, units, legibility, ranking] |
| Figure [ID] | [data/code or method-diagram specification] | [proof/visual explanation] | [replot/reflow panel grid; not mechanical scaling] | [vector/plot code] | [section] | [readable final size, labels, true data] |

Do not replace measurement with generated art. For new conceptual diagrams, author-verified editable structure comes before aesthetics.

## E. Writing and layout plan

- **Result and method dependencies:** [paragraphs derived from verified tables/figures]
- **Framing changes:** [abstract/introduction/related work/conclusion only when supported]
- **Discipline-specific checks:** [field-relevant study design, reporting guidelines and required ethical/data declarations; source links]
- **Template conversion:** [old/new column widths, reference/anonymity/bibliography and official style guards]
- **Page-count strategy:** [counted pages vs total; restructure before shrinking]
- **No-go changes:** [negative spacing hacks, deletion of strong baselines, fabricated new results]

## F. Execute and invalidate downstream

| Changed input | Downstream affected source | Stale evidence/QA to rerun |
|---|---|---|
| [result, hypothesis, venue style, figure or text] | [specific file/section] | [tables → plots → prose → compile → semantic/style/visual audits] |

Run the existing DAG only for relevant changed paths. A new evidence version invalidates any dependent previous approval. Preserve before/after source diff; do not let unrelated edits hide inside a format fix.

## G. Build, inspect, release

- **Build command and environment:** [actual recipe; shell escape disabled if practical]
- **Build status / citations/references:** [pass/fail/blocked plus log path; never inferred]
- **Semantic audit:** [numeric and claim/evidence/citation consistency, status and reviewer]
- **Style audit:** [official template hashes, captions/fonts/margins and source/runtime drift]
- **Visual audit:** [final compiled PDF hash, all inspected page numbers, clipped labels/tables/floats, unresolved findings]
- **Source ZIP:** [allowlisted files and clean extraction/rebuild, status]
- **Release status:** [blocked / ready for Author approval / author-approved; not automatically submitted]
- **Unresolved issues:** [specific blockers, assumptions and owner]

**Author approval:** [decision after reviewing the actual final PDF, source and venue obligations]. A successful compile alone is not proof of scientific or visual quality.
