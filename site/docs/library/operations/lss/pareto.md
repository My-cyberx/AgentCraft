---
title: Pareto Chart Generator
---

# Pareto Chart Generator

> Read a CSV of issues and produce a ranked Pareto chart (bars + cumulative % line) as a self-contained SVG.

**Type:** Script
**Domain:** Operations
**Vertical:** LSS
**Version:** v1.0.0
**Last tested:** 2026-06-03
**Cost per run:** Free (Python stdlib only)

[:material-github: Source on GitHub](https://github.com/My-cyberx/AgentCraft/blob/main/canon/operations/lss/pareto-script/) · [Drive canon](https://drive.google.com/) · [CHANGELOG](https://github.com/My-cyberx/AgentCraft/blob/main/canon/operations/lss/pareto-script/CHANGELOG.md)

## Trigger prompts

```text
Generate a Pareto chart from issues.csv, count the "Defect" column, output to pareto.svg.
```

```text
Use skill-pareto on the attached Q2 defect log, top 10 only.
```

```text
Build a Pareto for "Equipment failure modes" — count column, output to chart.svg.
```

## What it produces

A self-contained SVG (no JS, no external fonts) with:

- Bars sorted by count, descending
- Cumulative % line (blue) with markers
- 80/20 line (subtle)
- Y-axis: count (left) and cumulative % (right)
- X-axis: category labels (truncated to 18 chars, rotated 30°)
- Title + total count

Plus an ASCII summary to stdout for quick review.

### Sample ASCII output — Q2 2026 pipeline defects

```text
Pipeline Defects — Q2 2026 — top categories:
      6   24.0%  ██████████████████████████████ Valve leak
      4   40.0%  ████████████████████ Weld porosity
      2   48.0%  ██████████ Surface corrosion
      2   56.0%  ██████████ Pipe dent
      2   64.0%  ██████████ Coating failure
      2   72.0%  ██████████ Improper torque
      2   80.0%  ██████████ Operator error
      2   88.0%  ██████████ Material defect
      1   92.0%  █████ Misalignment
      1   96.0%  █████ Thread damage
```

## Inputs

```csv
Defect,Date,Location
Weld porosity,2026-05-01,Block 4
Valve leak,2026-05-02,Block 5
...
```

The `--column` flag specifies which column to count. Use `--top N` to limit categories.

## Install

```bash
python3 canon/operations/lss/pareto-script/pareto.py \
  --input canon/operations/lss/pareto-script/issues.example.csv \
  --column "Defect" \
  --output pareto.svg \
  --title "Pipeline Defects — Q2 2026"
```

No installs needed.

## Source files

| File | Path | Version |
|---|---|---|
| Source CSV spec | `drive/00-canon/operations/lss/pareto-script/00-pareto-v1.0.0-2026-06-03.csv` | v1.0.0 |
| Canonical script | `canon/operations/lss/pareto-script/pareto.py` | v1.0.0 |
| Example CSV | `canon/operations/lss/pareto-script/issues.example.csv` | v1.0.0 |
| CHANGELOG | `canon/operations/lss/pareto-script/CHANGELOG.md` | v1.0.0 |

## Version + last tested

- **v1.0.0** — released 2026-06-03
- Last tested: 2026-06-03 against the Q2 2026 example CSV (25 defects, 11 categories). Result: **6.4 KB SVG**, Valve leak = #1 (24% of all defects), Weld porosity = #2 (40% cumulative).

## Known limitations

- SVG only (no PNG export built-in; use `rsvg-convert` or Inkscape to convert).
- No date-range filtering (filter the CSV first).

## Pairs with

- [`skill-dmaic-template`](dmaic-template.md) — Use Pareto in the M/A phase of DMAIC.
- [`skill-fishbone`](fishbone.md) — Use the vital-few from Pareto as the bones of your fishbone.

---

[← Operations](../../index.md) · [Library](../../index.md) · [Home](../../../index.md)
