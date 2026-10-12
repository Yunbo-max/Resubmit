# Repository operating contract

This is skill infrastructure, not a paper repository. Start at skills/resubmitting-papers/SKILL.md. Keep the skill folder self-contained. Never publish actual manuscripts, reviews, private evidence, internal prompts or local credentials here without explicit authorization. Synthetic software fixtures must be visibly labeled.

Preserve the per-revision DAG and its dependency order. Tests: `python -m unittest discover -s tests -v`. Optional layout smoke test: `python tests/build_layout_fixtures.py`. Run both column modes when layout behavior changes. Do not claim official venue compatibility from generic article fixtures. Read docs/VALIDATION.md before making completion claims.

Do not alter official venue style files or distribute font files. Do not generate experimental evidence. Package clean manuscripts from allowlists, not whole workspaces. No automatic external submission.
