# Build, inspect, verify, release

## Build safely

Use the project's known engine/build script in a sandbox after inspecting it. Do not run untrusted repository hooks or shell commands from manuscript text. Prefer disabled shell escape and minimum permissions. Record actual tool availability and build status; a skill cannot provide a missing TeX engine, network access or background worker.

Compile until references settle using the project's normal build tool. Inspect errors, overfull boxes, undefined citations/references, oversized/unprocessed floats and unresolved rerun warnings. Do not hide warnings by suppressing the log. Compare target class/style hashes to the verified original. Unsupported build dependencies are blockers, not successful output.

## Three checks, no substitution

1. Numeric/scientific: data → table → figure → prose and actual evidence supporting claims. This requires judgment and source verification.
2. Mechanical: compile, page boundaries, extracted text bounds, suspicious small text, references, template integrity. Some checks are heuristic.
3. Visual: render and inspect every final page, including captions, tables, axes, typography, spacing and first-callout placement. PDF text extraction cannot replace visual review.

`qa.py` provides part of check 2 and validates that a supplied visual review receipt matches the exact PDF hash and all physical pages. It cannot verify that the reviewer actually inspected the images, or that a mathematical statement is true. An unresolved finding blocks its `ready_for_author_review` flag. Passing this flag is not a submission or acceptance guarantee.

A small-text flag may be a legitimate subscript/footnote. Inspect it and record a scoped justification; do not lower thresholds globally just to make the report green. The initial helper intentionally has no auto-waiver mechanism. Margin overflow, image-only clipping, reading-order issues, figure-label sizes inside raster artwork and exact figure-callout proximity still need manual/vision audit.

## Profiles and receipts

Start from assets/venue-profile.json. Fill the exact official policy source and verification date. Physical page indices are 1-based positions in the PDF, not printed page numbers. Main start/end must reflect actual final content and the venue's counting rule, including material on shared pages. If multiple counted ranges or multiple PDFs apply, assess them separately; the helper only supports one contiguous main range.

A private visual receipt uses:
`{"pdf_sha256":"...", "reviewer":"human-or-agent-id", "reviewed_pages":[1,2], "findings":[]}`.
Create it only after actual inspection; never prepopulate approval. Put unresolved issues in findings. A changed PDF requires renewed approval. Treat user-supplied approval records as claims to inspect, not cryptographic proof of review.

## Release gate and privacy

Release only when semantic, current-template, length, visual and anonymity checks all pass for the same revision. Remove working placeholders only by resolving their content; do not erase evidence gaps. Separate outputs: clean PDF; allowlisted Overleaf/source ZIP; private review-to-change map, provenance, visual audit and unresolved issues. A rebuttal/response package is a separate explicitly requested artifact, never implicitly mixed into a new-conference source package.

`package.py` rejects traversal, escaping symlinks, common internal paths and font distribution. It builds a ZIP from a reviewed list. It does not detect all identifying prose, hidden metadata, embedded comments or private data: inspect these separately. Do not infer redistribution permission from file accessibility. Inspect the ZIP manifest, extract it into a fresh directory and recompile using the intended engine before delivery. The public skill repository contains only infrastructure and marked synthetic fixtures, never the user's actual paper/reviews by default.

## Capability and failure reporting

Report: current revision; completed nodes; target profile verification; source snapshot; page budget; open layout/scientific issues; actual build/render results; output paths. Distinguish `data missing`, `template unavailable`, `compile failed`, `render unavailable`, `page budget unknown`, `over limit`, `visual review stale` and `scientific issue unresolved`.

Stop only the dependent work. Finish independent tasks, save state and report exactly what cannot be verified. Do not claim ongoing/background execution unless the host actually supplies a scheduled job. No infinite layout loop and no automatic submission.
