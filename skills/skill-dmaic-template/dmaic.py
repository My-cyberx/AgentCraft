#!/usr/bin/env python3
"""
DMAIC Template Generator v1.0.0 — Lean Six Sigma Green Belt.

Reads a problem description (YAML or JSON) and produces a complete
DMAIC project template as markdown, with sections auto-populated
from the input.

Usage:
    python dmaic.py --input problem.yaml --output dmaic.md
    python dmaic.py --input problem.yaml --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


def parse_yaml_simple(path: Path) -> dict:
    """Minimal YAML parser for flat scalar fields + simple lists."""
    text = path.read_text()
    out: dict = {}
    current_list_key: str | None = None
    for line in text.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith("  - "):
            if current_list_key:
                out[current_list_key].append(line[4:].strip().strip('"'))
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            k = k.strip()
            v = v.strip()
            if not v:
                # Start of a list
                out[k] = []
                current_list_key = k
            else:
                current_list_key = None
                out[k] = v.strip('"')
    return out


def render_dmaic_md(p: dict) -> str:
    today = date.today().isoformat()
    return f"""# DMAIC Project — {p.get('project_name', 'Untitled')}

**Project owner:** {p.get('owner', '—')}
**Date created:** {today}
**Phase:** Define

---

## D — Define

### Problem statement
{p.get('problem_statement', '[TODO: one-sentence problem statement]')}

### Goal / target
{p.get('goal', '[TODO: SMART goal]')}

### SIPOC
| Suppliers | Inputs | Process | Outputs | Customers |
|---|---|---|---|---|
{chr(10).join(f"| {x} | | | | |" for x in p.get('sipoc_suppliers', ['TODO'] * 3))}

### Voice of the Customer (VOC)
{chr(10).join(f"- {x}" for x in p.get('voc', ['[TODO: collect VOC data — surveys, interviews, complaints]']))}

### Project charter
- **Scope (in):** {p.get('scope_in', '[TODO]')}
- **Scope (out):** {p.get('scope_out', '[TODO]')}
- **Team:** {p.get('team', '[TODO: list members + roles]')}
- **Timeline:** {p.get('timeline', '[TODO: 8-12 weeks typical]')}

---

## M — Measure

### Key metric(s)
{chr(10).join(f"- **{x}**" for x in p.get('key_metrics', ['[TODO: name the metric, define it operationally]']))}

### Baseline
[Collect 30+ data points before any change. Document collection method, sampling plan, measurement system analysis (Gage R&R).]

### Data collection plan
| What | How | When | Who | Where stored |
|---|---|---|---|---|
[Fill in per metric]

---

## A — Analyze

### Fishbone (Ishikawa) — link to `fishbone-skill`
Use the AgentCraft fishbone skill to structure root cause analysis.

### 5 Whys
1. [First why]
2. [Second why]
3. [Third why]
4. [Fourth why]
5. [Root cause]

### Hypothesis test
- H0: [null hypothesis]
- H1: [alternative hypothesis]
- Test: [t-test, chi-square, ANOVA, etc.]
- α = 0.05
- Result: [p-value, decision]

---

## I — Improve

### Pilot solution
- **What:** [describe the change]
- **Where:** [pilot scope — 1 line, 1 shift, 1 unit]
- **Who:** [responsible person]
- **When:** [start/end date]
- **Success criteria:** [specific, measurable]

### Rollout plan
[Document training needs, communication plan, controls to prevent regression]

---

## C — Control

### Control plan
| Process step | What to monitor | Specification | Measurement method | Frequency | Owner |
|---|---|---|---|---|---|
[Fill in]

### Sustainment
- [ ] SOP updated
- [ ] Training delivered
- [ ] KPI dashboard live
- [ ] Quarterly review scheduled

### Lessons learned
[Document for future projects: what worked, what didn't, what we'd do differently]

---

## Sign-off

| Role | Name | Date | Signature |
|---|---|---|---|
| Project owner | | | |
| Process owner | | | |
| Sponsor | | | |
| LSS MBB / Champion | | | |
"""


def main() -> int:
    p = argparse.ArgumentParser(description="DMAIC Template Generator v1.0.0")
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", type=Path, help="Output markdown path")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if not args.input.exists():
        print(f"ERROR: input not found: {args.input}", file=sys.stderr)
        return 2

    if args.input.suffix in (".yaml", ".yml"):
        data = parse_yaml_simple(args.input)
    else:
        data = json.loads(args.input.read_text())

    md = render_dmaic_md(data)

    if args.json:
        # JSON mode = structured for downstream processing
        print(json.dumps(data, indent=2))
        return 0

    if args.output:
        args.output.write_text(md)
        print(f"✓ Wrote {args.output}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
