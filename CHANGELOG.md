# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed
- Plug Puller experiments (entire `Plug Puller Test/` tree, root
  `Plug_Puller_Parametric.scad`, root `Plug_Puller_v4_Parametric.scad`,
  `dxf_extracts/`, `obj_vertex_data.txt`,
  `artifacts/plug_puller_validation/`, and stray validation renders) —
  moved to
  [plug-puller-openscad](https://github.com/BrennenJohnston/plug-puller-openscad).
- DXF/SVG conversion scripts (`scripts/dxf_to_openscad_polygon.py`,
  `scripts/extract_svg_overlay_outline.py`) — moved to
  [cad-to-openscad-pipeline](https://github.com/BrennenJohnston/cad-to-openscad-pipeline).
- `braille_x_adjust` Customizer slider and the corresponding
  `active_braille_x_adjust` aggregator. On a cylinder the X axis is
  the angular wrap around the seam, so a linear "X adjust" had no
  useful meaning. Use `seam_offset_degrees` for angular pattern
  offset.
- Unused aggregators `active_emboss_base_diameter`,
  `active_emboss_top_diameter`, and `active_counter_top_diameter`
  (dead since the cylinder rewrite).
- Root `PARAMETER_MAPPING.md` duplicate. `docs/PARAMETER_MAPPING.md`
  is the single canonical copy; references in `CONTRIBUTING.md`,
  `docs/OPENSCAD_COORDINATE_SYSTEM_SPECIFICATIONS.md`, and
  `tests/parameter_mapping.json` updated.
- Dead `check_tool_version()` stub in `tests/conftest.py`. Real
  version enforcement lives in `OpenSCADRunner._enforce_version()`.
- `@pytest.mark.card` registration and the auto-tagging branch in
  `tests/conftest.py`. Card support was retired in v2.0; the marker
  served no purpose.

### Changed
- Renamed main file
  `Braille_Card_And_Cylinder_STL_Generator.scad` →
  `Braille_Cylinder_STL_Generator.scad`. Updated 26 reference sites
  (tests, scripts, README, archive docs, fixture metadata).
- Refactored preset routing: extracted constants and lookup helper
  into a new top-level `presets.scad` (`PRESET_04`, `PRESET_03`
  tables and `preset_value(preset, key, fallback)`). The main SCAD
  `include`s it inside `[Hidden]`. Critical OpenSCAD `search()`
  quirks documented inline.
- Hoisted shared cylinder grid math (`radius`, `grid_angle`,
  `start_angle`, `cell_spacing_angle`, `dot_spacing_angle`,
  `dot_col_angle_offsets`, `dot_row_offsets`, `dot_positions`) from
  `cylinder_emboss_plate` and `cylinder_counter_plate` to top-level
  scope. Names preserved so module bodies needed no internal edits.
- Pinned the backward-compat parameter block (`combined_shape`,
  `indicator_shapes`, `hemisphere_quality`, `shape_type`) under an
  explicit `/* [Hidden] */` marker so the Customizer no longer
  surfaces them as orphan uncategorized fields.
- README now links to the two spin-off repositories under a new
  "Spin-off Projects" section.
- Archived `CODEBASE_AUDIT_SUMMARY.md` →
  `docs/archive/CODEBASE_AUDIT_SUMMARY_2026-01-10.md`. It was a
  one-shot snapshot, not a living doc.

### Added
- Named geometry constants: `INDICATOR_OVERCUT` (0.05),
  `CYLINDER_SHELL_FN` (64), `INVALID_TEXT_Z_OFFSET` (5),
  `INVALID_TEXT_SIZE` (5), `INVALID_TEXT_DEPTH` (2). Replaces the
  prior magic numbers scattered through the geometry section.
- "TEXT TOO LONG" warning geometry: the cylinder emboss plate now
  renders a red `text("TEXT TOO LONG")` extrusion above the
  cylinder when any of `Line_1`–`Line_4` exceeds
  `active_grid_columns - (indicator_on ? 2 : 0)`. Stacks above the
  existing INVALID CHARACTERS warning when both fire.
- Documentation block at the top of the geometry section explaining
  the `$fn` tessellation policy. Five distinct `$fn` sources
  (`CYLINDER_SHELL_FN`, `cone_segments` slider, `quality_fn`-derived,
  `active_polygon_cutout_points` semantic, global `$fn = 32`
  default) are each documented with their intent.
- This `CHANGELOG.md` file.

### Fixed
- `docs/PARAMETER_MAPPING.md` "Indicator Shapes" section described
  the card layout (rectangle at col 0, triangle at col N-1).
  Rewrote for cylinder-only reality (col 0 triangle, col 1
  rectangle).
- `docs/PARAMETER_MAPPING.md` OpenSCAD workflow step said "Choose
  `shape_type`". Replaced with `dot_shape` (the actual Customizer
  control); `shape_type` lives in `[Hidden]` as a backward-compat
  alias.
- `docs/PARAMETER_MAPPING.md` "Unified Shape Selection" documented
  `combined_shape` as primary control. Documented `dot_shape` as
  primary; `combined_shape` framed as the test-system alias.
- `CONTRIBUTING.md` line 53: "Cylinder shapes (card temporarily
  hidden)" → "Cylinder shape (card support permanently removed)".
- `docs/archive/README.md` index now lists the newly archived
  audit document.

## [2.1.0] - 2026-01-11

Last tagged release prior to the v2.2.0 cleanup. See git history for details.
