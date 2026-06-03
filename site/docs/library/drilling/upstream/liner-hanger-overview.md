---
title: Liner Hanger Overview Flow
---

# Liner Hanger Overview Flow

> Convert a liner hanger technical deck (PPTX or PDF) into a modern, deployment-ready HTML microsite with interactive sections, technical diagrams, and a one-page operator cheat sheet.

**Type:** Flow
**Domain:** Drilling
**Vertical:** Upstream
**Version:** v1.0.0
**Last tested:** 2026-06-03
**Cost per run:** ~$0.16 (Gemini + DeepSeek + Vercel free tier)

[:material-github: Source on GitHub](https://github.com/My-cyberx/AgentCraft/blob/main/canon/drilling/upstream/liner-hanger-overview/) · [Drive canon](https://drive.google.com/) · [CHANGELOG](https://github.com/My-cyberx/AgentCraft/blob/main/canon/drilling/upstream/liner-hanger-overview/CHANGELOG.md)

## Trigger prompts

```text
flow-liner-hanger-overview: source=00-liner-hanger-overview-v2.0.0-2026-04-12.pptx, audience=drilling-engineers
```

```text
Convert the liner hanger deck to a website.
```

```text
Build a tech overview microsite for the new hydraulic liner hanger system.
```

## What it produces

A deployed, shareable microsite with the AgentCraft design system applied:

- Hero with product name + one-line value prop
- Specs (casing sizes, pressures, temperatures)
- Operating envelope (depth, deviation, formation type)
- 3 case studies (default: from the source deck)
- FAQ
- Contact / download
- Lighthouse: ~99 perf, 100 SEO/A11y

### Output

```
✓ Live at https://liner-hanger-<slug>.vercel.app

Built in 12m 30s | Cost: $0.16
Lighthouse: 99/100 (Perf), 100/100 (SEO, A11y)
```

## Inputs

1. **Source** — PPTX or PDF (the original deck)
2. **Audience** — drilling engineers (technical) / procurement (commercial) / management (executive)
3. **Branding** — optional: logo, color palette
4. **URL** — default: `liner-hanger.<your-domain>.vercel.app`

## Workflow (7 stages, ~15 min wall clock)

| # | Stage | Time | What happens |
|---|---|---|---|
| 1 | Source extraction | 1 min | `python-pptx` parses PPTX; `pymupdf` parses PDF |
| 2 | IA + outline | 1 min | Map slides → 7 sections (hero / specs / envelope / cases / FAQ / contact) |
| 3 | Copy generation | 3 min | DeepSeek rewrites for target audience, keeps specs exact |
| 4 | Design system | 1 min | Apply `frontend-design` skill — bold typography, color tokens |
| 5 | Build | 3 min | Next.js 14 + Tailwind + shadcn/ui |
| 6 | Deploy | 1 min | `vercel deploy --prod` |
| 7 | Hand-off | 1 min | GitHub repo, README, owner credentials handed off |

## Tool stack

| Tool | Use | Env var |
|---|---|---|
| `python-pptx` | PPTX parsing | (pip install) |
| `pymupdf` | PDF parsing | (pip install) |
| DeepSeek | Copy generation | `DEEPSEEK_API_KEY` |
| Gemini | Images (hero, section visuals) | `GEMINI_API_KEY` |
| Vercel | Deploy | `VERCEL_API_KEY` |
| frontend-design skill | Aesthetic direction | n/a |

## Source files

| File | Path | Version |
|---|---|---|
| Source flow design | `drive/00-canon/drilling/upstream/liner-hanger-overview/00-liner-hanger-overview-v1.0.0-2026-06-03.md` | v1.0.0 |
| Lead skill | `canon/drilling/upstream/liner-hanger-overview/SKILL.md` | v1.0.0 |
| CHANGELOG | `canon/drilling/upstream/liner-hanger-overview/CHANGELOG.md` | v1.0.0 |
| Public skill | `skills/skill-liner-hanger-overview/SKILL.md` | v1.0.0 |

## Install

```bash
# Drop the flow into your Hermes skills folder
cp -r skills/skill-liner-hanger-overview/ ~/.hermes/skills/
# /reload-skills

# Then paste a trigger prompt
flow-liner-hanger-overview: source=00-liner-hanger-overview-v2.0.0-2026-04-12.pptx, audience=drilling-engineers
```

## Cost estimate

- Gemini (images): ~$0.10
- DeepSeek (copy): ~$0.06
- Vercel (free tier): $0
- **Total: ~$0.16 per microsite**

## Failover

| Failure | Fallback |
|---|---|
| PPTX parse fail | Fall back to PDF (`pymupdf`) |
| DeepSeek quota | Gemini Flash for copy |
| Vercel deploy fail | Zip the .next/ + source for manual deploy |
| Domain DNS not propagated | Ship on `*.vercel.app` |

## Known limitations

- No multi-deck rollup yet.
- Custom branding requires manual edit of design tokens.

---

[← Drilling](../index.md) · [Library](../../index.md) · [Home](../../../index.md)
