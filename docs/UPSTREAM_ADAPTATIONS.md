# Design and attribution: integrated research templates

Reviewed 2026-10-16. The entries below are conceptual source comparisons for ReSubmit v0.3.2, not vendored code or runtime dependencies. **No third-party skill source code** or conference style files were copied into this release. Newly written templates are intentionally independent and portable.

## What we adopted, and what stays elsewhere

| Reviewed source | Practices worth adapting | ReSubmit implementation | Not claimed |
|---|---|---|---|
| [K-Dense scientific-writing](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md) | Claim-to-evidence provenance, domain-specific reporting requirements, authorship/ethical safeguards | Versioned claim/evidence registry, explicit source status, author approval and audit in [revision template](../skills/resubmitting-papers/assets/revision-plan-template.md) | Not the K-Dense writing engine, regulatory certification or accuracy results |
| [K-Dense peer-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/peer-review/SKILL.md) | Authorization and confidentiality gate, evidence-bound critique, separate human accountability | Private review-to-revision trace and venue AI-policy caution | ReSubmit does **not** become a confidential reviewer or impersonate editors |
| [K-Dense citation-management](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/citation-management/SKILL.md) | Bibliographic identity checks distinct from support for a stated claim | Provenance instruction in writing and report artifacts | No bundled Crossref/OpenAlex API client |
| [K-Dense scientific-schematics](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-schematics/SKILL.md) | Visual drafts must be verified against scientific labels and actual model semantics | Figure-specific QA; quantitative plots must come from verified data; diagrams ideally editable | No requirement to use a third-party image service; no generated empirical evidence |
| [K-Dense experimental-design / statistical-analysis](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills) | Respect study designs, independent sampling units, effect estimates and uncertainty | Field-aware evidence guidance and conservative table/report checks | No new statistical computations or expertise claim |
| [TobiasLee/Rebuttal-Skill](https://github.com/TobiasLee/Rebuttal-Skill/blob/main/SKILL.md) | Decision-critical review concern analysis, separating actual answers from promises | Stable Concern IDs, evidence status, repair action and acceptance check | No automatic acceptance inference from past reviews |
| [lachlanchen/paper-revision-skill](https://github.com/lachlanchen/paper-revision-skill/blob/main/SKILL.md) | Plan-before-edit, baselines, narrow allowed edits, real PDF/redline locations | Protected file scope, versioned plan and compile/semantic/style/visual release checks | No copying its script implementations or redline format |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/main/20-ml-paper-writing/ml-paper-writing) | ML argument construction, venue-specific writing and citation checks | Existing evidence-led writing module + context-specific reporting changes | No vendored templates or fixed year-specific venue rules |
| [VibeResearch publish-venue-targeting](https://github.com/lengmo1996/VibeResearch-skills/blob/main/skills/global/publish-venue-targeting/SKILL.md) | Actual opportunity gates, fit axes and primary/backup choice with switch conditions | Expanded [conference report](../skills/selecting-conference-venues/assets/report-template.md) | No trained probability prediction model |

## Our minimal interface

The **two original skills remain independently installable** and continue to load focused references progressively. We do not require the K-Dense catalog, GPU, external prediction API, independent metadata database or user manuscript upload.

- Venue intake: paper/version + domain -> verified ranking/CFP eligibility -> subjective host-LLM fit and backups -> explicit author choice -> a structured handoff.
- Revision intake: chosen target (or known target) + authorized manuscripts/reviews -> immutable evidence snapshots -> private [revision plan](../skills/resubmitting-papers/assets/revision-plan-template.md) -> edits in existing .tex -> semantic/style/visual audit -> author review.
- For a tiny formatting fix, skip the full review record: keep the original local edit path. For a new scientific method, use assumptions -> derivation -> distinctive prediction -> falsifier, not merely nicer language.
- A source change invalidates dependent checks. The existing revision DAG remains machine-readable and unchanged; human-editable templates are **artifacts**, not extra DAG nodes.

## Privacy and reuse boundaries

A public open-source skill definition may be read safely; unpublished manuscripts, restricted data and author-visible reviews are a different category. Do not automatically copy them to public issues, image-generation endpoints or external reference platforms. If external handling is necessary, check authority, venue policy and model service terms before sending content. Host-only instructions do not imply local-only processing.

All factual venue dates/ranks require official verification at actual use time. The reporting checklists are reminders, not completed scientific validations. Installed specialists add procedural knowledge, not instant credentials.

## Region-specific journals and outlet rankings

The additional [journal ranking source guide](../skills/selecting-conference-venues/references/ranking-systems.md) and [official-source notes](RANKING_2026_SOURCES.md) explain historical CAS partitions, JCR categories, AJG/ABDC/FT50 business-school distinctions and journal-vs-conference timing. These source links are for user verification only, not new runtime API integrations.
