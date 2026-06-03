---
name: skill-fishbone
description: Generate a Fishbone (Ishikawa) cause-and-effect diagram from a problem statement and 3-6 cause categories. Produces a publication-quality SVG with the problem at the head, category branches (the "bones"), and individual causes as sub-branches. Use this skill whenever the user says "fishbone", "Ishikawa", "cause-and-effect", "root cause analysis", or asks to "structure the causes of [problem]". Pairs with the DMAIC Analyze phase and the 5-Whys technique.
version: 1.0.0
last_tested: 2026-06-03
metadata:
  hermes:
    tags: [operations, lss, quality, root-cause, analysis]
    source_drive: 00-canon/operations/lss/fishbone-skill/00-fishbone-v1.0.0-2026-06-03.md
    public_slug: library/operations/lss/fishbone
  context:
    user:
      name: "Aiham Alhawar"
      role: "O&G quality / LSS Green Belt"
      voice: "Direct. Bullets > prose. Cite 5-Whys explicitly."
    domain:
      primary: "Lean Six Sigma, root cause analysis"
      tools_available: [python3, gemini]
    last_used:
      runs: 0
---

# Skill: Fishbone (Ishikawa) Diagram Generator

A Fishbone diagram is a structured way to brainstorm root causes of a problem. The problem sits at the head of the fish; cause categories branch off the spine (the classic 6M: Man, Machine, Material, Method, Measurement, Environment); individual causes attach to the category bones.

## Trigger prompts (copy any)

```
Generate a fishbone diagram for: "NPT on cementing operations exceeded target by 77%".
```

```
Build an Ishikawa for: "API Q1 audit found 17 HIGH-severity findings". Use 6M categories.
```

```
Use skill-fishbone on the problem: "Weld porosity in Block 4 pipe welds (12 incidents in 30 days)".
```

## What it produces

A publication-quality SVG file with:

- The problem statement as the "head" (right side of the fish)
- 3-6 cause categories (default: 6M — Man, Machine, Material, Method, Measurement, Environment; customisable)
- 2-5 individual causes per category
- Color-coded bones (orange = material, blue = method, etc.)
- Title + date stamp

## Inputs (YAML or JSON)

```yaml
problem: "NPT on cementing operations exceeded target by 77%"
categories:
  - name: "Man (People)"
    causes:
      - "Crew experience varies across shifts"
      - "Limited IWCF L4 coverage for night ops"
  - name: "Machine (Equipment)"
    causes:
      - "Cement unit #3 has recurring pressure sensor drift"
      - "Recirculating mixer wear above spec"
  - name: "Material"
    causes:
      - "Class G cement lot inconsistency from supplier"
      - "Anti-gas additive settling in storage"
  - name: "Method (Process)"
    causes:
      - "Pre-job checklist skipped on rushed operations"
      - "Pump schedule not adjusted for BHCT"
  - name: "Measurement"
    causes:
      - "Pressure test results not recorded in real time"
      - "Lab thickening-time tests don't match field conditions"
  - name: "Environment"
    causes:
      - "Ambient temps >40°C affect additive performance"
      - "Well site layout causes long hose runs"
```

The canonical script is in `canon/operations/lss/fishbone-skill/fishbone.py`.

## Output sample (SVG)

The script writes a self-contained SVG (no external fonts, no JS, no images) that can be embedded in a markdown report, opened in a browser, or converted to PNG via `rsvg-convert` or Inkscape.

## Files

- `fishbone.py` — the canonical script (stdlib only, pure Python)
- `inputs.example.yaml` — example Well A-12 NPT problem
- `CHANGELOG.md` — version history
- `00-fishbone-v1.0.0-2026-06-03.md` — source methodology doc (in Drive canon)

## Install

```bash
python3 canon/operations/lss/fishbone-skill/fishbone.py \
  --input inputs.example.yaml \
  --output fishbone.svg
```

No installs needed.

## Last tested

2026-06-03 — generated fishbone for "Reduce cementing NPT on Well A-12" with 6M categories; output is a 1100x800 SVG, 18 causes across 6 bones, renders cleanly in browser.
