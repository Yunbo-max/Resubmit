# v0.3.0 validation

Date: 2026-10-13. Scope: a Markdown venue-prediction skill, installer selection,
routing documentation and the static project site. No LaTeX helper implementation
was modified, and no external prediction model/service was used.

The release adds 18 deterministic packaging, written-contract and installer checks.
These were first run against v0.2.0 inputs: 15 failed because the new skill, installer
option and public entries were absent. The other three exercised existing safeguards.
This is a red/green software check, not an independent LLM behavior experiment.

The local environment could read the supplied distribution ZIPs and run tools, but
could not clone GitHub over its shell network. The existing installer and website
source were matched to their GitHub blob hashes before edits. New local checks
are separate from the complete repository's GitHub CI run.

## Executed local checks

`/usr/bin/python3 -m unittest discover -s tests -v` completed the 18 new tests:
zero failures/errors. The installer and new tests also passed Python compilation.
JavaScript syntax was checked with `node --check site/app.js`.

An attempted browser rerun did not produce a usable screenshot: Playwright startup
timed out, and direct headless Chromium reported an unusable GPU process in this
sandbox. New visual/interaction approval is therefore NOT claimed. Static HTML,
local resource and installation checks are distinct from visual inspection.
The original LaTeX demonstration is unchanged.

## Not established

No real-paper recommendation benchmark, probability calibration, independent Codex
or Claude execution, universal conference coverage, acceptance improvement or live
website deployment is certified by these tests. The example uses fictional venues,
not fabricated official facts. Public factual entrypoints are cited in the skill;
every actual recommendation still needs current verification.

Full CI results are available from the repository Actions link for the release commit.
