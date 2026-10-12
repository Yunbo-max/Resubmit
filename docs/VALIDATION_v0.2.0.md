# Validation — v0.2.0

This release changes public presentation, installation and project infrastructure, not the core LaTeX repair contracts. Historical validation records remain separate.

Date: 2026-10-13.

## Local checks

The local baseline was the provided v0.1.2 skill archive, compared with the current repository file identities. The full repository could not be cloned over this environment's network. Existing remote files are retained through a base-tree update rather than overwritten from that partial local workspace.

The public-distribution test file contains 16 cases covering safe complete-directory installation, preservation of existing installs, malformed sources, symlink rejection, destination containment, cache exclusion, version consistency, English entry points, local-only web assets, accessibility landmarks, repository health files, unchanged demo wording, synthetic labeling and static resource paths. The tests were introduced before the new installer and website files and initially failed on their absence. The final local command `python -m unittest discover -s tests -v` ran these 16 public-distribution tests with zero failures or errors. This local count does not include the 96 pre-existing remote tests.

The demo builder compiles before.tex and after.tex with latexmk and disabled shell escape. Both use shared text/table sources and differ only in the braces around the table input. It exports actual cropped rendered previews and records PDF hashes. These are synthetic generic article documents, not official author-kit compatibility or agent-effectiveness tests.

The project page was rendered in managed Chromium with its local assets inlined because file and localhost navigation were blocked by browser policy. Desktop (1440 px) and mobile (390 px) layouts, horizontal overflow, demo switching, agent installation options and the clipboard-unavailable fallback were checked. This tests the rendering and interaction logic, not public network hosting or actual clipboard permissions. Static asset paths are checked separately. No browser policy was changed. Both viewports had no horizontal overflow; demo switching, installation selection and the clipboard fallback passed, with zero JavaScript exceptions.

## Remote checks and hosting

The CI workflow runs the complete repository test suite on Python 3.10 and 3.13, then compiles native-editing fixtures and the website demo in a separate job. Consult the actual run for pass/fail; a checked-in workflow is not evidence that it ran successfully. The deployment workflow reports a disabled/unavailable Pages configuration and does not treat it as a live site.

## Limits

No real manuscript or private review is published. No all-venue compatibility, improved acceptance rate, host-agent behavioral guarantee or independent scientific validation is claimed. The static website does not accept manuscripts. Source layout and demo values are inspectable; attractive presentation is not scientific evidence.
