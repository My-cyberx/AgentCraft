---
name: skill-depro-calc
description: Calculate Daily Equivalent Production Offline (DEPRO) for a well using the canonical AgentCraft formula and run a Monte Carlo uncertainty band. Use this skill whenever the user says "calculate DEPRO", "well availability", "production efficiency", "what's the downtime cost", or attaches a well events log. Loads the `depro_calc.py` script + the source PDF + your voice.
version: 3.2.1
last_tested: 2026-06-03
metadata:
  hermes:
    tags: [drilling, upstream, depro, production-engineering]
    source_drive: 00-canon/drilling/upstream/depro-calc/00-depro-formula-v3.2.1-2026-06-03.pdf
    public_slug: library/drilling/upstream/depro-calc
  context:
    user:
      name: "Aiham Alhawar"
      role: "O&G production / drilling engineer"
      geography: "Abu Dhabi, UAE"
      voice: "Direct, execution-first. Numbers > narrative."
    domain:
      primary: "Upstream drilling, well performance"
      tools_available: [python3, deepseek, gemini]
    last_used:
      runs: 0
---

# Skill: DEPRO Calculator

Wraps `depro_calc.py` (the canonical script) with:
- The user-information block above (so the agent knows your voice + tools)
- The source PDF reference (so the agent can ground any explanation in the formula)
- A standard 3-step invocation: validate input → run script → format output

## Trigger prompts (copy any)

```
Run depro_calc.py on inputs.yaml for Well A-12.
```

```
Calculate DEPRO for the attached well events with 1000 MC runs and output JSON.
```

```
What's the DEPRO for Q1 2026? Use the events I pasted above.
```

## What it produces

A text report (default) or JSON (with `--json`) showing:

- Design rate, productive hours, downtime hours, availability %
- Actual production (bbl over the window)
- **DEPRO (bopd)** — the headline number
- Monte Carlo P10/P50/P90 + mean ± stdev (if `--mc-runs > 0`)

Example output (Well A-12, Q1 2026):

```
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
============================================================
```

## Inputs

- `--input <path>` — YAML or JSON file matching `inputs.example.yaml` shape
- `--mc-runs N` — Monte Carlo runs (0 = skip, 1000 = default if requested)
- `--json` — output machine-readable JSON instead of text
- `--output <path>` — write XLSX (requires `openpyxl`); falls back to JSON

## Files

- `depro_calc.py` — the canonical script (stdlib only, runnable)
- `inputs.example.yaml` — example Well A-12 Q1 2026 input
- `CHANGELOG.md` — version history
- `00-depro-formula-v3.2.1-2026-06-03.pdf` — source PDF reference (in Drive canon)

## Install

```bash
# No install — the script is stdlib only
python3 depro_calc.py --input inputs.example.yaml
```

## Last tested

2026-06-03 against the Well A-12 Q1 2026 events log. Result: 3,962.78 bopd DEPRO, 94.35% availability, MC P10/P90 = [3,957 / 3,968] bopd.
