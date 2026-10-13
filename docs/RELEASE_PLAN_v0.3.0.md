# v0.3.0 release plan

Goal: add host-LLM conference predictions without model training, a separate
inference service, a mandatory API key or changes to the LaTeX editing engine.

The user explicitly selected skill-driven predictions by their existing agent
and requested the finished GitHub update. This release implements that scope.

- [x] Test skill packaging and backward-compatible selection in the installer.
- [x] Add a self-contained selecting-conference-venues skill, evidence rules,
  prediction rubric, output template and clearly hypothetical example.
- [x] Keep known-venue LaTeX work on resubmitting-papers.
- [x] Update English README, setup, website and announcement copy.
- [x] Run new local checks; full GitHub CI status is recorded by Actions.
- [ ] Verify the published commit and report actual Pages status.

Checks of files and installation do not establish recommendation accuracy,
probability calibration or independent agent compliance. No private manuscript
or actual prediction is published in this release.
