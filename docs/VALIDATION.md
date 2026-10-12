# Validation record — v0.1.0

Date: 2026-10-12. Environment: Python 3.13.5, PyMuPDF 1.26.7, latexmk/TeX Live with article, booktabs, graphicx, tikz and flafter. All numbers in test fixtures are explicitly synthetic software-test values, not research results.

## What was executed

`python -m unittest discover -s tests -v` completed with **37 tests, zero failures/errors**. Tests cover DAG ordering/cycles/unknown dependencies and change propagation; table layout variants, ranking updates, protocol groups, missingness, nonfinite values, provenance and uncertainty metadata; physical main-page accounting, stale/incomplete/malformed visual receipts and log detection; allowlisted archives, internal-path exclusion, traversal, symlink escapes and font exclusion.

Tests were written before the helper implementations. The initial missing-implementation run failed. A later boundary run exposed malformed visual page lists and missing/invalid cell fields; those failures were reproduced and repaired. This is deterministic helper testing, not independent agent behavior evaluation.

`python tests/build_layout_fixtures.py` completed for both one-column and two-column article modes. Each final fixture produced four PDF pages: two body pages, one deliberately separate reference page and one deliberately separate appendix page. The script rendered every page using PyMuPDF. Both allowlisted source ZIPs were extracted into separate clean directories and successfully rebuilt without depending on the original workspace.

The final logs had no findings from the implemented error/overfull/undefined-reference/oversized-float/rerun checks. A contact-sheet visual inspection of earlier candidates exposed premature float placement and an isolated sparse float page despite successful compilation. The fixture was revised with permitted article-fixture float handling and an earlier full-width-table callout; then rebuilt. This change is specific to the test fixture, not a universal recommendation to add packages to conference templates. Sparse reference/appendix pages are intentional counting fixtures, not an aesthetic target.

The PDF preflight was executed against both final fixtures. It correctly reported a two-page main range within a two-page test budget while retaining total_pages=4. It also deliberately refused to declare ready_for_author_review because an official target policy and a final all-page approval receipt were not supplied. No fake venue approval was used to force a green result.

All relative links from the skill entry point resolve. The uploaded helper blobs, test suite, fixture and skill/reference files were compared against the locally tested files using Git blob hashes. A whitespace-only fixture-script difference was reconciled and the full suite/build rerun before final publication.

## What this does NOT establish

- It is not a test of actual ICML, ICLR or other official year/track/stage templates.
- It is not a measured improvement in review resolution, writing quality, aesthetics or acceptance rate.
- It does not prove an arbitrary host agent follows the written skill under pressure.
- It does not establish the truth of user-supplied numerical sources or scientific claims.
- The PDF helper cannot reliably assess raster-label sizes, visual semantics, exact margins or all float/callout relationships. Those remain explicit visual/venue audits.
- No real manuscript, reviews, private experimental evidence or font files were published.

## Recommended subsequent validation

Run real authorized retargeting cases with original templates and data. Compare a strong simple prompt against this skill under equal resources. Check evidence preservation, actual counted pages, minimum readable asset text, final-PDF defects, numeric consistency and rework cost. Evaluate agent compliance separately from helper unit tests. Do not use accepted/rejected status alone as causal proof of skill effectiveness.
