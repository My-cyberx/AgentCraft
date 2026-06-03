# AgentCraft

> A library of scripts, skills, and flows for O&G and API auditing — built from 9 years of fieldwork.

AgentCraft is a **curated, public, open-source library** of three artifact types:

- **Script** — a single, deterministic file (Python, Bash, SQL, JS) that does one job. No LLM in the loop.
- **Skill** — a `SKILL.md` with YAML frontmatter that an agent loads to gain a repeatable procedure + the right tools/env to execute it.
- **Flow** — a multi-stage, multi-tool composition (an agent + a sequence of skills + scripts + APIs) that produces a complete deliverable.

The whole point: a visitor lands on the site, reads one example, runs one command, and gets a real artifact back.

## Quick start

```bash
git clone https://github.com/ah-alhawar/agentcraft
cd agentcraft
pip install mkdocs mkdocs-material
mkdocs serve   # → http://localhost:8000
```

## Repo layout

| Path | What lives here |
|---|---|
| `canon/` | Source-of-truth artifacts (published). One folder per artifact, versioned. |
| `skills/` | Public-facing Hermes skills (mirror of the `canon/` artifact's skill wrapper). |
| `site/` | MkDocs static site — the public library. |
| `drive/` | Local mirror of the Google Drive folder structure. See `drive/SETUP_DRIVE.md`. |
| `ci/` | GitHub Actions — weekly smoke tests, Drive mtime check. |
| `scripts/` | Maintainer scripts (naming validator, new-artifact scaffolder). |

## What this is NOT

- Not a fork of Hermes. Hermes is the engine; AgentCraft is the curated catalog on top.
- Not a fork of claude-seo. The style is inspired by it, not copied.
- Not exhaustive. We curate 20-40 high-quality O&G artifacts, not all 240+ underlying skills.

## License

MIT — see `LICENSE`.
