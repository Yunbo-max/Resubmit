# Official facts for journal and conference eligibility

## Source hierarchy

Record each material fact with its official source URL, exact supporting passage or
locator, ranking/edition version, retrieval date and any unresolved conflict.
The retrieval date must be real, not copied from an earlier report.

- CORE/ICORE: https://portal.core.edu.au/conf-ranks/ and https://www.core.edu.au/.
  Preserve the actual scheme name and released version. CORE and ICORE references
  can refer to the same ranking lineage; do not pretend their labels are CCF labels.
- CCF: https://www.ccf.org.cn/Academic_Evaluation/By_category/ and its official
  category pages/released directory. Check amendments as well as the release.
- Deadlines and eligibility: the exact conference edition's CFP, author guide,
  submission portal and track-specific instructions.
- Candidate discovery: https://github.com/ccfddl/ccf-deadlines or another maintained
  aggregator. A live MCP connection is optional, never an installation requirement.
- Community fit: official CFP and relevant recent proceedings. A few accepted papers
  are supporting examples, not a complete distribution of accepted/rejected work.

Inspection notes on 2026-10-13: the CORE website announced ICORE 2026 availability;
CCF's official directory page showed the seventh edition, published 2026-03-31 and
an erratum update dated April 9. These are source-entry notes, not a permanently
pinned latest edition. Recheck whenever the skill is used.

If the official source is inaccessible, label the fact unverified. Preserve any
aggregator claim as a lead without upgrading it to official confirmation.
Do not infer that a missing record is a confirmed "not listed" result.

## Ranking logic

Store each scheme independently: canonical venue ID/name, rank, source version,
official source, retrieval date and applicable paper/track scope.

User "CORE A or above": allowed CORE set {A*, A}. User "CORE A exactly": {A}.
CCF A, A/B or other choices are separate explicit sets. Unspecified CCF cutoff means
display CCF, not silently impose an A threshold. Rankings are user constraints,
not a measure of an individual paper's scientific worth.

If the user specifies both:
- OR: at least one selected, verified condition must pass.
- AND: every selected condition must pass.
- If the relation is unspecified, show both filtered sets or state a provisional
  interpretation; never conceal the choice.
- A failed AND component excludes the candidate even if another is unknown.
  An unknown component prevents a fully verified AND pass.
  For OR, one verified pass is sufficient, but still display other unknown ranks.

Disambiguate namesakes, renamed or merged venues and main versus satellite events.
Do not inherit a parent's rank for a workshop. CCF's seventh-edition notice covers
Full/Regular papers and explicitly excludes Short, Demo, Technical Brief, Summary,
Findings and companion Workshop papers from that directory's scope. Recheck current
scope at use time; do not silently assign the series rank to an excluded paper type.
Institutional recognition is separate and must not be guessed.

## Submission stages and dates

The conference date, edition year and submission year are different fields.
Check abstract registration, full paper, mandatory author registration, supplementary
material and any prior-review/commitment requirement. Rolling or multi-round venues
need one record per relevant round. A future conference can have a closed submission.

Save the original date text and timezone. Convert to UTC and the author's IANA timezone
only when the instant is actually specified. Handle daylight saving at that date.
AoE means UTC-12 only when the source specifies it. Do not promote an aggregator's
default end-of-day or AoE convention to an official deadline. A date with no time/zone
has unknown precision; on a consequential boundary, require clarification/verification.

States:
- open: source confirms the submission opportunity is open and all known prerequisites
  are satisfiable or already fulfilled.
- conditional: e.g. mandatory abstract registration has passed, but authors who already
  registered can still submit; author status must be verified.
- announced-not-open: dates are confirmed but submissions are not open yet.
- closed: full paper or an unfulfilled mandatory prerequisite has passed.
- unannounced/unverified: future timing or eligibility cannot be established.

An open web portal alone does not override the announced deadline. A deadline in the
future alone does not prove registration is open. Display earliest remaining mandatory
action, full deadline, author-local time and verification date. Put forecasts of future
cycles in a separate watchlist, never the actionable shortlist.

## Handoff

For the chosen opportunity, provide venue/year/track/round/type, ranking checks, official
template and author-guide links, all mandatory deadlines, anonymity state, page-count
semantics, known declarations/checklists and unresolved requirements. Include the paper
version and evidence/revision priorities. Reverify live facts at the editing handoff and
again before any authorized submission. Selection does not authorize concurrent submission.


## Journal rankings and institutional requirements

For journal regular routes and Special Issues, use
[ranking-systems.md](ranking-systems.md),
[institution-profile.md](institution-profile.md) and
[journal-timing.md](journal-timing.md) in addition to venue-specific author instructions.

The CAS National Science Library announced **2026 discontinuation** of its updated
journal partition tables. Historic 2025-or-earlier official CAS partitions
may remain relevant **only when the institution adopts them**. JCR Q1
is not CAS partition 1; AJG, ABDC and FT50 are separate categories.
Record journal ISSN, scheme year, subject category, official source,
verification date and institution's policy before calling a rank verified.
See the cited CAS, Clarivate, Chartered ABS, ABDC and FT sources in the
ranking-systems reference.

## Journal submission and timing states

Regular journal submission can be verified as **rolling** (no general fixed
submission deadline), invitation-only, closed, or unverified; check the
actual article-type route and portal. A named **Special Issue** adds its
own opening/deadline and eligibility; a closed issue does not close
the ordinary journal route. Distinguish official publisher **first
decision**, time to acceptance, and time-to-publication — never infer
publication by a career deadline from a first-decision average.

Journal handoff: journal identity and ISSN, article type, regular vs
special issue, official author guide, required files, word/figure limits,
OA/APC/licence, ethics/originality/concurrent submission and verified
journal status. For conferences, retain edition, track, round, abstract
and full-paper stage checks.
