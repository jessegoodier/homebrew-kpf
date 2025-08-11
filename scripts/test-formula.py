#!/usr/bin/env python3
"""
Homebrew Formula Testing Script

This script helps test Homebrew formulas locally by handling common scenarios
including dealing with previously installed versions.
"""

import argparse
import subprocess
import sys
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""

    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


class FormulaTester:
    """Main class for testing Homebrew formulas."""

    def __init__(
        self,
        formula_name: str,
        force_reinstall: bool = False,
        skip_uninstall: bool = False,
        verbose: bool = False,
        dry_run: bool = False,
    ):
        self.formula_name = formula_name
        self.formula_path = Path(f"Formula/{formula_name}.rb")
        self.force_reinstall = force_reinstall
        self.skip_uninstall = skip_uninstall
        self.verbose = verbose
        self.dry_run = dry_run
        self.was_installed = False

    def print_status(self, message: str) -> None:
        """Print an informational message."""
        print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")

    def print_error(self, message: str) -> None:
        """Print an error message."""
        print(f"{Colors.RED}[ERROR]{Colors.NC} {message}", file=sys.stderr)

    def print_warning(self, message: str) -> None:
        """Print a warning message."""
        print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")

    def print_success(self, message: str) -> None:
        """Print a success message."""
        print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")

    def run_command(
        self, command: list, capture_output: bool = False, check: bool = True
    ) -> subprocess.CompletedProcess:
        """Run a shell command with proper error handling."""
        if self.dry_run:
            print(f"  DRY RUN: {' '.join(command)}")
            # Return a mock result for dry run
            return subprocess.CompletedProcess(command, 0, "", "")

        try:
            if capture_output:
                result = subprocess.run(command, capture_output=True, text=True, check=check)
            else:
                result = subprocess.run(command, check=check)
            return result
        except subprocess.CalledProcessError as e:
            if check:
                self.print_error(f"Command failed: {' '.join(command)}")
                sys.exit(1)
            return e

    def check_homebrew(self) -> None:
        """Check if Homebrew is available."""
        try:
            result = self.run_command(["brew", "--version"], capture_output=True)
            version_line = result.stdout.strip().split("\n")[0]
            self.print_status(f"Homebrew found: {version_line}")
        except FileNotFoundError:
            self.print_error("Homebrew is not installed or not in PATH")
            sys.exit(1)

    def check_formula_exists(self) -> None:
        """Check if the formula file exists."""
        if not self.formula_path.exists():
            self.print_error(f"Formula file {self.formula_path} not found")
            sys.exit(1)

        self.print_status(f"Formula file found: {self.formula_path}")

    def check_installation_status(self) -> bool:
        """Check if the formula is currently installed."""
        try:
            result = self.run_command(
                ["brew", "list", self.formula_name], capture_output=True, check=False
            )
            if result.returncode == 0:
                # Get version information
                version_result = self.run_command(
                    ["brew", "list", "--versions", self.formula_name],
                    capture_output=True,
                )
                version_line = version_result.stdout.strip()
                current_version = version_line.split()[-1] if version_line else "unknown"

                self.print_warning(
                    f"Formula {self.formula_name} is already installed (version: {current_version})"
                )

                if self.force_reinstall:
                    self.print_status(
                        f"{Colors.YELLOW}Force reinstall requested - will uninstall current version"
                    )
                else:
                    self.print_status(
                        f"{Colors.YELLOW}Use -f/--force to reinstall existing formula"
                    )

                return True
            else:
                self.print_status(
                    f"{Colors.GREEN}Formula {self.formula_name} is not currently installed"
                )
                return False
        except Exception as e:
            self.print_warning(f"Could not determine installation status: {e}")
            return False

    def uninstall_formula(self) -> None:
        """Uninstall the formula if it's currently installed."""
        try:
            result = self.run_command(
                ["brew", "list", self.formula_name], capture_output=True, check=False
            )
            if result.returncode == 0:
                self.print_status(f"{Colors.YELLOW}Uninstalling existing {self.formula_name}...")

                self.run_command(["brew", "uninstall", "--force", self.formula_name])
                self.print_success(f"Successfully uninstalled {self.formula_name}")
            else:
                self.print_status(f"{Colors.BLUE}No existing installation to remove")
        except Exception as e:
            self.print_warning(f"Error during uninstallation: {e}")

    def install_formula(self) -> None:
        """Install the formula from the local formula file."""
        self.print_status(f"{Colors.BLUE}Installing {self.formula_name} from local formula...")

        command = ["brew", "install"]
        if self.verbose:
            command.append("--verbose")
        command.append(str(self.formula_path))

        self.run_command(command)
        self.print_success(f"Successfully installed {self.formula_name}")

    def test_formula(self) -> None:
        """Run the formula's test suite."""
        self.print_status(f"{Colors.BLUE}Running formula tests...")

        command = ["brew", "test"]
        if self.verbose:
            command.append("--verbose")
        command.append(self.formula_name)

        self.run_command(command)
        self.print_success(f"All tests passed for {self.formula_name}")

    def show_formula_info(self) -> None:
        """Display information about the installed formula."""
        self.print_status(f"{Colors.BLUE}Formula information:")

        self.run_command(["brew", "info", self.formula_name])

    def cleanup(self) -> None:
        """Clean up the test installation."""
        if self.skip_uninstall:
            self.print_status(f"{Colors.YELLOW}Skipping cleanup (--skip-uninstall specified)")
            return

        self.print_status(f"{Colors.BLUE}Cleaning up test installation...")

        try:
            self.run_command(["brew", "uninstall", "--force", self.formula_name])
            self.print_success("Cleanup completed")
        except Exception as e:
            self.print_warning(f"Error during cleanup: {e}")

    def audit_formula(self) -> None:
        """Run formula audit checks."""
        self.print_status(f"{Colors.BLUE}Running formula audit...")

        try:
            result = self.run_command(
                ["brew", "audit", "--strict", str(self.formula_path)], check=False
            )
            if result.returncode == 0:
                self.print_success("Formula audit passed")
            else:
                self.print_warning("Formula audit had issues (this may not prevent installation)")
        except Exception as e:
            self.print_warning(f"Error during audit: {e}")

    def run_tests(self) -> None:
        """Main method to run the complete testing workflow."""
        self.print_status(f"{Colors.BLUE}Starting formula test for: {self.formula_name}")
        print()

        # Check prerequisites
        self.check_homebrew()
        self.check_formula_exists()

        # Check current installation status
        self.was_installed = self.check_installation_status()

        # Uninstall if force reinstall or already installed
        if self.force_reinstall or self.was_installed:
            self.uninstall_formula()

        print()

        # Run audit
        self.audit_formula()
        print()

        # Install formula
        self.install_formula()
        print()

        # Show formula info
        self.show_formula_info()
        print()

        # Test formula
        self.test_formula()
        print()

        # Cleanup
        self.cleanup()

        print()
        self.print_success("Formula testing completed successfully!")

        if self.was_installed:
            self.print_warning("Note: Original installation was restored")


def show_usage() -> None:
    """Display usage information."""
    usage = """
Usage: test-formula.py [OPTIONS] <formula-name>

Test a Homebrew formula locally with comprehensive cleanup and testing.

OPTIONS:
    -f, --force          Force reinstall even if formula is already installed
    -s, --skip-uninstall Skip uninstalling the formula after testing
    -v, --verbose        Enable verbose output
    -d, --dry-run        Show what would be done without executing
    -h, --help           Show this help message

EXAMPLES:
    test-formula.py kpf                    # Test the kpf formula
    test-formula.py -f kpf                # Force reinstall and test
    test-formula.py -s kpf                # Test without uninstalling afterward
    test-formula.py -v -d kpf             # Verbose dry run
"""
    print(usage)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test a Homebrew formula locally with comprehensive cleanup and testing.",
        add_help=False,
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force reinstall even if formula is already installed",
    )

    parser.add_argument(
        "-s",
        "--skip-uninstall",
        action="store_true",
        help="Skip uninstalling the formula after testing",
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing",
    )

    parser.add_argument("-h", "--help", action="store_true", help="Show this help message")

    parser.add_argument("formula_name", nargs="?", help="Name of the formula to test")

    args = parser.parse_args()

    # Handle help
    if args.help or not args.formula_name:
        show_usage()
        if not args.formula_name:
            sys.exit(1)
        sys.exit(0)

    # Create tester and run tests
    try:
        tester = FormulaTester(
            formula_name=args.formula_name,
            force_reinstall=args.force,
            skip_uninstall=args.skip_uninstall,
            verbose=args.verbose,
            dry_run=args.dry_run,
        )
        tester.run_tests()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[ERROR]{Colors.NC} Script interrupted", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR]{Colors.NC} Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
