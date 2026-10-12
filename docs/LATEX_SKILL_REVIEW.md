# AI-conference LaTeX skill review and v0.1.1 validation

## Selection (inspected 2026-10-12)

| Source | What was inspected | Adopt | Do not import unchanged |
|---|---|---|---|
| Orchestra-Research/AI-Research-SKILLs | ml-paper-writing/SKILL.md; blob 2090941c1d1e6b619e5ab32147741546c8dbdb09 | AI-conference writing, clean-template compile, migrate content instead of merging preambles | Static year/page-limit examples as current rules |
| bystander563/paper-compile-layout-qa | SKILL.md, blob 0a79bea6900e849fb240c7983aa5ddcd6bb90a0e; spacing playbook, blob 4246af975266f90a162aebd7a5c19a3ab938278e | Exact author-kit contract, classify source/glue/float/asset defects, bounded repair and changed-page review | Local numeric skips, forced breaks or table scaling as universal fixes |
| flonat/flonat-research | latex-template/SKILL.md, blob 33a1bb02842444c13f1e564cbc5c3a9436249eed | Semantic comparison of packages/options/macros, distinguish legitimate differences from conflicts | Its working-paper reference, default package set or numeric quality score as a conference authority |
| flonat/flonat-research | latex-polish/SKILL.md, blob a7b0391463f685ee8db1dd41be16a47bcd590512; source-pathologies.md, blob 469b774166c7cf45b6dcaaa9e4ed685bd882dcf1 | Source diagnostics plus rendered title/body/asset/bibliography checks | Eight-page cap as final all-page approval; general titlesec/parskip/setspace remedies |

Canonical source links and adaptation details are in
[the self-contained LaTeX reference](../skills/resubmitting-papers/references/latex-format.md).
No third-party runtime code was copied or installed. This is a source-level
comparison, not a head-to-head effectiveness benchmark. Upstream packages and
skills may need host-specific dependencies; availability of a SKILL.md is not proof
that its tools run in the current host.

## Scope of this update

Add `style_baseline` before blueprint work and `style_audit` before release. The
source scanner and runtime probe comparator are read-only diagnostics. Their
findings never automatically become a compliance failure or an approval. No new
universal heading, caption, font or spacing style is imposed.

This is an incremental extension of the user's authorized resubmission workflow,
not a replacement research controller. Existing experiments and manuscript data
are untouched. Source scanning requires an explicit active-file list and does not
expand TeX macros. Parameter comparison requires equivalent contexts and matching
toolchains; it cannot measure page-building glue or establish actual beauty.

## Executed checks for v0.1.1

- Original 37 helper tests were restored from the GitHub snapshot and checked
  against Git blob 46043c6073c7b95fc4f5237a9362965e8ffb7761 before rerunning.
- Thirty new diagnostics tests were run first without implementation: all failed
  on the missing module. After implementation they passed.
- Two new DAG dependency tests failed before changing the graph and passed after
  adding the baseline/audit dependencies.
- The full deterministic suite then ran: **69 tests, zero failures/errors**.
- `python tests/check_style_probe.py` compiled six generic article cases:
  reference / scoped change / leaked change, each in one and two columns.
  Reference self-comparison produced no parameter difference; scoped changes were
  confined to the local block; leaked changes remained visible after the block.
- All six PDFs were rendered. One leaked two-column page was visually inspected
  as a spot check. This is NOT all-page aesthetic approval of real manuscripts.

These are software tests with synthetic prose and deliberately introduced format
differences. They do not establish ICML/ICLR official-template compatibility,
automatic style repair, arbitrary agent compliance or improved acceptance rate.
The original table-layout smoke script was not rerun for this diagnostics-only
update; its earlier record remains in docs/VALIDATION.md.

Commands:

```bash
python -m unittest discover -s tests -v
python tests/check_style_probe.py
python skills/resubmitting-papers/scripts/workflow.py --changed style_baseline
```

No real paper, review text, private result, font file, or secret is published.
