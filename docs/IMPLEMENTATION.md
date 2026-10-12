# Layout-aware resubmission implementation plan

Goal: deliver a reusable skill and small, testable tools for evidence-preserving cross-conference conversion, with tables and figures first and final-PDF verification.
Architecture: one user-facing skill; a per-revision DAG; specialist references loaded on demand; deterministic helpers for dependencies, tables and PDF checks. No autonomous research service.
Stack: Python 3.10+ standard library, optional PyMuPDF for PDF QA; TeX Live and latexmk for fixture compilation.
Spec: docs/DESIGN.md.

## Constraints

Do not publish manuscripts/reviews. Do not alter venue class/style files. Do not invent research numbers. Test-fixture numbers are clearly synthetic and stay in tests. User authorized updating the new repository. No independent agent evaluation is available; report deterministic tests separately from behavioral effectiveness.

## Completed tasks

- [x] Write failing regression tests for DAG invalidation, table provenance/ranking/missingness, physical page accounting, stale visual approval and safe packaging.
- [x] Implement minimal helpers inside the installable skill directory.
- [x] Write the DAG, six operating stages, Autopilot writing adaptation, native table and redraw contracts, layout loop and publication boundaries.
- [x] Compile both one- and two-column article fixtures; inspect rendered page contact sheets and repair observed float-placement issues. These are not official venue templates.
- [x] Run all tests and document actual results; prepare publication of only skill infrastructure and synthetic fixtures.

## Review focus

1. Missing values never become zeros or winners; incompatible protocols cannot share rankings.
2. Boundary-unknown PDFs cannot pass a main-page limit by total-page guessing.
3. Changed PDF bytes invalidate old visual approvals.
4. Wide tables are restructured, not silently shrunk; typography warnings need review.
5. The public skill repository and anonymous submission package exclude private reviews and internal notes.

## Implementation rulings

The user explicitly requested redesign and repository update, so this turn delivered the integrated design and implementation without an additional approval cycle. The repository was empty; initialization preserved all subsequently created content. Research Autopilot principles were adapted into self-contained new references rather than copying the whole upstream controller. Full source publication uses GitHub's connector and a non-forced branch update with an expected-head check.
