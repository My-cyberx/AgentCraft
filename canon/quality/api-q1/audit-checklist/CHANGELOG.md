# CHANGELOG — api-q1-audit-checklist

## [1.4.0] — 2026-05-20

### Added
- Initial public release (Day-1 scaffold per `agentcraft-strategy-brief.md` §12).
- All 35 API Q1 11th ed. clauses (Sections 4-10) hard-coded with default severity + evidence list.
- Stdlib YAML/JSON parser; openpyxl XLSX output (optional dep, falls back to JSON).
- Severity + status summary; gap detection by diff against `evidence_present` list.

### Known limitations
- Hard-coded clause list; for clause updates, edit the `CLAUSES` constant in `audit_checklist.py`.
- No multi-org / multi-site audit yet (single org per run).
- Auditor notes field is captured but not round-tripped through XLSX.
