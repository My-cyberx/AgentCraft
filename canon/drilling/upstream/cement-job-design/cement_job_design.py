#!/usr/bin/env python3
"""
Cement Job Design v1.0.0 — Generate a cementing job design from a well spec.

Inputs (YAML or JSON):
  - well: name, TD (ft), casing OD (in), casing ID (in), previous casing ID (in)
  - hole: TD (ft), open hole size (in), inclination (deg)
  - fluids: mud weight (ppg), fluid loss (cc/30min)
  - targets: top of cement (ft), TOC above casing shoe (ft), excess %
  - cement: class, density (ppg), yield (ft3/sk), water gal/sk
  - additives: accelerator_pct, retarder_pct, fluid_loss_pct, anti-gas_pct

Outputs:
  - Lead slurry volume (bbl), tail slurry volume (bbl)
  - Total cement required (sk)
  - Mix water (gal)
  - Displacement volume (bbl)
  - Pump schedule (text)
  - Job design summary (markdown)

Source: drive/00-canon/drilling/upstream/cement-job-design/00-cement-job-design-v1.0.0-2026-06-03.pdf
Author: Aiham Alhawar (AgentCraft)
License: MIT
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class CementJobInput:
    well_name: str
    casing_od_in: float
    casing_id_in: float
    prev_casing_id_in: float | None
    hole_td_ft: float
    open_hole_in: float
    inclination_deg: float
    mud_weight_ppg: float
    fluid_loss_cc: float
    top_of_cement_ft: float
    excess_pct: float
    cement_class: str
    cement_density_ppg: float
    cement_yield_ft3_per_sk: float
    water_gal_per_sk: float
    accelerator_pct: float = 0.0
    retarder_pct: float = 0.0
    fluid_loss_pct: float = 0.0
    anti_gas_pct: float = 0.0

    @classmethod
    def from_yaml(cls, path: Path) -> "CementJobInput":
        import re
        text = path.read_text()
        # Extract flat scalar fields
        def scalar(key: str, default: str = "0.0") -> str:
            m = re.search(rf"^\s*{key}:\s*(.+?)\s*$", text, re.MULTILINE)
            return m.group(1).strip().strip('"') if m else default

        return cls(
            well_name=scalar("well_name", "Unknown"),
            casing_od_in=float(scalar("casing_od_in")),
            casing_id_in=float(scalar("casing_id_in")),
            prev_casing_id_in=float(scalar("prev_casing_id_in")) or None,
            hole_td_ft=float(scalar("hole_td_ft")),
            open_hole_in=float(scalar("open_hole_in")),
            inclination_deg=float(scalar("inclination_deg", "0")),
            mud_weight_ppg=float(scalar("mud_weight_ppg")),
            fluid_loss_cc=float(scalar("fluid_loss_cc", "0")),
            top_of_cement_ft=float(scalar("top_of_cement_ft")),
            excess_pct=float(scalar("excess_pct", "20")),
            cement_class=scalar("cement_class", "Class G"),
            cement_density_ppg=float(scalar("cement_density_ppg", "15.8")),
            cement_yield_ft3_per_sk=float(scalar("cement_yield_ft3_per_sk", "1.18")),
            water_gal_per_sk=float(scalar("water_gal_per_sk", "5.10")),
            accelerator_pct=float(scalar("accelerator_pct", "0")),
            retarder_pct=float(scalar("retarder_pct", "0")),
            fluid_loss_pct=float(scalar("fluid_loss_pct", "0")),
            anti_gas_pct=float(scalar("anti_gas_pct", "0")),
        )

    @classmethod
    def from_json(cls, path: Path) -> "CementJobInput":
        return cls(**json.loads(path.read_text()))


def annular_capacity(open_hole_in: float, casing_od_in: float) -> float:
    """Annular capacity in ft3/ft between open hole and casing OD."""
    return (open_hole_in ** 2 - casing_od_in ** 2) / 183.0  # 183 = 4 * pi / 24


def casing_capacity(casing_id_in: float) -> float:
    """Casing internal capacity in ft3/ft."""
    return casing_id_in ** 2 / 183.0


def compute_job(job: CementJobInput) -> dict:
    """Compute volumes and pump schedule for a cementing job."""
    # Physical validation
    if job.casing_od_in >= job.open_hole_in:
        raise ValueError(
            f"casing_od_in ({job.casing_od_in}) must be < open_hole_in ({job.open_hole_in}). "
            f"A casing cannot be run in a hole smaller than itself."
        )
    if job.casing_id_in >= job.casing_od_in:
        raise ValueError(
            f"casing_id_in ({job.casing_id_in}) must be < casing_od_in ({job.casing_od_in}). "
            f"Wall thickness would be zero or negative."
        )

    # Open-hole interval (from TOC down to TD)
    open_interval_ft = job.hole_td_ft - job.top_of_cement_ft
    if open_interval_ft < 0:
        raise ValueError(f"top_of_cement_ft ({job.top_of_cement_ft}) must be < hole_td_ft ({job.hole_td_ft})")

    # Annular volume (open hole section) — apply excess for washouts
    ann_cap = annular_capacity(job.open_hole_in, job.casing_od_in)
    annular_volume_ft3 = ann_cap * open_interval_ft * (1.0 + job.excess_pct / 100.0)

    # Casing volume from surface to top of cement
    casing_int_capacity = casing_capacity(job.casing_id_in)
    casing_volume_ft3 = casing_int_capacity * job.top_of_cement_ft

    # Total slurry volume required (ft3) = annular + casing
    total_slurry_ft3 = annular_volume_ft3 + casing_volume_ft3
    # Add 5% for contamination/circulation losses
    total_slurry_ft3 *= 1.05

    # Convert ft3 to bbl (1 bbl = 5.615 ft3)
    total_slurry_bbl = total_slurry_ft3 / 5.615

    # Cement sacks required
    sacks = total_slurry_ft3 / job.cement_yield_ft3_per_sk

    # Mix water
    water_gal = sacks * job.water_gal_per_sk

    # Additives (volumes in gal — assume liquid additives)
    water_weight_ppg = 8.33
    cement_weight_lb = sacks * 94  # 94 lb/sk standard
    additive_gal = {}
    if job.accelerator_pct > 0:
        # CaCl2 2% by weight of cement
        additive_gal["accelerator (CaCl2)"] = (cement_weight_lb * job.accelerator_pct / 100.0) / water_weight_ppg
    if job.retarder_pct > 0:
        additive_gal["retarder"] = (cement_weight_lb * job.retarder_pct / 100.0) / water_weight_ppg
    if job.fluid_loss_pct > 0:
        additive_gal["fluid-loss additive"] = (cement_weight_lb * job.fluid_loss_pct / 100.0) / water_weight_ppg
    if job.anti_gas_pct > 0:
        additive_gal["anti-gas migration"] = (cement_weight_lb * job.anti_gas_pct / 100.0) / water_weight_ppg

    # Displacement volume = casing volume to top of cement + drill string volume
    drill_string_capacity = 0.0075  # 5" drill pipe @ 0.0075 bbl/ft typical
    displacement_bbl = casing_int_capacity * job.top_of_cement_ft / 5.615

    # Pump schedule (rule of thumb)
    contact_time_min = (total_slurry_bbl * 5.615) / (casing_int_capacity * 5)  # 5 ft/min avg
    if job.fluid_loss_cc > 0:
        # Adjust for fluid loss — high FL means more thickening time needed
        thickening_factor = 1.0 + (job.fluid_loss_cc / 200.0)
        contact_time_min *= thickening_factor

    # Estimated final BHCT (bottomhole circulating temp) — simplified
    bhct_f = 120 + (job.hole_td_ft / 100.0) * 1.5  # rough geothermal + friction

    return {
        "well": job.well_name,
        "open_interval_ft": round(open_interval_ft, 1),
        "annular_volume_ft3": round(annular_volume_ft3, 1),
        "annular_volume_bbl": round(annular_volume_ft3 / 5.615, 1),
        "casing_volume_ft3": round(casing_volume_ft3, 1),
        "casing_volume_bbl": round(casing_volume_ft3 / 5.615, 1),
        "total_slurry_bbl": round(total_slurry_bbl, 1),
        "sacks_required": round(sacks, 0),
        "mix_water_gal": round(water_gal, 0),
        "additives_gal": {k: round(v, 1) for k, v in additive_gal.items()},
        "displacement_bbl": round(displacement_bbl, 1),
        "estimated_bhct_f": round(bhct_f, 0),
        "estimated_contact_time_min": round(contact_time_min, 0),
        "excess_pct_applied": job.excess_pct,
        "lead_tail_split": {
            "lead_bbl": round(total_slurry_bbl * 0.7, 1),  # 70% lead, 30% tail
            "tail_bbl": round(total_slurry_bbl * 0.3, 1),
        },
    }


def render_pump_schedule(result: dict) -> str:
    lead = result["lead_tail_split"]["lead_bbl"]
    tail = result["lead_tail_split"]["tail_bbl"]
    disp = result["displacement_bbl"]
    total = lead + tail + disp
    return f"""
PUMP SCHEDULE (estimated):
─────────────────────────────────────────────────
  Stage 1: Lead slurry       {lead:>8.1f} bbl   @ 4-6 bbl/min
  Stage 2: Tail slurry       {tail:>8.1f} bbl   @ 2-4 bbl/min
  Stage 3: Displacement      {disp:>8.1f} bbl   @ 6-8 bbl/min
─────────────────────────────────────────────────
  TOTAL PUMPED:              {total:>8.1f} bbl

  Estimated BHCT:            {result['estimated_bhct_f']:.0f} °F
  Estimated contact time:    {result['estimated_contact_time_min']:.0f} min

  Pre-job checks (verify before pumping):
    ✓ Mud weight, viscosity, fluid loss within spec
    ✓ Casing centralizers (every joint in deviated section)
    ✓ Cement tested (thickening time > pump time + 1 hr)
    ✓ Plug bump pressure calculated (typically 1000-1500 psi)
"""


def render_text(result: dict) -> str:
    out = [
        "=" * 60,
        f"  CEMENT JOB DESIGN — {result['well']}",
        "=" * 60,
        f"  Open interval:           {result['open_interval_ft']:>10.0f} ft",
        "",
        "  Volumes:",
        f"    Annular (open hole):   {result['annular_volume_bbl']:>10.1f} bbl",
        f"    Casing (to TOC):       {result['casing_volume_bbl']:>10.1f} bbl",
        f"    Total slurry:          {result['total_slurry_bbl']:>10.1f} bbl",
        "",
        f"  Lead / Tail split (70/30):",
        f"    Lead:                  {result['lead_tail_split']['lead_bbl']:>10.1f} bbl",
        f"    Tail:                  {result['lead_tail_split']['tail_bbl']:>10.1f} bbl",
        "",
        f"  Materials:",
        f"    Cement sacks:          {result['sacks_required']:>10.0f} sk",
        f"    Mix water:             {result['mix_water_gal']:>10.0f} gal",
    ]
    for name, gal in result['additives_gal'].items():
        out.append(f"    {name + ':':24}{gal:>10.1f} gal")
    out += [
        "",
        f"  Displacement:            {result['displacement_bbl']:>10.1f} bbl",
        "=" * 60,
        render_pump_schedule(result),
    ]
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description="Cement Job Design v1.0.0")
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if not args.input.exists():
        print(f"ERROR: input not found: {args.input}", file=sys.stderr)
        return 2

    if args.input.suffix in (".yaml", ".yml"):
        job = CementJobInput.from_yaml(args.input)
    else:
        job = CementJobInput.from_json(args.input)

    try:
        result = compute_job(job)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_text(result))

    return 0


if __name__ == "__main__":
    sys.exit(main())
