# Native LaTeX editing: the default working path

Use the existing `.tex` project as the authoritative editable source. Do not
convert it into Word/Markdown, recreate an already correct template, or rewrite
unrelated sections to fix one layout problem. Preserve the upstream research
and evidence rules; change the execution path, not the truth standard.

## Route by the requested edit

| Request | Operation and extent |
|---|---|
| Gap, font, caption, table width, equation break, float or reference fix | `latex-edit`; `layout-only` is its strict format-preserving alias |
| Change a supplied sentence, equation or algorithm | `latex-edit` with explicitly authorized content locations and before/after meaning checks |
| Add verified rebuttal results | `rebuttal-update`: reconcile evidence, regenerate dependent table/plot/prose; do not rewrite untouched parts |
| Move to another template | `retarget`: clean target kit, protected styles, mapped author macros and full-layout validation |
| Rebuild the whole argument | `full-revision`, only when actually requested or approved |
| Inspection only | `diagnose`: no source edits |

Choose the smallest applicable operation. A LaTeX editing request does not
implicitly authorize scientific redesign, title/method renaming, new experiments,
external submission, commits to another repository or public manuscript upload.

## 1. Freeze the actual source and scope

Identify build root, main file, engine, bibliography backend, generator, included
TeX, author-owned macros, figure/data sources and official kit files. Recover
known venue/year/track/stage settings rather than asking again. Reuse a verified
matching policy record; reverify only missing, conflicting or changed material
rules. A same-venue local edit does not require migrating to a new kit.

Record the specific target defect, allowed files AND allowed locations, protected
files, immutable facts and verification plan. Read adjacent source context.
Inventory from the source tree and known build dependencies (including `.fls`
when available), not just the file the user named. Inspect `git diff`/untracked
files when Git is available. Save a source snapshot before editing. Never undo
someone else's concurrent changes or overwrite the last valid PDF.

The helper `revision_check.py` hashes an EXPLICIT monitored file surface and
checks it against allowed/protected paths. It does not discover missing inputs,
parse TeX, limit locations within a file, or prove that prose is unchanged.
A protected file must already have a baseline hash; authors' mathematical
macros are not automatically official-template files.

```bash
# Paths below are illustrative: use actual paths from the project inventory.
python scripts/revision_check.py snapshot /path/to/paper \
  --files main.tex sections/results.tex macros.tex target.sty figures/plot.pdf \
  --out /path/to/private/rev-01-baseline.json
```

Use existing version control to preserve a complete baseline; the helper is an
additional focused check, not a substitute for repository history.

## 2. Build and see the baseline before diagnosing

Use the inspected project's established root, engine and build recipe. Do not
switch bibliography systems or engines merely because another tool is available.
Review custom scripts and `.latexmkrc` before executing them: they are executable
code. Compile untrusted TeX in an isolated, minimally privileged working copy;
disabling shell escape alone is not a security sandbox.

For a plain verified pdfLaTeX project without required custom build hooks, a
fallback is:

```bash
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error \
  -latexoption=-no-shell-escape main.tex
```

Do not impose this command on XeLaTeX, LuaLaTeX, Biber, custom generated assets or
an approved project-specific build. Missing dependencies are reported, not
silently bypassed. Preserve exit code, stdout/stderr, final log and expected PDF.
Do not treat an old PDF surviving a failed compile as the new output.

Store a private build receipt: revision, root, entry point, exact command,
engine/version, monitored source and asset hashes, kit hashes, log/PDF hashes,
return code and unresolved findings. These are actual observations, never
pre-filled success fields. The helpers do not create or certify this receipt.

Render the baseline at a fixed DPI. Inspect the named region and neighboring
pages; the target can be on a different PDF page from its source-file line.
If no baseline can compile, record `baseline unavailable`, diagnose from the
actual log and repair the build. Do not block all progress waiting for an
impossible baseline image, and do not later claim a visual before/after proof.

## 3. Diagnose at the owning layer

Use [latex-format.md](latex-format.md) for spacing/style ownership and
[layout.md](layout.md) for page-building decisions. Distinguish official style,
author macro/package override, declaration scope leakage, flexible page glue,
unbreakable blocks, float queues and whitespace inside an image.

Do not count source blank lines as rendered gaps. Do not make every role use the
same spacing. The first paragraph after a heading, a multi-line caption, display
math and ordinary body text can legitimately differ.

## 4. Make the smallest source-level repair

| Object | Native editing rule |
|---|---|
| Paragraphs/headings | Keep actual wording in format-only mode; repair owner/scope, not global fonts or heading skips |
| Captions/labels | Use exact kit hooks; preserve float/subfigure counters and `label` target; inspect short/multiline behavior |
| Lists | Check local depth and glue; no global compact-list reset to fix one contribution list |
| Equations | Use the appropriate aligned/split structure without changing notation, assumptions, numbering or meaning |
| Algorithms | Preserve control flow and line references; do not introduce conflicting algorithm packages or shrink all pseudocode |
| Tables | Keep native cells, units, uncertainty and baselines; isolate permitted local typography; generator owns generated TeX |
| Figures | Crop only real empty borders; preserve labels/evidence; redraw source topology only within the approved asset scope |
| Bibliography | Keep the required `.bst` and citation system; distinguish a missing key from stale build output |

An explicitly requested wording or mathematical change is allowed, but must be
recorded and scientifically checked. Format-only work cannot remove sentences,
change claims or move decisive evidence to an appendix to save space. If the
smallest sound fix requires broader scope, expose that decision rather than
quietly rewriting. Do not repair unknown macros with dummy definitions just to
make compilation green. Never modify official `.sty`/`.cls` to fit page limits.

## 5. Rebuild and compare the source AND the rendered footprint

Build with the same approved configuration. Run existing style/log/page checks.
Then check the source scope:

```bash
python scripts/revision_check.py check /path/to/paper \
  --baseline /path/to/private/rev-01-baseline.json \
  --allow sections/results.tex --protect target.sty \
  --out /path/to/private/rev-01-scope.json
```

List newly created relevant files with `--current-files`; allowed new files are
included automatically. Uninventoried files cannot be covered by a passing
report. Inspect textual/source diffs as well: changing a number inside an
allowed file can pass a file-level scope check but still violate the task.

Compare PDFs with the same renderer/DPI:

```bash
python scripts/pdf_revision_diff.py /path/to/before.pdf /path/to/after.pdf \
  --dpi 150 --render-dir /path/to/private/new-render-directory \
  --out /path/to/private/rev-01-pages.json
```

The tool renders all supplied physical pages, detects added/removed/resized or
visually changed pages and lists candidate neighboring pages for inspection.
It is not a semantic page matcher: insertion can flag all later indices. This
is conservative and expected. It never labels a changed page a defect, nor an
unchanged page scientifically correct. Equal pixels do not prove equal metadata,
links or accessibility. Reports and render directories must be new paths.

Classify each observed difference as intended local edit, necessary automatic
reflow, or unexpected regression. Inspect every changed page and affected
neighbors; do not reject unavoidable reflow solely because the user named one
page. Do reject a repair that breaks a later table, formula or bibliography.
Any meaningful change invalidates downstream approvals for the next revision.

## 6. Finish with two distinct status statements

`Local change verified` means the requested source change was contained, built
and inspected with the required evidence. `Submission-ready` additionally needs
the full target-venue, scientific, anonymity, length and all-page release gates.
Unknown venue requirements do not become certified just because a local gap was
fixed. Report the exact completed scope and every remaining blocker.

Final delivery retains the native LaTeX source, corrected PDF, clean allowlisted
source ZIP if requested, and a separate private change report. Every final page
must be inspected; iterative changed-page checks do not waive the final check.

## Integration provenance and boundary

The governing approach adapts `bystander563/paper-compile-layout-qa`: exact-kit
ownership, render-first diagnosis, smallest owning-layer fix, and before/after
containment. Also retain the author's Research Autopilot writing/evidence
contracts and the existing table/figure modules. This is a new self-contained
integration, not a vendored copy, an installed external plugin or an implementation
of the upstream provider's `conference_format_audit.py` CLI.

No arbitrary eight-page final inspection cap, default global style package,
universal spacing constant, beauty score or automatic submission is inherited.
