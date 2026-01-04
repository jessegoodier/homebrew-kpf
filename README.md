# homebrew-kpf

Homebrew tap for [kpf](https://github.com/jessegoodier/kpf) - A better way to port-forward with kubectl.

## Installation

```bash
brew tap jessegoodier/kpf
brew install kpf
```

Or install directly:

```bash
brew install jessegoodier/kpf/kpf
```

## Requirements

- kubectl configured with cluster access
- Python 3.11+ (automatically handled by Homebrew)

## Development & Testing

### Testing the Formula Locally

This repository includes a comprehensive test script to validate the formula before deployment:

```bash
# Basic test (will uninstall after testing)
./scripts/test-formula.py kpf

# Test with verbose output
./scripts/test-formula.py -v kpf

# Keep installation after testing (useful for manual verification)
./scripts/test-formula.py -s kpf

# Force reinstall if already installed
./scripts/test-formula.py -f kpf

# Dry run (see what would happen without executing)
./scripts/test-formula.py -d kpf
```

The test script performs the following steps:
1. **Audit** - Runs `brew audit` to check formula syntax and style
2. **Install** - Creates a temporary tap and installs from the local formula
3. **Verify Completions** - Checks that bash and zsh completions are installed correctly
4. **Info** - Displays formula information
5. **Test** - Runs the formula's built-in test suite
6. **Cleanup** - Removes the test installation and temporary tap (unless `-s` is used)

### Manual Testing

You can also test manually:

```bash
# Syntax check
brew ruby -e "$(cat Formula/kpf.rb)"

# Create a test tap and install
brew tap-new test/kpf
cp Formula/kpf.rb $(brew --repo test/kpf)/Formula/
brew install --build-from-source test/kpf/kpf

# Run tests
brew test kpf

# Check completions
ls -la $(brew --prefix)/etc/bash_completion.d/kpf
ls -la $(brew --prefix)/share/zsh/site-functions/_kpf

# Cleanup
brew uninstall kpf
brew untap test/kpf
```

### Important Notes

- The formula installs kpf from PyPI, not from the tap directory
- Shell completions are extracted from the PyPI tarball (if included in the sdist)
- The test script simulates a real-world installation by NOT copying completions to the tap
- Completions must be included in the `pyproject.toml` sdist configuration for Homebrew to install them

## Issues

For issues with the kpf tool itself, please visit the [main repository](https://github.com/jessegoodier/kpf/issues).

For issues with this Homebrew formula, please [open an issue here](https://github.com/jessegoodier/homebrew-kpf/issues).
