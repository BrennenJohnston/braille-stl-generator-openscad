// Braille Card and Cylinder STL Generator (OpenSCAD)
// Generates embossing plates and counter plates for both card and cylinder shapes
//
// =============================================================================
// WHAT THIS MAKES
// =============================================================================
//  • Card Emboss Plate (Raised Dots) — pushes braille out of the paper
//  • Card Counter Plate (Hemispherical Recesses) — supports the paper
//  • Cylinder Emboss Plate (Raised Dots) — dots on outer cylinder surface
//  • Cylinder Counter Plate (Hemispherical Recesses) — recesses on outer surface
//
// =============================================================================
// BEFORE YOU START
// =============================================================================
//  • Install OpenSCAD and open this .scad file
//  • In OpenSCAD, open View → Customizer to access all parameters
//  • This version requires pre-translated Unicode braille (no automatic translation)
//  • All parameters match the web-based generator UI for consistency
//
// =============================================================================
// TRANSLATE YOUR TEXT (REQUIRED) — BRANAH WORKFLOW
// =============================================================================
//  This OpenSCAD version does NOT include automatic translation. You must:
//  
//  1. Go to https://www.branah.com/braille-translator
//  2. In the options, select your desired braille grade:
//     - Grade 2 (contracted): Recommended for most uses
//     - Grade 1 (uncontracted): For names, emails, or when contractions cause confusion
//  3. Select Unicode Braille output (NOT ASCII Braille)
//  4. Type your English text in the left box
//  5. Copy the braille output (right box showing characters like ⠓⠑⠇⠇⠕)
//  6. In OpenSCAD's Customizer, paste into the Line_1, Line_2, etc. fields
//
//  IMPORTANT: If you paste ordinary English letters or see "INVALID CHARACTERS"
//  warning, re-translate on Branah and ensure Unicode Braille is selected.
//
// =============================================================================
// QUICK START GUIDE
// =============================================================================
//  1. Translate your text at https://www.branah.com/braille-translator
//  2. Paste pre-translated braille into Line_1, Line_2, etc.
//  3. Choose shape_type: Card or Cylinder
//  4. Choose plate_type: Positive (Embossing) or Negative (Counter Plate)
//  5. Choose combined_shape: Rounded or Cone (affects both plates)
//  6. Adjust dimensions in Expert Mode if needed
//  7. Render (F6) → File → Export → STL
//
// =============================================================================
// PARAMETER ORGANIZATION
// =============================================================================
//  Parameters are organized to match the web-based generator:
//
//  MAIN CONTROLS (always visible):
//  • Text Input - Pre-Translated Braille
//  • Shape and Plate Selection
//
//  EXPERT MODE (expandable submenus matching web UI):
//  • Expert Mode - Shape Selection (dot shapes, indicators, output shape)
//  • Expert Mode - Braille Spacing (grid layout + positioning)
//  • Expert Mode - Braille Dot Adjustments (emboss/counter dimensions)
//  • Expert Mode - Surface Dimensions (card and cylinder)
//
//  OPENSCAD-SPECIFIC:
//  • Rendering Quality
//
// =============================================================================
// REFERENCES
// =============================================================================
//  [1] Web-based Generator (with automatic translation): 
//      https://github.com/BrennenJohnston/braille-card-and-cylinder-stl-generator
//      https://braille-card-and-cylinder-stl-gener.vercel.app
//  [2] Branah Braille Translator: https://www.branah.com/braille-translator
//  [3] BANA — Size and Spacing: https://brailleauthority.org/size-and-spacing-braille-characters
//  [4] NLS — Specification 800: https://www.loc.gov/nls/
//  [5] 2010 ADA Standards: https://archive.ada.gov/
//
// =============================================================================
// ACKNOWLEDGMENTS
// =============================================================================
//  This OpenSCAD version is based on the web-based generator by Brennen Johnston.
//  Special thanks to Tobi Weinberg for the substantial time and effort volunteered
//  to help start the original project.
//
//  Original web app powered by Liblouis, an open-source professional braille
//  translator: https://liblouis.io/
// =============================================================================

/* [Text Input - Pre-Translated Braille] */
// Paste Unicode braille characters from https://www.branah.com/braille-translator
Line_1 = "⠓⠑⠇⠇⠕"; // First line of braille text
Line_2 = "⠺⠕⠗⠇⠙"; // Second line of braille text
Line_3 = ""; // Third line of braille text
Line_4 = ""; // Fourth line of braille text

/* [Shape and Plate Selection] */
// Choose the output shape type
// NOTE: Card option temporarily hidden (code preserved) until web UI parity is restored
shape_type = "cylinder"; // ["cylinder:Cylinder (Curved Surface)"]
// Choose which plate to generate
plate_type = "positive"; // ["positive:Embossing Plate", "negative:Universal Counter Plate"]

/* [Expert Mode - Shape Selection] */
// Braille Dot Shape (Emboss and Counter) - affects both plate types
combined_shape = "rounded"; // ["rounded:Rounded", "cone:Cone"]
// Indicator Shapes (Emboss and Counter) - Row start/end markers
indicator_shapes = "on"; // ["on:On", "off:Off"]

/* [Expert Mode - Surface Dimensions] */
// --- Cylinder Dimensions ---
cylinder_diameter_mm = 30.75; // [10:0.1:100] Cylinder outer diameter in mm
cylinder_height_mm = 52; // [20:1:150] Cylinder height in mm
polygon_cutout_radius_mm = 13.0; // [0:0.1:50] Polygonal cutout circumscribed radius (0 = no cutout)
polygon_cutout_points = 12; // [3:1:24] Number of sides/points for polygonal cutout
seam_offset_degrees = 355.0; // [0:1:360] Seam offset (degrees) — Rotates starting position around cylinder

// --- Plate (Card) Dimensions ---
card_width = 90; // [50:1:200] Card width in mm
card_height = 52; // [30:1:150] Card height in mm
card_thickness = 2.0; // [1:0.1:10] Card thickness in mm

/* [Expert Mode - Braille Spacing] */
// --- Braille Dimensions ---
grid_columns = 11; // [1:1:20] Number of braille cells per row available for text (2 cells reserved for indicators when On)
grid_rows = 4; // [1:1:10] Number of lines of braille
cell_spacing = 6.5; // [2:0.1:15] Horizontal spacing between cells (mm)
line_spacing = 10.0; // [5:0.1:25] Vertical spacing between lines (mm)
dot_spacing = 2.5; // [1:0.1:5] Spacing between dots within a cell (mm)

// --- Braille / Card Positioning ---
braille_x_adjust = 0.0; // [-10:0.1:10] Horizontal adjustment of braille pattern (mm)
braille_y_adjust = 0.0; // [-10:0.1:10] Vertical adjustment of braille pattern (mm)

/* [Expert Mode - Braille Dot Adjustments] */
// --- Embossing Braille Dot Dimensions (Rounded Shape) ---
rounded_dot_base_diameter = 2.0; // [0.5:0.1:3] Rounded dot base diameter (cone base) (mm)
rounded_dot_base_height = 0.2; // [0:0.1:2] Rounded dot base height (cone height) (mm)
rounded_dot_dome_diameter = 1.5; // [0.5:0.1:3] Rounded dome diameter (linked to cone flat top) (mm)
rounded_dot_dome_height = 0.6; // [0.1:0.1:2] Rounded dot dome height (mm)

// --- Embossing Braille Dot Dimensions (Cone Shape) ---
emboss_dot_base_diameter = 1.8; // [0.5:0.1:3] Cone dot base diameter (mm)
emboss_dot_height = 1.0; // [0.3:0.1:2] Cone dot height (mm)
emboss_dot_flat_hat = 0.4; // [0.1:0.1:2] Cone dot flat hat diameter (mm)

// --- Counter Braille Recessed Dot Dimensions (Rounded Shape / Bowl) ---
bowl_counter_dot_base_diameter = 1.8; // [0.5:0.1:5] Bowl recess base diameter (mm)
counter_dot_depth = 0.8; // [0.1:0.1:2] Bowl recess depth (mm)

// --- Counter Braille Recessed Dot Dimensions (Cone Shape) ---
cone_counter_dot_base_diameter = 1.6; // [0.5:0.1:3] Cone recess base diameter (mm)
cone_counter_dot_height = 0.8; // [0.3:0.1:2] Cone recess height (mm)
cone_counter_dot_flat_hat = 0.4; // [0.1:0.1:2] Cone recess flat hat diameter (mm)

/* [Rendering Quality] */
// Sphere quality for rounded shapes: Low (16 segments), Medium (32), High (64)
hemisphere_quality = "medium"; // ["low:Low (16)", "medium:Medium (32)", "high:High (64)"]
// Cone segments for cone shapes (8-32 range recommended)
cone_segments = 16; // [8:1:64] Number of segments for cone shapes

/* [Hidden] */
$fn = 32; // Resolution for curved surfaces

// Mathematical constants
PI = 3.14159265359;

// =============================================================================
// CALCULATED VALUES (Do not modify)
// =============================================================================

// Normalize enum-like inputs for robustness (works with legacy numeric toggles and label-valued customizer selections)
shape_type_norm = (shape_type == "card" || shape_type == "card:Card (Flat Plate)") ? "card" :
                  (shape_type == "cylinder" || shape_type == "cylinder:Cylinder (Curved Surface)") ? "cylinder" :
                  shape_type;
plate_type_norm = (plate_type == "positive" || plate_type == "positive:Embossing Plate") ? "positive" :
                  (plate_type == "negative" || plate_type == "negative:Universal Counter Plate") ? "negative" :
                  plate_type;
indicator_on = (indicator_shapes == "on" || indicator_shapes == "on:On" || indicator_shapes == 1 || indicator_shapes == true);
combined_shape_norm = (combined_shape == "rounded" || combined_shape == "rounded:Rounded") ? "rounded" :
                      (combined_shape == "cone" || combined_shape == "cone:Cone") ? "cone" :
                      combined_shape;

// Determine actual dot shape parameters based on combined_shape selection
use_rounded_dots = (combined_shape_norm == "rounded") ? 1 : 0;
use_cone_dots = (combined_shape_norm == "cone") ? 1 : 0;

// Active emboss dot parameters (based on shape selection)
active_emboss_base_diameter = use_rounded_dots ? rounded_dot_base_diameter : emboss_dot_base_diameter;
active_emboss_height = use_rounded_dots ? (rounded_dot_base_height + rounded_dot_dome_height) : emboss_dot_height;
active_emboss_top_diameter = use_rounded_dots ? rounded_dot_dome_diameter : emboss_dot_flat_hat;

// Active counter dot parameters (based on shape selection)
active_counter_base_diameter = use_rounded_dots ? bowl_counter_dot_base_diameter : cone_counter_dot_base_diameter;
active_counter_height = use_rounded_dots ? counter_dot_depth : cone_counter_dot_height;
active_counter_top_diameter = use_rounded_dots ? 0 : cone_counter_dot_flat_hat; // 0 for bowl (sphere)

// Grid dimensions (accounting for indicator shapes if enabled)
actual_grid_columns = indicator_on ? (grid_columns + 2) : grid_columns;
grid_width = (actual_grid_columns - 1) * cell_spacing;
left_margin = (card_width - grid_width) / 2;
grid_height = (grid_rows - 1) * line_spacing;
top_margin = (card_height - grid_height) / 2;

// Counter plate recess radii
bowl_recess_radius = bowl_counter_dot_base_diameter / 2;
hemisphere_radius = bowl_recess_radius; // For backward compatibility

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

// Check if a character is valid Unicode braille (U+2800 to U+28FF)
function is_braille_char(c) = (c >= 10240 && c <= 10495);

// Check if string contains invalid characters
function has_invalid_chars(str) = 
    len(str) == 0 ? false : 
    len([for (i = [0:len(str)-1]) if (!is_braille_char(ord(str[i]))) i]) > 0;

// Get the 6-dot pattern from a Unicode braille character
function get_dot_pattern(char) =
    let(code = ord(char))
    (code >= 10240 && code <= 10495) ?
        let(pattern = code - 10240)
        [
            (pattern % 2) >= 1 ? 1 : 0,              // Dot 1
            floor(pattern / 2) % 2 >= 1 ? 1 : 0,     // Dot 2
            floor(pattern / 4) % 2 >= 1 ? 1 : 0,     // Dot 3
            floor(pattern / 8) % 2 >= 1 ? 1 : 0,     // Dot 4
            floor(pattern / 16) % 2 >= 1 ? 1 : 0,    // Dot 5
            floor(pattern / 32) % 2 >= 1 ? 1 : 0     // Dot 6
        ]
    : [0,0,0,0,0,0]; // Empty pattern for non-braille

// =============================================================================
// DOT CREATION MODULES
// =============================================================================

// Create an embossing braille dot (cone or rounded shape) for CARD surface
// Geometry has base at Z=0, extends upward to Z=total_height
// For cards, dots are simply placed on top of the card surface (no rotation needed)
module braille_dot() {
    if (use_rounded_dots) {
        // Rounded dome dot with cone base - base at z=0, extends upward
        // 
        // Geometry structure:
        //   z=0:                Frustum base (base_diameter)
        //   z=base_height:      Frustum top / Dome base (dome_diameter)  
        //   z=base_height+dome_height: Dome apex
        //
        // Spherical cap (sphere radius) formula:
        //   R = (r² + h²) / (2h)  where r = dome_radius, h = dome_height
        //   Sphere center at z = base_height + dome_height - R
        //   This ensures sphere radius at z=base_height equals dome_diameter/2
        _dome_r = rounded_dot_dome_diameter / 2;
        _R_sphere = (_dome_r * _dome_r + rounded_dot_dome_height * rounded_dot_dome_height) / (2 * rounded_dot_dome_height);
        // Sphere center: cap base at z=base_height, apex at z=base_height+dome_height
        _center_z = rounded_dot_base_height + rounded_dot_dome_height - _R_sphere;
        
        union() {
            // Frustum base: z=0 to z=base_height
            translate([0, 0, rounded_dot_base_height / 2])
            cylinder(
                h = rounded_dot_base_height,
                r1 = rounded_dot_base_diameter / 2,
                r2 = rounded_dot_dome_diameter / 2,
                center = true,
                $fn = cone_segments
            );
            // Dome: proper spherical cap
            // Sphere positioned so cap base radius matches frustum top radius exactly
            intersection() {
                translate([0, 0, _center_z])
                sphere(r = _R_sphere, $fn = 32);
                // Clip to only show the cap (from z=base_height to z=base_height+dome_height)
                // Use large cube extending upward from z=base_height
                translate([0, 0, rounded_dot_base_height + _R_sphere])
                cube([_R_sphere * 4, _R_sphere * 4, _R_sphere * 2], center = true);
            }
        }
    } else {
        // Cone frustum dot - base at z=0, extends upward to z=height
        translate([0, 0, emboss_dot_height / 2])
        cylinder(
            h = emboss_dot_height,
            r1 = emboss_dot_base_diameter / 2,
            r2 = emboss_dot_flat_hat / 2,
            center = true,
            $fn = cone_segments
        );
    }
}

// Create an embossing braille dot CENTERED at origin for CYLINDER surface
// Geometry spans from -totalHeight/2 to +totalHeight/2 along Z axis
// 
// See: OPENSCAD_COORDINATE_SYSTEM_SPECIFICATIONS.md for detailed explanation
// 
// After centering, geometry spans [-totalHeight/2, +totalHeight/2]
// With radialOffset = cylRadius + totalHeight/2:
//   - Inner edge (frustum base) at: radialOffset - totalHeight/2 = cylRadius (flush with surface)
//   - Outer edge (dome top) at: radialOffset + totalHeight/2 = cylRadius + totalHeight
//
// After rotate([0, 90, θ]):
//   - Original +Z axis → radial outward direction (dome points outward) ✓
//   - Original -Z axis → radial inward direction (frustum base touches surface) ✓
module braille_dot_centered() {
    // Calculate total height for centering
    _total_height = use_rounded_dots ? 
                    (rounded_dot_base_height + rounded_dot_dome_height) : 
                    emboss_dot_height;
    
    if (use_rounded_dots) {
        // Spherical cap (sphere radius) formula:
        //   R = (r² + h²) / (2h)  where r = dome_radius, h = dome_height
        _dome_r = rounded_dot_dome_diameter / 2;
        _R_sphere = (_dome_r * _dome_r + rounded_dot_dome_height * rounded_dot_dome_height) / (2 * rounded_dot_dome_height);
        // Sphere center: cap base at z=base_height, apex at z=base_height+dome_height
        _center_z = rounded_dot_base_height + rounded_dot_dome_height - _R_sphere;
        
        // CRITICAL: Translate by -total_height/2 to center the combined geometry at Z=0
        // This ensures the frustum base ends up at -total_height/2 and dome top at +total_height/2
        translate([0, 0, -_total_height / 2]) {
            union() {
                // Frustum base: spans z=0 to z=base_height
                translate([0, 0, rounded_dot_base_height / 2])
                cylinder(
                    h = rounded_dot_base_height,
                    r1 = rounded_dot_base_diameter / 2,
                    r2 = rounded_dot_dome_diameter / 2,
                    center = true,
                    $fn = cone_segments
                );
                // Dome: proper spherical cap with matching junction diameter
                intersection() {
                    translate([0, 0, _center_z])
                    sphere(r = _R_sphere, $fn = 32);
                    // Clip to only show the cap (from z=base_height upward)
                    translate([0, 0, rounded_dot_base_height + _R_sphere])
                    cube([_R_sphere * 4, _R_sphere * 4, _R_sphere * 2], center = true);
                }
            }
        }
    } else {
        // Cone frustum - already centered at origin due to center=true
        // z ∈ [-height/2, +height/2] - no additional centering needed
        cylinder(
            h = emboss_dot_height,
            r1 = emboss_dot_base_diameter / 2,
            r2 = emboss_dot_flat_hat / 2,
            center = true,
            $fn = cone_segments
        );
    }
}

// Create a recess for counter plate (bowl or cone shape)
module counter_recess() {
    // Map quality level (string or legacy numeric) to $fn value
    quality_fn = (hemisphere_quality == "low" || hemisphere_quality == 1) ? 16 :     // Low quality
                 (hemisphere_quality == "medium" || hemisphere_quality == 2) ? 32 :  // Medium quality
                 (hemisphere_quality == "high" || hemisphere_quality == 3) ? 64 : 32; // High quality (default to medium)
    
    if (use_rounded_dots) {
        // Bowl recess (spherical cap)
        intersection() {
            // Sphere
            sphere(r = bowl_recess_radius, $fn = quality_fn);
            // Cut to depth
            translate([0, 0, -counter_dot_depth / 2])
            cube([bowl_counter_dot_base_diameter * 2, bowl_counter_dot_base_diameter * 2, counter_dot_depth], center = true);
        }
    } else {
        // Cone frustum recess
        translate([0, 0, -cone_counter_dot_height / 2])
        cylinder(
            h = cone_counter_dot_height,
            r1 = cone_counter_dot_flat_hat / 2,
            r2 = cone_counter_dot_base_diameter / 2,
            center = true,
            $fn = cone_segments
        );
    }
}

// =============================================================================
// CARD MODULES
// =============================================================================

module card_emboss_plate() {
    // Base card
    cube([card_width, card_height, card_thickness]);
    
    // Check for invalid characters
    invalid_found = has_invalid_chars(Line_1) || has_invalid_chars(Line_2) || 
                   has_invalid_chars(Line_3) || has_invalid_chars(Line_4);
    
    if (invalid_found) {
        translate([card_width/2, card_height/2, card_thickness + 5])
        color("red")
        linear_extrude(height = 2)
        text("INVALID CHARACTERS - Use Branah.com", size = 5, halign = "center", valign = "center");
    }
    
    // Check for oversized text
    lines = [Line_1, Line_2, Line_3, Line_4];
    oversized = (len(Line_1) > grid_columns) || 
                (len(Line_2) > grid_columns) || 
                (len(Line_3) > grid_columns) || 
                (len(Line_4) > grid_columns);
    
    if (oversized) {
        translate([card_width/2, card_height/2, card_thickness + 7])
        color("orange")
        linear_extrude(height = 2)
        text("TEXT TOO LONG", size = 6, halign = "center", valign = "center");
    }
    
    // Dot positioning constants
    dot_col_offsets = [-dot_spacing / 2, dot_spacing / 2];
    dot_row_offsets = [dot_spacing, 0, -dot_spacing];
    dot_positions = [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1]];
    
    // Create indicator shapes if enabled (row start/end markers)
    if (indicator_on) {
        for (row = [0 : grid_rows - 1]) {
            y_pos = card_height - top_margin - (row * line_spacing) + braille_y_adjust;
            
            // Start marker (left side, first column)
            start_x = left_margin + braille_x_adjust;
            translate([start_x, y_pos, card_thickness])
            cylinder(h = active_emboss_height, r = active_emboss_base_diameter / 3, $fn = 16);
            
            // End marker (right side, last column)
            end_x = left_margin + ((actual_grid_columns - 1) * cell_spacing) + braille_x_adjust;
            translate([end_x, y_pos, card_thickness])
            cylinder(h = active_emboss_height, r = active_emboss_base_diameter / 3, $fn = 16);
        }
    }
    
    // Create braille dots
    for (row = [0 : grid_rows - 1]) {
        y_pos = card_height - top_margin - (row * line_spacing) + braille_y_adjust;
        line_text = lines[row];
        
        if (len(line_text) > 0) {
            for (col = [0 : min(grid_columns - 1, len(line_text) - 1)]) {
                // Offset by 1 cell if indicator shapes are enabled
                actual_col = indicator_on ? (col + 1) : col;
                x_pos = left_margin + (actual_col * cell_spacing) + braille_x_adjust;
                dots = get_dot_pattern(line_text[col]);
                
                for (i = [0:5]) {
                    if (dots[i] == 1) {
                        dot_pos = dot_positions[i];
                        dot_x = x_pos + dot_col_offsets[dot_pos[1]];
                        dot_y = y_pos + dot_row_offsets[dot_pos[0]];
                        dot_z = card_thickness;
                        
                        translate([dot_x, dot_y, dot_z])
                        braille_dot();
                    }
                }
            }
        }
    }
}

module card_counter_plate() {
    // Create counter plate with recesses at ALL positions
    difference() {
        // Base plate
        cube([card_width, card_height, card_thickness]);
        
        // Dot positioning constants
        dot_col_offsets = [-dot_spacing / 2, dot_spacing / 2];
        dot_row_offsets = [dot_spacing, 0, -dot_spacing];
        dot_positions = [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1]];
        
        // Create indicator shape recesses if enabled
        if (indicator_on) {
            for (row = [0 : grid_rows - 1]) {
                y_pos = card_height - top_margin - (row * line_spacing) + braille_y_adjust;
                
                // Start marker recess (left side, first column)
                start_x = left_margin + braille_x_adjust;
                translate([start_x, y_pos, card_thickness])
                cylinder(h = active_counter_height * 2, r = active_emboss_base_diameter / 3, center = true, $fn = 16);
                
                // End marker recess (right side, last column)
                end_x = left_margin + ((actual_grid_columns - 1) * cell_spacing) + braille_x_adjust;
                translate([end_x, y_pos, card_thickness])
                cylinder(h = active_counter_height * 2, r = active_emboss_base_diameter / 3, center = true, $fn = 16);
            }
        }
        
        // Create recesses for ALL possible dot positions
        for (row = [0 : grid_rows - 1]) {
            y_pos = card_height - top_margin - (row * line_spacing) + braille_y_adjust;
            
            for (col = [0 : grid_columns - 1]) {
                // Offset by 1 cell if indicator shapes are enabled
                actual_col = indicator_on ? (col + 1) : col;
                x_pos = left_margin + (actual_col * cell_spacing) + braille_x_adjust;
                
                // Create all 6 recesses in this cell
                for (i = [0:5]) {
                    dot_pos = dot_positions[i];
                    dot_x = x_pos + dot_col_offsets[dot_pos[1]];
                    dot_y = y_pos + dot_row_offsets[dot_pos[0]];
                    
                    // Position recess at surface level
                    translate([dot_x, dot_y, card_thickness])
                    counter_recess();
                }
            }
        }
    }
}

// =============================================================================
// CYLINDER MODULES
// =============================================================================

module cylinder_shell() {
    difference() {
        // Outer cylinder
        cylinder(h = cylinder_height_mm, r = cylinder_diameter_mm / 2, center = true);
        
        // Polygonal cutout if specified
        if (polygon_cutout_radius_mm > 0) {
            // Create polygon cutout with specified number of sides
            cylinder(h = cylinder_height_mm + 2, r = polygon_cutout_radius_mm, $fn = polygon_cutout_points, center = true);
        }
    }
}

module cylinder_emboss_plate() {
    // Position cylinder upright for printing and keep all geometry aligned
    translate([0, 0, cylinder_height_mm/2]) {
        // Base cylinder
        cylinder_shell();

        // Check for invalid characters
        invalid_found = has_invalid_chars(Line_1) || has_invalid_chars(Line_2) || 
                       has_invalid_chars(Line_3) || has_invalid_chars(Line_4);
        
        if (invalid_found) {
            translate([0, 0, cylinder_height_mm/2 + 5])
            color("red")
            linear_extrude(height = 2)
            text("INVALID CHARACTERS", size = 5, halign = "center", valign = "center");
        }
        
        // Calculate angular spacing
        radius = cylinder_diameter_mm / 2;
        grid_angle = grid_width / radius;
        start_angle = -grid_angle / 2;
        cell_spacing_angle = cell_spacing / radius;
        
        // Dot positioning with angular offsets
        dot_spacing_angle = dot_spacing / radius;
        dot_col_angle_offsets = [-dot_spacing_angle / 2, dot_spacing_angle / 2];
        dot_row_offsets = [dot_spacing, 0, -dot_spacing];
        dot_positions = [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1]];
        
        // Create indicator shapes if enabled
        if (indicator_on) {
            for (row = [0 : grid_rows - 1]) {
                y_pos = cylinder_height_mm/2 - top_margin - (row * line_spacing) + braille_y_adjust;
                
                // Start marker
                start_angle_deg = start_angle * 180 / PI + seam_offset_degrees;
                start_x = (radius + active_emboss_height/2) * cos(start_angle_deg);
                start_y = (radius + active_emboss_height/2) * sin(start_angle_deg);
                translate([start_x, start_y, y_pos])
                rotate([0, 90, start_angle_deg])
                cylinder(h = active_emboss_height, r = active_emboss_base_diameter / 3, center = true, $fn = 16);
                
                // End marker
                end_angle_rad = start_angle + ((actual_grid_columns - 1) * cell_spacing_angle);
                end_angle_deg = end_angle_rad * 180 / PI + seam_offset_degrees;
                end_x = (radius + active_emboss_height/2) * cos(end_angle_deg);
                end_y = (radius + active_emboss_height/2) * sin(end_angle_deg);
                translate([end_x, end_y, y_pos])
                rotate([0, 90, end_angle_deg])
                cylinder(h = active_emboss_height, r = active_emboss_base_diameter / 3, center = true, $fn = 16);
            }
        }
        
        // Create braille dots on cylinder surface
        lines = [Line_1, Line_2, Line_3, Line_4];
        
        for (row = [0 : min(grid_rows - 1, len(lines) - 1)]) {
            if (len(lines[row]) > 0) {
                y_pos = cylinder_height_mm/2 - top_margin - (row * line_spacing) + braille_y_adjust;
                
                for (col = [0 : min(grid_columns - 1, len(lines[row]) - 1)]) {
                    // Offset by 1 cell if indicator shapes are enabled
                    actual_col = indicator_on ? (col + 1) : col;
                    angle_rad = start_angle + (actual_col * cell_spacing_angle);
                    angle_deg = angle_rad * 180 / PI + seam_offset_degrees;
                    dots = get_dot_pattern(lines[row][col]);
                    
                    for (i = [0:5]) {
                        if (dots[i] == 1) {
                            dot_pos = dot_positions[i];
                            dot_angle_rad = angle_rad + dot_col_angle_offsets[dot_pos[1]];
                            dot_angle_deg = dot_angle_rad * 180 / PI + seam_offset_degrees;
                            dot_y = y_pos + dot_row_offsets[dot_pos[0]];
                            
                            // Transform to cylindrical coordinates
                            x = (radius + active_emboss_height/2) * cos(dot_angle_deg);
                            y = (radius + active_emboss_height/2) * sin(dot_angle_deg);
                            
                            translate([x, y, dot_y])
                            rotate([0, 90, dot_angle_deg])
                            braille_dot_centered();
                        }
                    }
                }
            }
        }
    }
}

module cylinder_counter_plate() {
    // Position cylinder upright for printing
    translate([0, 0, cylinder_height_mm/2])
    difference() {
        // Base cylinder
        cylinder_shell();
        
        // Calculate angular spacing
        radius = cylinder_diameter_mm / 2;
        grid_angle = grid_width / radius;
        start_angle = -grid_angle / 2;
        cell_spacing_angle = cell_spacing / radius;
        
        // Dot positioning with angular offsets
        dot_spacing_angle = dot_spacing / radius;
        dot_col_angle_offsets = [-dot_spacing_angle / 2, dot_spacing_angle / 2];
        dot_row_offsets = [dot_spacing, 0, -dot_spacing];
        dot_positions = [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1]];
        
        // Create indicator shape recesses if enabled
        if (indicator_on) {
            for (row = [0 : grid_rows - 1]) {
                y_pos = cylinder_height_mm/2 - top_margin - (row * line_spacing) + braille_y_adjust;
                
                // Start marker recess
                start_angle_deg = start_angle * 180 / PI + seam_offset_degrees;
                overcut = 0.05;
                start_x = (radius + overcut) * cos(start_angle_deg);
                start_y = (radius + overcut) * sin(start_angle_deg);
                translate([start_x, start_y, y_pos])
                rotate([0, 90, start_angle_deg])
                cylinder(h = active_counter_height * 2, r = active_emboss_base_diameter / 3, center = true, $fn = 16);
                
                // End marker recess
                end_angle_rad = start_angle + ((actual_grid_columns - 1) * cell_spacing_angle);
                end_angle_deg = end_angle_rad * 180 / PI + seam_offset_degrees;
                end_x = (radius + overcut) * cos(end_angle_deg);
                end_y = (radius + overcut) * sin(end_angle_deg);
                translate([end_x, end_y, y_pos])
                rotate([0, 90, end_angle_deg])
                cylinder(h = active_counter_height * 2, r = active_emboss_base_diameter / 3, center = true, $fn = 16);
            }
        }
        
        // Create recesses for ALL possible dot positions
        for (row = [0 : grid_rows - 1]) {
            y_pos = cylinder_height_mm/2 - top_margin - (row * line_spacing) + braille_y_adjust;
            
            for (col = [0 : grid_columns - 1]) {
                // Offset by 1 cell if indicator shapes are enabled
                actual_col = indicator_on ? (col + 1) : col;
                angle_rad = start_angle + (actual_col * cell_spacing_angle);
                angle_deg = angle_rad * 180 / PI + seam_offset_degrees;
                
                for (i = [0:5]) {
                    dot_pos = dot_positions[i];
                    dot_angle_rad = angle_rad + dot_col_angle_offsets[dot_pos[1]];
                    dot_angle_deg = dot_angle_rad * 180 / PI + seam_offset_degrees;
                    dot_y = y_pos + dot_row_offsets[dot_pos[0]];
                    
                    // Transform to cylindrical coordinates
                    // Add small overcut to ensure clean openings
                    overcut = 0.05;
                    x = (radius + overcut) * cos(dot_angle_deg);
                    y = (radius + overcut) * sin(dot_angle_deg);
                    
                    translate([x, y, dot_y])
                    rotate([0, 90, dot_angle_deg])
                    counter_recess();
                }
            }
        }
    }
}

// =============================================================================
// MAIN RENDERING
// =============================================================================

// Select and render the appropriate model based on shape_type and plate_type
    if (shape_type_norm == "card") {
        if (plate_type_norm == "positive") {
        card_emboss_plate();
    } else {
        card_counter_plate();
    }
    } else if (shape_type_norm == "cylinder") {
        if (plate_type_norm == "positive") {
        cylinder_emboss_plate();
    } else {
        cylinder_counter_plate();
    }
}

// End of file
