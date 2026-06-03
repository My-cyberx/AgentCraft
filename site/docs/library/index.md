# Library

The AgentCraft catalog. Curated, versioned, tested weekly.

## Browse

- **By domain** — [Drilling](drilling/index.md) · [Quality](quality/index.md) · [HSE](hse/index.md) · [Operations](operations/index.md)
- **By type** — Scripts · Skills · Flows (filter in the nav)
- **By use case** — Run an audit · Train a new hire · Respond to incident · Onboard a vendor (coming soon)

## All artifacts

| Slug | Type | Domain | Vertical | Version | Last tested | Cost / run |
|---|---|---|---|---|---|---|
| [depro-calc](drilling/upstream/depro-calc.md) | Script | Drilling | Upstream | v3.2.1 | 2026-06-03 | Free |
| [audit-checklist](quality/api-q1/audit-checklist.md) | Script | Quality | API Q1 | v1.4.0 | 2026-06-03 | Free (openpyxl optional) |
| [flow-audit-deliverable](operations/sme-audit/flow-audit-deliverable.md) | Flow | Operations | SME Audit | v1.0.0 | 2026-06-03 | ~$0.54 |

## Coming soon

| Slug | Type | Domain | Target |
|---|---|---|---|
| `cement-job-design` | Skill | Drilling | Day-2 |
| `liner-hanger-overview` | Flow | Drilling | Day-2 |
| `iwcf-l4-drill` | Skill | HSE | Day-2 |
| `pareto-script` | Script | Operations | Day-2 |
| `fishbone-skill` | Skill | Operations | Day-2 |
| `dmaic-template` | Script | Operations | Day-2 |
| `lead-research` (flow) | Flow | Sales | Day-5 |
| `content-publish` (flow) | Flow | Marketing | Day-5 |
| `build-website` (flow) | Flow | Web | Day-5 |
| `api-q2-audit-checklist` | Script | Quality | Day-4 |

## Filter by tag

| Tag | Meaning |
|---|---|
| `#offline` | Runs with zero API keys |
| `#needs-api` | Needs DeepSeek / Gemini / etc. |
| `#abu-dhabi` | UAE-specific (regulatory, vendors) |
| `#beginner` / `#intermediate` / `#advanced` | Skill level required |
| `#script` / `#skill` / `#flow` | Artifact type |

## How to read an artifact page

Every artifact page follows the same 7-section template (per the strategy brief §11.2):

1. **One-sentence description** — what it is
2. **Trigger prompt** — the literal sentence to paste
3. **What it produces** — artifact preview, file list, or output sample
4. **Inputs required** — form, file, or env var
5. **Source files** — links to the original Drive canon
6. **Install** — one command, copy-paste
7. **Version + last tested** — auto-generated from Drive mtime + CHANGELOG.md

Click into any artifact to see this in action.
