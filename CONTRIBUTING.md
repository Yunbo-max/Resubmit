# Contributing to ReSubmit

Useful contributions include reproducible LaTeX failures, focused helper improvements, exact-year author-kit checks, accessible examples and clearer operating contracts. Discuss broad controller changes in an issue before adding another mandatory stage.

Use English for public documentation and user-facing tool messages. Keep one self-contained skill directory and preserve its existing identifier. Minimize runtime dependencies. Keep rule-based checks in small testable helpers; use the skill for judgments that cannot be settled by a regular expression.

## Before opening a pull request

Create a focused branch. Add a regression test that fails on the reported behavior, implement the smallest fix, and run `python -m unittest discover -s tests -v`. For visual/layout changes, compile the relevant fixtures, render before and after at the same DPI, and inspect affected pages and neighbors. A successful build is not visual approval. Explain any skipped test and its missing dependency.

Website changes should pass `node --check site/app.js`, the public distribution tests, a local demo rebuild, and desktop/mobile keyboard and overflow checks. Do not add trackers, external fonts, a manuscript upload endpoint, unsupported compatibility badges or invented usage metrics.

## Evidence and privacy

Use minimal synthetic reproductions by default and label them. Do not post unpublished papers, confidential reviews, author identities, private paths, credentials, font files or restricted author-kit assets. For an official template test, record the venue, year, track, stage and official source, and verify redistribution permission first. Never edit the official style to force a fixture to fit.

## Review checklist

Does the change preserve scientific meaning and negative results? Does it keep local edits local? Are outputs and failure states honest? Are source/asset hashes and page checks current? Does documentation distinguish implemented behavior from proposed work? Retain copyright and attribution notices for any permitted reuse.

Be constructive and respectful. Critique behavior and evidence, not contributors. Maintainers may remove abusive or privacy-violating content.
