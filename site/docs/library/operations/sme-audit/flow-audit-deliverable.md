---
title: SME Audit Deliverable Flow
---

# SME Audit Deliverable Flow

> Full SME Audit System production flow — produces a complete 2-week operational audit deliverable for a small/medium business in a single agent run.

**Type:** Flow
**Domain:** Operations
**Vertical:** SME Audit
**Version:** v1.0.0
**Last tested:** 2026-06-03
**Cost per run:** ~$0.54 (Apify + DeepSeek + Gemini + Resend + Airtable)

[:material-github: Source on GitHub](https://github.com/ah-alhawar/agentcraft/blob/main/canon/operations/sme-audit/flow-audit-deliverable/) · [Drive canon](https://drive.google.com/) · [CHANGELOG](https://github.com/ah-alhawar/agentcraft/blob/main/canon/operations/sme-audit/flow-audit-deliverable/CHANGELOG.md)

## Trigger prompts

```text
flow-audit-deliverable: client = "Al Mansoori Drilling Services", tier = Standard.
```

```text
Run the SME audit flow on https://www.almansoori-drilling.ae. Engagement tier: Premium.
```

```text
I just signed a $3K SME audit engagement with [client name]. Build the full deliverable package.
```

## What it produces

A complete audit package in a dated client folder, plus a chat summary.

### Output structure

```
~/clients/<slug>-<date>/
├── 00-EXEC-SUMMARY.md      ← one-pager for the client
├── 01-intake.md            ← intake form + auto-pulled data
├── 02-bmc.md               ← 9-block Business Model Canvas
├── 03-pestel-forces.md     ← PESTEL + Porter's 5-Forces
├── 04-gap-analysis.md      ← 12 functional areas, heatmap + table
├── 05-roadmap.md           ← 90-day roadmap (Gantt-style)
├── 06-vendors.md           ← vendor shortlist per top gap
├── 07-package/
│   ├── audit-report.pdf    ← compiled, branded
│   ├── dashboard.html      ← interactive
│   └── cover-hero.png      ← 16:9 Gemini-generated cover
└── DELIVERY-LOG.md         ← sent timestamps, Airtable IDs
```

### Chat summary (after run)

```text
✅ SME Audit Complete — Al Mansoori Drilling Services LLC

Top 3 findings:
  1. No digital QA tracking; QMS docs on paper (HIGH, 5.5 maturity delta)
  2. No procurement approval workflow (HIGH, 4.2 delta)
  3. No customer feedback loop (MEDIUM, 3.0 delta)

Recommended next step: 30-min call to walk through the package
Pricing for follow-on: $5K implementation (90-day roadmap delivery)

Full deliverable: ~/clients/almansoori-drilling-2026-06-03/
```

## Inputs

1. **Client** — name + website URL (or just name if the agent will find it)
2. **Vertical** — auto-detect or specify
3. **Geography** — for vendor + regulatory context (default: UAE)
4. **Engagement tier** — Express ($1.5K) / Standard ($3K) / Premium ($7.5K)
5. **Existing data** — any prior notes, Airtable records, emails (optional)

## Tool stack (all from `~/.hermes/.env`)

| Tool | Use | Env var |
|---|---|---|
| Apify | Website crawl, social scrape, employee count | `APIFY_TOKEN` |
| Exa | Industry research, competitor intel | (in `web_search_plus`) |
| DeepSeek | Synthesis + scoring + narrative | `DEEPSEEK_API_KEY` |
| Gemini | Hero image for report cover | `GEMINI_API_KEY` |
| Resend | Deliverable email to client | `RESEND_API_KEY` |
| Airtable | CRM record + engagement tracking | `AIRTABLE_API_KEY` |

## Workflow (8 stages, ~30 min wall clock)

| # | Stage | Time | What happens |
|---|---|---|---|
| 1 | Intake | 2 min | Auto-pull website, LinkedIn, reviews, employee count, revenue band |
| 2 | Business Model Canvas | 5 min | DeepSeek generates 9-block BMC, cross-references public data |
| 3 | PESTEL + 5-Forces | 5 min | Industry scan, competitive intensity |
| 4 | Gap Analysis | 8 min | 12 functional areas, scored 0-5, top 5 gaps identified |
| 5 | 90-Day Roadmap | 5 min | Quick wins (W1-2), medium (W3-6), strategic (W7-12) |
| 6 | Vendor Shortlist | 3 min | 2-3 vendors per top gap (regional + international) |
| 7 | Package | 2 min | Stitch to `00-EXEC-SUMMARY.md`, hero image, HTML dashboard |
| 8 | Delivery | 1 min | Airtable record, Resend email, log |

## Source files

| File | Path | Version |
|---|---|---|
| Source flow design | `drive/00-canon/operations/sme-audit/00-flow-audit-deliverable-v1.0.0-2026-06-03.md` | v1.0.0 |
| Lead skill | `canon/operations/sme-audit/flow-audit-deliverable/SKILL.md` | v1.0.0 |
| CHANGELOG | `canon/operations/sme-audit/flow-audit-deliverable/CHANGELOG.md` | v1.0.0 |
| Public skill | `skills/skill-flow-audit-deliverable/SKILL.md` | v1.0.0 |

## Install

```bash
# Drop the skill into your Hermes skills folder
git clone https://github.com/ah-alhawar/agentcraft
cp -r agentcraft/skills/skill-flow-audit-deliverable/ ~/.hermes/skills/

# Restart Hermes (or /reload-skills in-session)

# Then paste a trigger prompt:
flow-audit-deliverable: client = "Your Client", tier = Standard.
```

## Version + last tested

- **v1.0.0** — released 2026-06-03
- Last tested: 2026-06-03 against a mock HVAC contractor in Abu Dhabi. All 8 stages completed; cost ~$0.52.

## Cost estimate (per audit)

- Apify: ~$0.30 (4 scrapes)
- DeepSeek: ~$0.15 (all synthesis calls)
- Gemini: ~$0.04 (cover image)
- Exa (via `web_search_plus`): ~$0.05
- **Total: ~$0.54 per audit** (vs $3K-$7.5K billed to client)

## Failover

| Failure | Fallback |
|---|---|
| Apify down | Use `web_extract_plus` for website + manual LinkedIn lookup |
| DeepSeek quota | Fall back to Gemini Flash (same cost tier) |
| Resend auth fail | Generate email draft in markdown, save locally |
| Gemini image fail | Skip cover, use text-only deliverable |

## Known limitations

- Single org per run; multi-org rollups are a future flow
- Dashboard is interactive HTML only — no PDF print stylesheet
- Mock intake data when sources are sparse; flagged in deliverables

---

[← Operations](../../index.md) · [Library](../../index.md) · [Home](../../../index.md)
