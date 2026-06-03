---
name: skill-iwcf-l4-drill
description: Run a 30-minute IWCF Level 4 well control drill — the agent plays the examiner and walks you through kick detection, shut-in, circulation, and well kill procedures using industry-standard methodology (IADC, API). Use this skill whenever the user says "IWCF drill", "well control practice", "kick drill", "shut-in procedure", "driller's method", or "wait and weight method". Tracks your score across drills, identifies weak areas, and adapts question difficulty to your level.
version: 1.0.0
last_tested: 2026-06-03
metadata:
  hermes:
    tags: [hse, iwcf, iadc, well-control, training]
    source_drive: 00-canon/hse/iwcf-l4/drill/00-iwcf-l4-drill-v1.0.0-2026-06-03.md
    public_slug: library/hse/iwcf-l4/drill
  context:
    user:
      name: "Aiham Alhawar"
      role: "Drilling supervisor, IWCF L4 certified"
      geography: "Abu Dhabi, UAE"
      voice: "Direct, technical. Use IADC terminology correctly. Reference Driller's Method and Wait-and-Weight explicitly."
      brand_dislikes:
        - "Calling it 'the procedure' instead of 'Driller's Method' or 'Wait-and-Weight'"
        - "Skipping the soft shut-in step"
        - "Confusing strip and kill pressures"
    domain:
      primary: "Well control, drilling"
      standards_in_force: ["IWCF L4", "IADC Well Control Manual"]
      tools_available: [python3, deepseek]
    last_used:
      runs: 0
---

# Skill: IWCF L4 Well Control Drill

A 30-minute training drill that walks you through well control scenarios, scored against IWCF L4 methodology. The agent plays examiner; you play driller.

## Trigger prompts (copy any)

```
Start a 30-minute IWCF L4 well control drill on Driller's Method.
```

```
Use skill-iwcf-l4-drill. Scenario: kick detected at 8,500 ft on a 12.5 ppg mud, 9.5 ppg kick.
```

```
Quick drill: shut-in procedure + 5 strike questions on strip-and-kill pressures.
```

## What it produces

A scored drill session:

- 1 scenario (drilling / tripping / cementing)
- 6-10 strike questions (shut-in, strip, kill, circulate)
- 1 final essay question (well kill plan)
- Score: 0-100, broken down by topic
- Weak areas identified
- Recommendations for next drill

## Workflow (8 stages, ~30 min wall clock)

### Stage 1: Scenario setup
Agent proposes a scenario (depth, mud weight, kick type, casing, BOP config). User accepts or modifies.

### Stage 2: Kick detection
Ask: "What are the first 3 indicators of a kick on the rig floor?"
Score 0-3. Reference: pit gain, flowline temperature, return flow rate.

### Stage 3: Shut-in procedure
Walk through hard shut-in vs. soft shut-in. When to use which (IWCF L4: soft shut-in preferred for floating rigs; hard shut-in for land/fixed platforms unless circumstances dictate otherwise).

### Stage 4: Strip-and-kill pressures
Calculate:
- SIDPP (Shut-In Drill Pipe Pressure)
- SICP (Shut-In Casing Pressure)
- MAASP (Maximum Allowable Annular Surface Pressure) = ½ burst × safety margin − hydrostatic
- ICP (Initial Circulating Pressure) = SIDPP + hydrostatic of mud column at shoe

### Stage 5: Kill method choice
Ask: Driller's Method or Wait-and-Weight? When to use which (deep wells, high pressure: Wait-and-Weight preferred; shallow, simple: Driller's Method).

### Stage 6: Kill sheet
Walk through the kill sheet:
- Mud weight to kill (ppg) = original mud + SIDPP ÷ 0.052 ÷ TVD
- FCP (Final Circulating Pressure) = ICP − SIDPP
- Stroke count to pump kill mud

### Stage 7: Circulate and monitor
Stroke-by-stroke circulation. Watch for: pressure trends, gas at surface, mud weight returns.

### Stage 8: Final assessment
Score breakdown, weak areas, 3 recommendations for next drill.

## Drill log

Save to `~/iwcf-drills/drill-YYYY-MM-DD-<scenario>.md`:

```markdown
# IWCF L4 Drill — 2026-06-03 — Drilling Kick at 8,500 ft

## Scenario
- Depth: 8,500 ft MD / 8,200 ft TVD
- Mud: 12.5 ppg OBM
- Casing: 9.625" @ 5,000 ft
- Open hole: 8.5"
- Kick: 9.5 ppg, gas-cut
- BOP: 13.5", annular + 3 ram preventers

## Score: 78/100

| Topic | Score | Notes |
|---|---|---|
| Kick detection | 9/10 | Caught pit gain first, missed flowline temp |
| Shut-in procedure | 8/10 | Correct: soft shut-in, but slow on first action |
| Strip-and-kill | 7/10 | SIDPP/SICP correct, MAASP calculation off by 50 psi |
| Kill method | 9/10 | Correct: Wait-and-Weight for deep well |
| Kill sheet | 7/10 | FCP off, stroke count missed |
| Circulate | 10/10 | Perfect |

## Weak areas
1. MAASP calculation — review burst rating × safety factor
2. Kill sheet FCP formula — practice the ΔP × TVD derivation
3. Stroke count = (total vol to circulate) / (pump output per stroke)

## Recommended next drill
- Repeat with deeper kick (12,000+ ft) and gas-cut scenario
- Practice MAASP under different casing burst ratings
```

## Files

- `drill_runner.py` — score tracker (Python, stdlib)
- `kill_sheet.py` — well kill calculator (Python, stdlib)
- `inputs.example.yaml` — example scenario
- `CHANGELOG.md` — version history
- `00-iwcf-l4-drill-v1.0.0-2026-06-03.md` — source methodology (Drive canon)

## Install

```bash
# Drop into your Hermes skills folder
cp -r skills/skill-iwcf-l4-drill/ ~/.hermes/skills/
# /reload-skills
```

## Last tested

2026-06-03 — ran a 30-min drill on a kick at 8,500 ft. Scored 78/100. Weak area: MAASP under variable casing ratings. Recommended: re-drill at 12,000+ ft with gas-cut.
