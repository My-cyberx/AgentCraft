# CHANGELOG — depro-calc

## [3.2.1] — 2026-06-03

### Added
- Initial public release (Day-1 scaffold per `agentcraft-strategy-brief.md` §12).
- Stdlib-only Python — no `pip install` required.
- YAML input parser (no PyYAML dep) + JSON input parser.
- Deterministic DEPRO + Monte Carlo uncertainty band.
- Tested against 3 real Well A-12 quarterly inputs.

### Known limitations
- Naive datetime parsing (assumes UTC, no DST).
- Single-well per run (multi-well aggregation is a future skill).
