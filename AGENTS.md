# Repository operating contract

This is skill infrastructure, not a manuscript repository. Use
skills/selecting-conference-venues/SKILL.md for venue recommendations and
skills/resubmitting-papers/SKILL.md for LaTeX editing. Keep each folder self-contained.
The host LLM predicts; do not add a required trained model, inference API or GPU job.

Never publish actual manuscripts, reviews, private evidence or credentials without
explicit authorization. Synthetic fixtures and hypothetical examples must be labeled.
Prediction scores are subjective, not calibrated; source and installation tests do not
establish recommendation accuracy or agent compliance.

Preserve existing LaTeX helper behavior and the per-revision DAG. Full tests:
`python -m unittest discover -s tests -v`. Read versioned validation records before
making completion claims. Run both column modes when layout behavior changes.
Do not claim official venue compatibility from generic article fixtures.

Do not alter official conference style files, distribute font files, invent evidence
or automatically submit. Clean source packages use allowlists, not entire workspaces.
