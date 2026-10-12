# LaTeX spacing and style: diagnose before normalizing

Use this module when the PDF compiles but paragraph gaps, captions, headings,
list/equation spacing, table typography or bibliography style differ unexpectedly.
A new template changes the reference style; the old paper is not the authority.
This reference is a diagnosis procedure, not a universal set of spacing constants.

## Two workflow gates

`style_baseline` runs after the exact venue contract and before the blueprint.
Compile the untouched target kit, preserve its style hashes, engine/package
versions and representative rendered examples. Review the migration's active
preamble, included author-owned files and any generator. Make a difference ledger:
source location, setting, scope, controlling layer, target default, reason,
proposed action and verification. Classify as preserve / restore target default /
permitted local exception / unresolved. Never remove scientific macros blindly.

`style_audit` runs on the compiled candidate before release, alongside scientific
and visual checks. Reconcile the source ledger, measured parameters, same-role
rendered elements and changed pages. A corrected source invalidates compilation
and downstream approvals in the next revision. Do not declare the node done from
a regex report or parameter match alone.

## Diagnose the owning layer

| Symptom | Inspect before changing anything |
|---|---|
| Same-level headings differ | Target heading macros; `titlesec`/`sectsty` overrides; font scope; surrounding floats, lists and flexible glue |
| Paragraph gaps or indents differ | `parskip`, `parindent`, `baselinestretch`, `setspace`; empty paragraph boundaries; grouped declarations; page-building stretch |
| Caption font, label or gap differs | Kit caption hooks; `caption`/subcaption packages and options; global/local `captionsetup`; short versus multi-line caption behavior |
| Equation gaps/leading differ | Display versus short-display skips, preceding line length, `jot`, `align`/`aligned`, local fonts and unbreakable math blocks |
| List spacing differs | `topsep`, `partopsep`, `itemsep`, `parsep`, list depth, blank line before list, optional list settings |
| Tables differ after a rebuttal update | Generator defaults, locally scoped `arraystretch`/`tabcolsep`, row struts, `p` versus `m` columns, uncertainty text and caption settings |
| Figure has a large gap | Float-to-text glue versus whitespace INSIDE the asset; bounding box/crop; `center` environment versus scoped `centering`; queued floats |
| One page has a large blank band | Unbreakable boxes, `[H]`, barriers, forced breaks and stretched glue; not just source blank lines |
| Bibliography looks different | Exact `.bst`, natbib/biblatex system/options, entry spacing/indent, font scope and citation commands |
| Body or math font changes later | Font packages/engine, local `small`/`fontsize`/`selectfont`, group boundaries and paragraph end; intended math/text roles |

A package name is not proof of a conflict. Check who loads it, with which options,
when, and whether the target kit expects it. Changing package order blindly can
create another problem. An unchanged official `.sty` does not establish compliant
output if an author macro overrides the same setting later.

## Safe repair order

1. Restore the verified target kit and mode; isolate necessary scientific macros
   from old geometry, caption, heading, font and bibliography overrides.
2. Resolve actual duplicate-option/definition conflicts and unintended scope
   leakage. Modify the generator if it owns the affected TeX.
3. Inspect rendered evidence to distinguish nominal spacing from page-building
   stretch, forced float/break behavior, and internal asset whitespace.
4. Repair the responsible structure or permitted local setting with a bounded
   diff. Preserve intended paragraph breaks and mathematical meaning.
5. Rebuild with the same toolchain; inspect the target, every changed page and
   affected neighbors. Only then continue page-budget optimization.

Do not globally introduce `titlesec`, `parskip`, `setspace`, `raggedbottom` or new
font packages to make one page look better. Do not copy numerical skips from a
working-paper/thesis example into a conference paper. A `vfill/newpage` recipe,
negative spacing, table scaling or landscape page is never a generic fix.
Content compression or appendix relocation needs the manuscript revision scope.

## Consistency is contextual, not identical pixels

Compare like with like under the official rules. The first paragraph after a
heading may intentionally differ from later paragraphs. Short and multi-line
captions can have different alignment; main text and appendix may use different
modes; mathematical and text fonts have different roles. Equal nominal skip
values can render differently when the page builder stretches glue. Restoring all
gaps to one number is not the goal. Ordinary-page bottom alignment is distinct
from last-page column balancing; preserve the exact kit's behavior.

## Read-only helper

From the installed skill directory:

```bash
python scripts/latex_format.py scan /path/to/paper \
  --files main.tex sections/results.tex author-macros.sty --out /tmp/source-style.json
python scripts/latex_format.py compare \
  --reference /tmp/target-baseline/main.log \
  --candidate /tmp/revision/main.log --out /tmp/style-drift.json
```

The scanner reports command sites, common style packages and repeated package
loads across the EXPLICIT file list. It masks ordinary comments and common
verbatim forms; it does not expand TeX, interpret conditionals, automatically
follow inputs or reconstruct runtime load order. Findings mean review required,
not noncompliance. It never rewrites input files.

For runtime comparisons, load `assets/latex-style-probe.tex` in WORKING COPIES of
the reference and candidate, then call `\ResubmitStyleProbe{unique-context}` at
equivalent sites: body, inside the relevant environment and after it. Use matching
engine/package versions and record any permitted extra packages. The probe logs
font attributes and nominal dimensions/skips without assigning new style lengths.
Missing contexts/fields cannot pass, and malformed or truncated probes are errors.
A reused context name is rejected; use unique labels. Remove debug calls from the
clean submission package.

The comparator detects literal parameter drift after whitespace normalization,
not physical gaps, font embedding, caption text/label styles or heading macro
semantics. Neither tool certifies compliance. Integrate its findings with final
PDF inspection and official rules, not with a made-up universal style score.

## Sources and selective adaptation

Inspected 2026-10-12; newly written procedure/tools, no vendored upstream code.

- Orchestra `ml-paper-writing`: AI-conference writing and content-only template migration.
  https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/main/20-ml-paper-writing/ml-paper-writing/SKILL.md
- `paper-compile-layout-qa`: exact-kit contract, defect classification and bounded visual repair.
  https://github.com/bystander563/paper-compile-layout-qa/blob/main/SKILL.md
  https://github.com/bystander563/paper-compile-layout-qa/blob/main/references/latex-spacing-playbook.md
- flonat `latex-template`: compare semantic preamble blocks and classify differences;
  DO NOT substitute its working-paper template or scoring rules for the official kit.
  https://github.com/flonat/flonat-research/blob/main/skills/latex-template/SKILL.md
- flonat `latex-polish` and source catalogue: source signals plus rendered inspection;
  DO NOT import generic heading/spacing package remedies, an eight-page final
  inspection cap, or grep findings as proof of a defect.
  https://github.com/flonat/flonat-research/blob/main/skills/latex-polish/SKILL.md
  https://github.com/flonat/flonat-research/blob/main/skills/latex/references/source-pathologies.md
