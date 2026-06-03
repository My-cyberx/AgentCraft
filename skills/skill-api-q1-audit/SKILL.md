---
name: skill-api-q1-audit
description: Generate a structured API Q1 11th edition audit checklist with severity-tagged clauses, evidence-gap detection, and an optional XLSX export. Use this skill whenever the user says "API Q1 audit", "QMS audit checklist", "API Q1 findings", "ISO 9001 / API Q1 cross-walk", or attaches an org description and asks for gaps. Hard-codes all 35 API Q1 11th ed. clauses (Sections 4-10) with default severity and required evidence list.
version: 1.4.0
last_tested: 2026-06-03
metadata:
  hermes:
    tags: [quality, api-q1, qms, audit, iso-9001]
    source_drive: 00-canon/quality/api-q1/audit-checklist/00-api-q1-audit-checklist-v1.4.0-2026-05-20.xlsx
    public_slug: library/quality/api-q1/audit-checklist
  context:
    user:
      name: "Aiham Alhawar"
      role: "API Q1/Q2 lead auditor, ISO 9001 lead auditor, SME audit consultant"
      geography: "Abu Dhabi, UAE"
      voice: "Direct, execution-first. Cite clause numbers. No generic disclaimers."
      brand_dislikes: ["'this is not professional advice'", "vague AI-isms", "inter font, purple gradients"]
    domain:
      primary: "Quality management systems, O&G service companies"
      standards_in_force: ["API Q1 11th ed", "API Q2 2nd ed", "ISO 9001:2015", "IWCF L4"]
      tools_available: [python3, openpyxl-optional, deepseek]
    last_used:
      runs: 0
---

# Skill: API Q1 Audit Checklist Generator

Wraps `audit_checklist.py` (the canonical script) with the user-information block above.

## Trigger prompts (copy any)

```
Use skill-api-q1-audit on the attached org description. Output XLSX.
```

```
Generate an API Q1 11th ed. audit checklist for "Al Mansoori Drilling Services LLC".
List every gap with severity and clause number.
```

```
Cross-walk our ISO 9001 evidence list against API Q1 11th ed.
```

## What it produces

A text report (default) or JSON showing:

- Severity counts (CRITICAL / HIGH / MEDIUM / LOW)
- Status counts (OPEN / PARTIAL / CLOSED) — derived from gap analysis
- All 35 clauses, each with: required evidence, present evidence, gaps, notes
- Optional XLSX output (if `openpyxl` installed and `--output` specified)

Example summary (Al Mansoori, partial-evidence example):

```
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
```

## Inputs

- `--input <path>` — YAML or JSON org description (YAML: name + `evidence_present` list)
- `--output <path>` — XLSX path (requires `openpyxl`; falls back to JSON if missing)
- `--json` — JSON output only

## Clause coverage (API Q1 11th ed.)

All 35 clauses across Sections 4-10:

- 4: Context of organization (4.1-4.4)
- 5: Leadership (5.1-5.3)
- 6: Planning (6.1-6.2)
- 7: Support (7.1-7.5.2)
- 8: Operation (8.1-8.7)
- 9: Performance evaluation (9.1.1-9.3)
- 10: Improvement (10.1-10.3)

## Files

- `audit_checklist.py` — canonical script (stdlib; openpyxl optional for XLSX)
- `inputs.example.yaml` — example Al Mansoori inputs
- `CHANGELOG.md` — version history
- `00-api-q1-audit-checklist-v1.4.0-2026-05-20.xlsx` — source XLSX (in Drive canon)

## Install

```bash
python3 audit_checklist.py --input inputs.example.yaml

# With XLSX output
pip install openpyxl
python3 audit_checklist.py --input inputs.example.yaml --output findings.xlsx
```

## Last tested

2026-06-03 against the Al Mansoori example. Result: 36 clauses, 0 CRITICAL, 17 HIGH, 14 MEDIUM, 5 LOW. 18 OPEN, 16 PARTIAL, 2 CLOSED.
