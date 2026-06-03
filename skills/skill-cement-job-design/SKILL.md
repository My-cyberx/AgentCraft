---
name: skill-cement-job-design
description: Generate a complete cementing job design from a well spec — volumes, materials, pump schedule, BHCT, contact time. Use this skill whenever the user says "cement job design", "cementing job", "pump schedule", "slurry volume", "Class G cement", or attaches a well spec and asks for the cement program. Pairs with the IWCF L4 well kill method.
version: 1.0.0
last_tested: 2026-06-03
metadata:
  hermes:
    tags: [drilling, upstream, cementing, job-design]
    source_drive: 00-canon/drilling/upstream/cement-job-design/00-cement-job-design-v1.0.0-2026-06-03.pdf
    public_slug: library/drilling/upstream/cement-job-design
  context:
    user:
      name: "Aiham Alhawar"
      role: "O&G drilling engineer, 9 yr Weatherford + ADNOC cementing experience"
      voice: "Direct, technical. Cite IWCF L4 + API 10A. No marketing fluff."
    domain:
      primary: "Drilling, cementing, completions"
      standards_in_force: ["API 10A", "API 65-2", "IWCF L4", "ISO 10426"]
      tools_available: [python3, deepseek]
    last_used:
      runs: 0
---

# Skill: Cement Job Design

Wraps `cement_job_design.py` (the canonical script) with the user-information block above.

## Trigger prompts (copy any)

```
Run cement_job_design.py on inputs.yaml for Well B-7.
```

```
Design a cementing job for: 9.625" casing, 12,500 ft TD, 10.5 ppg mud, 15% excess.
```

```
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

```
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

## Install

```bash
python3 canon/drilling/upstream/cement-job-design/cement_job_design.py \
  --input canon/drilling/upstream/cement-job-design/inputs.example.yaml
```

## Last tested

2026-06-03 — Well B-7, Block 5, 7" casing, 12,500 ft TD. Result: 490.6 bbl total slurry, 2,334 sacks, 92.5 bbl annular + 374.7 bbl casing. All validation checks passed.
