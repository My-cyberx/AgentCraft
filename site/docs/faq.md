# FAQ

## What is AgentCraft?

A curated, open-source, MIT-licensed library of three artifact types — **scripts** (deterministic, no LLM), **skills** (agent-loaded procedures), and **flows** (multi-tool compositions) — built from 9 years of O&G and API-auditing work. Each artifact is published with a trigger prompt, a one-line install, a sample output, and a `last_tested` date.

## Is it free?

Yes. MIT-licensed, no paid tier. Some flows use paid third-party APIs (Apify, DeepSeek, Gemini, etc.), but each run is <$1, and the offline scripts run with zero API cost. The site is static HTML, hosted on a free tier of Cloudflare Pages or Vercel.

## How is it different from the 240+ Hermes skills I already have?

Hermes is the engine. AgentCraft is the **curated, public, O&G-specific catalog** built on top of it. We promote 20-40 high-quality, O&G-relevant artifacts from the underlying skill set, wrap them with source attribution, trigger prompts, and a public site. The other 200+ stay in your private Hermes.

## How is it different from the Claude Code plugin ecosystem?

Claude Code plugins are installable modules with slash commands, agents, and hooks. AgentCraft is a **library of recipes** — the trigger prompt is the unit of value, not the install. A visitor to AgentCraft copies a sentence, pastes it into their agent, and gets a real artifact. The install is implicit; the value is the recipe.

## What does "domain-first" mean in the catalog?

[Drilling / Quality / HSE / Operations](library/index.md) is the primary navigation. You browse by what you *do*, not by what *tech* the artifact uses. Type (Script / Skill / Flow) and vertical (Upstream / Midstream / etc.) are secondary filters. A fallback "use-case-first" navigation exists for cross-cutting workflows (audit, training, tendering).

## Can I submit my own artifact?

Yes, PRs welcome. Every artifact must:

- Have a source-of-truth document in the Drive `00-canon/` folder
- Include a trigger prompt that loads the right skill when pasted
- Be reproducible (same input → same output, or variance documented)
- Cite the standards it uses correctly (API Q1 11th ed., not "Q1"; ISO 9001:2015, not "ISO 9001")
- Pass [`CONTRIBUTING.md`](https://github.com/ah-alhawar/agentcraft/blob/main/CONTRIBUTING.md#pr-checklist) (filename convention check)

[`CONTRIBUTING.md`](https://github.com/ah-alhawar/agentcraft/blob/main/CONTRIBUTING.md#pr-checklist)

## How do I know an artifact is still good?

Every page shows a `last_tested` date in the footer. **CI runs every flow weekly** (Mondays at 06:00 UTC) with a 3-5 minute smoke test. A failure sends a Telegram alert to the maintainer. Stale artifacts (no test in 90+ days) are flagged with a yellow banner; broken artifacts (test failing) are flagged red.

## What if a flow breaks because an API changed?

- The flow's `CHANGELOG.md` is updated within 24h of the fix
- The public page shows a "broken" banner until the fix lands
- Drive's version history lets you roll back to the last working version
- The maintainer publishes a `vN.N.(N+1)` patch in the same week

## Why is the catalog only 3 artifacts at launch?

Because curation is the value. A library of 240 artifacts with no curation is a search engine, not a library. The 20-40 artifacts that earn a place in AgentCraft will be the ones that:

- Solved a real problem for a real client
- Have a source-of-truth document in Drive
- Have a trigger prompt that consistently loads the right skill
- Are tested weekly without flakes

Day-7 target: 7 artifacts. Day-30 target: 20. Day-90 target: 40.

## What's a "trigger prompt" and why does it matter?

A trigger prompt is the literal sentence a visitor pastes into their agent to invoke an artifact. Example for the DEPRO calc:

> Run depro_calc.py on inputs.yaml for Well A-12.

The trigger prompt is the **secret weapon** of AgentCraft. It turns a static library into an immediately usable one. A visitor doesn't have to guess how to invoke a skill; they copy a sentence, paste it, and the agent does the right thing.

Every artifact page has a "Trigger prompts" section with 3 variations. Copy any.

## Does this work on Windows / Linux / macOS?

Yes for scripts (pure Python, stdlib). Skills and flows need an agent runtime — Hermes works on all three, Claude Code works on all three. The site is pure static HTML, deploys anywhere.

## How do I deploy the site myself?

```bash
mkdocs build
# → site/site/  (deploy this directory)
```

To Cloudflare Pages:

```bash
wrangler pages deploy site/site --project-name=agentcraft
```

To Vercel:

```bash
vercel deploy --prod site/site
```

Both free tiers work.

## Where's the source brief?

[`agentcraft-strategy-brief.md`](https://github.com/ah-alhawar/agentcraft/blob/main/agentcraft-strategy-brief.md) in the repo root. 763 lines, 16 sections, the full strategy this library was built from.

## I have feedback or a request.

Open an issue on GitHub. Use the `enhancement` or `request` template. Be specific about your O&G / QMS / API-auditing use case — the maintainer prioritizes by frequency × impact.
