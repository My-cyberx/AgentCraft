#!/usr/bin/env python3
"""
DEPRO Calculator v3.2.1 — Daily Equivalent Production Offline.

Calculates the Daily Equivalent Production Offline for an oil/gas well
given a YAML/JSON input of well events. Pure stdlib, zero LLM in the loop.

Formula (per the source PDF `00-depro-formula-v3.2.1-2026-06-03.pdf`):

    DEPRO = (Q_design * T_prod) / (T_prod + T_down)

Where:
    Q_design  = design production rate (bopd or mmscfd)
    T_prod    = total productive time in the analysis window (hours)
    T_down    = total downtime in the analysis window (hours)

Plus a Monte Carlo uncertainty band by perturbing each downtime event
within its reported error margin.

Usage:
    python depro_calc.py --input inputs.example.yaml
    python depro_calc.py --input inputs.example.yaml --mc-runs 1000
    python depro_calc.py --input inputs.example.yaml --json

Author: Aiham Alhawar (AgentCraft)
License: MIT
Source:  drive/00-canon/drilling/upstream/depro-calc/00-depro-formula-v3.2.1-2026-06-03.pdf
"""
from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class WellEvent:
    """A single downtime or production event in the analysis window."""
    start: str                  # ISO datetime
    end: str                    # ISO datetime
    rate: float | None = None   # production rate during this event (bopd), None for downtime
    reason: str = ""
    error_hours: float = 0.0    # uncertainty band for MC perturbation


@dataclass
class WellInput:
    name: str
    design_rate_bopd: float
    analysis_window_hours: float
    events: list[WellEvent] = field(default_factory=list)

    @classmethod
    def from_yaml(cls, path: Path) -> "WellInput":
        """Minimal YAML parser (no PyYAML dep). Supports the inputs.example.yaml shape."""
        import re
        text = path.read_text()
        # Extract scalar fields
        def scalar(key: str) -> str:
            m = re.search(rf"^\s*{key}:\s*(.+)$", text, re.MULTILINE)
            return m.group(1).strip().strip('"') if m else ""

        name = scalar("name")
        design_rate = float(scalar("design_rate_bopd"))
        window = float(scalar("analysis_window_hours"))

        # Extract events block (list of dicts)
        events: list[WellEvent] = []
        in_events = False
        cur: dict = {}
        for line in text.splitlines():
            if line.strip().startswith("events:"):
                in_events = True
                continue
            if not in_events:
                continue
            if line.startswith("  - "):
                if cur:
                    events.append(WellEvent(**cur))
                cur = {}
                kv = line[4:].strip()
                if ":" in kv:
                    k, v = kv.split(":", 1)
                    cur[k.strip()] = _coerce(v.strip())
            elif line.startswith("    "):
                if ":" in line:
                    k, v = line.strip().split(":", 1)
                    cur[k.strip()] = _coerce(v.strip())
        if cur:
            events.append(WellEvent(**cur))

        return cls(name=name, design_rate_bopd=design_rate,
                   analysis_window_hours=window, events=events)

    @classmethod
    def from_json(cls, path: Path) -> "WellInput":
        data = json.loads(path.read_text())
        return cls(
            name=data["name"],
            design_rate_bopd=data["design_rate_bopd"],
            analysis_window_hours=data["analysis_window_hours"],
            events=[WellEvent(**e) for e in data.get("events", [])],
        )


def _coerce(v: str):
    """Coerce a YAML/JSON-ish scalar to the right Python type."""
    v = v.strip().strip('"').strip("'")
    if v.lower() in ("null", "none", "~", ""):
        return None
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    try:
        if "." in v or "e" in v.lower():
            return float(v)
        return int(v)
    except ValueError:
        return v


def hours_between(start: str, end: str) -> float:
    """Naive ISO datetime difference in hours. No tz handling — assume UTC."""
    from datetime import datetime
    fmt = "%Y-%m-%dT%H:%M:%S"
    s = datetime.strptime(start, fmt)
    e = datetime.strptime(end, fmt)
    return (e - s).total_seconds() / 3600.0


def compute_depro(well: WellInput) -> dict:
    """Compute the deterministic DEPRO. Returns dict with all inputs + result."""
    t_down = sum(hours_between(e.start, e.end) for e in well.events if e.rate is None)
    t_prod = well.analysis_window_hours - t_down
    if t_prod + t_down == 0:
        depro = 0.0
    else:
        depro = (well.design_rate_bopd * t_prod) / (t_prod + t_down)

    availability = t_prod / well.analysis_window_hours if well.analysis_window_hours else 0.0
    actual_production = well.design_rate_bopd * t_prod  # bbl over the window

    return {
        "well": well.name,
        "design_rate_bopd": well.design_rate_bopd,
        "analysis_window_hours": well.analysis_window_hours,
        "productive_hours": round(t_prod, 2),
        "downtime_hours": round(t_down, 2),
        "availability_pct": round(availability * 100, 2),
        "actual_production_bbl": round(actual_production, 2),
        "depro_bopd": round(depro, 2),
        "downtime_events": len([e for e in well.events if e.rate is None]),
    }


def monte_carlo(well: WellInput, runs: int = 1000, seed: int = 42) -> dict:
    """Perturb each downtime event within its error_hours band, recompute DEPRO."""
    random.seed(seed)
    samples = []
    downtime_events = [e for e in well.events if e.rate is None]

    for _ in range(runs):
        perturbed_t_down = 0.0
        for e in downtime_events:
            base = hours_between(e.start, e.end)
            # Uniform perturbation in ±error_hours
            perturbed = base + random.uniform(-e.error_hours, e.error_hours)
            perturbed_t_down += max(0.0, perturbed)
        t_prod = max(0.0, well.analysis_window_hours - perturbed_t_down)
        denom = t_prod + perturbed_t_down
        depro = (well.design_rate_bopd * t_prod) / denom if denom else 0.0
        samples.append(depro)

    return {
        "mc_runs": runs,
        "mean_bopd": round(statistics.mean(samples), 2),
        "stdev_bopd": round(statistics.stdev(samples), 2) if len(samples) > 1 else 0.0,
        "p10_bopd": round(sorted(samples)[int(0.10 * len(samples))], 2),
        "p50_bopd": round(sorted(samples)[int(0.50 * len(samples))], 2),
        "p90_bopd": round(sorted(samples)[int(0.90 * len(samples))], 2),
        "min_bopd": round(min(samples), 2),
        "max_bopd": round(max(samples), 2),
    }


def render_text(result: dict, mc: dict | None = None) -> str:
    lines = [
        "=" * 60,
        f"  DEPRO Report — {result['well']}",
        "=" * 60,
        f"  Design rate:         {result['design_rate_bopd']:>10,.0f} bopd",
        f"  Analysis window:     {result['analysis_window_hours']:>10,.1f} hours",
        f"  Productive hours:    {result['productive_hours']:>10,.2f}",
        f"  Downtime hours:      {result['downtime_hours']:>10,.2f}",
        f"  Availability:        {result['availability_pct']:>10.2f} %",
        f"  Actual production:   {result['actual_production_bbl']:>10,.0f} bbl",
        f"  Downtime events:     {result['downtime_events']:>10d}",
        "-" * 60,
        f"  DEPRO:               {result['depro_bopd']:>10,.2f} bopd",
        "=" * 60,
    ]
    if mc:
        lines += [
            "",
            f"  Monte Carlo ({mc['mc_runs']} runs):",
            f"    Mean:   {mc['mean_bopd']:>10,.2f} bopd",
            f"    Stdev:  {mc['stdev_bopd']:>10,.2f} bopd",
            f"    P10:    {mc['p10_bopd']:>10,.2f} bopd",
            f"    P50:    {mc['p50_bopd']:>10,.2f} bopd",
            f"    P90:    {mc['p90_bopd']:>10,.2f} bopd",
            f"    Range:  [{mc['min_bopd']:,.2f}, {mc['max_bopd']:,.2f}]",
            "=" * 60,
        ]
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="DEPRO Calculator v3.2.1")
    p.add_argument("--input", required=True, type=Path, help="YAML or JSON well input file")
    p.add_argument("--mc-runs", type=int, default=0, help="Monte Carlo runs (0 = skip)")
    p.add_argument("--seed", type=int, default=42, help="MC random seed")
    p.add_argument("--json", action="store_true", help="Output as JSON only")
    args = p.parse_args()

    if not args.input.exists():
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        return 2

    if args.input.suffix in (".yaml", ".yml"):
        well = WellInput.from_yaml(args.input)
    else:
        well = WellInput.from_json(args.input)

    result = compute_depro(well)
    mc = monte_carlo(well, args.mc_runs, args.seed) if args.mc_runs > 0 else None

    if args.json:
        out = {"deterministic": result}
        if mc:
            out["monte_carlo"] = mc
        print(json.dumps(out, indent=2))
    else:
        print(render_text(result, mc))

    return 0


if __name__ == "__main__":
    sys.exit(main())
