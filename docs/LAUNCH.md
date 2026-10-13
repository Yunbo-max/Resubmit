# ReSubmit v0.3.0 — launch copy

Use the repository link as the canonical launch destination. Do not advertise the
project-site URL as live until the Pages deployment is verified.

## One line

ReSubmit: open-source Agent Skills that help your existing LLM choose a conference,
then revise the LaTeX without losing the science.

## Short post

I've open-sourced ReSubmit: two skills for the work between submissions.

Your existing agent reads a paper, checks CORE/ICORE and CCF rankings plus current
submission deadlines, and recommends primary and backup venues with explicit fit,
readiness and revision-risk judgments. Then it can update the original LaTeX:
tables, figures, templates, writing and rendered-PDF checks.

No model training. No separate prediction API. No acceptance guarantees.
Recommendations are subjective model judgments grounded in verified sources.

Code, install instructions, reproducible LaTeX examples and validation:
https://github.com/Yunbo-max/Resubmit-to-a-different-conference

## Longer description

ReSubmit connects two tasks that are usually disconnected: deciding where a paper
should go and preparing it for that venue. The venue-selection skill instructs
Codex, Claude Code or another skills-compatible host LLM to assess the manuscript,
verify official ranking and deadline facts, and make an evidence-linked recommendation.
The LaTeX-native editing skill handles scoped fixes and full retargeting, with
source protection, evidence-preserving table updates and rendered-page comparison.

This is an early open-source workflow, not a trained acceptance-prediction model.
Tests cover software and packaging behavior; they do not establish recommendation
accuracy or guarantee any conference outcome. Contributions and reproducible,
non-confidential failure reports are welcome.
