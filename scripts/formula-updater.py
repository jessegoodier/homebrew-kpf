#!/usr/bin/env python3
"""
Formula Updater Script for kpf Homebrew Formula

This script handles fetching PyPI package information and updating/generating
Homebrew formulas for the kpf package.
"""

import argparse
import json
import os
import sys
from typing import Dict

try:
    import requests
except ImportError:
    print("Error: requests module not found. Please install with: pip install requests")
    sys.exit(1)


class FormulaUpdater:
    def __init__(self, package_name: str = "kpf"):
        self.package_name = package_name
        self.pypi_base_url = "https://pypi.org/pypi"

    def fetch_latest_version(self) -> str:
        """Fetch the latest version from PyPI."""
        url = f"{self.pypi_base_url}/{self.package_name}/json"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            version = data["info"]["version"]
            print(f"Latest version from PyPI: {version}")
            return version
        except requests.RequestException as e:
            print(f"Error fetching latest version: {e}")
            sys.exit(1)
        except KeyError as e:
            print(f"Error parsing PyPI response: {e}")
            sys.exit(1)

    def fetch_version_info(self, version: str) -> Dict[str, str]:
        """Fetch version-specific information from PyPI."""
        url = f"{self.pypi_base_url}/{self.package_name}/{version}/json"
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
                print(f"No source distribution found for version {version}")
                sys.exit(1)

            homepage = (
                data["info"].get("home_page")
                or data["info"].get("project_urls", {}).get("Homepage")
                or "https://github.com/jessegoodier/kpf"
            )

            return {
                "version": version,
                "url": sdist_url,
                "sha256": sdist_sha256,
                "homepage": homepage,
                "description": "Kubernetes utility to improve kubectl port-forward reliability and usability",
            }

        except requests.RequestException as e:
            print(f"Error fetching version {version}: {e}")
            sys.exit(1)
        except KeyError as e:
            print(f"Error parsing PyPI response: {e}")
            sys.exit(1)

    def generate_formula_content(self, version_info: Dict[str, str]) -> str:
        """Generate the complete Homebrew formula content."""
        formula_template = """class Kpf < Formula
  include Language::Python::Virtualenv

  desc "Kubernetes utility to improve kubectl port-forward reliability and usability"
  homepage "{homepage}"
  url "{url}"
  sha256 "{sha256}"
  license "MIT"

  depends_on "python@3.14"

  def install
    virtualenv_create(libexec, "python3.14")
    
    # Install kpf and its dependencies directly from PyPI using wheels
    # This bypasses all the build system compatibility issues
    system libexec/"bin/python", "-m", "pip", "install", "--ignore-requires-python", "kpf=={version}"
    
    # Create binary symlink
    bin.install_symlink libexec/"bin/kpf"

    # Install shell completions
    bash_completion.install "completions/kpf.bash" => "kpf"
    zsh_completion.install "completions/_kpf" => "_kpf"
  end

  test do
    # Test that the kpf command exists and shows help
    assert_match "A better Kubectl Port-Forward", shell_output("#{{bin}}/kpf --help")
    
    # Test version output
    version_output = shell_output("#{{bin}}/kpf --version")
    assert_match "kpf {version}", version_output
  end
end"""

        return formula_template.format(**version_info)

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

        try:
            # Create directory if needed (only if there's a directory component)
            dir_path = os.path.dirname(output_file)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            with open(output_file, "w") as f:
                f.write(formula_content)
            print(f"Formula written to {output_file}")
        except IOError as e:
            print(f"Error writing formula file: {e}")
            sys.exit(1)


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
  
  # Output for GitHub Actions
  %(prog)s --fetch-version-from-pypi --output-format env
        """,
    )

    version_group = parser.add_mutually_exclusive_group(required=True)
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
        "--package-name", default="kpf", help="Package name on PyPI (default: kpf)"
    )

    args = parser.parse_args()

    updater = FormulaUpdater(args.package_name)

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
