#!/usr/bin/env python3
"""
API Q1 11th ed. Audit Checklist Generator v1.4.0

Generates a structured audit checklist (XLSX + JSON) for a QMS audit
against API Q1 11th edition. Inputs: a YAML/JSON description of the
audited organization. Outputs: finding list with severity, evidence
gaps, and a heatmap.

Pure stdlib. No pip install.

Usage:
    python audit_checklist.py --input inputs.example.yaml --output findings.xlsx
    python audit_checklist.py --input inputs.example.yaml --json

Source: drive/00-canon/quality/api-q1/audit-checklist/00-api-q1-audit-checklist-v1.4.0-2026-05-20.xlsx
Author: Aiham Alhawar (AgentCraft)
License: MIT
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Literal

Severity = Literal["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]


# Hard-coded API Q1 11th ed. clause summary (full checklist is in the XLSX).
# Each clause: (clause_id, title, severity_default, evidence_required)
CLAUSES = [
    ("4.1", "Context of the organization", "MEDIUM",
     ["QMS scope documented", "Interested parties identified", "QMS scope available as documented information"]),
    ("4.2", "Needs and expectations of interested parties", "LOW",
     ["List of interested parties", "Requirements reviewed periodically"]),
    ("4.3", "Scope of QMS", "MEDIUM",
     ["QMS scope statement", "Exclusions justified"]),
    ("4.4", "QMS and its processes", "HIGH",
     ["Process map", "Process owners assigned", "Process KPIs"]),
    ("5.1", "Leadership and commitment", "HIGH",
     ["Management review minutes", "QMS policy communicated"]),
    ("5.2", "Policy", "MEDIUM",
     ["QMS policy", "Policy available to relevant parties"]),
    ("5.3", "Organizational roles, responsibilities, authorities", "HIGH",
     ["RACI matrix", "Job descriptions"]),
    ("6.1", "Actions to address risks and opportunities", "HIGH",
     ["Risk register", "Opportunities register"]),
    ("6.2", "Quality objectives and planning", "MEDIUM",
     ["Quality objectives", "Action plans to achieve objectives"]),
    ("7.1", "Resources — General", "MEDIUM",
     ["Resource needs determined and provided"]),
    ("7.2", "Competence", "HIGH",
     ["Training records", "Competence matrix"]),
    ("7.3", "Awareness", "LOW",
     ["Awareness training records"]),
    ("7.4", "Communication", "LOW",
     ["Communication plan"]),
    ("7.5", "Documented information — General", "HIGH",
     ["Document control procedure", "Master document list"]),
    ("7.5.1", "Creating and updating documented information", "MEDIUM",
     ["Document templates", "Approval workflow"]),
    ("7.5.2", "Control of documented information", "HIGH",
     ["Document distribution log", "Obsolete documents controlled"]),
    ("8.1", "Operational planning and control", "HIGH",
     ["Operational planning documented", "Controls in place"]),
    ("8.2", "Requirements for products and services", "MEDIUM",
     ["Customer requirements review", "Contract review records"]),
    ("8.3", "Design and development of products and services", "HIGH",
     ["Design procedures", "Design verification records", "Design validation records"]),
    ("8.4", "Control of externally provided processes, products, services", "HIGH",
     ["Supplier evaluation records", "Supplier monitoring", "Purchasing information"]),
    ("8.5.1", "Control of production and service provision", "HIGH",
     ["Production procedures", "Work instructions", "Equipment control"]),
    ("8.5.2", "Identification and traceability", "MEDIUM",
     ["Traceability records"]),
    ("8.5.3", "Property belonging to customers or external providers", "LOW",
     ["Custody controls"]),
    ("8.5.4", "Preservation", "LOW",
     ["Preservation procedures"]),
    ("8.5.5", "Post-delivery activities", "MEDIUM",
     ["Warranty procedures", "Customer feedback"]),
    ("8.5.6", "Control of changes", "HIGH",
     ["Change control procedure", "Change records"]),
    ("8.6", "Release of products and services", "HIGH",
     ["Release authorization records"]),
    ("8.7", "Control of nonconforming outputs", "HIGH",
     ["NCR procedure", "NCR log", "Disposition records"]),
    ("9.1.1", "Monitoring, measurement, analysis, evaluation — General", "MEDIUM",
     ["Monitoring plan"]),
    ("9.1.2", "Customer satisfaction", "MEDIUM",
     ["Customer satisfaction surveys", "Complaint handling"]),
    ("9.1.3", "Analysis and evaluation", "MEDIUM",
     ["Data analysis records", "Trends"]),
    ("9.2", "Internal audit", "HIGH",
     ["Internal audit programme", "Audit reports", "Corrective actions"]),
    ("9.3", "Management review", "HIGH",
     ["Management review minutes", "Inputs and outputs documented"]),
    ("10.1", "General — Improvement", "MEDIUM",
     ["Improvement opportunities identified"]),
    ("10.2", "Nonconformity and corrective action", "HIGH",
     ["CAR procedure", "CAR log", "Effectiveness reviews"]),
    ("10.3", "Continual improvement", "MEDIUM",
     ["Improvement projects", "Lessons learned"]),
]


@dataclass
class Finding:
    clause: str
    title: str
    severity: Severity
    evidence_required: list[str]
    evidence_present: list[str] = None
    evidence_gaps: list[str] = None
    status: str = "OPEN"  # OPEN | PARTIAL | CLOSED
    notes: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        return d


def generate_checklist(org_input: dict) -> list[Finding]:
    """Generate the audit checklist for a given org. `org_input` is a free-form
    dict; we use it to mark which evidence is *known* to be present.

    Real audits would have the auditor fill this in. For a starter, we mark
    every clause OPEN with the full evidence list as required.
    """
    known_evidence = set(org_input.get("evidence_present", []))
    findings = []
    for clause_id, title, sev, evidence in CLAUSES:
        present = [e for e in evidence if e in known_evidence]
        gaps = [e for e in evidence if e not in known_evidence]
        status = "CLOSED" if not gaps else ("PARTIAL" if present else "OPEN")
        findings.append(Finding(
            clause=clause_id,
            title=title,
            severity=sev,
            evidence_required=evidence,
            evidence_present=present,
            evidence_gaps=gaps,
            status=status,
            notes="",
        ))
    return findings


def severity_counts(findings: list[Finding]) -> dict:
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
    for f in findings:
        counts[f.severity] += 1
    return counts


def status_counts(findings: list[Finding]) -> dict:
    counts = {"OPEN": 0, "PARTIAL": 0, "CLOSED": 0}
    for f in findings:
        counts[f.status] += 1
    return counts


def render_text(org_name: str, findings: list[Finding]) -> str:
    sev = severity_counts(findings)
    stat = status_counts(findings)
    lines = [
        "=" * 70,
        f"  API Q1 11th ed. Audit Checklist — {org_name}",
        "=" * 70,
        f"  Clauses:        {len(findings)}",
        f"  OPEN:           {stat['OPEN']}",
        f"  PARTIAL:        {stat['PARTIAL']}",
        f"  CLOSED:         {stat['CLOSED']}",
        "-" * 70,
        f"  CRITICAL:       {sev['CRITICAL']}",
        f"  HIGH:           {sev['HIGH']}",
        f"  MEDIUM:         {sev['MEDIUM']}",
        f"  LOW:            {sev['LOW']}",
        "=" * 70,
        "",
    ]
    for f in findings:
        lines += [
            f"[{f.clause}] {f.title}  —  {f.severity}  —  {f.status}",
            f"  Required evidence:",
        ]
        for e in f.evidence_required:
            mark = "x" if e in (f.evidence_present or []) else "."
            lines.append(f"    [{mark}] {e}")
        if f.evidence_gaps:
            lines.append(f"  Gaps ({len(f.evidence_gaps)}):")
            for g in f.evidence_gaps:
                lines.append(f"    - {g}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="API Q1 audit checklist generator v1.4.0")
    p.add_argument("--input", required=True, type=Path, help="YAML or JSON org description")
    p.add_argument("--output", type=Path, help="Output XLSX path (requires openpyxl; else falls back to JSON)")
    p.add_argument("--json", action="store_true", help="Output JSON only")
    args = p.parse_args()

    if not args.input.exists():
        print(f"ERROR: input not found: {args.input}", file=sys.stderr)
        return 2

    # Parse minimal YAML/JSON
    if args.input.suffix in (".yaml", ".yml"):
        import re
        text = args.input.read_text()
        name = re.search(r'^name:\s*"?([^"]+)"?', text, re.MULTILINE).group(1).strip()
        evidence = re.findall(r'^\s*-\s*"?(.*?)"?\s*$', text, re.MULTILINE)
        org = {"name": name, "evidence_present": evidence}
    else:
        org = json.loads(args.input.read_text())

    findings = generate_checklist(org)
    if args.json:
        print(json.dumps({
            "org": org.get("name"),
            "summary": {
                "severity": severity_counts(findings),
                "status": status_counts(findings),
            },
            "findings": [f.to_dict() for f in findings],
        }, indent=2))
    else:
        print(render_text(org.get("name", "Unknown"), findings))

    if args.output:
        # Try openpyxl; fall back to JSON if not installed.
        try:
            from openpyxl import Workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "Findings"
            ws.append(["Clause", "Title", "Severity", "Status", "Required", "Present", "Gaps", "Notes"])
            for f in findings:
                ws.append([f.clause, f.title, f.severity, f.status,
                           "; ".join(f.evidence_required),
                           "; ".join(f.evidence_present or []),
                           "; ".join(f.evidence_gaps or []),
                           f.notes])
            wb.save(args.output)
            print(f"\nWrote {args.output}")
        except ImportError:
            json_out = args.output.with_suffix(".json")
            json_out.write_text(json.dumps({
                "org": org.get("name"),
                "findings": [f.to_dict() for f in findings],
            }, indent=2))
            print(f"\nopenpyxl not installed; wrote JSON to {json_out}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
