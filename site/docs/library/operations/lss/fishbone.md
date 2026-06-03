---
title: Fishbone (Ishikawa) Diagram Generator
---

# Fishbone (Ishikawa) Diagram Generator

> Generate a Fishbone (Ishikawa) cause-and-effect diagram from a problem statement and 3-6 cause categories. Produces a publication-quality SVG.

**Type:** Skill (wraps a Python SVG generator)
**Domain:** Operations
**Vertical:** LSS
**Version:** v1.0.0
**Last tested:** 2026-06-03
**Cost per run:** Free (Python stdlib only)

[:material-github: Source on GitHub](https://github.com/My-cyberx/AgentCraft/blob/main/canon/operations/lss/fishbone-skill/) · [Drive canon](https://drive.google.com/) · [CHANGELOG](https://github.com/My-cyberx/AgentCraft/blob/main/canon/operations/lss/fishbone-skill/CHANGELOG.md)

## Trigger prompts

```text
Generate a fishbone diagram for: "NPT on cementing operations exceeded target by 77%".
```

```text
Build an Ishikawa for: "API Q1 audit found 17 HIGH-severity findings". Use 6M categories.
```

```text
Use skill-fishbone on the problem: "Weld porosity in Block 4 pipe welds (12 incidents in 30 days)".
```

## What it produces

A publication-quality SVG file with:

- Problem statement as the "head" (right side of the fish)
- 3-6 cause categories (default: 6M — Man, Machine, Material, Method, Measurement, Environment; customisable)
- 2-5 individual causes per category
- Color-coded bones (orange = material, blue = method, etc.)
- Title + date stamp
- **5.2 KB** SVG output, no JS, no external fonts, opens in any browser

## Inputs (YAML or JSON)

```yaml
problem: "NPT on cementing operations exceeded target by 77% (14.2h vs 8h budget over 6 months)"
categories:
  - name: "Man (People)"
    causes:
      - "Crew experience varies across shifts (IWCF L4 only on day shift)"
      - "Night-shift cementer callout delays average 90 min"
  - name: "Machine (Equipment)"
    causes:
      - "Cement unit #3 pressure sensor drift (last cal 14 months ago)"
      - "Recirculating mixer wear above manufacturer spec"
  - name: "Material"
    causes:
      - "Class G cement lot inconsistency (2 of 5 recent lots failed thickening time)"
      - "Anti-gas additive settling in storage tanks (no agitation log)"
  - name: "Method (Process)"
    causes:
      - "Pre-job checklist skipped on rushed operations (8 of 12 jobs)"
      - "Pump schedule not adjusted for actual BHCT — uses plan number"
  - name: "Measurement"
    causes:
      - "Pressure test results not logged in real time"
      - "Lab thickening-time tests run at 100°F, field BHCT often 180°F+"
  - name: "Environment"
    causes:
      - "Ambient temps >40°C affect additive performance"
      - "Well site layout forces 45m hose run, adds 8 min circulation time"
```

## Install

```bash
python3 canon/operations/lss/fishbone-skill/fishbone.py \
  --input canon/operations/lss/fishbone-skill/problem.example.yaml \
  --output fishbone.svg
```

No installs needed.

## Source files

| File | Path | Version |
|---|---|---|
| Source methodology | `drive/00-canon/operations/lss/fishbone-skill/00-fishbone-v1.0.0-2026-06-03.md` | v1.0.0 |
| Canonical script | `canon/operations/lss/fishbone-skill/fishbone.py` | v1.0.0 |
| Example problem | `canon/operations/lss/fishbone-skill/problem.example.yaml` | v1.0.0 |
| CHANGELOG | `canon/operations/lss/fishbone-skill/CHANGELOG.md` | v1.0.0 |

## Version + last tested

- **v1.0.0** — released 2026-06-03
- Last tested: 2026-06-03 — generated fishbone for "Reduce cementing NPT on Well A-12" with 6M categories. Result: **6 categories, 13 causes, 5.2 KB SVG**, renders cleanly in browser.

## Pairs with

- [`skill-dmaic-template`](dmaic-template.md) — Use Fishbone in the Analyze phase of a DMAIC project.
- [`skill-pareto`](pareto.md) — Use Pareto to identify the vital few causes to put on the fishbone.

---

[← Operations](../../index.md) · [Library](../../index.md) · [Home](../../../index.md)
