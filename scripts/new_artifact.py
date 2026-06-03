#!/usr/bin/env python3
"""
Scaffold a new AgentCraft artifact.

Creates the canon/ folder, a SKILL.md frontmatter template (or starter script),
a CHANGELOG.md seed, and a .placeholder for the source file. Then prints
the next steps.

Usage:
    python scripts/new_artifact.py \\
        --domain drilling \\
        --vertical upstream \\
        --slug cement-job-design \\
        --type skill \\
        --name "Cementing Job Design" \\
        --version 1.0.0

    python scripts/new_artifact.py --help
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path


TYPES = ("script", "skill", "flow")

NN_BY_TYPE = {
    "skill": "10",
    "flow": "20",
    "script": "00",
}

TEMPLATE_FRONT = """---
name: {slug}
description: TODO — one-sentence description. Include BOTH what it does AND specific trigger phrases ("use when user says X, Y, Z").
version: {version}
last_tested: {today}
metadata:
  hermes:
    tags: [{domain}, {vertical}]
    source_drive: 00-canon/{domain}/{vertical}/{slug}/00-{slug}-v{version}-{today}.<ext>
    public_slug: library/{domain}/{vertical}/{slug}
  context:
    user:
      name: "Aiham Alhawar"
      role: "TODO — your role for this domain"
      geography: "Abu Dhabi, UAE"
      voice: "Direct, execution-first. No fluff. Bullet lists > paragraphs."
    domain:
      primary: "TODO"
      standards_in_force: ["API Q1 11th ed", "API Q2 2nd ed", "ISO 9001:2015", "IWCF L4"]
      tools_available: [python3, deepseek, gemini, exa, apify, airtable, resend, vercel]
    last_used:
      runs: 0
---

# {title}

TODO — write the artifact body here. See existing artifacts in canon/ for the
shape: when to use, inputs, tool stack, workflow stages, outputs, failover,
cost estimate.
"""

CHANGELOG_SEED = """# CHANGELOG — {slug}

## [{version}] — {today}

### Added
- Initial scaffold created via `scripts/new_artifact.py`.
- TODO: write the body of the SKILL.md / script.
- TODO: add the source file to `00-canon/{domain}/{vertical}/{slug}/`.
"""


def main() -> int:
    p = argparse.ArgumentParser(description="Scaffold a new AgentCraft artifact")
    p.add_argument("--domain", required=True, help="drilling | quality | hse | operations")
    p.add_argument("--vertical", required=True, help="upstream | midstream | downstream | api-q1 | api-q2 | iso-9001 | iwcf-l4 | iadc | lss | sme-audit")
    p.add_argument("--slug", required=True, help="kebab-case, e.g. cement-job-design")
    p.add_argument("--type", choices=TYPES, required=True, help="script | skill | flow")
    p.add_argument("--name", required=True, help='Human-readable name, e.g. "Cementing Job Design"')
    p.add_argument("--version", default="0.1.0", help="semver (default: 0.1.0)")
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent.parent,
                   help="Path to agentcraft repo root (default: parent of this script)")
    args = p.parse_args()

    today = date.today().isoformat()
    nn = NN_BY_TYPE[args.type]

    canon_dir = args.repo / "canon" / args.domain / args.vertical / args.slug
    canon_dir.mkdir(parents=True, exist_ok=True)

    # Source-file placeholder — exact §2.2 filename
    placeholder = canon_dir / f"00-{args.slug}-v{args.version}-{today}.pdf.placeholder"
    placeholder.write_text(
        f"Drop the real source file here, keeping the §2.2 name:\n"
        f"  00-{args.slug}-v{args.version}-{today}.pdf\n"
    )

    # SKILL.md or starter script
    if args.type in ("skill", "flow"):
        skill_path = canon_dir / "SKILL.md"
        skill_path.write_text(TEMPLATE_FRONT.format(
            slug=args.slug, version=args.version, today=today,
            domain=args.domain, vertical=args.vertical, title=args.name,
        ))
    else:  # script
        script_path = canon_dir / f"{args.slug.replace('-', '_')}.py"
        script_path.write_text(f'#!/usr/bin/env python3\n"""{args.name} v{args.version} — TODO"""\n')

    # CHANGELOG
    (canon_dir / "CHANGELOG.md").write_text(CHANGELOG_SEED.format(
        slug=args.slug, version=args.version, today=today,
        domain=args.domain, vertical=args.vertical,
    ))

    # Mirror into skills/ (Hermes-loaded location)
    if args.type in ("skill", "flow"):
        skills_dst = args.repo / "skills" / f"skill-{args.slug}"
        skills_dst.mkdir(parents=True, exist_ok=True)
        for fname in ("SKILL.md", "CHANGELOG.md"):
            src = canon_dir / fname
            if src.exists():
                (skills_dst / fname).write_text(src.read_text())

    print(f"\n✓ Scaffolded new artifact:")
    print(f"  Canon:      {canon_dir}")
    print(f"  Placeholder: {placeholder.name}")
    print(f"  Type:        {args.type}  (NN prefix: {nn})")
    print(f"  Version:     {args.version}")
    print()
    print("Next steps:")
    print(f"  1. Edit the SKILL.md / script body in {canon_dir}/")
    print(f"  2. Drop the real source file at {placeholder.name} (remove .placeholder)")
    print(f"  3. Add a site page at site/docs/library/{args.domain}/{args.vertical}/{args.slug}.md")
    print(f"  4. Run python scripts/validate_naming.py")
    print(f"  5. Open a PR — see CONTRIBUTING.md for the checklist")
    return 0


if __name__ == "__main__":
    sys.exit(main())
