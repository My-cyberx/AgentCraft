# LSS (Lean Six Sigma — Green Belt)

LSS artifacts, all Green-Belt appropriate. Pair them for a complete DMAIC project.

| Artifact | Type | Version | Last tested |
|---|---|---|---|
| [DMAIC Template](dmaic-template.md) | Script | v1.0.0 | 2026-06-03 |
| [Fishbone](fishbone.md) | Skill | v1.0.0 | 2026-06-03 |
| [Pareto](pareto.md) | Script | v1.0.0 | 2026-06-03 |

## How they fit together

```
D (Define)    → dmaic-template   (problem statement, charter, SIPOC, VOC)
M (Measure)   → pareto           (vital few from a defect log)
A (Analyze)   → fishbone         (root causes from the vital few)
I (Improve)   → [your pilot]     (write the pilot plan in the DMAIC markdown)
C (Control)   → [your plan]      (control plan is the bottom of the DMAIC markdown)
```

## Quick example — "Reduce NPT on Well A-12"

1. **Define** — `dmaic.py --input problem.example.yaml --output dmaic.md` → 114-line project charter
2. **Measure** — `pareto.py --input npt_log.csv --column "Cause" --output pareto.svg` → identify the vital few
3. **Analyze** — `fishbone.py --input problem.example.yaml --output fishbone.svg` → root causes on 6 bones
4. **Improve + Control** — edit the `I-Improve` and `C-Control` sections of `dmaic.md`

---

[← Operations](../index.md) · [Library](../../index.md) · [Home](../../../index.md)
