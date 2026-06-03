# Install

AgentCraft is a GitHub repo with a static site. You don't "install" the library — you browse it, copy the artifact you want, and use it.

## Step 1: Clone the repo

```bash
git clone https://github.com/ah-alhawar/agentcraft
cd agentcraft
```

## Step 2: Browse the site locally

```bash
pip install mkdocs mkdocs-material
mkdocs serve
```

Open http://localhost:8000. That's the library.

## Step 3: Copy an artifact

Pick an artifact from the [library](library/index.md). The artifact page has a one-line install at the top. Examples:

```bash
# Script — no install, just run
python3 canon/drilling/upstream/depro-calc/depro_calc.py --input inputs.example.yaml

# Skill — copy SKILL.md into your Hermes skills folder
cp -r skills/skill-depro-calc/ ~/.hermes/skills/

# Flow — drop the SKILL.md into your agent's skills folder
cp -r skills/skill-flow-audit-deliverable/ ~/.hermes/skills/
```

Then restart Hermes (or `/reload-skills` in-session) to pick it up.

## Step 4: Run it

Each artifact page has a **trigger prompt** — a literal sentence you paste into the agent. Example for the DEPRO calc:

> Run depro_calc.py on inputs.yaml for Well A-12.

The agent loads the right skill, runs the script, formats the output in your voice.

## Requirements

| What | Why |
|---|---|
| Python 3.10+ | Most scripts are Python. Stdlib only unless noted. |
| `mkdocs` + `mkdocs-material` | Only needed to build the site locally. |
| `openpyxl` (optional) | Only for XLSX export of the API Q1 audit checklist. |
| `pyyaml` (optional) | Most YAML inputs use a stdlib parser, but complex YAML may want PyYAML. |
| `bun` + `uv` (optional) | Only for flows that bundle a worker service. |

You do **not** need:
- Docker
- A cloud account
- A specific OS (macOS / Linux / WSL / Windows all work)
- An API key, for the offline scripts (DEPRO, API Q1 checklist, LSS)

## What you get for each artifact type

| Type | Install cost | Runtime cost | Internet needed |
|---|---|---|---|
| Script (stdlib) | Zero | Zero | No |
| Script (with optional XLSX) | `pip install openpyxl` | Zero | No |
| Skill (Hermes) | Copy + `/reload-skills` | Token cost (per agent call) | Yes (for LLM) |
| Flow | Copy + `/reload-skills` | API cost (per run) | Yes |

## Deploying the site

To deploy the public site to `agentcraft.md` (Cloudflare Pages) or `agentcraft.ae` (Vercel):

```bash
mkdocs build
# → site/site/  (deploy this directory)

# Cloudflare Pages
wrangler pages deploy site/site --project-name=agentcraft

# Vercel
vercel deploy --prod site/site
```

The site is pure static HTML/CSS/JS. No server, no database, no runtime. Free tier on either host.
