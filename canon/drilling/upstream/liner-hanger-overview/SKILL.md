---
name: flow-liner-hanger-overview
description: Convert a liner hanger technical deck (PPTX or PDF) into a modern, deployment-ready HTML microsite with interactive sections, technical diagrams, and a one-page operator cheat sheet. Use this skill whenever the user says "rebuild the liner hanger deck as a website", "convert the PPTX to a landing page", "build a tech overview for [product]", or "I need a sharable URL for this presentation". Built on the AgentCraft frontend-design aesthetic (no Inter font, no purple gradients, no AI slop).
version: 1.0.0
last_tested: 2026-06-03
metadata:
  hermes:
    tags: [drilling, upstream, flow, presentation, build-website]
    source_drive: 00-canon/drilling/upstream/liner-hanger-overview/00-liner-hanger-overview-v1.0.0-2026-06-03.md
    public_slug: library/drilling/upstream/liner-hanger-overview
    requires_env: [GEMINI_API_KEY, DEEPSEEK_API_KEY, VERCEL_API_KEY]
  context:
    user:
      name: "Aiham Alhawar"
      role: "O&G drilling engineer, 9 yr Weatherford + ADNOC liner hanger experience"
      voice: "Technical, specific. No marketing fluff. Cite specs and well numbers."
    domain:
      primary: "Drilling, liner hangers, completions"
      tools_available: [python3, deepseek, gemini, vercel]
    last_used:
      runs: 0
---

# Flow: Liner Hanger Overview — PPTX → Live Microsite

A flow that turns a static technical deck into a deployed, shareable microsite with the AgentCraft design system.

## When to use

- "Convert the liner hanger deck to a website"
- "Build a tech overview microsite for [product/system]"
- "I need a sharable URL for the field"
- "Make the PPTX accessible to non-engineers (procurement, management)"

## Inputs

1. **Source** — PPTX or PDF (the original deck)
2. **Audience** — drilling engineers (technical) / procurement (commercial) / management (executive)
3. **Branding** — optional: logo, color palette
4. **URL** — default: `liner-hanger.<your-domain>.com`

## Workflow (7 stages, ~15 min wall clock)

### Stage 1: Source extraction
- Parse PPTX via `python-pptx` (or PDF via `pymupdf`)
- Extract: titles, body text, tables, images, speaker notes
- Output: structured `slides.json`

### Stage 2: IA + outline
- Map slides to microsite sections
- Default IA: Hero → Specs → Operating envelope → Case studies → FAQ → Contact
- Output: `outline.md`

### Stage 3: Copy generation (DeepSeek)
- Rewrite technical copy for the target audience
- Keep specs, equations, drawings exact
- Strip vendor-speak

### Stage 4: Design system
- Apply `frontend-design` skill → bold typography pairing
- Color tokens (CSS variables)
- Spacing, radius, shadow scale

### Stage 5: Build
- Next.js 14 (App Router) + Tailwind + shadcn/ui
- One section per slide
- Embed original diagrams (SVG conversion for vector; PNG fallback)

### Stage 6: Deploy
- `vercel deploy --prod` to a Vercel project
- Custom domain wired (if provided)

### Stage 7: Hand-off
- GitHub repo with source
- README with deploy instructions
- Owner credentials (NEVER auto-store)

## Output

```
✓ Live at https://liner-hanger-<slug>.vercel.app

Built in 12m 30s | Cost: $0.18 (Gemini images + DeepSeek copy)
Lighthouse: 99/100 (Perf), 100/100 (SEO, A11y)
```

## Example

Source: `00-liner-hanger-overview-v2.0.0-2026-04-12.pptx` (28 slides, Weatherford)

Run:
```
flow-liner-hanger-overview: source=00-liner-hanger-overview-v2.0.0-2026-04-12.pptx, audience=drilling-engineers
```

Output: 7-section microsite with technical specs, operating envelope, 3 case studies from ADNOC wells, embedded diagrams.

## Failover

- **PPTX parse fail**: fall back to PDF
- **DeepSeek quota**: use Gemini Flash for copy
- **Vercel deploy fail**: zip the .next/ + source for manual deploy
- **Domain DNS not propagated**: ship on `*.vercel.app`

## Cost

- Gemini (images): ~$0.10
- DeepSeek (copy): ~$0.06
- Vercel (free tier): $0
- **Total: ~$0.16 per microsite**

## Files

- `00-liner-hanger-overview-v1.0.0-2026-06-03.md` — flow design (Drive canon)
- `CHANGELOG.md` — version history
