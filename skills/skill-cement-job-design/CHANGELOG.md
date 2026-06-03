# CHANGELOG — cement-job-design

## [1.0.0] — 2026-06-03

### Added
- Initial public release (Day-2 scaffold).
- Annular + casing volume calculations.
- 70/30 lead/tail split (configurable in source).
- Mix water, additives (accelerator / retarder / FL / anti-gas).
- Pump schedule with displacement volume.
- BHCT estimate, contact time estimate.
- Stdlib only; pure Python.

### Known limitations
- Lead/tail split is hard-coded 70/30; configurable in source.
- No temperature model beyond simple geothermal estimate.
- No centralizer placement optimizer.
- No API spec validation (Class G assumed).
