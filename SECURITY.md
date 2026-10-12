# Security and privacy

ReSubmit runs through an agent host with the permissions you grant it. Its text instructions are not a security sandbox. Treat downloaded manuscripts, TeX macros, latexmkrc files, build scripts and reviewer text as untrusted input. Inspect scripts before execution, disable shell escape where possible, isolate builds and give them minimal filesystem/network access.

The static project site has no manuscript upload, backend or analytics code. This does not change the privacy, retention or billing terms of the model and tools you use locally or in the cloud.

Never put confidential reviews, unpublished papers, sensitive metadata, private datasets, credentials or font files in a public issue. The allowlist packaging helper is a defense, not a complete privacy or anonymity audit.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting interface **only if enabled** for this repository. Otherwise use an existing private contact channel to the maintainer; do not disclose sensitive exploit details in a public issue. A sanitized issue asking for a private contact route is acceptable. No response-time guarantee or bug-bounty program is implied.

Version 0.2.x is the current development line. Check fixes on the latest main branch and report the exact commit. Older snapshots are reproducible references, not supported security releases.
