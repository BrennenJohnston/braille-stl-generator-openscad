"""
Regenerate Reference Fixtures from Web Generator

This script generates reference STL files from the web-based generator
to serve as the ground truth for cross-platform validation.

It:
1. Loads test cases from tests/fixtures/cross_platform/test_cases.json
2. Calls the web generator API for each test case
3. Saves reference STL files to fixture directories
4. Records fixture version metadata

Usage:
    python scripts/regenerate_fixtures.py [--web-api-url URL] [--test-case NAME]

License: PolyForm Noncommercial 1.0.0
"""

import argparse
import hashlib
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logger = logging.getLogger(__name__)

# Default web API URL (update this to point to your deployed web generator)
DEFAULT_WEB_API_URL = "http://localhost:5000"  # Local development
# For production: "https://braille-card-and-cylinder-stl-gener.vercel.app"


class FixtureGenerator:
    """Generate reference fixtures from web generator API."""

    def __init__(self, web_api_url: str):
        """
        Initialize fixture generator.

        Args:
            web_api_url: Base URL of web generator API
        """
        self.web_api_url = web_api_url.rstrip("/")
        self.session = requests.Session()

    def check_api_health(self) -> bool:
        """
        Check if web API is accessible.

        Returns:
            True if API is healthy
        """
        try:
            response = self.session.get(f"{self.web_api_url}/health", timeout=5)
            if response.status_code == 200:
                logger.info(f"✓ Web API is accessible: {self.web_api_url}")
                return True
            else:
                logger.error(
                    f"Web API returned status {response.status_code}"
                )
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Cannot reach web API: {e}")
            return False

    def generate_stl(self, parameters: Dict[str, Any]) -> bytes:
        """
        Generate STL from web API.

        Args:
            parameters: Test case parameters

        Returns:
            STL file content as bytes

        Raises:
            RuntimeError: If API request fails
        """
        # Map parameters to web API format
        # The web API expects a specific request format
        # Adjust this based on your actual web API endpoint

        api_params = self._map_params_for_web_api(parameters)

        logger.debug(f"Calling web API with params: {list(api_params.keys())}")

        try:
            response = self.session.post(
                f"{self.web_api_url}/generate_braille_stl",
                json=api_params,
                timeout=60,
            )

            if response.status_code == 200:
                # Check if response is STL (binary) or JSON (error)
                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type:
                    error_data = response.json()
                    raise RuntimeError(
                        f"API returned JSON instead of STL: {error_data}"
                    )
                return response.content
            else:
                raise RuntimeError(
                    f"API request failed with status {response.status_code}: "
                    f"{response.text}"
                )

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")

    def _map_params_for_web_api(
        self, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Map test case parameters to web API format.

        The web API uses snake_case parameter names (matching OpenSCAD),
        so this is mostly a pass-through, but we may need to handle
        special cases or structure differences.

        Args:
            parameters: Test case parameters (from test_cases.json)

        Returns:
            Parameters formatted for web API
        """
        # For now, pass through directly since both use snake_case
        # and the parameter names are aligned
        return parameters.copy()

    def generate_fixture(
        self, test_case: Dict[str, Any], output_dir: Path
    ) -> Dict[str, Any]:
        """
        Generate reference fixture for a test case.

        Args:
            test_case: Test case definition
            output_dir: Output directory for fixture

        Returns:
            Fixture metadata
        """
        test_name = test_case["name"]
        parameters = test_case["parameters"]

        logger.info(f"Generating fixture: {test_name}")

        # Create output directory
        fixture_dir = output_dir / test_name
        fixture_dir.mkdir(parents=True, exist_ok=True)

        # Generate STL from web API
        try:
            stl_content = self.generate_stl(parameters)
        except RuntimeError as e:
            logger.error(f"Failed to generate STL for {test_name}: {e}")
            raise

        # Save STL file
        stl_path = fixture_dir / "reference.stl"
        stl_path.write_bytes(stl_content)
        logger.info(f"  Saved: {stl_path} ({len(stl_content)} bytes)")

        # Compute checksum
        checksum = hashlib.sha256(stl_content).hexdigest()

        # Save parameters
        params_path = fixture_dir / "params.json"
        with open(params_path, "w", encoding="utf-8") as f:
            json.dump(parameters, f, indent=2, ensure_ascii=False)

        # Create metadata
        metadata = {
            "test_name": test_name,
            "description": test_case.get("description", ""),
            "tags": test_case.get("tags", []),
            "priority": test_case.get("priority", "medium"),
            "reference_stl": str(stl_path.relative_to(output_dir.parent)),
            "stl_size_bytes": len(stl_content),
            "stl_sha256": checksum,
            "parameters_file": str(params_path.relative_to(output_dir.parent)),
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }

        # Save metadata
        metadata_path = fixture_dir / "metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        return metadata

    def generate_all_fixtures(
        self, test_cases: List[Dict[str, Any]], output_dir: Path
    ) -> Dict[str, Any]:
        """
        Generate all reference fixtures.

        Args:
            test_cases: List of test case definitions
            output_dir: Output directory for fixtures

        Returns:
            Summary metadata for all fixtures
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        fixtures_metadata = []
        failed_cases = []

        for test_case in test_cases:
            test_name = test_case["name"]
            try:
                metadata = self.generate_fixture(test_case, output_dir)
                fixtures_metadata.append(metadata)
            except Exception as e:
                logger.error(f"Failed to generate {test_name}: {e}")
                failed_cases.append({"name": test_name, "error": str(e)})

        # Create version file
        version_info = {
            "version": "1.0.0",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "web_api_url": self.web_api_url,
            "web_generator_commit": "TBD",  # TODO: Get from API if available
            "total_fixtures": len(fixtures_metadata),
            "failed_fixtures": len(failed_cases),
            "fixtures": fixtures_metadata,
        }

        if failed_cases:
            version_info["failures"] = failed_cases

        version_path = output_dir / "FIXTURES_VERSION.txt"
        with open(version_path, "w") as f:
            f.write("# Reference Fixture Version Information\n")
            f.write(f"# Generated: {version_info['generated_at']}\n")
            f.write(f"# Web API: {version_info['web_api_url']}\n")
            f.write(f"# Total fixtures: {version_info['total_fixtures']}\n")
            f.write("\n")
            f.write("# See FIXTURES_VERSION.json for full metadata\n")

        version_json_path = output_dir / "FIXTURES_VERSION.json"
        with open(version_json_path, "w") as f:
            json.dump(version_info, f, indent=2)

        logger.info(f"\n{'='*70}")
        logger.info(f"Fixture generation complete:")
        logger.info(f"  Generated: {len(fixtures_metadata)}")
        logger.info(f"  Failed: {len(failed_cases)}")
        logger.info(f"  Version file: {version_path}")
        logger.info(f"{'='*70}")

        return version_info


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate reference fixtures from web generator"
    )
    parser.add_argument(
        "--web-api-url",
        default=DEFAULT_WEB_API_URL,
        help=f"Web generator API URL (default: {DEFAULT_WEB_API_URL})",
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
        "--verbose", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check if web API is accessible",
    )

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    try:
        # Create generator
        generator = FixtureGenerator(args.web_api_url)

        # Check API health
        if not generator.check_api_health():
            logger.error("Web API is not accessible. Cannot generate fixtures.")
            logger.error(
                f"Please ensure the web generator is running at: {args.web_api_url}"
            )
            logger.error(
                "\nFor local development, you can start the web generator with:"
            )
            logger.error("  cd <web-generator-repo>")
            logger.error("  python app.py")
            return 1

        if args.check_only:
            logger.info("✓ Web API check complete")
            return 0

        # Load test cases
        with open(args.test_cases_file, encoding="utf-8") as f:
            test_cases_data = json.load(f)

        test_cases = test_cases_data["test_cases"]

        # Filter to specific test case if requested
        if args.test_case:
            test_cases = [
                tc for tc in test_cases if tc["name"] == args.test_case
            ]
            if not test_cases:
                logger.error(f"Test case not found: {args.test_case}")
                return 1

        # Generate fixtures
        logger.info(
            f"Generating {len(test_cases)} fixture(s) from {args.web_api_url}"
        )
        version_info = generator.generate_all_fixtures(
            test_cases, args.output_dir
        )

        if version_info["failed_fixtures"] > 0:
            logger.warning("Some fixtures failed to generate")
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
