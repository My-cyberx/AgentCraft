---
name: flow-audit-deliverable
description: Full SME Audit System production flow — produces a complete 2-week operational audit deliverable for a small/medium business in a single agent run. Combines intake form, business analysis, gap report, 90-day roadmap, vendor shortlist, and proposal email. Use when user says "run an audit on [client]", "produce a deliverable for [business]", or "I need an SME audit package for [name]". All output goes to a dated client folder in ~/clients/<slug>/.
version: 1.0.0
last_tested: 2026-06-03
metadata:
  hermes:
    tags: [flow, audit, sme, production, deliverable]
    requires_env: [DEEPSEEK_API_KEY, GEMINI_API_KEY, RESEND_API_KEY, APIFY_TOKEN, AIRTABLE_API_KEY]
    source_drive: 00-canon/operations/sme-audit/00-flow-audit-deliverable-v1.0.0-2026-06-03.md
    public_slug: library/operations/sme-audit/flow-audit-deliverable
  context:
    user:
      name: "Aiham Alhawar"
      role: "O&G quality / API auditor / SME audit consultant"
      geography: "Abu Dhabi, UAE"
      voice: "Direct, execution-first. No fluff. Bullet lists > paragraphs."
      brand_dislikes:
        - "AI-isms ('delve into', 'navigate the landscape', 'leverage')"
        - "Inter font, purple gradients, cookie-cutter layouts"
        - "Generic disclaimers ('this is not professional advice')"
        - "20-line preambles before the answer"
      brand_likes:
        - "Bullet points, tables, copy-paste ready artifacts"
        - "Specific names, dates, AED/USD figures"
        - "IWCF L4, IADC, ISO 9001, API Q1/Q2 references used correctly"
        - "Real deliverable > slide deck"
    domain:
      primary: "SME operations, O&G upstream, drilling, cementing, liner hangers, QMS audits"
      standards_in_force: ["API Q1 11th ed", "API Q2 2nd ed", "ISO 9001:2015", "IWCF L4"]
      tools_available: [apify, deepseek, gemini, exa, airtable, resend, beehiiv, vercel, n8n, linear, telegram, github]
      cost_sensitivity: "high — prefer DeepSeek + Gemini over OpenAI; Airtable free tier where possible"
    session:
      memory_key: "ah-alhawar-default"
      preferred_cwd: "~/projects"
      default_delivery: "telegram"
    last_used:
      runs: 0
---

# Flow: SME Audit Deliverable (Single-Shot)

A complete client audit package in one run — the equivalent of a 2-week engagement compressed into 30 minutes of agent work.

## When to use

- "Run an audit on [client name / website]"
- "Produce an SME audit deliverable for [business]"
- "I just signed [X] — build me the audit package"
- "Generate the full gap report + roadmap for [company]"

## Inputs

1. **Client** — name + website URL (or just name if I'll find it)
2. **Vertical** — auto-detect or ask
3. **Geography** — for vendor + regulatory context
4. **Engagement tier** — Express ($1.5K) / Standard ($3K) / Premium ($7.5K)
5. **Existing data** — any prior notes, Airtable records, emails (optional)

## Tool stack

| Tool | Use | Env var |
|------|-----|---------|
| Apify | Website crawl, social scrape, employee count | APIFY_TOKEN |
| Exa | Industry research, competitor intel | (in web_search_plus) |
| DeepSeek | Synthesis + scoring + narrative | DEEPSEEK_API_KEY |
| Gemini | Hero image for report cover | GEMINI_API_KEY |
| Resend | Deliverable email to client | RESEND_API_KEY |
| Airtable | CRM record + engagement tracking | AIRTABLE_API_KEY |

## Workflow (8 stages, ~30 min wall clock)

### Stage 1: Intake (2 min)
- Auto-pull: website, LinkedIn, Google reviews, employee count, revenue band
- Generate intake form responses (mock if data sparse — flag in deliverables)
- Save to `~/clients/<slug>/01-intake.md`

### Stage 2: Business Model Canvas (5 min)
- DeepSeek generates 9-block BMC: customers, value prop, channels, relationships, revenue, activities, resources, partners, costs
- Cross-reference with public data
- Save to `02-bmc.md`

### Stage 3: PESTEL + 5-Forces (5 min)
- Industry scan: political, economic, social, tech, environmental, legal
- Competitive intensity: existing rivals, new entrants, substitutes, buyer power, supplier power
- Save to `03-pestel-forces.md`

### Stage 4: Gap Analysis (8 min)
- 12 functional areas: Sales, Marketing, Operations, Finance, HR, Tech, Compliance, CX, Supply Chain, Procurement, Reporting, Leadership
- Score 0-5 maturity each
- Identify top 5 gaps (largest delta vs industry benchmark)
- Save to `04-gap-analysis.md` (heatmap + table)

### Stage 5: 90-Day Roadmap (5 min)
- Top 3 quick wins (Week 1-2)
- 3 medium initiatives (Week 3-6)
- 2 strategic plays (Week 7-12)
- Each item: owner, cost estimate, expected impact
- Save to `05-roadmap.md` (Gantt-style)

### Stage 6: Vendor Shortlist (3 min)
- For each top gap, recommend 2-3 vendors (regional + international)
- Cost range, integration notes, red flags
- Save to `06-vendors.md`

### Stage 7: Deliverable Package (2 min)
- Stitch into `00-EXEC-SUMMARY.md` (the cover doc)
- Generate cover hero image (Gemini, 16:9, professional)
- Build interactive HTML dashboard (use `build-dashboard` skill)
- Save to `07-package/`

### Stage 8: Delivery (1 min)
- Airtable: create engagement record, link to folder
- Resend: send "Your audit is ready" email with secure folder link
- Log to user's personal CRM

## Output (final deliverable)

```
~/clients/<slug>-<date>/
├── 00-EXEC-SUMMARY.md      (one-pager for client)
├── 01-intake.md
├── 02-bmc.md
├── 03-pestel-forces.md
├── 04-gap-analysis.md
├── 05-roadmap.md
├── 06-vendors.md
├── 07-package/
│   ├── audit-report.pdf    (compiled, branded)
│   ├── dashboard.html      (interactive)
│   └── cover-hero.png
└── DELIVERY-LOG.md         (sent timestamps, Airtable IDs)
```

Plus chat summary with top 3 findings, recommended next step, pricing for follow-on engagements.

## Failover

- **Apify down**: use `web_extract_plus` for website + manual LinkedIn lookup
- **DeepSeek quota**: fallback to Gemini Flash (same cost tier)
- **Resend auth fail**: generate email draft in markdown, save locally
- **Gemini image fail**: skip cover, use text-only deliverable

## Cost estimate (per audit)

- Apify: ~$0.30 (4 scrapes)
- DeepSeek: ~$0.15 (all synthesis calls)
- Gemini: ~$0.04 (cover image)
- Exa (via web_search_plus): ~$0.05
- **Total: ~$0.54 per audit** (vs $3K-$7.5K billed to client)
