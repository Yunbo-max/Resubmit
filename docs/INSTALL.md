# Installation

## Requirements

An agent host that can load Agent Skills, read/edit local files, and run the tools you authorize. Python 3.10+ is required for bundled helpers. PDF inspection and comparison require PyMuPDF. Compilation requires your project's TeX engine and packages, normally invoked through latexmk. The skill is not an LLM, remote service, or compiler.

## Local Codex or Claude Code

From a reviewed clone of this repository:

```bash
python scripts/install_skill.py --agent codex
# OR
python scripts/install_skill.py --agent claude
```

Codex destination: `~/.agents/skills/resubmitting-papers/`.
Claude Code destination: `~/.claude/skills/resubmitting-papers/`.
The entire directory is copied, including references, assets and scripts. No dependency is installed automatically. The installer rejects existing destinations and symlinked source contents rather than risking unintended replacement.

For a project-specific or other supported host location:

```bash
python scripts/install_skill.py --destination /path/to/paper/.agents/skills/resubmitting-papers
```

Start a new agent session, check that `resubmitting-papers` is discovered, and ask for a read-only diagnosis of a copy of a manuscript first. A file copy is not proof that the host has loaded it. The local paths above do not automatically install a cloud ChatGPT plugin.

## Updating and uninstalling

Record the currently installed VERSION and back up any local changes. Review the new version in a separate clone. Move the old skill directory to a backup location outside the host's discovery directories, then rerun the installer. There is intentionally no force-overwrite flag. To uninstall, remove only the skill directory you installed, after preserving local modifications; manuscript files are separate.

## Optional dependencies

```bash
python -m pip install -r requirements-qa.txt
# For the website demo only:
python -m pip install -r requirements-demo.txt
```

Use the existing paper's documented build method. Do not run untrusted latexmkrc files or enable shell escape merely to get a green build. In a fresh sandbox, use a reviewed copy with the minimum needed permissions.

## Troubleshooting

**Skill not visible:** verify the full directory and SKILL.md exist, inspect the host's discovery settings, and open a new session. **Installer refuses:** an existing install is protected; back it up first. **Missing PDF tooling:** install optional dependencies in your chosen environment. **TeX cannot build:** report the actual compiler log; do not claim a visual comparison without a baseline PDF. **Cloud host:** follow that host's supported skill/plugin packaging instructions instead of assuming it can access your local filesystem.

Official references checked on 2026-10-13: [Codex skill discovery](https://developers.openai.com/codex/skills/), [Claude Code skills](https://code.claude.com/docs/en/skills), [Agent Skills specification](https://agentskills.io/specification). Runtime versions and administration policies can change discovery behavior.
