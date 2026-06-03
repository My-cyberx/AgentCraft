---
title: IWCF L4 Well Control Drill
---

# IWCF L4 Well Control Drill

> Run a 30-minute IWCF Level 4 well control drill — the agent plays the examiner and walks you through kick detection, shut-in, circulation, and well kill procedures using industry-standard methodology (IADC, API).

**Type:** Skill (agent-driven, interactive)
**Domain:** HSE
**Vertical:** IWCF L4
**Version:** v1.0.0
**Last tested:** 2026-06-03
**Cost per run:** ~$0.02 (DeepSeek tokens)

[:material-github: Source on GitHub](https://github.com/My-cyberx/AgentCraft/blob/main/canon/hse/iwcf-l4/drill/) · [Drive canon](https://drive.google.com/) · [CHANGELOG](https://github.com/My-cyberx/AgentCraft/blob/main/canon/hse/iwcf-l4/drill/CHANGELOG.md)

## Trigger prompts

```text
Start a 30-minute IWCF L4 well control drill on Driller's Method.
```

```text
Use skill-iwcf-l4-drill. Scenario: kick detected at 8,500 ft on a 12.5 ppg mud, 9.5 ppg kick.
```

```text
Quick drill: shut-in procedure + 5 strike questions on strip-and-kill pressures.
```

## What it produces

A scored drill session (markdown file) saved to `~/iwcf-drills/`:

- 1 scenario (drilling / tripping / cementing)
- 6-10 strike questions (shut-in, strip, kill, circulate)
- 1 final essay question (well kill plan)
- Score: 0-100, broken down by topic
- Weak areas identified
- Recommendations for next drill

### Sample output — IWCF L4 Drill 2026-06-03

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

## Workflow (8 stages, ~30 min wall clock)

| # | Stage | Time | What happens |
|---|---|---|---|
| 1 | Scenario setup | 2 min | Agent proposes scenario; user accepts or modifies |
| 2 | Kick detection | 3 min | 3 indicators — pit gain, flowline temp, return flow |
| 3 | Shut-in procedure | 3 min | Hard vs. soft shut-in (IWCF L4: soft preferred for floating rigs) |
| 4 | Strip-and-kill | 5 min | SIDPP, SICP, MAASP, ICP calculations |
| 5 | Kill method | 3 min | Driller's Method vs. Wait-and-Weight (deep wells: W&W) |
| 6 | Kill sheet | 5 min | Mud weight to kill, FCP, stroke count |
| 7 | Circulate | 5 min | Stroke-by-stroke, watch for gas / pressure trends |
| 8 | Final assessment | 4 min | Score, weak areas, 3 recommendations |

## Source files

| File | Path | Version |
|---|---|---|
| Source methodology | `drive/00-canon/hse/iwcf-l4/drill/00-iwcf-l4-drill-v1.0.0-2026-06-03.md` | v1.0.0 |
| Lead skill | `canon/hse/iwcf-l4/drill/SKILL.md` | v1.0.0 |
| CHANGELOG | `canon/hse/iwcf-l4/drill/CHANGELOG.md` | v1.0.0 |
| Public skill | `skills/skill-iwcf-l4-drill/SKILL.md` | v1.0.0 |

## Install

```bash
# Drop into your Hermes skills folder
cp -r skills/skill-iwcf-l4-drill/ ~/.hermes/skills/
# /reload-skills
```

## Version + last tested

- **v1.0.0** — released 2026-06-03
- Last tested: 2026-06-03 — 30-min drill on a kick at 8,500 ft. Scored **78/100**. Weak area: MAASP under variable casing ratings. Recommended: re-drill at 12,000+ ft with gas-cut.

## Known limitations

- Kill sheet math is approximate (uses simplified BHCT model).
- Scoring rubric is built into the skill, not externally calibrated to IWCF exam weights.

---

[← HSE](../../index.md) · [Library](../../../index.md) · [Home](../../../index.md)
