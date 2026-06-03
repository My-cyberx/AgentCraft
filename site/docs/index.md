# AgentCraft

> A library of scripts, skills, and flows for O&G and API auditing — built from 9 years of fieldwork.

## One-liner

**AgentCraft is a curated, open-source, MIT-licensed library of three artifact types: scripts (deterministic, no LLM), skills (agent-loaded procedures), and flows (multi-tool compositions) — sourced from real O&G and API-auditing work, each published with a trigger prompt and a one-line install.**

## What you get

- **Scripts** — copy a single file, run it, get a number. DEPRO calculator, API Q1 audit checklist, Pareto chart, LSS DMAIC. Stdlib only where possible.
- **Skills** — drop a `SKILL.md` into your Hermes / Claude / Cursor setup; the agent now knows how to do a specific procedure in your voice, with the right tools, citing the right standards.
- **Flows** — multi-stage compositions that produce a complete deliverable in one agent run. SME audit (7 docs in 30 min), lead research (ICP → 50 scored leads in Airtable), content publish (1 topic → blog + thread + LinkedIn + newsletter), build website (brief → live URL on Vercel).

## The first 9 artifacts

| Artifact | Type | Domain | Cost / run | Status |
|---|---|---|---|---|
| [DEPRO Calculator](library/drilling/upstream/depro-calc.md) | Script | Drilling / Upstream | Free (stdlib) | ✅ v3.2.1 |
| [Cement Job Design](library/drilling/upstream/cement-job-design.md) | Skill | Drilling / Upstream | Free (stdlib) | ✅ v1.0.0 |
| [Liner Hanger Overview](library/drilling/upstream/liner-hanger-overview.md) | Flow | Drilling / Upstream | ~$0.16 | ✅ v1.0.0 |
| [API Q1 Audit Checklist](library/quality/api-q1/audit-checklist.md) | Script | Quality / QMS | Free (stdlib; openpyxl optional) | ✅ v1.4.0 |
| [IWCF L4 Drill](library/hse/iwcf-l4/drill.md) | Skill | HSE / IWCF L4 | ~$0.02 | ✅ v1.0.0 |
| [DMAIC Template](library/operations/lss/dmaic-template.md) | Script | Operations / LSS | Free (stdlib) | ✅ v1.0.0 |
| [Fishbone Generator](library/operations/lss/fishbone.md) | Skill | Operations / LSS | Free (stdlib) | ✅ v1.0.0 |
| [Pareto Chart](library/operations/lss/pareto.md) | Script | Operations / LSS | Free (stdlib) | ✅ v1.0.0 |
| [SME Audit Deliverable Flow](library/operations/sme-audit/flow-audit-deliverable.md) | Flow | Operations / SME Audit | ~$0.54 | ✅ v1.0.0 |

## Live site

- **Production:** https://agentcraft-8lp.pages.dev
- **Custom domain:** wired in step 5 (see [Deployment](deployment.md))

## Install

```bash
git clone https://github.com/My-cyberx/AgentCraft
cd AgentCraft
pip install mkdocs mkdocs-material
cd site && mkdocs serve   # → http://localhost:8000
```

## Why this exists

The 240+ skills installed in your Hermes are general-purpose. The 30+ Drive folders of O&G PDFs and decks are reference material. **AgentCraft is the curated intersection** — only the artifacts that turn a specific O&G or API-auditing task into a one-line command, with the right voice, the right tools, and a real artifact at the end.

It's not exhaustive. It's not a fork of Hermes. It's a published catalog, modeled on the claude-seo.md style — install command near the top, decision tree in the middle, FAQ anchored at the bottom.

## The 7-second pitch

1. You have 9 years of O&G and API-auditing work in Drive.
2. You have 240+ skills in Hermes.
3. Pick the 20-40 artifacts that are worth sharing.
4. Wrap each in a SKILL.md with your voice, your tools, your standards.
5. Publish with a trigger prompt and a one-line install.
6. CI runs every flow weekly. Stale artifacts get flagged.
7. New artifacts go through a 7-stage workflow (draft → test → review → version → publish → index → maintain).

Full brief: [`agentcraft-strategy-brief.md`](https://github.com/ah-alhawar/agentcraft/blob/main/agentcraft-strategy-brief.md).

## What's next

- Day-2: add cement-job-design, liner-hanger-overview, IWCF L4 drill, LSS DMAIC, Pareto, Fishbone.
- Day-3: cross-walk ISO 9001 evidence lists against API Q1 11th ed.
- Day-4: API Q2 2nd ed. audit checklist (mirror of API Q1 with the Q2-specific clauses).
- Day-5: 2-3 more flows (lead-research, content-publish, build-website) — these are already in Hermes at `~/.hermes/skills/flow-*`, just need the public SKILL.md.
- Day-6: production deploy of the site to `agentcraft.md` (Cloudflare Pages) or `agentcraft.ae` (Vercel).
- Day-7: announce on LinkedIn, post the install command, open the PR queue to the community.
