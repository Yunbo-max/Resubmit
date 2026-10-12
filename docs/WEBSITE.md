# Project website

The self-contained static site lives in `site/`. It uses system fonts and local CSS/JavaScript; no framework, account, analytics, remote font service or manuscript backend is required. ReSubmit is a short display title; repository and skill names do not change.

## Design references

[Orchestra's AI Research Skills page](https://www.orchestra-research.com/ai-research-skills) demonstrates a focused product introduction with prominent installation. [rebuttal-skills](https://github.com/yjoonjang/rebuttal-skills) links a browser-based ReviewSearch demo and shows workflow examples. Its linked hosted demo was not accessible from this session, so no claim about its current runtime was made. Our original page borrows these information priorities, not their artwork or layout source. It foregrounds our narrower task: existing LaTeX revision, actual rendered before/after evidence and transparent boundaries.

## Build and preview

Install latexmk/TeX with article and booktabs, then:

```bash
python -m pip install -r requirements-qa.txt -r requirements-demo.txt
python scripts/build_demo.py
python -m http.server 8000 --directory site --bind 127.0.0.1
```

Open `http://localhost:8000`. Generated previews are ignored in Git and regenerated from checked-in TeX. The before/after case deliberately demonstrates a font-scope failure; it is not an official template or a benchmark of agent performance. The hero illustration is labeled illustrative.

## GitHub Pages

The repository was observed with Pages disabled when this release was prepared. The source alone does not turn it on. A maintainer can select **Settings → Pages → Source: GitHub Actions**, then run **Deploy project site** in Actions. After the first successful deployment, pushing relevant website files to main redeploys the site. The workflow checks the Pages API first and skips deployment with a clear message while Pages is disabled; it does not request a personal token or attempt to grant itself administration privileges.

Expected URL after a verified successful deployment:
`https://yunbo-max.github.io/Resubmit-to-a-different-conference/`

No custom domain or existing personal-site route is changed. See [official Pages publishing instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). The separate CI workflow builds the demo and uploads a preview artifact even without Pages.
