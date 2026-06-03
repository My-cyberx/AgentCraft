---
title: LSS DMAIC Template
---

# LSS DMAIC Template

> Generate a complete Lean Six Sigma Green Belt DMAIC project template from a problem description — Define, Measure, Analyze, Improve, Control.

**Type:** Script
**Domain:** Operations
**Vertical:** LSS (Lean Six Sigma — Green Belt)
**Version:** v1.0.0
**Last tested:** 2026-06-03
**Cost per run:** Free (Python stdlib only)

[:material-github: Source on GitHub](https://github.com/My-cyberx/AgentCraft/blob/main/canon/operations/lss/dmaic-template/) · [Drive canon](https://drive.google.com/) · [CHANGELOG](https://github.com/My-cyberx/AgentCraft/blob/main/canon/operations/lss/dmaic-template/CHANGELOG.md)

## Trigger prompts

```text
Generate a DMAIC project template for: "Reduce NPT on Well A-12 cementing operations".
```

```text
Use skill-dmaic-template on the attached problem statement.
```

```text
Build a Green Belt DMAIC for: weld porosity in Block 4 pipe welds.
```

## What it produces

A full D-M-A-I-C project template as markdown (114 lines for the example), with sections:

- **Define** — problem statement, SIPOC, VOC, charter (scope in/out, team, timeline)
- **Measure** — key metrics, baseline, data collection plan
- **Analyze** — Fishbone (links to `skill-fishbone`), 5 Whys, hypothesis test
- **Improve** — pilot solution, rollout plan
- **Control** — control plan, sustainment checklist, lessons learned
- **Sign-off** — owner / process owner / sponsor / LSS MBB

## Inputs (YAML or JSON)

```yaml
project_name: "Reduce NPT on Well A-12 Cementing Operations"
owner: "Aiham Alhawar, Operations Manager"
problem_statement: "Non-productive time (NPT) on the A-12 cementing job was 14.2 hours over the last 6 months, exceeding the 8-hour project target by 77%."
goal: "Reduce cementing-related NPT to ≤4 hours per well within 6 months (50% reduction)"
sipoc_suppliers:
  - "Cement service company"
  - "Mud engineering"
  - "Drilling crew"
voc:
  - "Operations manager: 'We lose time waiting on cement tests that come back inconsistent'"
  - "Cementer: 'Lab results don't match field conditions, especially with high-temp wells'"
team: "Aiham (lead), cementing engineer, mud engineer, drilling supervisor, lab tech"
scope_in: "Cementing operations on Well A-12 and similar Block 5 wells (depth 10,000-13,000 ft)"
scope_out: "Other wells in different blocks, drilling-only NPT, completions NPT"
timeline: "12 weeks (Aug-Oct 2026)"
key_metrics:
  - "Cementing NPT hours per well (target ≤ 4)"
  - "First-time pressure test pass rate (target ≥ 95%)"
  - "Cement job quality (bond log, compressive strength) — no regression"
```

## Install

```bash
python3 canon/operations/lss/dmaic-template/dmaic.py \
  --input canon/operations/lss/dmaic-template/problem.example.yaml \
  --output dmaic-project.md
```

No installs needed.

## Source files

| File | Path | Version |
|---|---|---|
| Source template | `drive/00-canon/operations/lss/dmaic-template/00-dmaic-template-v1.0.0-2026-06-03.md` | v1.0.0 |
| Canonical script | `canon/operations/lss/dmaic-template/dmaic.py` | v1.0.0 |
| Example problem | `canon/operations/lss/dmaic-template/problem.example.yaml` | v1.0.0 |
| CHANGELOG | `canon/operations/lss/dmaic-template/CHANGELOG.md` | v1.0.0 |

## Version + last tested

- **v1.0.0** — released 2026-06-03
- Last tested: 2026-06-03 against "Reduce NPT on Well A-12" problem. Result: 114-line markdown template, all 5 phases populated.

## Known limitations

- No statistical engine (t-tests, ANOVA) — describe the test, don't run it.
- Pair with `skill-pareto` for the M-phase analysis.

---

[← Operations](../../index.md) · [Library](../../index.md) · [Home](../../../index.md)
