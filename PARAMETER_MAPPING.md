# OpenSCAD to Web App Parameter Mapping

This document maps the OpenSCAD customizer parameters to the web-based braille generator UI controls.

**Note:** This repository contains only the OpenSCAD generator. For the web app source code, see [braille-card-and-cylinder-stl-generator](https://github.com/BrennenJohnston/braille-card-and-cylinder-stl-generator). This mapping ensures the OpenSCAD Customizer stays aligned with web UI terminology and defaults.

## Overview

The OpenSCAD version has been updated to match the web-based generator's UI parameters exactly. The only difference is that the OpenSCAD version requires **pre-translated Unicode braille** characters (no automatic translation).

## Translation Workflow

1. **Web App**: Automatic translation using Liblouis (Grade 1 or Grade 2)
2. **OpenSCAD**: Manual translation required at https://www.branah.com/braille-translator
   - User must select Grade 1 or Grade 2 manually
   - Copy Unicode braille output
   - Paste into OpenSCAD Line_1, Line_2, etc.

## Parameter Mapping

### Text Input - Pre-Translated Braille
| OpenSCAD Parameter | Web App Equivalent | Notes |
|--------------------|-------------------|-------|
| `Line_1` | Line 1 text input | Must be pre-translated Unicode braille |
| `Line_2` | Line 2 text input | Must be pre-translated Unicode braille |
| `Line_3` | Line 3 text input | Must be pre-translated Unicode braille |
| `Line_4` | Line 4 text input | Must be pre-translated Unicode braille |

### Shape and Plate Selection
| OpenSCAD Parameter | Web App Equivalent | Values |
|--------------------|-------------------|--------|
| `shape_type` | Output Shape | `"card"`, `"cylinder"` |
| `plate_type` | Select Plate to Generate | `"positive"` (Embossing Plate), `"negative"` (Counter Plate) |

### Expert Mode - Shape Selection
| OpenSCAD Parameter | Web App Equivalent | Values |
|--------------------|-------------------|--------|
| `combined_shape` | Braille Dot Shape | `"rounded"`, `"cone"` |
| `indicator_shapes` | Indicator Shapes | `"on"`, `"off"` |

### Expert Mode - Card Dimensions
| OpenSCAD Parameter | Web App Equivalent | Default | Range |
|--------------------|-------------------|---------|-------|
| `card_width` | Card Width | 90 mm | 50-200 mm |
| `card_height` | Card Height | 52 mm | 30-150 mm |
| `card_thickness` | Card Thickness | 2.0 mm | 1-10 mm |

### Expert Mode - Cylinder Dimensions
| OpenSCAD Parameter | Web App Equivalent | Default | Range |
|--------------------|-------------------|---------|-------|
| `cylinder_diameter_mm` | Diameter | 30.75 mm | 10-100 mm |
| `cylinder_height_mm` | Height | 52 mm | 20-150 mm |
| `polygon_cutout_radius_mm` | Cutout Radius | 13.0 mm | 0-50 mm |
| `polygon_cutout_points` | Cutout Points/Sides | 12 | 3-24 |
| `seam_offset_degrees` | Seam Offset | 355.0° | 0-360° |

### Expert Mode - Braille Spacing
| OpenSCAD Parameter | Web App Equivalent | Default | Range |
|--------------------|-------------------|---------|-------|
| `grid_columns` | Number of Braille Cells | 11 | 1-20 |
| `grid_rows` | Number of Braille Lines | 4 | 1-10 |
| `cell_spacing` | Braille Cell Spacing | 6.5 mm | 2-15 mm |
| `line_spacing` | Braille Line Spacing | 10.0 mm | 5-25 mm |
| `dot_spacing` | Braille Dot Spacing | 2.5 mm | 1-5 mm |

### Expert Mode - Braille Positioning
| OpenSCAD Parameter | Web App Equivalent | Default | Range |
|--------------------|-------------------|---------|-------|
| `braille_x_adjust` | X Adjust | 0.0 mm | -10 to 10 mm |
| `braille_y_adjust` | Y Adjust | 0.0 mm | -10 to 10 mm |

### Expert Mode - Emboss Dot Dimensions (Rounded Shape)
| OpenSCAD Parameter | Web App Equivalent | Default | Range |
|--------------------|-------------------|---------|-------|
| `rounded_dot_base_diameter` | Rounded dot base diameter (cone base) | 2.0 mm | 0.5-3 mm |
| `rounded_dot_base_height` | Rounded dot base height (cone height) | 0.2 mm | 0-2 mm |
| `rounded_dot_dome_diameter` | Rounded dome diameter | 1.5 mm | 0.5-3 mm |
| `rounded_dot_dome_height` | Rounded dot dome height | 0.6 mm | 0.1-2 mm |

### Expert Mode - Emboss Dot Dimensions (Cone Shape)
| OpenSCAD Parameter | Web App Equivalent | Default | Range |
|--------------------|-------------------|---------|-------|
| `emboss_dot_base_diameter` | Dot diameter | 1.8 mm | 0.5-3 mm |
| `emboss_dot_height` | Dot height | 1.0 mm | 0.3-2 mm |
| `emboss_dot_flat_hat` | Flat hat diameter | 0.4 mm | 0.1-2 mm |

### Expert Mode - Counter Dot Dimensions (Rounded Shape / Bowl)
| OpenSCAD Parameter | Web App Equivalent | Default | Range |
|--------------------|-------------------|---------|-------|
| `bowl_counter_dot_base_diameter` | Bowl Recess Dot Base Diameter | 1.8 mm | 0.5-5 mm |
| `counter_dot_depth` | Bowl Recess Depth | 0.8 mm | 0.1-2 mm |

### Expert Mode - Counter Dot Dimensions (Cone Shape)
| OpenSCAD Parameter | Web App Equivalent | Default | Range |
|--------------------|-------------------|---------|-------|
| `cone_counter_dot_base_diameter` | Cone recess base diameter | 1.6 mm | 0.5-3 mm |
| `cone_counter_dot_height` | Cone recess height | 0.8 mm | 0.3-2 mm |
| `cone_counter_dot_flat_hat` | Cone recess flat hat diameter | 0.4 mm | 0.1-2 mm |

### Rendering Quality
| OpenSCAD Parameter | Web App Equivalent | Default | Values |
|--------------------|-------------------|---------|--------|
| `hemisphere_quality` | Hemisphere Quality | `"medium"` | `"low"` (16 segments), `"medium"` (32 segments), `"high"` (64 segments) |
| `cone_segments` | Cone Segments | 16 | 8-64 |

## Key Features Implemented

### 1. **Unified Shape Selection**
- `combined_shape` parameter controls both emboss and counter plate dot shapes
- When set to `"rounded"`: Uses rounded dome dots for emboss, bowl recesses for counter
- When set to `"cone"`: Uses cone frustum dots for emboss, cone recesses for counter

### 2. **Indicator Shapes**
- `indicator_shapes = "on"` (On): Adds start/end markers to each row
  - Reserves 2 cells per row (1 at start, 1 at end)
  - Displayed as small cylinders
  - Helps align plates during embossing
- `indicator_shapes = "off"` (Off): All cells available for braille text

### 3. **Flexible Counter Plate Recesses**
- **Bowl Recess (Rounded)**: Spherical cap with adjustable diameter and depth
- **Cone Recess (Cone)**: Frustum cone matching emboss dot shape
- Universal counter plates work for all possible dot positions

### 4. **Multiple Dot Shapes**
- **Rounded**: Cone base + hemispherical dome (more comfortable to touch)
- **Cone**: Frustum cone (traditional, easier to print)

### 5. **Cylinder Support**
- Full parametric control over diameter, height, and polygonal cutout
- Seam offset allows rotation adjustment
- Supports both rounded and cone dot shapes on curved surfaces

## Default Values Alignment

All default values match the web-based generator's defaults:
- Card: 90mm × 52mm (standard business card size)
- Cylinder: 30.75mm diameter
- Grid: 11 text cells × 4 rows (with indicator shapes ON, 2 additional cells are reserved = 13 total)
- Spacing matches BANA specifications
- Default shape: Rounded (bowl recess for counter)

## Workflow Comparison

### Web App Workflow:
1. Enter English text
2. Select language/grade
3. Choose shape and plate type
4. Adjust expert parameters (optional)
5. Generate STL
6. Download

### OpenSCAD Workflow:
1. Translate text at https://www.branah.com/braille-translator
2. Copy Unicode braille output
3. Open OpenSCAD file
4. Paste braille into Line_1, Line_2, etc.
5. Choose shape_type and plate_type in Customizer
6. Adjust expert parameters (optional)
7. Render (F6)
8. Export STL (File → Export → Export as STL)

## Advantages of Each Version

### Web App Advantages:
- ✅ Automatic braille translation (Liblouis)
- ✅ Live 3D preview in browser
- ✅ No software installation required
- ✅ Auto-placement mode (word wrapping)
- ✅ Multi-language support (100+ braille tables)

### OpenSCAD Advantages:
- ✅ Works offline (after text translation)
- ✅ Full parametric control in native CAD environment
- ✅ Can modify and extend code
- ✅ Integration with existing OpenSCAD workflows
- ✅ Version control friendly (plain text .scad files)
- ✅ Batch processing possible via command line

## Notes

1. **Indicator Shapes**: When enabled (`indicator_shapes = "on"`), they reserve the first and last cell of each row. The `grid_columns` parameter represents the number of cells *available for text*, not including indicators. The code internally adds 2 cells when indicators are on.

2. **Rounded vs. Cone**: The web app calls these "Rounded" and "Cone" - both terms refer to the combined emboss+counter shape pair.

3. **Counter Plate Universality**: Counter plates have recesses at ALL possible dot positions (all 6 dots × all cells × all rows), making them universal for any braille pattern.

4. **Parameter Names**: OpenSCAD uses snake_case (e.g., `grid_columns`) to match the web app's JavaScript variable names, ensuring consistency across platforms.

## References

- Web-based Generator: https://braille-card-and-cylinder-stl-gener.vercel.app
- Web App Source: https://github.com/BrennenJohnston/braille-card-and-cylinder-stl-generator
- OpenSCAD Version: https://github.com/BrennenJohnston/braille-stl-generator-openscad
- Branah Braille Translator: https://www.branah.com/braille-translator
- BANA Size & Spacing: https://brailleauthority.org/size-and-spacing-braille-characters


