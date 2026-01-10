"""
Generate Web Reference Fixtures using Playwright

This script generates reference STL files from the web generator UI
by automating browser interactions to download STLs with specific parameters.

This is the FALLBACK approach since the web API was deprecated (410 Gone as of 2026-01-05).
The PREFERRED approach would be to run the web generator source code headlessly,
but this Playwright automation provides a working alternative.

Usage:
    # Install Playwright browsers first (one-time setup)
    python -m playwright install chromium
    
    # Generate all fixtures from web UI
    python scripts/generate_web_fixtures.py --web-url https://braille-stl-generator.example.com
    
    # Generate specific fixture
    python scripts/generate_web_fixtures.py --web-url https://braille-stl-generator.example.com --test-case cylinder_rounded_emboss_indicators_on
    
    # Dry run (check without downloading)
    python scripts/generate_web_fixtures.py --web-url https://braille-stl-generator.example.com --dry-run

Requirements:
    pip install playwright
    python -m playwright install chromium

License: PolyForm Noncommercial 1.0.0
"""

import argparse
import hashlib
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logger = logging.getLogger(__name__)


class WebFixtureGenerator:
    """Generate reference fixtures from web UI using Playwright automation."""

    def __init__(self, web_url: str, download_dir: Path, headless: bool = True):
        """
        Initialize web fixture generator.

        Args:
            web_url: Base URL of web generator
            download_dir: Directory for downloaded STL files
            headless: Run browser in headless mode
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise ImportError(
                "Playwright is required for web fixture generation.\n"
                "Install with: pip install playwright\n"
                "Then run: python -m playwright install chromium"
            )

        self.web_url = web_url.rstrip("/")
        self.download_dir = download_dir
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def __enter__(self):
        """Context manager entry."""
        from playwright.sync_api import sync_playwright

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        
        # Create context with download path
        self.context = self.browser.new_context(
            accept_downloads=True,
            locale="en-US",
            viewport={"width": 1920, "height": 1080},
        )
        
        self.page = self.context.new_page()
        logger.info(f"Browser initialized (headless={self.headless})")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def navigate_to_generator(self) -> bool:
        """
        Navigate to web generator and verify it's loaded.

        Returns:
            True if successful
        """
        try:
            logger.info(f"Navigating to {self.web_url}")
            self.page.goto(self.web_url, wait_until="networkidle", timeout=30000)
            
            # Wait for key UI elements to be visible
            # Adjust selectors based on actual web UI structure
            self.page.wait_for_selector("textarea, input[type='text']", timeout=10000)
            logger.info("✓ Web generator loaded")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load web generator: {e}")
            return False

    def set_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Set generator parameters in the web UI.

        Args:
            parameters: Test case parameters

        Returns:
            True if successful
        """
        try:
            # Map parameters to web UI controls
            # NOTE: These selectors are PLACEHOLDERS and must be updated
            # based on the actual web UI structure
            
            # Set text lines
            for i in range(1, 5):
                line_key = f"Line_{i}"
                if line_key in parameters:
                    line_value = parameters[line_key]
                    # Placeholder selector - update based on actual UI
                    selector = f"#line{i}, [name='line{i}'], textarea[placeholder*='Line {i}']"
                    try:
                        self.page.fill(selector, line_value, timeout=5000)
                    except:
                        logger.warning(f"Could not set {line_key} (selector may need updating)")
            
            # Set dropdowns (shape_type, plate_type, combined_shape, indicator_shapes)
            dropdown_params = {
                "shape_type": parameters.get("shape_type", "cylinder"),
                "plate_type": parameters.get("plate_type", "positive"),
                "combined_shape": parameters.get("combined_shape", "rounded"),
                "indicator_shapes": parameters.get("indicator_shapes", "on"),
            }
            
            for param_name, param_value in dropdown_params.items():
                # Placeholder selector - update based on actual UI
                selector = f"select[name='{param_name}'], #{param_name}"
                try:
                    self.page.select_option(selector, value=param_value, timeout=5000)
                except:
                    logger.warning(f"Could not set {param_name} (selector may need updating)")
            
            # Set numeric parameters (if exposed in UI)
            # Most numeric params may use defaults in web UI
            
            logger.info("✓ Parameters set")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set parameters: {e}")
            return False

    def download_stl(self, output_path: Path) -> bool:
        """
        Trigger STL download and save to output path.

        Args:
            output_path: Where to save the downloaded STL

        Returns:
            True if successful
        """
        try:
            # Find and click download button
            # Placeholder selector - update based on actual UI
            download_button_selectors = [
                "button:has-text('Download STL')",
                "button:has-text('Generate')",
                "a:has-text('Download')",
                "#download-stl",
                ".download-button",
            ]
            
            download_button = None
            for selector in download_button_selectors:
                try:
                    download_button = self.page.wait_for_selector(selector, timeout=2000)
                    if download_button:
                        break
                except:
                    continue
            
            if not download_button:
                logger.error("Could not find download button (selectors may need updating)")
                return False
            
            # Start waiting for download
            with self.page.expect_download(timeout=60000) as download_info:
                download_button.click()
            
            download = download_info.value
            
            # Save download to output path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            download.save_as(output_path)
            
            logger.info(f"✓ Downloaded STL: {output_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to download STL: {e}")
            return False

    def generate_fixture(
        self, test_case: Dict[str, Any], output_dir: Path
    ) -> Optional[Dict[str, Any]]:
        """
        Generate reference fixture for a test case.

        Args:
            test_case: Test case definition
            output_dir: Output directory for fixtures

        Returns:
            Fixture metadata or None if failed
        """
        test_name = test_case["name"]
        parameters = test_case["parameters"]

        logger.info(f"Generating web fixture: {test_name}")

        # Create fixture directory
        fixture_dir = output_dir / test_name
        fixture_dir.mkdir(parents=True, exist_ok=True)

        # Navigate to generator
        if not self.navigate_to_generator():
            return None

        # Set parameters
        if not self.set_parameters(parameters):
            return None

        # Download STL
        stl_path = fixture_dir / "reference.stl"
        if not self.download_stl(stl_path):
            return None

        # Verify STL file
        if not stl_path.exists() or stl_path.stat().st_size == 0:
            logger.error(f"Downloaded STL is missing or empty: {stl_path}")
            return None

        # Read STL content for checksum
        stl_content = stl_path.read_bytes()
        checksum = hashlib.sha256(stl_content).hexdigest()

        # Extract mesh properties using trimesh
        try:
            import trimesh

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

            logger.info(f"  Volume: {mesh_properties['volume_mm3']:.2f} mm³")
            logger.info(f"  Faces: {mesh_properties['face_count']}")
            logger.info(f"  Watertight: {mesh_properties['is_watertight']}")
        except Exception as e:
            logger.warning(f"Could not extract mesh properties: {e}")
            mesh_properties = {}

        # Save parameters
        params_path = fixture_dir / "params.json"
        with open(params_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "test_case": test_name,
                    "parameters": parameters,
                    "generated_with": "web_ui",
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        # Create metadata
        metadata = {
            "test_name": test_name,
            "description": test_case.get("description", ""),
            "tags": test_case.get("tags", []),
            "priority": test_case.get("priority", "medium"),
            "reference_stl": f"cross_platform/{test_name}/reference.stl",
            "stl_size_bytes": len(stl_content),
            "stl_sha256": checksum,
            "mesh_properties": mesh_properties,
            "generation": {
                "method": "web_ui_playwright",
                "web_url": self.web_url,
                "browser": "chromium",
                "headless": self.headless,
            },
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }

        # Save metadata
        metadata_path = fixture_dir / "metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        return metadata


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate reference fixtures from web UI using Playwright",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate all fixtures from web UI
    python scripts/generate_web_fixtures.py --web-url https://braille-generator.example.com
    
    # Generate specific fixture
    python scripts/generate_web_fixtures.py --web-url https://example.com --test-case cylinder_rounded_emboss_indicators_on
    
    # Dry run (check without downloading)
    python scripts/generate_web_fixtures.py --web-url https://example.com --dry-run
    
    # Run with visible browser (for debugging)
    python scripts/generate_web_fixtures.py --web-url https://example.com --no-headless

Setup:
    pip install playwright
    python -m playwright install chromium
        """,
    )

    parser.add_argument(
        "--web-url",
        required=True,
        help="Base URL of web generator (e.g., https://braille-generator.example.com)",
    )
    parser.add_argument(
        "--test-case",
        help="Generate only a specific test case (by name)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "tests" / "fixtures" / "cross_platform",
        help="Output directory for fixtures",
    )
    parser.add_argument(
        "--test-cases-file",
        type=Path,
        default=PROJECT_ROOT
        / "tests"
        / "fixtures"
        / "cross_platform"
        / "test_cases.json",
        help="Test cases definition file",
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Run browser in visible mode (for debugging)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Check setup without generating fixtures",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    try:
        # Check Playwright installation
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            logger.error("Playwright is not installed.")
            logger.info("Install with: pip install playwright")
            logger.info("Then run: python -m playwright install chromium")
            return 1

        # Load test cases
        with open(args.test_cases_file, encoding="utf-8") as f:
            test_cases_data = json.load(f)
        test_cases = test_cases_data["test_cases"]

        # Filter to specific test case if requested
        if args.test_case:
            test_cases = [tc for tc in test_cases if tc["name"] == args.test_case]
            if not test_cases:
                logger.error(f"Test case not found: {args.test_case}")
                return 1

        if args.dry_run:
            logger.info("=" * 70)
            logger.info("DRY RUN - Setup Check")
            logger.info("=" * 70)
            logger.info(f"Web URL: {args.web_url}")
            logger.info(f"Test cases: {len(test_cases)}")
            logger.info(f"Output dir: {args.output_dir}")
            logger.info("✓ Playwright installed")
            logger.info("=" * 70)
            logger.info("Run without --dry-run to generate fixtures")
            return 0

        # Generate fixtures
        logger.info("=" * 70)
        logger.info("Web UI Fixture Generation (Playwright)")
        logger.info("=" * 70)
        logger.info(f"Web URL: {args.web_url}")
        logger.info(f"Generating {len(test_cases)} fixture(s)...")
        logger.info(f"Output directory: {args.output_dir}")
        logger.info("")

        download_dir = args.output_dir / "downloads"
        download_dir.mkdir(parents=True, exist_ok=True)

        fixtures_metadata = []
        failed_cases = []

        with WebFixtureGenerator(
            web_url=args.web_url,
            download_dir=download_dir,
            headless=not args.no_headless,
        ) as generator:
            for test_case in test_cases:
                test_name = test_case["name"]
                try:
                    metadata = generator.generate_fixture(test_case, args.output_dir)
                    if metadata:
                        fixtures_metadata.append(metadata)
                        logger.info(f"  ✓ {test_name}")
                    else:
                        failed_cases.append(
                            {"name": test_name, "error": "Generation failed"}
                        )
                        logger.error(f"  ✗ {test_name}: Generation failed")
                except Exception as e:
                    logger.error(f"  ✗ {test_name}: {e}")
                    failed_cases.append({"name": test_name, "error": str(e)})

        # Create version file
        version_info = {
            "version": "1.0.0",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "generation_method": "web_ui_playwright",
            "web_url": args.web_url,
            "total_fixtures": len(fixtures_metadata),
            "failed_fixtures": len(failed_cases),
            "fixtures": fixtures_metadata,
        }

        if failed_cases:
            version_info["failures"] = failed_cases

        # Save version files
        version_txt_path = args.output_dir / "FIXTURES_VERSION.txt"
        with open(version_txt_path, "w") as f:
            f.write("# Reference Fixture Version Information\n")
            f.write(f"# Generated: {version_info['generated_at']}\n")
            f.write(f"# Method: Web UI (Playwright automation)\n")
            f.write(f"# Web URL: {version_info['web_url']}\n")
            f.write(f"# Total fixtures: {version_info['total_fixtures']}\n")
            f.write(f"# Failed: {version_info['failed_fixtures']}\n")
            f.write("\n")
            f.write("# See FIXTURES_VERSION.json for full metadata\n")

        version_json_path = args.output_dir / "FIXTURES_VERSION.json"
        with open(version_json_path, "w") as f:
            json.dump(version_info, f, indent=2)

        # Print summary
        print("\n" + "=" * 70)
        print("WEB FIXTURE GENERATION COMPLETE")
        print("=" * 70)
        print(f"  Generated: {version_info['total_fixtures']}")
        print(f"  Failed: {version_info['failed_fixtures']}")
        print(f"  Method: Web UI (Playwright)")
        print(f"  Web URL: {version_info['web_url']}")
        print(f"  Output: {args.output_dir}")
        print("=" * 70)

        if version_info["failed_fixtures"] > 0:
            logger.warning("Some fixtures failed to generate")
            logger.info(
                "NOTE: Web UI selectors may need updating based on actual UI structure"
            )
            return 1

        logger.info("✓ All fixtures generated successfully")
        return 0

    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.verbose)
        return 1


if __name__ == "__main__":
    sys.exit(main())
