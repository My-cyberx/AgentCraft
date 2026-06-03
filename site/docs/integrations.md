# Integrations — the tool stack

AgentCraft artifacts are designed to work with the [Hermes Agent](https://hermes-agent.nousresearch.com) `.env` tool stack. All integrations are optional. Each artifact page lists which `.env` keys it needs.

## What the integration looks like

Every skill and flow in AgentCraft reads from the same `.env` file at `~/.hermes/.env` (or wherever your agent loads it from). You set the keys you have; artifacts that need a missing key fail loudly with a clear error.

```bash
# Example ~/.hermes/.env
APIFY_TOKEN=apify_api_xxx
DEEPSEEK_API_KEY=sk-xxx
GEMINI_API_KEY=AIzaSy...
EXA_API_KEY=xxx
AIRTABLE_API_KEY=patxxx
RESEND_API_KEY=re_xxx
BEEHIIV_API_KEY=xxx
VERCEL_API_KEY=xxx
GITHUB_API_KEY=ghp_xxx
```

## The 14 tools AgentCraft uses

| Tool | Use | Env var | Free? |
|---|---|---|---|
| **Apify** | LinkedIn scrapers, company search, social data | `APIFY_TOKEN` | Pay per actor run |
| **DeepSeek** | Long-form drafting, enrichment, scoring | `DEEPSEEK_API_KEY` | Cheap ($0.14/M input tokens) |
| **Gemini** | Hero images, section visuals, cover art | `GEMINI_API_KEY` / `GOOGLE_API_KEY` | Free tier, then pay |
| **Exa** | Research, semantic web search | `EXA_API_KEY` | Pay per query |
| **Airtable** | CRM, lead storage, engagement tracking | `AIRTABLE_API_KEY` | Free tier, then $20/mo |
| **Resend** | Deliverable email to clients | `RESEND_API_KEY` | Free tier (3K/mo) |
| **Beehiiv** | Newsletter drafts + scheduling | `BEEHIIV_API_KEY` | Free tier |
| **Vercel** | Static site deploys | `VERCEL_API_KEY` | Free tier (hobby) |
| **GitHub** | Source repo, public page hosting | `GITHUB_API_KEY` | Free |
| **OpenRouter** | Quality pass / humanize (Claude, GPT) | `OPENROUTER_API_KEY` | Pay per token |
| **n8n** | Workflow automation (optional backend) | n8n instance URL | Self-hosted free |
| **Linear** | Task tracking, engagement pipeline | Linear OAuth | Free tier |
| **Telegram** | Cron job delivery, alerts | `TELEGRAM_BOT_TOKEN` | Free |
| **Firecrawl** | Backup web scraper (Exa fallback) | `FIRECRAWL_API_KEY` | Pay per page |

## What runs offline (no API needed)

These artifacts work with **zero** API keys:

- **DEPRO Calculator** — pure Python, stdlib only
- **API Q1 Audit Checklist** — pure Python, stdlib; openpyxl optional for XLSX
- **Pareto chart** — pure Python
- **Fishbone diagram** — pure Python + SVG
- **DMAIC template** — pure Python
- **IWCF L4 drill** (offline mode) — uses the agent's LLM, but no external APIs
- **All scripts** — by design, no LLM, no API

## Cost discipline

The strategy is **DeepSeek + Gemini first, OpenAI/Anthropic as the quality pass**:

- Drafts and synthesis: DeepSeek (~5x cheaper than GPT-4)
- Images: Gemini Flash (free tier covers most flows)
- Quality pass / humanize: OpenRouter Claude (only on the final 10% of each output)

A typical flow run costs $0.17–$0.55. A full SME audit (7 documents) costs ~$0.54. You're not paying for a SaaS subscription — you're paying per artifact, and the cost is small enough to bill to a client or absorb as overhead.

## Adding a new tool

When you add a new tool to your `.env`:

1. Update each artifact's `metadata.hermes.requires_env` list in its `SKILL.md` frontmatter
2. Add the tool to the `tools_available` list in the `context.domain` block
3. The next CI run will pick it up; the public site integrates page will show the new key automatically

## Why this list?

These 14 tools are the ones that:
- Are present in 90%+ of the underlying 240+ Hermes skills
- Have generous free tiers
- Are the right cost-per-call for production flows
- Don't overlap (each one has a clear, non-overlapping job)

If a new tool displaces one of these on cost or capability, the maintainer updates this list. If a tool has a clear niche and isn't on the list (e.g., Perplexity, Tavily, Browserbase), add it with a one-line use-case.
