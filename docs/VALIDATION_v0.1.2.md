# v0.1.2 validation — LaTeX-native integration

Date: 2026-10-12. The unchanged v0.1.1 skill files came from the supplied skill ZIP.
The two previous test files were retrieved from commit
`4435a3045eb93ae4fcac28e68263ea1f9b2f143d`; their Git blob hashes were verified as
`46043c6073c7b95fc4f5237a9362965e8ffb7761` and
`56f0b2806f031bb58a05bf1969f836745b4da354` before running them.

## Executed tests

The new suite was written first. Its initial run had 27 expected failures because
the two helpers and local route did not yet exist. After implementation,
`python -m unittest discover -s tests -v` ran **96 tests with zero failures/errors**:
69 unchanged tests and 27 new tests. This is helper testing, not fresh-agent
behavior evaluation.

New coverage includes protected template changes, unrelated edits, deletions,
explicit new-file tracking, path/symlink escape rejection, malformed baselines,
read-only audit behavior, source-snapshot hashes, local DAG/CLI selection,
changed/added/removed/resized physical PDF pages, metadata-only changes, invalid
DPI, non-overwriting render output and preservation of PDF inputs.

`python tests/check_latex_native.py --out build/native-02` executed four real
latexmk/pdfLaTeX builds: before and after in both article column modes. Shell
escape and rc loading were disabled for these plain fixtures. The same words and
main source were used, with only `note.tex` changed to scope its local font and
paragraph-spacing declarations. Candidate body fontsize returned to 10, with
normal paragraph skip. Official-format files were not involved; a test-only
protected style stood in for hash protection.

The single-column fixture changed from three physical pages to two, and the
comparison reported pages 1, 2 and removed page 3. The two-column fixture remained
two pages, both reported changed. This is evidence of the deliberately injected
scope-leak fix, not a general page-saving claim. A separate unrelated edit to
`main.tex` was correctly rejected by the scope check and then restored.

All before/after physical pages were rendered at 120 DPI. The four final candidate
page images and representative baseline images were visually inspected. They
show the intended local note remaining small while subsequent body text regains
normal type. Deliberate section/page boundaries and sparse test regions are
fixture design, not an aesthetic target or an instruction to force breaks in a
conference paper. An earlier fixture was improved by ending the preceding
paragraph explicitly and extending text to exercise column reflow; production
helpers were unchanged by that fixture correction.

## Scope of conclusions

- No actual ICML/ICLR year/track kit or real manuscript was used in this run.
- No acceptance, aesthetics, scientific correctness or agent-compliance advantage
  was measured.
- The source helper covers the explicit monitored list only; it is not a full
  dependency discoverer, intra-file scope checker or semantic diff.
- PDF differences compare physical indices and pixels, not semantic page identity.
  Equal pixels do not audit links, metadata, fonts or evidence validity.
- Build receipts in the test record actual commands and hashes; the new helpers
  do not themselves execute or certify an arbitrary user's build.
- No third-party script was copied or executed. No real user papers, private
  reviews, font files or credentials are included in publication.

The source package retains the existing skill references and adds a native-edit
reference, two small checkers and a local DAG. It is self-contained; optional
PyMuPDF is needed for PDF rendering, and a host-provided TeX engine for compilation.
