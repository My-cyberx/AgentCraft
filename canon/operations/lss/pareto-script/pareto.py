#!/usr/bin/env python3
"""
Pareto Chart Generator v1.0.0 — CSV → ranked bar chart with cumulative %.

Reads a CSV of issues (one per row) and produces a Pareto chart as an
SVG file, with bars sorted descending and a cumulative percentage line.

Pure stdlib. No matplotlib. SVG output is editable in any vector tool.

Usage:
    python pareto.py --input issues.csv --column "Issue Type" --output pareto.svg
    python pareto.py --input issues.csv --column "Defect" --top 10 --output pareto.svg

Input CSV must have a header row. The --column specifies which column to count.
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


def count_issues(csv_path: Path, column: str) -> list[tuple[str, int]]:
    counts: Counter = Counter()
    with csv_path.open() as f:
        reader = csv.DictReader(f)
        if column not in reader.fieldnames:
            print(f"ERROR: column '{column}' not in CSV. Available: {reader.fieldnames}", file=sys.stderr)
            sys.exit(2)
        for row in reader:
            val = row[column].strip()
            if val:
                counts[val] += 1
    return counts.most_common()


def render_svg(pareto_data: list[tuple[str, int]], title: str, top_n: int | None) -> str:
    data = pareto_data[:top_n] if top_n else pareto_data
    if not data:
        return "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 100'><text x='20' y='50'>No data</text></svg>"

    total = sum(c for _, c in data)
    cumulative = 0
    bars = []
    line_pts = []
    chart_w, chart_h = 800, 480
    pad_l, pad_r, pad_t, pad_b = 80, 60, 60, 140
    plot_w = chart_w - pad_l - pad_r
    plot_h = chart_h - pad_t - pad_b
    max_count = max(c for _, c in data) or 1
    bar_w = plot_w / len(data) * 0.7
    bar_gap = plot_w / len(data) * 0.3

    for i, (label, count) in enumerate(data):
        x = pad_l + i * (bar_w + bar_gap) + bar_gap / 2
        h = (count / max_count) * plot_h
        y = pad_t + plot_h - h
        cumulative += count
        cum_pct = (cumulative / total) * 100
        line_pts.append((x + bar_w / 2, pad_t + plot_h - (cum_pct / 100) * plot_h))

        # Truncate long labels
        display_label = label if len(label) <= 18 else label[:15] + "..."
        bars.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" '
            f'fill="#E07850"><title>{label} — {count} ({count/total*100:.1f}%)</title></rect>'
        )
        bars.append(
            f'<text x="{x + bar_w/2:.1f}" y="{pad_t + plot_h + 15:.1f}" '
            f'transform="rotate(-30 {x + bar_w/2:.1f} {pad_t + plot_h + 15:.1f})" '
            f'text-anchor="end" font-size="11" fill="#333">{display_label}</text>'
        )
        bars.append(
            f'<text x="{x + bar_w/2:.1f}" y="{y - 4:.1f}" text-anchor="middle" '
            f'font-size="11" font-weight="bold" fill="#333">{count}</text>'
        )

    # Cumulative line
    if len(line_pts) >= 2:
        pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in line_pts)
        bars.append(f'<polyline points="{pts_str}" stroke="#4A90E2" stroke-width="2" fill="none"/>')
        for x, y in line_pts:
            bars.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#4A90E2"/>')

    # Axes + grid
    grid = []
    for pct in (0, 25, 50, 75, 100):
        y = pad_t + plot_h - (pct / 100) * plot_h
        grid.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l + plot_w}" y2="{y:.1f}" stroke="#eee"/>')
        grid.append(f'<text x="{pad_l - 10}" y="{y + 4:.1f}" text-anchor="end" font-size="10" fill="#666">{pct}%</text>')
        # Right axis (cumulative %)
        grid.append(f'<text x="{pad_l + plot_w + 10}" y="{y + 4:.1f}" font-size="10" fill="#4A90E2">{pct}%</text>')

    # 80/20 line (vertical)
    target_x = pad_l + (0.8 * total / max(data, key=lambda x: x[1])[1] / max_count) * plot_w
    # Simpler: place 80% marker on cumulative line
    if line_pts:
        # find first bar where cumulative >= 80%
        cumsum = 0
        for i, (_, count) in enumerate(data):
            cumsum += count
            if cumsum / total >= 0.8:
                # that's the bar where 80% threshold is crossed
                pass

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {chart_w} {chart_h + 40}" font-family="system-ui,sans-serif">
  <style>
    .lbl {{ font-family: 'JetBrains Mono', monospace; }}
  </style>
  <rect width="{chart_w}" height="{chart_h + 40}" fill="#FAFAFA"/>
  <text x="{chart_w/2}" y="30" text-anchor="middle" font-size="18" font-weight="700" fill="#333">{title}</text>
  <text x="{pad_l}" y="{chart_h + 30}" font-size="10" fill="#666" class="lbl">Count</text>
  <text x="{pad_l + plot_w}" y="{chart_h + 30}" text-anchor="end" font-size="10" fill="#4A90E2" class="lbl">Cumulative %</text>
  {chr(10).join(grid)}
  {chr(10).join(bars)}
  <line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#333" stroke-width="1"/>
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#333" stroke-width="1"/>
  <line x1="{pad_l + plot_w}" y1="{pad_t}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#4A90E2" stroke-width="1"/>
  <text x="{chart_w/2}" y="{chart_h + 20}" text-anchor="middle" font-size="10" fill="#666">Total: {total} items, {len(data)} categories</text>
</svg>"""


def main() -> int:
    p = argparse.ArgumentParser(description="Pareto Chart Generator v1.0.0")
    p.add_argument("--input", required=True, type=Path, help="CSV with issues")
    p.add_argument("--column", required=True, help="Column to count (e.g. 'Defect', 'Issue Type')")
    p.add_argument("--output", default="pareto.svg", type=Path, help="Output SVG path")
    p.add_argument("--title", default="Pareto Analysis", help="Chart title")
    p.add_argument("--top", type=int, help="Show only top N categories")
    args = p.parse_args()

    if not args.input.exists():
        print(f"ERROR: input not found: {args.input}", file=sys.stderr)
        return 2

    data = count_issues(args.input, args.column)
    if not data:
        print("WARN: no issues found in column", file=sys.stderr)

    svg = render_svg(data, args.title, args.top)
    args.output.write_text(svg)
    print(f"✓ Wrote {args.output} ({len(data)} categories, {sum(c for _, c in data)} total)")

    # Also print ASCII summary
    print(f"\n{args.title} — top categories:")
    total = sum(c for _, c in data) or 1
    cum = 0
    for label, count in data[:args.top or 10]:
        cum += count
        bar = "█" * int((count / data[0][1]) * 30)
        print(f"  {count:>5}  {cum/total*100:>5.1f}%  {bar} {label}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
