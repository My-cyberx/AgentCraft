#!/usr/bin/env python3
"""
Fishbone (Ishikawa) Diagram Generator v1.0.0

Reads a YAML/JSON problem description + cause categories and writes a
publication-quality SVG fishbone diagram.

Pure stdlib. No external deps. No JS, no external fonts.

Usage:
    python fishbone.py --input problem.yaml --output fishbone.svg
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# Color palette per category (named 6M by default)
DEFAULT_CATEGORY_COLORS = {
    "man": "#E07850",
    "people": "#E07850",
    "machine": "#4A90E2",
    "equipment": "#4A90E2",
    "material": "#7B61FF",
    "method": "#52C41A",
    "process": "#52C41A",
    "measurement": "#F0A830",
    "environment": "#13C2C2",
    "milieu": "#13C2C2",
}
DEFAULT_COLOR = "#888888"


def color_for(category_name: str) -> str:
    name_lower = category_name.lower().split("(")[0].strip()
    return DEFAULT_CATEGORY_COLORS.get(name_lower, DEFAULT_COLOR)


def parse_input(path: Path) -> dict:
    text = path.read_text()
    if path.suffix in (".yaml", ".yml"):
        out: dict = {"problem": "", "categories": []}
        current_cat: dict | None = None
        in_causes = False
        in_categories = False
        for line in text.splitlines():
            stripped = line.rstrip()
            if not stripped.strip() or stripped.strip().startswith("#"):
                continue
            # Top-level problem
            if stripped.startswith("problem:"):
                in_categories = False
                out["problem"] = stripped.partition(":")[2].strip().strip('"')
                continue
            # categories: at indent 0
            if stripped == "categories:":
                in_categories = True
                continue
            if not in_categories:
                continue
            # - name: at indent 2 → start a new category
            if line.startswith("  - name:"):
                if current_cat:
                    out["categories"].append(current_cat)
                current_cat = {"name": stripped.partition(":")[2].strip().strip('"'), "causes": []}
                in_causes = False
                continue
            # causes: at indent 4
            if stripped.strip() == "causes:" and current_cat is not None:
                in_causes = True
                continue
            # cause line at indent 6
            if line.startswith("      - ") and current_cat is not None and in_causes:
                cause = stripped[8:].strip().strip('"')
                current_cat["causes"].append(cause)
                continue
        if current_cat:
            out["categories"].append(current_cat)
        return out
    return json.loads(text)


def render_svg(data: dict, title: str) -> str:
    problem = data.get("problem", "Problem")
    categories = data.get("categories", [])
    if not categories:
        return "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 100'><text x='20' y='50'>No categories</text></svg>"

    # Layout
    W, H = 1200, max(700, 180 * len(categories))
    pad_l, pad_r, pad_t, pad_b = 100, 280, 100, 80
    spine_x_start = pad_l
    spine_x_end = W - pad_r
    spine_y = H / 2
    box_w, box_h = 200, 70

    # Distribute categories above and below the spine
    n = len(categories)
    upper_n = (n + 1) // 2
    lower_n = n - upper_n
    upper = categories[:upper_n]
    lower = categories[upper_n:]

    parts = []
    parts.append(f'<rect width="{W}" height="{H}" fill="#FAFAFA"/>')
    parts.append(f'<text x="{W/2}" y="40" text-anchor="middle" font-size="22" font-weight="700" fill="#333">{title}</text>')
    parts.append(f'<text x="{W/2}" y="65" text-anchor="middle" font-size="12" fill="#888">{problem}</text>')

    # Spine (the main horizontal line)
    parts.append(f'<line x1="{spine_x_start}" y1="{spine_y}" x2="{spine_x_end}" y2="{spine_y}" stroke="#333" stroke-width="3"/>')
    # Arrow head
    parts.append(f'<polygon points="{spine_x_end},{spine_y} {spine_x_end-15},{spine_y-10} {spine_x_end-15},{spine_y+10}" fill="#333"/>')

    # Problem box (head)
    parts.append(
        f'<rect x="{spine_x_end + 20}" y="{spine_y - box_h/2}" width="{box_w}" height="{box_h}" '
        f'fill="#333" stroke="none"/>'
    )
    parts.append(
        f'<foreignObject x="{spine_x_end + 25}" y="{spine_y - box_h/2 + 5}" width="{box_w - 10}" height="{box_h - 10}">'
        f'<div xmlns="http://www.w3.org/1999/xhtml" style="color:#fff;font-family:system-ui;font-size:13px;line-height:1.3;overflow:hidden;">'
        f'<b>PROBLEM</b><br/>{problem[:120]}{"..." if len(problem) > 120 else ""}</div></foreignObject>'
    )

    # Categories upper
    for i, cat in enumerate(upper):
        col = color_for(cat["name"])
        # Branch point on spine
        bx = spine_x_start + (spine_x_end - spine_x_start) * (i + 1) / (upper_n + 1)
        by = spine_y
        # Bone endpoint (diagonal up-left)
        ex = bx - 200
        ey = spine_y - 220
        parts.append(f'<line x1="{bx}" y1="{by}" x2="{ex}" y2="{ey}" stroke="{col}" stroke-width="2.5"/>')
        # Category label
        parts.append(
            f'<rect x="{ex - 90}" y="{ey - 25}" width="180" height="32" fill="{col}" rx="4"/>'
        )
        parts.append(
            f'<text x="{ex}" y="{ey - 4}" text-anchor="middle" fill="#fff" font-weight="700" font-size="13">{cat["name"]}</text>'
        )
        # Causes
        for j, cause in enumerate(cat.get("causes", [])):
            cy = ey + 30 + j * 26
            cx = ex + 50 + (j % 2) * 20
            parts.append(f'<line x1="{ex}" y1="{ey + 8 + j * 26}" x2="{cx}" y2="{cy}" stroke="{col}" stroke-width="1"/>')
            parts.append(
                f'<text x="{cx + 6}" y="{cy + 4}" font-size="11" fill="#333">{cause[:60]}{"..." if len(cause) > 60 else ""}</text>'
            )

    # Categories lower
    for i, cat in enumerate(lower):
        col = color_for(cat["name"])
        bx = spine_x_start + (spine_x_end - spine_x_start) * (i + 1) / (lower_n + 1)
        by = spine_y
        ex = bx - 200
        ey = spine_y + 220
        parts.append(f'<line x1="{bx}" y1="{by}" x2="{ex}" y2="{ey}" stroke="{col}" stroke-width="2.5"/>')
        parts.append(
            f'<rect x="{ex - 90}" y="{ey - 8}" width="180" height="32" fill="{col}" rx="4"/>'
        )
        parts.append(
            f'<text x="{ex}" y="{ey + 13}" text-anchor="middle" fill="#fff" font-weight="700" font-size="13">{cat["name"]}</text>'
        )
        for j, cause in enumerate(cat.get("causes", [])):
            cy = ey + 40 + j * 26
            cx = ex + 50 + (j % 2) * 20
            parts.append(f'<line x1="{ex}" y1="{ey + 18 + j * 26}" x2="{cx}" y2="{cy}" stroke="{col}" stroke-width="1"/>')
            parts.append(
                f'<text x="{cx + 6}" y="{cy + 4}" font-size="11" fill="#333">{cause[:60]}{"..." if len(cause) > 60 else ""}</text>'
            )

    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="system-ui,sans-serif">\n' + "\n".join(parts) + "\n</svg>"


def main() -> int:
    p = argparse.ArgumentParser(description="Fishbone Diagram Generator v1.0.0")
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--title", default="Root Cause Analysis — Fishbone Diagram")
    args = p.parse_args()

    if not args.input.exists():
        print(f"ERROR: input not found: {args.input}", file=sys.stderr)
        return 2

    data = parse_input(args.input)
    svg = render_svg(data, args.title)
    args.output.write_text(svg)
    print(f"✓ Wrote {args.output} ({len(data.get('categories', []))} categories, "
          f"{sum(len(c.get('causes', [])) for c in data.get('categories', []))} causes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
