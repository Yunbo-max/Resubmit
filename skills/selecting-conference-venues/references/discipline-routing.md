# Discipline-aware conference routing

This is guidance for the host LLM, not a trained classifier, an automatically installed tool, a medical device or a domain correctness guarantee. Read this when a manuscript combines disciplines or has a non-ML scientific contribution.

## Classify the contribution

Identify the primary research domain, at most two secondary domains, the genuine novelty (e.g. a new algorithm vs. an application), the intended scientific audience, and what evidence underpins the main claims. With an abstract only, make provisional judgments. Distinguish the application area from the novel contribution.

## Domain-specific questions to check

| Research contribution | Relevant evidence and reviewer norms |
|---|---|
| ML / AI architecture, algorithm or theory | Strong current baselines, compute/fairness, ablations, scale, stated mathematical assumptions |
| NLP / language models | Contamination, data lineage, evaluation protocols, human annotation, languages and generalization |
| Computer vision / 3D | Appropriate benchmark tasks, matching training conditions, qualitative-evidence provenance |
| Systems / AI systems | Real workloads, throughput/latency/resource accounting, hardware descriptions, reproducibility |
| ML theory / statistics / causal inference | Assumptions, estimands, proofs, counterexamples, statistical uncertainty |
| Bioinformatics / computational biology | Cohort/split leakage, biological plausibility, independent validations and reporting |
| Computational chemistry / materials | Correct units, scientific controls, experimental or computational validation |
| Neuroscience / healthcare AI | Ethical/privacy restrictions, study design, bias, uncertainty, external validation; no claim of clinical usability from research benchmarks |
| Robotics / engineering | Safety conditions, environment shift, physical constraints, simulation versus hardware details |

These are guiding questions, not a universal checklist or substitute for professional expertise. Check recent relevant accepted papers, official scope and reporting requirements for the exact edition and track.

## Optional specialist references

If already installed *and authorized*, consult at most two relevant domain skills, for example selected modules from [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills). They offer broad scientific procedures, analysis tools, writing and evidence workflows; ReSubmit does not duplicate them. No external skill is required for ordinary ReSubmit use.

Do not silently install dependencies, run external research services, disclose unpublished manuscripts or claim specialist competence. Read any specialist skill's confidentiality and policy requirements first. Domain tools inform evidence assessment; current ranks, deadlines, active tracks and policy still require their own official-source verification.

If the user's requirement is CORE/CCF A but the work is fundamentally chemistry or biology, note that computing-conference ranks may not cover the most appropriate outlets. Respect explicit user constraints, and distinguish unranked from low-ranked and from unknown.

## Handoff

Maintain a private assessment with primary field, secondary fields, contribution type, relevant evidence norms, known gaps, potential specialist reference and uncertainty. Pass the assessment to the main venue workflow. The order stays: official eligibility first, model judgment second, author decision third, authorized LaTeX revision afterward.


## Structured reporting and scientific-source provenance

When recommending outside a generic AI/ML venue, record the specific evaluation
norm used (e.g., external clinical validation, sample-unit independence, physical
units, or reproducibility expectations), its source or established protocol, and
whether the manuscript actually meets it. Apply only relevant checks; an empty
checkbox is not evidence of compliance. On author request, consult an authorized
pre-installed specialist guide from K-Dense or a comparable provider. Do not
automatically download a broad collection, run specialist experiments or assert
that model reasoning constitutes a valid laboratory assessment.

ReSubmit's venue report must distinguish the application field from the
scientific contribution, and separate: observed paper evidence, scientific
practice references, current official CFP/ranks, model-inferred fit, and missing
information. The current target venue is always the deciding official source for
submission requirements.
