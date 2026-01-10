"""Quick test script for counter plate generation with low quality settings."""
import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.openscad_runner import OpenSCADRunner

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

runner = OpenSCADRunner(default_timeout_seconds=600)

# Counter plate with LOW quality for faster rendering
params = {
    "Line_1": "⠓⠑⠇⠇⠕",
    "Line_2": "",
    "Line_3": "",
    "Line_4": "",
    "shape_type": "card",
    "plate_type": "negative",
    "combined_shape": "rounded",
    "indicator_shapes": "on",
    "card_width": 90.0,
    "card_height": 52.0,
    "card_thickness": 2.0,
    "grid_columns": 11,
    "grid_rows": 4,
    "cell_spacing": 6.5,
    "line_spacing": 10.0,
    "dot_spacing": 2.5,
    "braille_x_adjust": 0.0,
    "braille_y_adjust": 0.0,
    "rounded_dot_base_diameter": 2.0,
    "rounded_dot_base_height": 0.2,
    "rounded_dot_dome_diameter": 1.5,
    "rounded_dot_dome_height": 0.6,
    "bowl_counter_dot_base_diameter": 1.8,
    "counter_dot_depth": 0.8,
    "hemisphere_quality": "low",  # LOW quality for faster rendering
    "cone_segments": 8,  # Fewer segments
}

print("Testing counter plate with LOW quality (should be faster)...")
print("Timeout set to 10 minutes. Progress updates every 15 seconds.")
print()

result = runner.generate_stl(
    Path("Braille_Card_And_Cylinder_STL_Generator.scad"),
    Path("tests/fixtures/cross_platform/card_rounded_counter_basic/reference.stl"),
    params,
    timeout_seconds=600,
)

print()
print(f"Success: {result.success}")
print(f"Duration: {result.duration_seconds:.1f}s")
if not result.success:
    print(f"Error: {result.stderr}")
