# Tables are first-class revision artifacts

## Reconcile before drawing

A rebuttal is not a numeric database. Trace each new number to an artifact, verified table, or explicitly supplied authoritative result. Preserve the old snapshot and record additions, replacements, changed protocols, missing runs and conflicts. Do not silently prefer the newest sentence over older raw evidence. Old and new results are comparable only under declared settings.

Cell identity: dataset/task + split + method/version + protocol/budget + metric + aggregation + sample unit. Store value, unit, direction, precision, uncertainty type, run count, source locator/hash and evidence status. Keep reported literature values distinct from reruns. `missing` is not zero, and `not comparable` is not `missing`.

When values change, recompute rankings, ties, mean/aggregate if justified, delta, best/second-best emphasis and every headline number. Absolute change is new minus baseline; relative change is that difference divided by baseline with units and sign stated. For percentages distinguish percentage points from relative percent. A zero baseline makes relative percentage change undefined. Do not average unlike metrics or independently reported standard errors without a justified estimator.

## Table contract

Every table has a stable ID, scientific job, source snapshot, all row/column definitions, comparable groups, units/directions, uncertainty notes, treatment of missingness, emphasis rule, caption, intended width and first callout. Preserve materially adverse results and strong baselines. Any summary-to-appendix mapping must retain the complete matrix privately and make the needed scientific evidence visible to readers.

Bold is not a significance test. Rank using unrounded comparable values; explain displayed ties or increase precision where needed. Do not infer statistical significance from the largest mean. Significance symbols require the actual test, unit, sample count and correction policy when relevant.

## Width-aware redesign order

1. Remove redundant prose from headers; move shared units/settings into caption or notes.
2. Group columns by dataset/metric and introduce explicit short labels.
3. Reorder or transpose if it improves the comparison the reader must make.
4. Split into logically complete panels/tables with clear common protocol labels.
5. Use a full-width `table*` in an allowed two-column template, or a native full-width table in one column.
6. Move secondary detail only when the main table still carries decisive comparisons and qualifications.
7. Only adjust permitted local table typography after these structural options; verify the smallest actual printed text.

Never default to `resizebox`, `scalebox`, landscape pages or `tiny`. Never solve overflow by deleting a losing row or an inconvenient uncertainty column. Changing from one to two columns is a structure problem, not a universal scaling factor. Source `linewidth` depends on the enclosing float/minipage.

## Helper

`python scripts/tables.py results.json --out paper/tables/main.tex --columns 2 --span full`

The JSON form appears in `tests/fixtures/results.json` in the repository. The renderer validates finite numbers, explicit missingness, provenance fields, protocol groups and optional sd/se metadata; recomputes best-value bolding; escapes plain text; emits all cells as a `booktabs` table and a provenance sidecar. The enclosing paper must load `booktabs`. It deliberately does not shrink content or certify fit.

Limitations: source strings are locators, not independently verified evidence. The helper does not recompute supplied statistics or derived formulas, validate citations, infer comparability, verify seed independence, implement complex multilevel tables or perform significance tests. Those require evidence audit/custom table code. Never advertise these field checks as proof that a number is correct.

For custom layouts, keep the same canonical data and tests. Do not hand-edit rendered numbers. Use full-width/column-width render variants from one snapshot and compare them in the real target template.

## End-to-end numeric audit

Match data → generated TeX → compiled PDF → plot labels → results prose → abstract/conclusion. Check signs, decimal precision, percent/percentage points, denominator, count of datasets, highlighted winners and caption qualifiers. A source change marks the whole dependent chain stale. Put source locators in the private ledger and appropriate scholarly citations in the public caption; never leak local paths into the manuscript.
