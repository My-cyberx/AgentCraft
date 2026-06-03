#!/usr/bin/env python3
"""
Validate filenames against the AgentCraft §2.2 convention.

Pattern: <NN>-<artifact-name>-v<MAJOR>.<MINOR>.<PATCH>-<YYYY-MM-DD>.<ext>
Where:
  - NN is one of: 00, 10, 20, 30, 90
  - artifact-name is lowercase-kebab-case
  - Date is ISO format YYYY-MM-DD
  - Extension is the original (lowercased recommended)

Usage:
    python scripts/validate_naming.py                 # checks the whole repo
    python scripts/validate_naming.py canon/ skills/  # check specific paths

Exit codes:
  0 — all filenames conform
  1 — at least one violation (prints each)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Files exempt from the convention (project-level files)
EXEMPT_FILES = {
    "README.md", "CHANGELOG.md", "LICENSE", "CONTRIBUTING.md",
    "LICENSE.txt", "_README.md", "_CHANGELOG.md",
    "validate_naming.py", "new_artifact.py", "package_skill.py",
    "quick_validate.py", "improve_description.py",
    "aggregate_benchmark.py", "generate_report.py", "run_loop.py",
    "run_eval.py", "utils.py", "__init__.py",
    "mkdocs.yml", "smoke.yml", "weekly-smoke.yml", ".gitkeep", ".gitignore",
    "package.json", "requirements.txt", "Makefile",
    # Skill/SKILL.md and source files inside artifact folders are exempt
    "SKILL.md", "SKILL.md.placeholder", "depro_calc.py", "audit_checklist.py",
    "inputs.example.yaml", "inputs.yaml", "inputs.json",
}

EXEMPT_DIRS = {
    "site/docs",          # MkDocs pages — they are the catalog, not artifacts
    "site/site",          # MkDocs build output — never version-controlled
    ".git",
    "__pycache__",
    "node_modules",
}

# Site docs files that are navigation pages (not artifacts) — these are
# already covered by EXEMPT_DIRS but listed here for documentation.
# Per brief §11.2, site pages are kebab-case WITHOUT version numbers.
# Only CANON artifact source files must follow §2.2.

PATTERN = re.compile(
    r"^(?P<nn>00|10|20|30|90)-"
    r"(?P<name>[a-z0-9]+(?:-[a-z0-9]+)*)-"
    r"v(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)-"
    r"(?P<date>\d{4}-\d{2}-\d{2})"
    r"\.(?P<ext>[a-zA-Z0-9]+)$"
)

PLACEHOLDER_SUFFIX = ".placeholder"


def is_exempt(path: Path, root: Path) -> bool:
    if path.name in EXEMPT_FILES:
        return True
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path
    # Check if any parent directory of the file matches an exempt dir
    rel_str = str(rel)
    for exempt in EXEMPT_DIRS:
        if rel_str.startswith(exempt + "/") or rel_str == exempt:
            return True
    if path.suffix == ".placeholder":
        return True
    if path.name.startswith("."):
        return True
    return False


def check(root: Path) -> list[tuple[Path, str]]:
    violations = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if is_exempt(p, root):
            continue
        if not PATTERN.match(p.name):
            try:
                rel = p.relative_to(root)
            except ValueError:
                rel = p
            violations.append((p, f"  {rel}  -- does not match §2.2 pattern"))
    return violations


def main() -> int:
    if len(sys.argv) > 1:
        targets = [Path(a) for a in sys.argv[1:]]
    else:
        repo = Path(__file__).resolve().parent.parent
        targets = [repo]

    all_violations = []
    for t in targets:
        if not t.exists():
            print(f"WARN: path does not exist: {t}", file=sys.stderr)
            continue
        all_violations.extend(check(t))

    if all_violations:
        print(f"FAIL: {len(all_violations)} filename(s) violate §2.2 convention:")
        for _, msg in all_violations:
            print(msg)
        print()
        print("Pattern: <NN>-<artifact-name>-v<MAJOR>.<MINOR>.<PATCH>-<YYYY-MM-DD>.<ext>")
        print("  NN      = 00 | 10 | 20 | 30 | 90")
        print("  name    = lowercase-kebab-case")
        print("  date    = ISO YYYY-MM-DD")
        return 1

    print("OK: all filenames conform to §2.2.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
