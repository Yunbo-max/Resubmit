# Dependency-first revision

## Why the join happens early

Target geometry must be known before choosing table orientation, panel grids, line lengths and space allocation. Evidence must be reconciled before selecting what the table, plot, caption or abstract claims. These inputs are independent and can be collected in parallel. Long-form writing starts only after the evidence and asset design are stable enough to reference.

The first layout blueprint is provisional, not a final page count. Early representative table/figure probes can expose an impossible design before the full rewrite. Final pagination is determined by the compiled target PDF, never by source word count alone.

## DAG contracts

| Node | Input | Output / exit condition |
|---|---|---|
| intake | authorized project and target | immutable baseline; file inventory; missing inputs |
| venue | exact venue/year/track/stage | verified policy links and template checksums; measured geometry; counted/excluded sections |
| evidence | old paper, review history, actual artifacts | atomic concerns and source locators; disagreements and unfulfilled rebuttal promises |
| results | reconciled evidence | versioned numeric snapshot; comparable protocol groups; no silent overwrite |
| blueprint | venue + results | supported thesis; section duties; essential evidence; asset roles; initial space budget |
| tables | blueprint + results + geometry | native table variants, captions, provenance; updated rankings/deltas |
| figures | blueprint + results + geometry | regenerable plots/editable diagrams, final-width variants, captions |
| body | tables + figures + blueprint | evidence-led results/method sections; appendix allocation |
| framing | body | synchronized introduction, related positioning, abstract/title, limitations/conclusion |
| assemble | prose + assets + official template | target source tree; stable labels; first-callout placement |
| compile | assembled source | PDF + log + source/asset hashes; converged references |
| semantic_audit | compiled PDF + result snapshot | every important number/claim/caption reconciled; cited claims verified |
| visual_audit | compiled PDF + venue contract | every physical page reviewed; real page count; final-size readability |
| release | both audits at same revision | clean PDF + source ZIP + private change report |

A node need not produce a separate file. Use one private `revision-state.json`; keep immutable evidence and generated artifacts separately. Helpers produce derived reports, not competing sources of truth.

## Minimal state

Record revision ID, baseline commit/hash, target contract, result snapshot hash, node status, input/output hashes, changed objects, unresolved blockers, layout measurements and the last inspected PDF hash. Allowed statuses: `pending`, `ready`, `running`, `done`, `stale`, `blocked`, `not-required`. `not-required` needs a reason and must never bypass a mandatory audit. `done` requires evidence of the node's exit condition.

A written reply, scientific resolution, manuscript implementation and visual approval are separate facts. Preserve rebuttal promises until real artifacts fulfill them. No reviewer reply is not reviewer agreement.

## Changes and rework

Each pass is a DAG. A change creates revision k+1 and invalidates affected descendants; never claim a graph with feedback edges is a DAG. The bundled helper conservatively plans at stage level. Object-level pruning is an agent responsibility and needs recorded unchanged inputs.

| Change | Revisit |
|---|---|
| Result / protocol / uncertainty | tables, dependent plots, numerical prose, captions, abstract, compile, both audits |
| Added baseline | comparable groups, winners/deltas, width, asset variants, claims and both audits |
| Target template / column width | blueprint space plan, table and figure layout, assembly, compile, visual audit; prose if moved or shortened |
| Plot composition only | figure + caption consistency, assembly, compile, visual audit; semantic check on mappings |
| Claim narrowed | all occurrences, relevant evidence placement, assembly and both audits |
| Spelling fix | affected paragraph + compile + changed pages; reuse other evidence checks only if meaning and hashes permit |

Parallelize evidence/venue intake and independent assets when tools permit. Use a single writer for shared manuscript files. Do not claim parallel execution without actual workers. Cache verified outputs; never infer that cached rendered pages still match a changed PDF.

## Three implementation choices

A late-stage formatter is too late to repair asset topology. A giant research controller duplicates Autopilot. The chosen architecture is one lightweight orchestrator plus specialist contracts and deterministic checks. Only hand back to research when a real scientific gap cannot be resolved from available evidence; a formatting issue never triggers a full idea-generation loop.
