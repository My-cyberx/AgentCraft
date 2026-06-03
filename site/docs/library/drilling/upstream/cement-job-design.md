---
title: Cement Job Design
---

# Cement Job Design

> Generate a complete cementing job design from a well spec — volumes, materials, pump schedule, BHCT, contact time.

**Type:** Skill (wraps a Python script)
**Domain:** Drilling
**Vertical:** Upstream
**Version:** v1.0.0
**Last tested:** 2026-06-03
**Cost per run:** Free (Python stdlib only)

[:material-github: Source on GitHub](https://github.com/My-cyberx/AgentCraft/blob/main/canon/drilling/upstream/cement-job-design/) · [Drive canon PDF](https://drive.google.com/) · [CHANGELOG](https://github.com/My-cyberx/AgentCraft/blob/main/canon/drilling/upstream/cement-job-design/CHANGELOG.md)

## Trigger prompts

```text
Run cement_job_design.py on inputs.yaml for Well B-7.
```

```text
Design a cementing job for: 9.625" casing, 12,500 ft TD, 10.5 ppg mud, 15% excess.
```

```text
What's the lead/tail split, sacks required, and pump schedule for the cement job?
```

## What it produces

A text report (default) or JSON showing:

- Open interval (TOC to TD)
- Annular volume (open hole)
- Casing volume (surface to TOC)
- Total slurry (with 5% circulation loss)
- 70/30 lead/tail split
- Sacks required, mix water, additives (gal)
- Displacement volume
- Pump schedule (3 stages)
- Estimated BHCT, contact time

### Sample output — Well B-7 (Block 5, ADNOC Onshore)

```text
============================================================
  CEMENT JOB DESIGN — Well B-7 (Block 5, ADNOC Onshore)
============================================================
  Open interval:                 3000 ft

  Volumes:
    Annular (open hole):         92.5 bbl
    Casing (to TOC):            374.7 bbl
    Total slurry:               490.6 bbl

  Lead / Tail split (70/30):
    Lead:                       343.4 bbl
    Tail:                       147.2 bbl

  Materials:
    Cement sacks:                2334 sk
    Mix water:                  11905 gal
    retarder:                    131.7 gal
    anti-gas migration:          105.4 gal
============================================================
```

## Inputs (YAML or JSON)

```yaml
well_name: "Well B-7 (Block 5, ADNOC Onshore)"
casing_od_in: 7.0
casing_id_in: 6.366
hole_td_ft: 12500
open_hole_in: 8.75
inclination_deg: 12.0
mud_weight_ppg: 10.5
fluid_loss_cc: 18
top_of_cement_ft: 9500
excess_pct: 15
cement_class: "Class G (HSR)"
cement_density_ppg: 15.8
cement_yield_ft3_per_sk: 1.18
water_gal_per_sk: 5.10
retarder_pct: 0.5
anti_gas_pct: 0.4
```

## Physical validation

The script validates:

- `casing_od_in < open_hole_in` (casing must fit in the hole)
- `casing_id_in < casing_od_in` (positive wall thickness)
- `top_of_cement_ft < hole_td_ft` (TOC above TD)

Fails loudly with a clear error message if any check fails.

## Source files

| File | Path | Version |
|---|---|---|
| Source PDF | `drive/00-canon/drilling/upstream/cement-job-design/00-cement-job-design-v1.0.0-2026-06-03.pdf` | v1.0.0 |
| Canonical script | `canon/drilling/upstream/cement-job-design/cement_job_design.py` | v1.0.0 |
| Example input | `canon/drilling/upstream/cement-job-design/inputs.example.yaml` | v1.0.0 |
| CHANGELOG | `canon/drilling/upstream/cement-job-design/CHANGELOG.md` | v1.0.0 |
| Public skill | `skills/skill-cement-job-design/SKILL.md` | v1.0.0 |

## Install

```bash
git clone https://github.com/My-cyberx/AgentCraft
python3 agentcraft/canon/drilling/upstream/cement-job-design/cement_job_design.py \
  --input agentcraft/canon/drilling/upstream/cement-job-design/inputs.example.yaml
```

## Version + last tested

- **v1.0.0** — released 2026-06-03
- Last tested: 2026-06-03 against Well B-7, Block 5, 7" casing, 12,500 ft TD. Result: **490.6 bbl total slurry, 2,334 sacks**, 92.5 bbl annular + 374.7 bbl casing. All validation checks passed.

## Known limitations

- Lead/tail split is hard-coded 70/30; configurable in source.
- No temperature model beyond simple geothermal estimate.
- No centralizer placement optimizer.

---

[← Drilling](../index.md) · [Library](../../index.md) · [Home](../../../index.md)
