# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed
- Plug Puller experiments (entire `Plug Puller Test/` tree, root
  `Plug_Puller_Parametric.scad`, root `Plug_Puller_v4_Parametric.scad`,
  `dxf_extracts/`, `obj_vertex_data.txt`, `artifacts/plug_puller_validation/`,
  and stray validation renders) — moved to
  [plug-puller-openscad](https://github.com/BrennenJohnston/plug-puller-openscad).
- DXF/SVG conversion scripts (`scripts/dxf_to_openscad_polygon.py`,
  `scripts/extract_svg_overlay_outline.py`) — moved to
  [cad-to-openscad-pipeline](https://github.com/BrennenJohnston/cad-to-openscad-pipeline).

### Changed
- README now links to the two spin-off repositories under a new
  "Spin-off Projects" section.

### Added
- This `CHANGELOG.md` file.

## [2.1.0] - 2026-01-11

Last tagged release prior to the v2.2.0 cleanup. See git history for details.
