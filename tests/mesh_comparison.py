"""
Mesh Comparison Module for Cross-Platform STL Validation

This module provides mesh comparison capabilities using:
1. trimesh for property-based comparison (volume, area, bbox, watertightness)
2. CloudCompare CLI for optional numeric surface deviation (Hausdorff-like distance)

License: PolyForm Noncommercial 1.0.0
"""

import json
import logging
import platform
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import numpy as np
import trimesh

logger = logging.getLogger(__name__)


@dataclass
class MeshProperties:
    """Properties extracted from a mesh."""

    volume: float  # mm³
    surface_area: float  # mm²
    bounding_box: np.ndarray  # [[min_x, min_y, min_z], [max_x, max_y, max_z]]
    face_count: int
    vertex_count: int
    is_watertight: bool
    centroid: np.ndarray  # [x, y, z]


@dataclass
class ComparisonResult:
    """Result of mesh comparison."""

    passed: bool
    reference_properties: MeshProperties
    test_properties: MeshProperties

    # Differences
    volume_diff_percent: float
    surface_area_diff_percent: float
    bounding_box_diff_mm: float
    face_count_diff: int
    vertex_count_diff: int
    watertightness_match: bool

    # Optional numeric deviation (CloudCompare)
    max_surface_deviation_mm: Optional[float] = None
    mean_surface_deviation_mm: Optional[float] = None
    cloudcompare_available: bool = False

    # ICP alignment info
    icp_performed: bool = False
    icp_rms_mm: Optional[float] = None

    # Failures
    failures: list = field(default_factory=list)

    # Metadata
    comparison_time_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "passed": self.passed,
            "reference_properties": {
                "volume_mm3": self.reference_properties.volume,
                "surface_area_mm2": self.reference_properties.surface_area,
                "bounding_box_mm": self.reference_properties.bounding_box.tolist(),
                "face_count": self.reference_properties.face_count,
                "vertex_count": self.reference_properties.vertex_count,
                "is_watertight": self.reference_properties.is_watertight,
                "centroid_mm": self.reference_properties.centroid.tolist(),
            },
            "test_properties": {
                "volume_mm3": self.test_properties.volume,
                "surface_area_mm2": self.test_properties.surface_area,
                "bounding_box_mm": self.test_properties.bounding_box.tolist(),
                "face_count": self.test_properties.face_count,
                "vertex_count": self.test_properties.vertex_count,
                "is_watertight": self.test_properties.is_watertight,
                "centroid_mm": self.test_properties.centroid.tolist(),
            },
            "differences": {
                "volume_diff_percent": self.volume_diff_percent,
                "surface_area_diff_percent": self.surface_area_diff_percent,
                "bounding_box_diff_mm": self.bounding_box_diff_mm,
                "face_count_diff": self.face_count_diff,
                "vertex_count_diff": self.vertex_count_diff,
                "watertightness_match": self.watertightness_match,
            },
            "numeric_deviation": {
                "max_surface_deviation_mm": self.max_surface_deviation_mm,
                "mean_surface_deviation_mm": self.mean_surface_deviation_mm,
                "cloudcompare_available": self.cloudcompare_available,
            },
            "alignment": {
                "icp_performed": self.icp_performed,
                "icp_rms_mm": self.icp_rms_mm,
            },
            "failures": self.failures,
            "comparison_time_seconds": self.comparison_time_seconds,
        }


class MeshComparator:
    """
    Compare two STL meshes using multiple metrics.

    Provides:
    - Property-based comparison (trimesh)
    - Optional numeric deviation (CloudCompare CLI)
    - Optional ICP alignment before comparison
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize mesh comparator with configuration.

        Args:
            config: Configuration dict (from tests/compare_config.json)
        """
        self.config = config
        self.tolerances = config["tolerances"]
        self.required_checks = config["required_checks"]
        self.alignment_config = config["alignment"]
        self.cloudcompare_config = config.get("cloudcompare", {})

        # Try to find CloudCompare (optional)
        self.cloudcompare_path = self._find_cloudcompare()
        if self.cloudcompare_path:
            logger.info(f"CloudCompare found: {self.cloudcompare_path}")
        else:
            logger.warning(
                "CloudCompare not found - numeric deviation checks will be skipped"
            )

    def _find_cloudcompare(self) -> Optional[Path]:
        """Find CloudCompare executable (optional)."""
        # Check if in PATH
        cc_cmd = shutil.which("CloudCompare")
        if cc_cmd:
            return Path(cc_cmd)

        # Platform-specific paths
        system = platform.system()
        if system == "Windows":
            paths = [
                Path(r"C:\Program Files\CloudCompare\CloudCompare.exe"),
            ]
        elif system == "Darwin":
            paths = [
                Path(
                    "/Applications/CloudCompare.app/Contents/MacOS/CloudCompare"
                ),
            ]
        elif system == "Linux":
            paths = [
                Path("/snap/bin/cloudcompare"),
                Path("/usr/bin/cloudcompare"),
                Path("/usr/local/bin/cloudcompare"),
            ]
        else:
            paths = []

        for path in paths:
            if path.exists():
                return path

        return None

    def load_mesh(self, stl_path: Path) -> trimesh.Trimesh:
        """
        Load STL file as trimesh.

        Args:
            stl_path: Path to STL file

        Returns:
            Loaded mesh

        Raises:
            FileNotFoundError: If STL file doesn't exist
            ValueError: If STL file is invalid
        """
        if not stl_path.exists():
            raise FileNotFoundError(f"STL file not found: {stl_path}")

        try:
            mesh = trimesh.load(stl_path, force="mesh")
            logger.debug(
                f"Loaded mesh: {mesh.faces.shape[0]} faces, "
                f"{mesh.vertices.shape[0]} vertices"
            )
            return mesh
        except Exception as e:
            raise ValueError(f"Failed to load STL {stl_path}: {e}")

    def extract_properties(self, mesh: trimesh.Trimesh) -> MeshProperties:
        """
        Extract properties from mesh.

        Args:
            mesh: trimesh mesh

        Returns:
            MeshProperties with extracted data
        """
        return MeshProperties(
            volume=float(mesh.volume),
            surface_area=float(mesh.area),
            bounding_box=mesh.bounds,
            face_count=len(mesh.faces),
            vertex_count=len(mesh.vertices),
            is_watertight=mesh.is_watertight,
            centroid=mesh.centroid,
        )

    def compare(
        self, reference_stl: Path, test_stl: Path
    ) -> ComparisonResult:
        """
        Compare two STL files.

        Args:
            reference_stl: Path to reference STL (web generator)
            test_stl: Path to test STL (OpenSCAD)

        Returns:
            ComparisonResult with all metrics
        """
        import time

        start_time = time.time()

        # Load meshes
        ref_mesh = self.load_mesh(reference_stl)
        test_mesh = self.load_mesh(test_stl)

        # Extract properties
        ref_props = self.extract_properties(ref_mesh)
        test_props = self.extract_properties(test_mesh)

        # Calculate differences
        volume_diff_pct = (
            abs(ref_props.volume - test_props.volume)
            / ref_props.volume
            * 100.0
            if ref_props.volume > 0
            else 0.0
        )

        area_diff_pct = (
            abs(ref_props.surface_area - test_props.surface_area)
            / ref_props.surface_area
            * 100.0
            if ref_props.surface_area > 0
            else 0.0
        )

        bbox_diff = np.max(np.abs(ref_props.bounding_box - test_props.bounding_box))

        face_diff = abs(ref_props.face_count - test_props.face_count)
        vertex_diff = abs(ref_props.vertex_count - test_props.vertex_count)
        watertight_match = (
            ref_props.is_watertight == test_props.is_watertight
        )

        # Check for alignment needs
        icp_performed = False
        icp_rms = None

        centroid_distance = np.linalg.norm(
            ref_props.centroid - test_props.centroid
        )
        threshold = self.alignment_config["icp"]["threshold_for_alignment_mm"]

        if centroid_distance > threshold:
            logger.info(
                f"Centroid distance {centroid_distance:.3f}mm > {threshold}mm, "
                f"ICP alignment recommended but not yet implemented"
            )
            # TODO: Implement ICP alignment with CloudCompare
            # For now, just log the warning

        # Numeric deviation (optional, requires CloudCompare)
        max_deviation = None
        mean_deviation = None
        cloudcompare_available = self.cloudcompare_path is not None

        if cloudcompare_available and self.cloudcompare_config.get(
            "enabled", True
        ):
            try:
                max_deviation, mean_deviation = self._compute_surface_deviation(
                    reference_stl, test_stl
                )
            except Exception as e:
                logger.warning(
                    f"CloudCompare surface deviation computation failed: {e}"
                )

        # Check against tolerances
        failures = []

        # Volume check
        if self.required_checks["volume"]["required"]:
            vol_tol = self.tolerances["volume"]["percent"]
            if volume_diff_pct > vol_tol:
                failures.append(
                    f"Volume difference {volume_diff_pct:.2f}% exceeds "
                    f"tolerance {vol_tol}%"
                )

        # Surface area check
        if self.required_checks["surface_area"]["required"]:
            area_tol = self.tolerances["surface_area"]["percent"]
            if area_diff_pct > area_tol:
                failures.append(
                    f"Surface area difference {area_diff_pct:.2f}% exceeds "
                    f"tolerance {area_tol}%"
                )

        # Bounding box check
        if self.required_checks["bounding_box"]["required"]:
            bbox_tol = self.tolerances["bounding_box"]["mm"]
            if bbox_diff > bbox_tol:
                failures.append(
                    f"Bounding box difference {bbox_diff:.3f}mm exceeds "
                    f"tolerance {bbox_tol}mm"
                )

        # Watertightness check
        if self.required_checks["watertightness"]["required"]:
            if not watertight_match:
                failures.append(
                    f"Watertightness mismatch: ref={ref_props.is_watertight}, "
                    f"test={test_props.is_watertight}"
                )
            if (
                self.required_checks["watertightness"]["must_match"]
                and not test_props.is_watertight
            ):
                failures.append("Test mesh is not watertight (required)")

        # Numeric deviation check (optional)
        if (
            max_deviation is not None
            and not self.required_checks["max_surface_deviation"].get(
                "skip_if_missing_tools", False
            )
        ):
            dev_tol = self.tolerances["max_surface_deviation"]["mm"]
            if max_deviation > dev_tol:
                failures.append(
                    f"Max surface deviation {max_deviation:.3f}mm exceeds "
                    f"tolerance {dev_tol}mm"
                )

        passed = len(failures) == 0
        duration = time.time() - start_time

        return ComparisonResult(
            passed=passed,
            reference_properties=ref_props,
            test_properties=test_props,
            volume_diff_percent=volume_diff_pct,
            surface_area_diff_percent=area_diff_pct,
            bounding_box_diff_mm=float(bbox_diff),
            face_count_diff=face_diff,
            vertex_count_diff=vertex_diff,
            watertightness_match=watertight_match,
            max_surface_deviation_mm=max_deviation,
            mean_surface_deviation_mm=mean_deviation,
            cloudcompare_available=cloudcompare_available,
            icp_performed=icp_performed,
            icp_rms_mm=icp_rms,
            failures=failures,
            comparison_time_seconds=duration,
        )

    def _compute_surface_deviation(
        self, reference_stl: Path, test_stl: Path
    ) -> Tuple[float, float]:
        """
        Compute surface deviation using CloudCompare CLI.

        This is a placeholder implementation. Full implementation would:
        1. Sample reference mesh → point cloud
        2. Compute C2M distance to test mesh
        3. Sample test mesh → point cloud
        4. Compute C2M distance to reference mesh
        5. Return max(both directions) and mean

        Args:
            reference_stl: Reference STL path
            test_stl: Test STL path

        Returns:
            Tuple of (max_deviation_mm, mean_deviation_mm)

        Raises:
            RuntimeError: If CloudCompare execution fails
        """
        if not self.cloudcompare_path:
            raise RuntimeError("CloudCompare not available")

        # TODO: Implement CloudCompare CLI invocation
        # For now, return None to skip numeric deviation
        logger.warning(
            "CloudCompare surface deviation computation not yet fully implemented"
        )
        return None, None


def main():
    """Example usage and testing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Compare two STL meshes"
    )
    parser.add_argument("reference", type=Path, help="Reference STL file")
    parser.add_argument("test", type=Path, help="Test STL file")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("tests/compare_config.json"),
        help="Comparison config JSON",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        help="Output comparison result as JSON",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    try:
        # Load config
        with open(args.config) as f:
            config = json.load(f)

        # Create comparator
        comparator = MeshComparator(config)

        # Compare meshes
        logger.info(f"Comparing: {args.reference.name} vs {args.test.name}")
        result = comparator.compare(args.reference, args.test)

        # Print results
        print("\n" + "=" * 70)
        print("MESH COMPARISON RESULTS")
        print("=" * 70)
        print(f"Status: {'✓ PASS' if result.passed else '✗ FAIL'}")
        print(f"\nVolume difference: {result.volume_diff_percent:.2f}%")
        print(
            f"Surface area difference: {result.surface_area_diff_percent:.2f}%"
        )
        print(f"Bounding box difference: {result.bounding_box_diff_mm:.3f} mm")
        print(f"Face count difference: {result.face_count_diff}")
        print(f"Vertex count difference: {result.vertex_count_diff}")
        print(
            f"Watertightness match: {'Yes' if result.watertightness_match else 'No'}"
        )

        if result.max_surface_deviation_mm is not None:
            print(
                f"\nMax surface deviation: {result.max_surface_deviation_mm:.3f} mm"
            )
            print(
                f"Mean surface deviation: {result.mean_surface_deviation_mm:.3f} mm"
            )
        elif result.cloudcompare_available:
            print("\nNumeric deviation: Not computed (implementation pending)")
        else:
            print("\nNumeric deviation: Skipped (CloudCompare not available)")

        if result.failures:
            print("\nFailures:")
            for failure in result.failures:
                print(f"  - {failure}")

        print(
            f"\nComparison time: {result.comparison_time_seconds:.2f} seconds"
        )
        print("=" * 70)

        # Save JSON output if requested
        if args.output_json:
            with open(args.output_json, "w") as f:
                json.dump(result.to_dict(), f, indent=2)
            logger.info(f"Results saved to: {args.output_json}")

        return 0 if result.passed else 1

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit(main())
