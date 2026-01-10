"""Generate remaining counter plate fixtures with low quality settings."""
import sys
import json
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import trimesh
from tests.openscad_runner import OpenSCADRunner

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

PROJECT_ROOT = Path(__file__).parent.parent
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures" / "cross_platform"
SCAD_FILE = PROJECT_ROOT / "Braille_Card_And_Cylinder_STL_Generator.scad"

# Load test cases
with open(FIXTURES_DIR / "test_cases.json", encoding="utf-8") as f:
    test_cases_data = json.load(f)

# Counter plates to generate (the ones that need low quality)
counter_plates = [
    "card_rounded_counter_basic",
    "card_cone_counter_basic",
    "cylinder_rounded_counter_basic",
]

runner = OpenSCADRunner(default_timeout_seconds=600)  # 10 min timeout

for tc in test_cases_data["test_cases"]:
    if tc["name"] not in counter_plates:
        continue
    
    test_name = tc["name"]
    fixture_dir = FIXTURES_DIR / test_name
    stl_path = fixture_dir / "reference.stl"
    
    # Check if already exists
    if stl_path.exists():
        print(f"✓ {test_name} already exists, skipping")
        continue
    
    print(f"\n{'='*60}")
    print(f"Generating: {test_name}")
    print(f"{'='*60}")
    
    # Override quality settings for faster generation
    params = tc["parameters"].copy()
    params["hemisphere_quality"] = "low"
    params["cone_segments"] = 8
    
    # Ensure directory exists
    fixture_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate STL
    result = runner.generate_stl(
        scad_file=SCAD_FILE,
        output_stl=stl_path,
        parameters=params,
        timeout_seconds=600,
    )
    
    if not result.success:
        print(f"✗ FAILED: {test_name}")
        print(f"  Error: {result.stderr}")
        continue
    
    print(f"✓ Generated in {result.duration_seconds:.1f}s")
    
    # Extract mesh properties
    stl_content = stl_path.read_bytes()
    checksum = hashlib.sha256(stl_content).hexdigest()
    
    mesh = trimesh.load(stl_path, force="mesh")
    mesh_properties = {
        "volume_mm3": float(mesh.volume),
        "surface_area_mm2": float(mesh.area),
        "bounding_box_mm": mesh.bounds.tolist(),
        "face_count": len(mesh.faces),
        "vertex_count": len(mesh.vertices),
        "is_watertight": mesh.is_watertight,
        "centroid_mm": mesh.centroid.tolist(),
    }
    
    print(f"  Volume: {mesh_properties['volume_mm3']:.2f} mm³")
    print(f"  Faces: {mesh_properties['face_count']}")
    print(f"  Watertight: {mesh_properties['is_watertight']}")
    
    # Save metadata
    metadata = {
        "test_name": test_name,
        "description": tc.get("description", ""),
        "tags": tc.get("tags", []),
        "priority": tc.get("priority", "medium"),
        "reference_stl": f"cross_platform/{test_name}/reference.stl",
        "stl_size_bytes": len(stl_content),
        "stl_sha256": checksum,
        "mesh_properties": mesh_properties,
        "generation": {
            "method": "openscad",
            "openscad_version": runner.get_version(),
            "scad_file": SCAD_FILE.name,
            "duration_seconds": result.duration_seconds,
            "quality_override": "low (for faster generation)",
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    
    with open(fixture_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    # Update params.json with actual params used
    with open(fixture_dir / "params.json", "w", encoding="utf-8") as f:
        json.dump({
            "test_case": test_name,
            "parameters": params,
            "generated_with": "openscad",
            "quality_note": "Generated with low quality for faster OpenSCAD rendering"
        }, f, indent=2, ensure_ascii=False)

print("\n" + "="*60)
print("DONE!")
print("="*60)
