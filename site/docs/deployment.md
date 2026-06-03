# Deployment

AgentCraft's public site is built with MkDocs and deployed to Cloudflare Pages.

## Live URL

- **Production:** https://agentcraft-8lp.pages.dev
- **Repository:** https://github.com/My-cyberx/AgentCraft
- **Cloudflare project:** `agentcraft` under account `3711732b7581e3345a259368c3c26d62`

## Architecture

```
GitHub repo (My-cyberx/AgentCraft)
    ↓ git push
    ↓
Local build: mkdocs build → site/site/  (16 HTML pages, 3MB)
    ↓
Cloudflare Pages (free tier)
    ↓ wrangler pages deploy
    ↓
Live at https://agentcraft-8lp.pages.dev
```

## Local build

```bash
cd site
mkdocs build --strict   # → site/site/
```

The `--strict` flag fails the build on any warning (broken links, missing pages, etc.). The CI workflow also runs this check on every push.

## Manual deploy

One-time setup (already done for this repo):

```bash
# Login to Cloudflare
wrangler login
# Opens browser for OAuth
```

Each deploy:

```bash
cd ~/Documents/agentcraft
mkdocs build --strict --site-dir site/site  # (or use site/ as the workdir)
wrangler pages deploy site/site --project-name=agentcraft --branch=main
```

Wrangler returns a unique URL per deployment (e.g. `https://6fed11c8.agentcraft-8lp.pages.dev`) plus the production URL (`https://agentcraft-8lp.pages.dev`).

## Auto-deploy on git push

The site can be configured to auto-deploy on every push to `main`. Two options:

### Option A: Cloudflare dashboard (recommended for v1)

1. Go to https://dash.cloudflare.com → Workers & Pages → `agentcraft`
2. Settings → Builds → Connect to Git
3. Select `My-cyberx/AgentCraft`, branch `main`
4. Build settings:
   - Build command: `cd site && pip install mkdocs mkdocs-material && mkdocs build --strict`
   - Build output: `site/site`
   - Root directory: `/`
5. Save. Every `git push` triggers a new deploy.

### Option B: GitHub Actions (token-based)

If you prefer the deploy to happen in CI (with full logs in GitHub), add this workflow at `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloudflare Pages
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Build
        run: |
          pip install mkdocs mkdocs-material
          cd site && mkdocs build --strict
      - name: Deploy
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: 3711732b7581e3345a259368c3c26d62
          projectName: agentcraft
          directory: site/site
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

To use Option B, you need a Cloudflare API token (not the OAuth login). Create one at https://dash.cloudflare.com/profile/api-tokens with `Cloudflare Pages: Edit` scope, and add it to GitHub repo secrets as `CLOUDFLARE_API_TOKEN`.

For now, **Option A is simpler** — connect via the dashboard and let Cloudflare handle the deploys.

## Custom domain

To attach a custom domain (e.g. `agentcraft.md`):

1. Cloudflare dashboard → `agentcraft` Pages project → Custom domains
2. Add the domain
3. If the domain is on Cloudflare, the CNAME is added automatically
4. If the domain is elsewhere, add the CNAME record at the registrar pointing to `agentcraft-8lp.pages.dev`

SSL is provisioned automatically by Cloudflare.

## Rollback

Cloudflare keeps every deployment. To roll back:

```bash
wrangler pages deployment list --project-name=agentcraft
# Pick the deployment ID
wrangler pages deployment rollback <deployment-id> --project-name=agentcraft
```

Or via the dashboard: Deployments → click any past deployment → "Rollback to this deploy".
