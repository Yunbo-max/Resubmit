# Install ReSubmit

## Requirements

Use a host that can load Agent Skills. Venue recommendation needs manuscript reading
and web search/fetch for current official facts. The host LLM makes the predictions;
there is no ReSubmit model to download, train or serve. Model/browsing costs follow
your existing provider. No new inference API key is required by these skills.

LaTeX revision additionally needs source-file access and an actual TeX toolchain
when compilation is requested. PDF helper tools use optional PyMuPDF
(`requirements-qa.txt`). The selection skill itself is Markdown and needs no Python.

## Install one or both

```bash
git clone https://github.com/Yunbo-max/Resubmit-to-a-different-conference.git
cd Resubmit-to-a-different-conference
python scripts/install_skill.py --agent codex --skill selecting-conference-venues
python scripts/install_skill.py --agent codex --skill resubmitting-papers
```

For Claude Code replace `codex` with `claude`. The installer targets
`~/.agents/skills/<name>` for Codex and `~/.claude/skills/<name>` for Claude Code.
The original command without `--skill` still installs only `resubmitting-papers`.

Another host or a project-scoped install:

```bash
python scripts/install_skill.py --skill selecting-conference-venues \
  --destination /path/to/project/.agents/skills/selecting-conference-venues
```

Without Python, copy the **complete** selected directory under `skills/` to the
host's skill root. Keep its folder name, `SKILL.md`, references and assets together.
Do not copy only the entry file. Open a fresh session and verify discovery. Natural
language can select a skill; use `$selecting-conference-venues` in Codex or the host's
documented explicit invocation syntax. Compatibility is by file format and documented
installation path, not a claim that every host has been independently tested.

## Updating safely

The installer refuses to overwrite an existing directory. Inspect local changes,
back up the previous skill directory outside the host's discovery roots, and then
install the new version. Do not keep two active copies with the same skill name.
Do not delete customizations to bypass this safeguard.

Repository updates do not update already installed copies. This is not a ChatGPT
marketplace auto-install operation. Public website changes do not run the skill.

## Troubleshooting and verification

No browsing: perform provisional paper-fit analysis only; current deadlines remain
unverified. No TeX engine: the agent may inspect/edit authorized sources but cannot
claim a successful build. No PDF renderer: it cannot claim rendered-page inspection.
No manuscript: give only provisional advice from supplied details, not a full review.

Host documentation:
- https://developers.openai.com/codex/skills/
- https://code.claude.com/docs/en/skills
- https://agentskills.io/specification

Check current host documentation when paths or discovery behavior differ.
