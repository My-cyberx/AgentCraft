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
| [cement-job-design](drilling/upstream/cement-job-design.md) | Skill | Drilling | Upstream | v1.0.0 | 2026-06-03 | Free |
| [liner-hanger-overview](drilling/upstream/liner-hanger-overview.md) | Flow | Drilling | Upstream | v1.0.0 | 2026-06-03 | ~$0.16 |
| [audit-checklist](quality/api-q1/audit-checklist.md) | Script | Quality | API Q1 | v1.4.0 | 2026-06-03 | Free (openpyxl optional) |
| [iwcf-l4-drill](hse/iwcf-l4/drill.md) | Skill | HSE | IWCF L4 | v1.0.0 | 2026-06-03 | ~$0.02 |
| [dmaic-template](operations/lss/dmaic-template.md) | Script | Operations | LSS | v1.0.0 | 2026-06-03 | Free |
| [fishbone](operations/lss/fishbone.md) | Skill | Operations | LSS | v1.0.0 | 2026-06-03 | Free |
| [pareto](operations/lss/pareto.md) | Script | Operations | LSS | v1.0.0 | 2026-06-03 | Free |
| [flow-audit-deliverable](operations/sme-audit/flow-audit-deliverable.md) | Flow | Operations | SME Audit | v1.0.0 | 2026-06-03 | ~$0.54 |

**9 artifacts** across 4 domains. All Day-1 + Day-2 complete.

## Coming soon

| Slug | Type | Domain | Target |
|---|---|---|---|
| `non-conformance-flow` | Skill | Quality | Day-3 |
| `lead-research` (flow) | Flow | Sales | Day-5 |
| `content-publish` (flow) | Flow | Marketing | Day-5 |
| `build-website` (flow) | Flow | Web | Day-5 |
| `api-q2-audit-checklist` | Script | Quality | Day-4 |
| `iso-9001-lead-auditor-prep` | Skill | Quality | Day-3 |

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
