# Examples

Worked end-to-end runs. Every example has a real input, a real output, and a `last_tested` date.

## 1. DEPRO Calculator — Well A-12, Q1 2026

**Input:** `inputs.example.yaml` (Well A-12, 4,200 bopd design, 2,160 hours, 4 downtime events)

**Run:**

```bash
python3 canon/drilling/upstream/depro-calc/depro_calc.py \
  --input canon/drilling/upstream/depro-calc/inputs.example.yaml \
  --mc-runs 1000
```

**Output (excerpt):**

```text
  Design rate:              4,200 bopd
  Availability:             94.35 %
  DEPRO:                 3,962.78 bopd

  Monte Carlo (1000 runs):
    Mean:     3,962.70 bopd
    P10:      3,957.08 bopd
    P90:      3,968.27 bopd
```

**Result:** 94.35% availability, **3,962.78 bopd DEPRO**, MC P10/P90 band [3,957 / 3,968] bopd.

[Full artifact page →](../library/drilling/upstream/depro-calc.md)

---

## 2. API Q1 Audit Checklist — Al Mansoori Drilling Services LLC

**Input:** `inputs.example.yaml` (org name + 22 evidence items known-present)

**Run:**

```bash
python3 canon/quality/api-q1/audit-checklist/audit_checklist.py \
  --input canon/quality/api-q1/audit-checklist/inputs.example.yaml \
  --output findings.xlsx
```

**Output (summary):**

```text
  Clauses:        36
  OPEN:           18
  PARTIAL:        16
  CLOSED:         2

  CRITICAL:       0
  HIGH:           17
  MEDIUM:         14
  LOW:            5
```

**Result:** 36 clauses audited, **0 CRITICAL / 17 HIGH / 14 MEDIUM / 5 LOW**, 18 OPEN / 16 PARTIAL / 2 CLOSED. Output XLSX with per-clause evidence, gaps, and notes.

[Full artifact page →](../library/quality/api-q1/audit-checklist.md)

---

## 3. SME Audit Deliverable Flow — mock HVAC contractor, Abu Dhabi

**Input:** client name + website, Standard tier ($3K)

**Run:**

```text
flow-audit-deliverable: client = "Cool Air HVAC LLC", tier = Standard.
```

**Output:** 7-document package in `~/clients/cool-air-hvac-2026-06-03/`, plus Airtable CRM record, Resend email to client, ~$0.54 cost.

**Result:** Full deliverable in ~30 min wall clock. Chat summary lists top 3 findings, recommends next step (call booking), quotes follow-on pricing.

[Full artifact page →](../library/operations/sme-audit/flow-audit-deliverable.md)

---

## 4-7. Coming soon

| # | Example | Artifact | Target |
|---|---|---|---|
| 4 | Cementing job design from a well spec | `cement-job-design` | Day-2 |
| 5 | IWCF L4 30-min drill | `iwcf-l4-drill` | Day-2 |
| 6 | Pareto chart from a CSV of issues | `pareto-script` | Day-2 |
| 7 | Full 50-lead ICP research | `flow-lead-research` | Day-5 |

---

[← Home](index.md)
