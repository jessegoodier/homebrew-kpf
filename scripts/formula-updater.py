#!/usr/bin/env python3
"""
Formula Updater Script for kpf Homebrew Formula

This script handles fetching PyPI package information and updating/generating
Homebrew formulas for the kpf package.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict

FORMULA_CLASS_NAME = "Kpf"
FORMULA_NAME = "kpf"
PYTHON_FORMULA = "python@3.14"
PYTHON_EXECUTABLE = "python3.14"
HOMEPAGE_FALLBACK = "https://github.com/jessegoodier/kpf"
DESCRIPTION = "Kubernetes utility to improve kubectl port-forward reliability and usability"
EXPECTED_COMMANDS = ("kpf", "kpfh")
CAVEATS = """      kpfh is installed alongside kpf.
      Use kpfh to quickly reconnect to previously used port-forwards."""
CURRENT_VERSION_PATTERNS = (
    re.compile(r"kpf==(?P<version>[0-9]+\.[0-9]+\.[0-9]+[^\"'\s]*)"),
    re.compile(r"kpf-(?P<version>[0-9]+\.[0-9]+\.[0-9]+[^\"'\s]*)\.tar\.gz"),
)


def import_requests():
    """Import requests only for network-backed operations."""
    try:
        import requests
    except ImportError:
        print(
            "Error: requests module not found. Please install with: pip install requests",
            file=sys.stderr,
        )
        sys.exit(1)

    return requests


class FormulaUpdater:
    def __init__(self, package_name: str = FORMULA_NAME):
        self.package_name = package_name
        self.pypi_base_url = "https://pypi.org/pypi"

    def fetch_latest_version(self) -> str:
        """Fetch the latest version from PyPI."""
        url = f"{self.pypi_base_url}/{self.package_name}/json"
        requests = import_requests()
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            version = data["info"]["version"]
            print(f"Latest version from PyPI: {version}", file=sys.stderr)
            return version
        except requests.RequestException as e:
            print(f"Error fetching latest version: {e}", file=sys.stderr)
            sys.exit(1)
        except KeyError as e:
            print(f"Error parsing PyPI response: {e}", file=sys.stderr)
            sys.exit(1)

    def fetch_version_info(self, version: str) -> Dict[str, str]:
        """Fetch version-specific information from PyPI."""
        url = f"{self.pypi_base_url}/{self.package_name}/{version}/json"
        requests = import_requests()
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Find source distribution
            sdist_url = None
            sdist_sha256 = None

            for url_info in data["urls"]:
                if url_info["packagetype"] == "sdist":
                    sdist_url = url_info["url"]
                    sdist_sha256 = url_info["digests"]["sha256"]
                    break

            if not sdist_url:
                print(
                    f"No source distribution found for version {version}",
                    file=sys.stderr,
                )
                sys.exit(1)

            homepage = (
                data["info"].get("home_page")
                or data["info"].get("project_urls", {}).get("Homepage")
                or HOMEPAGE_FALLBACK
            )

            return {
                "version": version,
                "url": sdist_url,
                "sha256": sdist_sha256,
                "homepage": homepage,
                "description": DESCRIPTION,
            }

        except requests.RequestException as e:
            print(f"Error fetching version {version}: {e}", file=sys.stderr)
            sys.exit(1)
        except KeyError as e:
            print(f"Error parsing PyPI response: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_formula_content(self, version_info: Dict[str, str]) -> str:
        """Generate the complete Homebrew formula content.

        Keep tap-local behavior, such as caveats and additional command symlinks,
        in this template so automated version bumps cannot overwrite them.
        """
        version = version_info["version"]
        command_symlinks = "\n".join(
            f'    bin.install_symlink libexec/"bin/{command}"'
            for command in EXPECTED_COMMANDS
        )

        return f'''class {FORMULA_CLASS_NAME} < Formula
  include Language::Python::Virtualenv

  desc "{version_info["description"]}"
  homepage "{version_info["homepage"]}"
  url "{version_info["url"]}"
  sha256 "{version_info["sha256"]}"
  license "MIT"

  depends_on "{PYTHON_FORMULA}"

  def caveats
    <<~EOS
{CAVEATS}
    EOS
  end

  def install
    virtualenv_create(libexec, "{PYTHON_EXECUTABLE}")

    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "--ignore-requires-python", "{self.package_name}=={version}"

    # Create binary symlinks
{command_symlinks}

    # Install shell completions
    bash_completion.install "src/kpf/completions/kpf.bash" => "kpf"
    zsh_completion.install "src/kpf/completions/_kpf" => "_kpf"
  end

  test do
    # Test that the kpf command exists and shows help
    assert_match "A better Kubectl Port-Forward", shell_output("#{{bin}}/kpf --help")

    # Test that the kpfh command exists and shows help
    assert_match "Usage:", shell_output("#{{bin}}/kpfh --help")

    # Test version output
    version_output = shell_output("#{{bin}}/kpf --version")
    assert_match "kpf {version}", version_output
  end
end
'''

    def output_results(self, version_info: Dict[str, str], output_format: str) -> None:
        """Output results in the specified format."""
        if output_format == "json":
            print(json.dumps(version_info, indent=2))
        elif output_format == "env":
            # Output in GitHub Actions environment format
            github_output = os.getenv("GITHUB_OUTPUT")
            if github_output:
                with open(github_output, "a") as f:
                    for key, value in version_info.items():
                        f.write(f"{key}={value}\n")

            # Also print to stdout for debugging
            for key, value in version_info.items():
                print(f"{key}={value}")
        else:
            # Human-readable format
            print(f"Version: {version_info['version']}")
            print(f"URL: {version_info['url']}")
            print(f"SHA256: {version_info['sha256']}")
            print(f"Homepage: {version_info['homepage']}")
            print(f"Description: {version_info['description']}")

    def write_formula(self, version_info: Dict[str, str], output_file: str) -> None:
        """Write the formula to a file."""
        formula_content = self.generate_formula_content(version_info)
        self.validate_formula_content(formula_content, version_info["version"])

        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(formula_content)
            print(f"Formula written to {output_file}")
        except IOError as e:
            print(f"Error writing formula file: {e}", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def read_current_version(formula_file: str) -> str:
        """Read the currently pinned version from a formula file."""
        formula_path = Path(formula_file)
        if not formula_path.exists():
            return "0.0.0"

        formula_content = formula_path.read_text()
        for pattern in CURRENT_VERSION_PATTERNS:
            match = pattern.search(formula_content)
            if match:
                return match.group("version")

        return "0.0.0"

    @staticmethod
    def validate_formula_content(
        formula_content: str, expected_version: str | None = None
    ) -> None:
        """Validate generated formula content includes required tap behavior."""
        required_snippets = [
            "def caveats",
            "kpfh is installed alongside kpf.",
            'bin.install_symlink libexec/"bin/kpf"',
            'bin.install_symlink libexec/"bin/kpfh"',
            'shell_output("#{bin}/kpfh --help")',
        ]

        if expected_version:
            required_snippets.append(f'"{FORMULA_NAME}=={expected_version}"')
            required_snippets.append(f'assert_match "kpf {expected_version}"')

        missing_snippets = [
            snippet for snippet in required_snippets if snippet not in formula_content
        ]
        if missing_snippets:
            print("Formula validation failed. Missing required content:", file=sys.stderr)
            for snippet in missing_snippets:
                print(f"  - {snippet}", file=sys.stderr)
            sys.exit(1)

    def validate_formula_file(
        self, formula_file: str, expected_version: str | None = None
    ) -> None:
        """Validate an existing formula file includes required tap behavior."""
        formula_content = Path(formula_file).read_text()
        self.validate_formula_content(formula_content, expected_version)
        print(f"Formula validation passed: {formula_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Update or generate Homebrew formula for kpf package",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch latest version from PyPI
  %(prog)s --fetch-version-from-pypi

  # Use specific version
  %(prog)s --version 0.1.10

  # Generate formula file
  %(prog)s --version 0.1.10 --output-formula Formula/kpf.rb

  # Read the current formula version
  %(prog)s --current-version Formula/kpf.rb

  # Validate the generated tap-specific formula behavior
  %(prog)s --validate-formula Formula/kpf.rb --version 0.1.10

  # Output for GitHub Actions
  %(prog)s --fetch-version-from-pypi --output-format env
        """,
    )

    version_group = parser.add_mutually_exclusive_group(required=False)
    version_group.add_argument("--version", help="Specific version to use")
    version_group.add_argument(
        "--fetch-version-from-pypi",
        action="store_true",
        help="Fetch the latest version from PyPI",
    )

    parser.add_argument(
        "--output-format",
        choices=["json", "env", "human"],
        default="human",
        help="Output format (default: human)",
    )

    parser.add_argument("--output-formula", help="Write formula to specified file")
    parser.add_argument(
        "--current-version", help="Read current version from formula file"
    )
    parser.add_argument(
        "--validate-formula", help="Validate generated formula behavior"
    )

    parser.add_argument(
        "--package-name",
        default=FORMULA_NAME,
        help=f"Package name on PyPI (default: {FORMULA_NAME})",
    )

    args = parser.parse_args()

    if args.current_version:
        print(FormulaUpdater.read_current_version(args.current_version))
        return

    updater = FormulaUpdater(args.package_name)

    if args.validate_formula:
        updater.validate_formula_file(args.validate_formula, args.version)
        return

    if not args.version and not args.fetch_version_from_pypi:
        parser.error(
            "one of --version, --fetch-version-from-pypi, --current-version, "
            "or --validate-formula is required"
        )

    # Get version
    if args.fetch_version_from_pypi:
        version = updater.fetch_latest_version()
    else:
        version = args.version

    # Fetch version information
    version_info = updater.fetch_version_info(version)

    # Output results
    updater.output_results(version_info, args.output_format)

    # Write formula if requested
    if args.output_formula:
        updater.write_formula(version_info, args.output_formula)


if __name__ == "__main__":
    main()
