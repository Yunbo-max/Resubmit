# LaTeX-native editing

## What changed in v0.1.2

v0.1.1 introduced format scanning and runtime style probes, but the entry point still encouraged a full-paper retargeting workflow. v0.1.2 made existing TeX the default: distinguish local edits, format-only repairs, rebuttal result updates, template migration and full rewrites. A local fix does not require new research, replacement of every asset or rewriting the introduction and abstract.

The skill remains `resubmitting-papers`. It includes the native-editing reference, a local DAG, source-scope checks and before/after PDF comparison. Existing table, figure, writing, layout and quality modules are reused without requiring an external plugin.

## Default order

Freeze source and scope → verify/reuse target constraints → build the baseline → inspect the PDF or record the build error → diagnose the owning layer → make the smallest source change → rebuild → check source, pages, meaning and style → inspect changed and neighboring pages → final all-page review.

Each revision is a DAG. A missing baseline PDF permits log-based debugging but not a claimed image comparison. The final candidate still has to be compiled and inspected.

## Adaptation, not wholesale import

The main external influence is `bystander563/paper-compile-layout-qa`: exact author-kit contracts, render-first diagnosis, owning-layer fixes and changed-page review. Research Autopilot supplies the evidence and writing principles. No third-party runtime source was copied, and no compatibility with the upstream `conference_format_audit.py` interface is claimed.

Do not inherit global heading or paragraph resets, universal skip constants, an eight-page cap for final inspection, or the assumption that every changed pixel is a defect.

## Tool boundaries

`revision_check.py` hashes explicitly monitored files and flags protected or out-of-scope changes. It does not discover every input or establish that changes within one allowed file stayed inside the requested paragraph; inspect the source diff and new files too.

`pdf_revision_diff.py` compares physical pages at matching DPI using PyMuPDF, reports additions/deletions, size and pixel changes, and identifies neighboring pages to inspect. It does not semantically align pages, assess beauty or certify metadata and links.

The host supplies the compiler and permission model. The skill does not install that environment, run indefinitely or submit papers.

Sources: [compile-layout skill](https://github.com/bystander563/paper-compile-layout-qa/blob/main/SKILL.md), [spacing playbook](https://github.com/bystander563/paper-compile-layout-qa/blob/main/references/latex-spacing-playbook.md), [Autopilot writing](https://github.com/Yunbo-max/Research_Autopilot/tree/main/skills/writing-top-tier-papers), [latexmk](https://ctan.org/pkg/latexmk), [PyMuPDF rendering](https://pymupdf.readthedocs.io/en/latest/page.html#Page.get_pixmap).

These are engineering adaptations, not claims of academic priority.
