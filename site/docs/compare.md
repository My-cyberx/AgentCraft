# Compare

AgentCraft vs. the alternatives — when to use which.

## AgentCraft vs. raw Hermes Agent (240+ skills)

| | AgentCraft | Raw Hermes |
|---|---|---|
| **Curation** | 20-40 O&G-relevant artifacts, vetted | 240+ skills, mixed quality |
| **Discovery** | Public site with search + filter | `hermes skills list` in terminal |
| **Trigger prompts** | 3 copy-paste sentences per artifact | You write your own |
| **Source attribution** | Every artifact links to its Drive canon PDF | None |
| **Maintenance** | CI runs every flow weekly | Curator (idle skill detection) |
| **Cost transparency** | Per-artifact cost estimate on the page | You figure it out |
| **Offline scripts** | First-class citizens (stdlib Python) | Mixed |
| **Private** | Public (read by anyone) | Private to you |

**Use AgentCraft when:** you want to find a specific O&G or API-auditing artifact fast, see a sample output, copy a trigger prompt, run it.

**Use raw Hermes when:** you're building a one-off skill for a personal workflow that doesn't need to be public.

## AgentCraft vs. Claude Code plugin ecosystem

| | AgentCraft | Claude Code plugin |
|---|---|---|
| **Unit of value** | The trigger prompt (recipe) | The install command (module) |
| **Distribution** | GitHub repo + static site | Plugin marketplace |
| **Format** | `SKILL.md` + scripts + flows | Plugin with slash commands, agents, hooks |
| **Use case** | "I want to do X — show me how" | "I want to extend Claude Code with capability Y" |
| **Lock-in** | None — pure files, no plugin manager | Plugin manager + marketplace |
| **Versioning** | semver in the filename, CHANGELOG.md | Marketplace versioning |

**Use AgentCraft when:** you're a domain expert with a real workflow to share, and you want a low-overhead way to publish it.

**Use Claude Code plugins when:** you're building a complex multi-agent system with hooks, statuslines, and slash commands.

## AgentCraft vs. n8n / Make.com / Zapier

| | AgentCraft | n8n / Make / Zapier |
|---|---|---|
| **Interface** | Trigger prompt (text) | Visual workflow editor |
| **Execution** | In your agent (LLM in the loop) | Serverless functions |
| **Best for** | Tasks that need LLM judgment + multi-step + multi-tool | Tasks that are pure data plumbing, no judgment |
| **Cost** | Per-token + per-API-call | Per-operation (often flat fee) |
| **Local** | Yes | No (cloud) |
| **Custom code** | Python scripts in `canon/` | Code nodes (sandboxed) |
| **Debugging** | Read the agent's transcript | Visual node inspector |

**Use AgentCraft when:** the task needs the agent to interpret, decide, or write — e.g., "review this NCR against API Q1 11th ed." or "produce a 7-doc audit deliverable."

**Use n8n when:** the task is pure data plumbing — e.g., "when a new row hits Airtable, send a Slack message." No judgment, no LLM needed.

## AgentCraft vs. Ahrefs / Semrush (for SEO audits)

Not comparable directly. AgentCraft is a library of artifacts, not a SaaS. But for the small overlap (the "build a website" flow includes SEO basics like meta tags, OG tags, sitemap, robots.txt), AgentCraft is free and the artifact is copy-paste, not a $99/mo subscription.

## AgentCraft vs. a Notion / Confluence wiki

| | AgentCraft | Wiki |
|---|---|---|
| **Format** | Executable code + agent-loaded skills | Static documents |
| **Runnable** | Yes | No |
| **Trigger prompts** | Yes | No |
| **Version control** | git, semver, CHANGELOG | Page history (no semver) |
| **Search** | MkDocs Material search + Drive | Notion / Confluence search |
| **Update friction** | PR + CI | Click "Edit" |

**Use AgentCraft when:** the artifact is a procedure the agent can run.

**Use a wiki when:** the artifact is reference material the human reads (a glossary, a policy doc, a knowledge base).

## The decision in one sentence

> **AgentCraft is for "I want to do this O&G or API-auditing task and I want a recipe I can run in 30 seconds" — not for "I want to extend my agent" (Claude Code plugin), "I want to plumb data between SaaS apps" (n8n/Make), or "I want to look something up" (wiki).**
