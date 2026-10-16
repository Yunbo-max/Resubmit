# Template migration, page control and visual quality

## Freeze the target contract first

Identify exact venue, year, track and stage. Verify official instructions and archive their source/access date; record conflicting rules. Protect official class/style files with checksums. Begin from the clean target template and migrate semantic content into it, instead of importing the entire old preamble and replacing one package name.

Record engine, column modes (including appendix), paper size, text/column widths, spacing, fonts, permitted float variants, bibliography style, anonymity, required sections and what counts toward the page limit. An 8-page main-paper limit is not an 8-page PDF limit. References/appendix/ethics/checklists can have different counting rules. Do not assume older conference-year rules apply.

The bundled profile is provisional; no official template or venue rules are bundled. The article examples test mechanics only. On a template change, recompile a representative difficult table and figure before doing the entire prose rewrite.

Use `assets/layout-probe.tex` in a working copy to log dimensions without redefining them. Treat extracted source lengths as preliminary; verify the compiled asset bounds. Avoid mixing TeX pt and PDF bp.

## Spacing and style ownership

Before optimizing pagination, run the [LaTeX style procedure](latex-format.md). Compile a clean-kit baseline and separate official defaults from imported preamble overrides, local declarations, flexible page glue and asset whitespace. After assembly, audit same-role elements and runtime probes; identical nominal lengths do not guarantee identical rendered gaps. Never standardize intentional venue differences into one universal spacing.

## Two levels of budgeting

Before drafting: a soft section/asset budget based on scientific duties. Allocate room for title/abstract, required declarations, caption notes, references if counted and float overhead. Protect decisive evidence and essential assumptions; do not impose universal section lengths.

After compiling: measure actual physical pages and asset positions. Record for every important object its width/span, height, caption height, smallest text, first callout, actual page and any overflow. `qa.py` reports total PDF pages and uses explicit verified main-page boundaries; unknown boundaries remain unknown.

The target may include an author-preferred page count below the hard maximum. Treat that as an editorial goal, never an excuse for filler or hiding evidence. A shorter coherent paper is better than padding to the ceiling.

## Repair order when the paper is too long

First fix accidental layout waste: oversized whitespace, unsuitable aspect ratios, unnecessarily wide column headers, repeated legends, bad float ordering and redundant caption prose. Then restructure assets: grouped native tables, shared axes where scientifically valid, compact panel grids, sensible one/two-column spans and first-callout placement.

Next tighten repeated writing while preserving settings, qualifiers, citations and negative evidence. Reallocate main/appendix only when permitted and only when the main paper remains independently sufficient for its headline claims. Broad scientific scope changes require author-level decisions, not hidden typographical edits.

Never alter official margins, body font, line spacing, style files, baseline stretch or use negative `vspace`/`enlargethispage` as hidden page-limit evasion. Local formatting is allowed only where venue rules allow it. A table that fits only with unreadable text does not fit.

## One column versus two

Single → double: a wide table may need grouped headers, panel split or `table*`; a horizontal figure may need topology-aware reflow, a new panel grid or full-width placement. Equations may require legitimate aligned line breaks with unchanged math. Local `linewidth` rather than blindly using `textwidth` matters inside columns and minipages.

Double → single: do not enlarge every narrow figure to the whole page. Keep a justified compact width, combine related panels only if they answer the same question, and use the additional width to improve labels/headers rather than expanding whitespace. Revisit paragraph rhythm, caption length, equation breaks and float heights. Full-width floats do not have identical behavior in every class; compile the exact target.

Main → appendix: check the appendix's own column mode, numbering, allowed content and limits. Do not hide the only strong baseline or main mechanism evidence there. Keep cross-reference links and core qualifications in the main paper.

## Beauty as a constrained review, not a score to game

Hard failures: clipped/colliding text, unreadable labels, wrong figure/table values, broken math, style tampering, missing material evidence, over-limit counted pages, stale citations or invalid anonymity.

Soft objectives: clear hierarchy, consistent typography, balanced whitespace, readable density, aligned tables, restrained semantic color, captions near objects, logical reading order and proximity to first substantive callouts. Sparse pages are not automatically bad; dense pages are not automatically good. Do not maximize ink coverage or a made-up aesthetic score.

Use inspect → diagnose → one bounded repair → compile → inspect. Preserve the prior valid candidate. If repeated repairs only trade one defect for another, stop and expose the trade-off and remaining blocker. Resume on new evidence, assets or an author scope decision, not endlessly.

## Versioned visual review

Inspect all pages after the first assembled target draft and the final release. After a local change, inspect affected pages and propagated float pages; final approval must cover every page of the exact PDF hash. Saved approval for an earlier PDF cannot approve a later PDF. Preview contact sheets help navigation but do not replace checking dense tables and figures at readable resolution.


## Journal manuscript source and layout

Check the journal **author guide, accepted article type, publisher
source-file requirements and current revision stage**. Some journals
accept initial PDF/Word/LaTeX formats flexibly; others prescribe style,
structured abstract, manuscript length, figure/table file formats,
references, ethics forms, graphical abstract, OA licensing or cover letter.
Do not assume a conference two-column template or impose an article
class on a journal whose author instructions differ.

For regular journal vs Special Issue, the scientific evaluation and
styling requirements may be shared, while the CFP and permitted article
type/deadline differ. Preserve manuscript metadata and journal title/ISSN.
Do not conflate the publisher's page-charge/APC conditions with deadline
constraints. A journal source package can require original editable
figures and separate table files. Protect approved core claims and actual
data during reformatting.
