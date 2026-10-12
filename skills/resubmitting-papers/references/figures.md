# Redraw for the target, not for a zoomed preview

Classify each asset before editing: quantitative plot, method/pipeline diagram, qualitative evidence panel or conceptual illustration. Record its claim, locked facts, source data/code, semantic encodings, final width, maximum useful height, smallest text, caption and first callout.

## Production routes

Quantitative plots: regenerate with deterministic plotting code from verified data. Recompute encodings and annotations; preserve metric units, aggregation, uncertainty and comparison conditions. Do not infer per-example data, distributions, confidence intervals or significance from aggregate means. A generative image tool must not render measured evidence.

Method diagrams: redraw as editable SVG/PDF or a vector source such as TikZ/Graphviz/Figma with real text objects and independently editable nodes/arrows. Preserve module identities, mathematical symbols, branches, loops, inputs/outputs and training versus inference semantics. Reflow a horizontal pipeline into a compact multi-row or vertical design when column width demands it; check that the new reading path has not changed execution order. Feedback arrows in a scientific method are fine; only the revision dependency graph must be acyclic.

Qualitative evidence: compose actual examples deterministically. Preserve IDs, alignment, cropping rules, scale, selection criteria and failures. Do not replace observations with generated examples.

Conceptual art: generated art may be used only for non-measured illustration when appropriate and clearly identified. No invented scientific labels, curves, tables or evidence.

## Final-width variants

Measure the target class's `textwidth`, `columnwidth` and local `linewidth`; do not assume all two-column conferences have the same dimensions. Convert TeX pt to physical size correctly: 72.27 TeX pt per inch, 72 PDF bp per inch. Generate figure canvas dimensions at intended physical size. If scaling by s, all source text is scaled by s too; a nominal source 9 pt label may become unreadable.

Useful variants: single-column compact / full-width detailed. Vary panel grids, legend placement, direct labels, line breaks, information hierarchy and caption split, not just export resolution. Use common symbols, fonts, colors and units across figures. No color-only distinction; check grayscale. Match the manuscript visual language without redistributing font files.

For a new key Figure 1, compare a small number of genuinely different layouts before selecting one. For an unchanged figure that already fits, reuse it and recheck final size. This intentionally adapts Autopilot's full three-candidate design process rather than forcing three designs for every mechanical resize.

## Output and QA

Keep data/spec/plotting or vector source, editable export, paper PDF and raster preview, with input and output hashes. Export vector text/lines for plots where practical. Inspect the figure inside the compiled paper at 100%/physical size, not only as a standalone enlarged SVG. Check labels, caption, clipping, panel order, legends, error bars, cropped axis origins, line weights and correspondence with the results table.

If only a raster image exists, never pretend exact underlying data are recovered. Preserve evidence, redesign surrounding layout, request original assets only when indispensable, or label the blocked redraw. Decorative polishing cannot change semantic structure.
