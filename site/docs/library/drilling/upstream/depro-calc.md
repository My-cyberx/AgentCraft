---
title: DEPRO Calculator
---

# DEPRO Calculator

> Calculate Daily Equivalent Production Offline (DEPRO) for an oil/gas well using the canonical AgentCraft formula and run a Monte Carlo uncertainty band.

**Type:** Script
**Domain:** Drilling
**Vertical:** Upstream
**Version:** v3.2.1
**Last tested:** 2026-06-03
**Cost per run:** Free (Python stdlib only)

[:material-github: Source on GitHub](https://github.com/ah-alhawar/agentcraft/blob/main/canon/drilling/upstream/depro-calc/) · [Drive canon PDF](https://drive.google.com/) · [CHANGELOG](https://github.com/ah-alhawar/agentcraft/blob/main/canon/drilling/upstream/depro-calc/CHANGELOG.md)

## Trigger prompts

```text
Run depro_calc.py on inputs.yaml for Well A-12.
```

```text
Calculate DEPRO for the attached well events with 1000 MC runs and output JSON.
```

```text
What's the DEPRO for Q1 2026? Use the events I pasted above.
```

## What it produces

A text report (default) or JSON (with `--json`) showing:

- Design rate, productive hours, downtime hours, availability %
- Actual production (bbl over the window)
- **DEPRO (bopd)** — the headline number
- Monte Carlo P10/P50/P90 + mean ± stdev (if `--mc-runs > 0`)

### Sample output — Well A-12, Q1 2026

```text
============================================================
  DEPRO Report — Well A-12
============================================================
  Design rate:              4,200 bopd
  Analysis window:        2,160.0 hours
  Productive hours:      2,038.00
  Downtime hours:          122.00
  Availability:             94.35 %
  Actual production:    8,559,600 bbl
  Downtime events:              4
------------------------------------------------------------
  DEPRO:                 3,962.78 bopd
============================================================

  Monte Carlo (1000 runs):
    Mean:     3,962.70 bopd
    Stdev:        4.20 bopd
    P10:      3,957.08 bopd
    P50:      3,962.70 bopd
    P90:      3,968.27 bopd
    Range:  [3,952.82, 3,972.60]
============================================================
```

## Inputs

- `--input <path>` — YAML or JSON well events file (YAML shape: `name`, `design_rate_bopd`, `analysis_window_hours`, `events: [...]`)
- `--mc-runs N` — Monte Carlo runs (0 = skip, 1000 = recommended)
- `--seed N` — MC random seed for reproducibility (default: 42)
- `--json` — output machine-readable JSON
- `--output <path>` — write XLSX (requires `openpyxl`; falls back to JSON)

### Example input

```yaml
name: "Well A-12"
design_rate_bopd: 4200
analysis_window_hours: 2160

events:
  - start: "2026-01-15T08:00:00"
    end:   "2026-01-17T14:00:00"
    reason: "ESP failure - pulled and replaced"
    error_hours: 2.0
  - start: "2026-02-21T11:00:00"
    end:   "2026-02-23T19:00:00"
    reason: "flowline leak - hot tap repair"
    error_hours: 3.0
```

## Source files

| File | Path | Version |
|---|---|---|
| Source PDF | `drive/00-canon/drilling/upstream/depro-calc/00-depro-formula-v3.2.1-2026-06-03.pdf` | v3.2.1 |
| Canonical script | `canon/drilling/upstream/depro-calc/depro_calc.py` | v3.2.1 |
| Example input | `canon/drilling/upstream/depro-calc/inputs.example.yaml` | v3.2.1 |
| CHANGELOG | `canon/drilling/upstream/depro-calc/CHANGELOG.md` | v3.2.1 |
| Public skill | `skills/skill-depro-calc/SKILL.md` | v3.2.1 |

## Install

```bash
# No install — the script is stdlib only
git clone https://github.com/ah-alhawar/agentcraft
python3 agentcraft/canon/drilling/upstream/depro-calc/depro_calc.py \
  --input agentcraft/canon/drilling/upstream/depro-calc/inputs.example.yaml
```

## Version + last tested

- **v3.2.1** — released 2026-06-03
- Last tested: 2026-06-03 against the Well A-12 Q1 2026 events log. Result: **3,962.78 bopd DEPRO**, 94.35% availability, MC P10/P90 = [3,957 / 3,968] bopd.

## Known limitations

- Naive datetime parsing (assumes UTC, no DST handling)
- Single-well per run (multi-well aggregation is a future skill)
- No timezone-aware input — convert all timestamps to UTC before analysis

---

[← Drilling](../index.md) · [Library](../../index.md) · [Home](../../../index.md)
