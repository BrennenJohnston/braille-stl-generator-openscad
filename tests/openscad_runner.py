"""
OpenSCAD CLI Runner for Cross-Platform STL Validation

This module automates OpenSCAD CLI execution to generate STL files from .scad files
with specified parameters. It handles parameter mapping, command construction, and
error handling for the validation framework.

License: PolyForm Noncommercial 1.0.0
"""

import json
import logging
import platform
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


@dataclass
class OpenSCADResult:
    """Result of an OpenSCAD CLI execution."""

    success: bool
    output_path: Optional[Path]
    stdout: str
    stderr: str
    returncode: int
    duration_seconds: float
    command: str


class OpenSCADNotFoundError(Exception):
    """Raised when OpenSCAD executable cannot be found."""

    pass


class OpenSCADExecutionError(Exception):
    """Raised when OpenSCAD execution fails."""

    pass


class OpenSCADRunner:
    """
    Wrapper for OpenSCAD CLI to generate STL files from .scad scripts.

    Handles:
    - OpenSCAD executable detection across platforms
    - Parameter passing via -D flags or parameter files
    - Command construction and execution
    - Timeout handling
    - Error reporting
    """

    def __init__(
        self,
        openscad_path: Optional[Path] = None,
        default_timeout_seconds: int = 300,
    ):
        """
        Initialize OpenSCAD runner.

        Args:
            openscad_path: Path to OpenSCAD executable. If None, auto-detect.
            default_timeout_seconds: Default timeout for OpenSCAD execution
        """
        self.openscad_path = openscad_path or self._find_openscad()
        self.default_timeout_seconds = default_timeout_seconds
        self._verify_openscad()

    def _find_openscad(self) -> Path:
        """
        Auto-detect OpenSCAD executable path based on platform.

        Returns:
            Path to OpenSCAD executable

        Raises:
            OpenSCADNotFoundError: If OpenSCAD cannot be found
        """
        system = platform.system()

        # First check if 'openscad' is in PATH
        openscad_cmd = shutil.which("openscad")
        if openscad_cmd:
            return Path(openscad_cmd)

        # Platform-specific default locations
        if system == "Windows":
            default_paths = [
                Path(r"C:\Program Files\OpenSCAD\openscad.exe"),
                Path(r"C:\Program Files (x86)\OpenSCAD\openscad.exe"),
            ]
        elif system == "Darwin":  # macOS
            default_paths = [
                Path("/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"),
            ]
        elif system == "Linux":
            default_paths = [
                Path("/usr/bin/openscad"),
                Path("/usr/local/bin/openscad"),
                Path("/snap/bin/openscad"),
            ]
        else:
            default_paths = []

        for path in default_paths:
            if path.exists():
                return path

        raise OpenSCADNotFoundError(
            f"OpenSCAD executable not found. Searched PATH and default locations.\n"
            f"Please install OpenSCAD or set OPENSCAD_PATH environment variable.\n"
            f"See tests/tool_versions.yml for installation instructions."
        )

    def _verify_openscad(self) -> None:
        """
        Verify OpenSCAD executable works and get version.

        Raises:
            OpenSCADNotFoundError: If OpenSCAD doesn't work
        """
        try:
            result = subprocess.run(
                [str(self.openscad_path), "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            version_output = result.stdout or result.stderr
            logger.info(f"Found OpenSCAD: {version_output.strip()}")
        except Exception as e:
            raise OpenSCADNotFoundError(
                f"OpenSCAD executable found at {self.openscad_path} but failed to run: {e}"
            )

    def get_version(self) -> str:
        """
        Get OpenSCAD version string.

        Returns:
            Version string (e.g., "OpenSCAD version 2023.12.11")
        """
        result = subprocess.run(
            [str(self.openscad_path), "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return (result.stdout or result.stderr).strip()

    def generate_stl(
        self,
        scad_file: Path,
        output_stl: Path,
        parameters: Optional[Dict[str, Any]] = None,
        timeout_seconds: Optional[int] = None,
    ) -> OpenSCADResult:
        """
        Generate STL file from OpenSCAD file with parameters.

        Args:
            scad_file: Path to .scad input file
            output_stl: Path to output STL file
            parameters: Dictionary of OpenSCAD variables to set (via -D flags)
            timeout_seconds: Execution timeout (uses default if None)

        Returns:
            OpenSCADResult with execution details

        Raises:
            OpenSCADExecutionError: If OpenSCAD execution fails
        """
        import time

        if not scad_file.exists():
            raise FileNotFoundError(f"OpenSCAD file not found: {scad_file}")

        # Ensure output directory exists
        output_stl.parent.mkdir(parents=True, exist_ok=True)

        # Build command
        cmd = self._build_command(scad_file, output_stl, parameters)
        timeout = timeout_seconds or self.default_timeout_seconds

        logger.info(f"Running OpenSCAD: {scad_file.name} -> {output_stl.name}")
        logger.debug(f"Command: {' '.join(cmd)}")

        # Execute OpenSCAD
        start_time = time.time()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=scad_file.parent,  # Run in scad file directory
            )
            duration = time.time() - start_time

            success = result.returncode == 0 and output_stl.exists()

            if not success:
                logger.error(f"OpenSCAD failed (returncode={result.returncode})")
                if result.stderr:
                    logger.error(f"stderr: {result.stderr}")

            return OpenSCADResult(
                success=success,
                output_path=output_stl if success else None,
                stdout=result.stdout,
                stderr=result.stderr,
                returncode=result.returncode,
                duration_seconds=duration,
                command=" ".join(cmd),
            )

        except subprocess.TimeoutExpired as e:
            duration = time.time() - start_time
            logger.error(f"OpenSCAD timed out after {timeout} seconds")
            return OpenSCADResult(
                success=False,
                output_path=None,
                stdout=e.stdout.decode() if e.stdout else "",
                stderr=e.stderr.decode() if e.stderr else "",
                returncode=-1,
                duration_seconds=duration,
                command=" ".join(cmd),
            )

    def _build_command(
        self,
        scad_file: Path,
        output_stl: Path,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> List[str]:
        """
        Build OpenSCAD command with parameters.

        Args:
            scad_file: Path to .scad file
            output_stl: Path to output STL
            parameters: Dictionary of OpenSCAD variables

        Returns:
            Command as list of strings
        """
        cmd = [
            str(self.openscad_path),
            "-o",
            str(output_stl),
        ]

        # Add parameter definitions
        if parameters:
            for key, value in parameters.items():
                cmd.extend(["-D", self._format_parameter(key, value)])

        # Add input file
        cmd.append(str(scad_file))

        return cmd

    def _format_parameter(self, key: str, value: Any) -> str:
        """
        Format parameter for OpenSCAD -D flag.

        Args:
            key: Parameter name
            value: Parameter value

        Returns:
            Formatted parameter string (e.g., 'Line_1="⠓⠑⠇⠇⠕"')
        """
        if isinstance(value, str):
            # Escape quotes and wrap in quotes
            escaped_value = value.replace('"', '\\"')
            return f'{key}="{escaped_value}"'
        elif isinstance(value, bool):
            # OpenSCAD booleans are lowercase true/false
            return f"{key}={str(value).lower()}"
        elif isinstance(value, (int, float)):
            return f"{key}={value}"
        else:
            # For other types, convert to string
            return f'{key}="{str(value)}"'

    def generate_stl_from_json(
        self,
        scad_file: Path,
        output_stl: Path,
        params_json: Path,
        timeout_seconds: Optional[int] = None,
    ) -> OpenSCADResult:
        """
        Generate STL using parameters from JSON file.

        This is a convenience method that loads parameters from a JSON file
        (e.g., test fixture params.json) and calls generate_stl().

        Args:
            scad_file: Path to .scad input file
            output_stl: Path to output STL file
            params_json: Path to JSON file with parameters
            timeout_seconds: Execution timeout

        Returns:
            OpenSCADResult with execution details
        """
        with open(params_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extract parameters - handle both direct params and nested structure
        if "parameters" in data:
            parameters = data["parameters"]
        else:
            parameters = data

        return self.generate_stl(
            scad_file=scad_file,
            output_stl=output_stl,
            parameters=parameters,
            timeout_seconds=timeout_seconds,
        )


def main():
    """Example usage and testing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate STL from OpenSCAD file with parameters"
    )
    parser.add_argument("scad_file", type=Path, help="Input .scad file")
    parser.add_argument("output_stl", type=Path, help="Output STL file")
    parser.add_argument(
        "--params-json", type=Path, help="JSON file with parameters"
    )
    parser.add_argument(
        "--timeout", type=int, default=300, help="Timeout in seconds"
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
        runner = OpenSCADRunner()
        logger.info(f"Using OpenSCAD: {runner.get_version()}")

        if args.params_json:
            result = runner.generate_stl_from_json(
                scad_file=args.scad_file,
                output_stl=args.output_stl,
                params_json=args.params_json,
                timeout_seconds=args.timeout,
            )
        else:
            result = runner.generate_stl(
                scad_file=args.scad_file,
                output_stl=args.output_stl,
                timeout_seconds=args.timeout,
            )

        if result.success:
            logger.info(
                f"✓ STL generated successfully in {result.duration_seconds:.1f}s"
            )
            logger.info(f"  Output: {result.output_path}")
            return 0
        else:
            logger.error("✗ STL generation failed")
            if result.stderr:
                logger.error(f"  Error: {result.stderr}")
            return 1

    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
