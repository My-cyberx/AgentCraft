---
title: API Q1 Audit Checklist
---

# API Q1 Audit Checklist

> Generate a structured API Q1 11th edition audit checklist with severity-tagged clauses, evidence-gap detection, and an optional XLSX export.

**Type:** Script
**Domain:** Quality
**Vertical:** API Q1
**Version:** v1.4.0
**Last tested:** 2026-06-03
**Cost per run:** Free (Python stdlib; `openpyxl` optional for XLSX)

[:material-github: Source on GitHub](https://github.com/ah-alhawar/agentcraft/blob/main/canon/quality/api-q1/audit-checklist/) · [Drive canon XLSX](https://drive.google.com/) · [CHANGELOG](https://github.com/ah-alhawar/agentcraft/blob/main/canon/quality/api-q1/audit-checklist/CHANGELOG.md)

## Trigger prompts

```text
Use skill-api-q1-audit on the attached org description. Output XLSX.
```

```text
Generate an API Q1 11th ed. audit checklist for "Al Mansoori Drilling Services LLC".
List every gap with severity and clause number.
```

```text
Cross-walk our ISO 9001 evidence list against API Q1 11th ed.
```

## What it produces

A text report (default) or JSON showing:

- Severity counts (CRITICAL / HIGH / MEDIUM / LOW)
- Status counts (OPEN / PARTIAL / CLOSED) — derived from gap analysis
- All 35 clauses, each with: required evidence, present evidence, gaps, notes
- Optional XLSX output (if `openpyxl` installed and `--output` specified)

### Sample output — Al Mansoori Drilling Services LLC (partial evidence)

```text
======================================================================
  API Q1 11th ed. Audit Checklist — Al Mansoori Drilling Services LLC
======================================================================
  Clauses:        36
  OPEN:           18
  PARTIAL:        16
  CLOSED:         2
----------------------------------------------------------------------
  CRITICAL:       0
  HIGH:           17
  MEDIUM:         14
  LOW:            5
======================================================================

[4.1] Context of the organization  —  MEDIUM  —  PARTIAL
  Required evidence:
    [x] QMS scope documented
    [.] Interested parties identified
    [.] QMS scope available as documented information
  Gaps (2):
    - Interested parties identified
    - QMS scope available as documented information

[4.4] QMS and its processes  —  HIGH  —  PARTIAL
  Required evidence:
    [x] Process map
    [.] Process owners assigned
    [.] Process KPIs
  Gaps (2):
    - Process owners assigned
    - Process KPIs
...
```

## Inputs

- `--input <path>` — YAML or JSON org description (YAML: `name` + `evidence_present` list)
- `--output <path>` — XLSX path (requires `openpyxl`; falls back to JSON if missing)
- `--json` — output JSON only

### Example input

```yaml
name: "Al Mansoori Drilling Services LLC"

# List the evidence the org has confirmed is present at the start of the audit.
# Anything not listed here will appear as a GAP in the output.
evidence_present:
  - "QMS scope documented"
  - "Process map"
  - "QMS policy"
  - "RACI matrix"
  - "Document control procedure"
  - "Master document list"
  - "Training records"
  - "Risk register"
  - "Internal audit programme"
  - "Audit reports"
  - "Management review minutes"
  - "NCR procedure"
  - "NCR log"
  - "CAR procedure"
  - "CAR log"
  - "Customer requirements review"
  - "Supplier evaluation records"
  - "Production procedures"
  - "Work instructions"
  - "Release authorization records"
  - "Change control procedure"
  - "Improvement projects"
```

## Clause coverage (API Q1 11th ed.)

All 35 clauses across Sections 4-10:

- **4: Context of organization** (4.1, 4.2, 4.3, 4.4)
- **5: Leadership** (5.1, 5.2, 5.3)
- **6: Planning** (6.1, 6.2)
- **7: Support** (7.1, 7.2, 7.3, 7.4, 7.5, 7.5.1, 7.5.2)
- **8: Operation** (8.1, 8.2, 8.3, 8.4, 8.5.1-8.5.6, 8.6, 8.7)
- **9: Performance evaluation** (9.1.1, 9.1.2, 9.1.3, 9.2, 9.3)
- **10: Improvement** (10.1, 10.2, 10.3)

## Source files

| File | Path | Version |
|---|---|---|
| Source XLSX | `drive/00-canon/quality/api-q1/audit-checklist/00-api-q1-audit-checklist-v1.4.0-2026-05-20.xlsx` | v1.4.0 |
| Canonical script | `canon/quality/api-q1/audit-checklist/audit_checklist.py` | v1.4.0 |
| Example input | `canon/quality/api-q1/audit-checklist/inputs.example.yaml` | v1.4.0 |
| CHANGELOG | `canon/quality/api-q1/audit-checklist/CHANGELOG.md` | v1.4.0 |
| Public skill | `skills/skill-api-q1-audit/SKILL.md` | v1.4.0 |

## Install

```bash
git clone https://github.com/ah-alhawar/agentcraft

# Stdlib only — text report
python3 agentcraft/canon/quality/api-q1/audit-checklist/audit_checklist.py \
  --input agentcraft/canon/quality/api-q1/audit-checklist/inputs.example.yaml

# With XLSX output
pip install openpyxl
python3 agentcraft/canon/quality/api-q1/audit-checklist/audit_checklist.py \
  --input agentcraft/canon/quality/api-q1/audit-checklist/inputs.example.yaml \
  --output findings.xlsx
```

## Version + last tested

- **v1.4.0** — released 2026-05-20
- Last tested: 2026-06-03 against the Al Mansoori example. Result: 36 clauses, **0 CRITICAL, 17 HIGH, 14 MEDIUM, 5 LOW**. 18 OPEN, 16 PARTIAL, 2 CLOSED.

## Known limitations

- Hard-coded clause list. For clause updates, edit the `CLAUSES` constant in `audit_checklist.py` (or update the XLSX in Drive canon and re-run with a regenerated `CLAUSES`).
- No multi-org / multi-site audit yet (single org per run).
- Auditor notes field is captured but not round-tripped through XLSX.
- ISO 9001 cross-walk is manual; a future skill will auto-generate the cross-walk table.

---

[← Quality](../../index.md) · [Library](../../index.md) · [Home](../../../index.md)
