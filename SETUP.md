# Homebrew Tap Setup Guide

This document explains how to set up and maintain the homebrew-kpf tap.

## Initial Setup

### 1. Create the Repository

1. Create a new GitHub repository named `homebrew-kpf`
2. Clone this repository to your local machine
3. Copy the files from this directory structure

### 2. Configure GitHub Secrets

For the automation to work, you need to set up the following secrets in both repositories:

#### In the main kpf repository (`jessegoodier/kpf`):
- `HOMEBREW_TAP_TOKEN`: A GitHub Personal Access Token with `repo` scope to trigger workflows in the homebrew-kpf repository

#### In the homebrew-kpf repository (`jessegoodier/homebrew-kpf`):
- `GITHUB_TOKEN`: Usually available by default, but ensure it has necessary permissions

### 3. Set up Personal Access Token

1. Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Generate new token with `repo` scope
3. Add the token as `HOMEBREW_TAP_TOKEN` secret in the main kpf repository

## How the Automation Works

### Automatic Updates

1. **Release Trigger**: When a new release is published in the main kpf repository, it triggers the `update-homebrew.yml` workflow
2. **Repository Dispatch**: The workflow sends a repository dispatch event to the homebrew-kpf repository
3. **Formula Update**: The homebrew-kpf repository's `update-formula.yml` workflow:
   - Fetches the new version information from PyPI
   - Updates the formula with new URL and SHA256
   - Regenerates dependency resources
   - Tests the formula
   - Commits and pushes the changes

### Manual Updates

You can also trigger updates manually:

1. Go to the homebrew-kpf repository
2. Navigate to Actions > Manual Formula Update
3. Click "Run workflow"
4. Enter the version you want to update to

## Testing the Formula

### Local Testing

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add the tap
brew tap jessegoodier/kpf

# Install the formula
brew install kpf

# Test the installation
kpf --help
kpf --version
```

### Formula Validation

```bash
# Validate the formula syntax
brew formula-check Formula/kpf.rb

# Audit the formula
brew audit --strict Formula/kpf.rb

# Test the formula
brew test Formula/kpf.rb
```

## Maintenance

### Updating Dependencies

If kpf adds new dependencies or changes existing ones:

1. The automatic workflow should handle this via `homebrew-pypi-poet`
2. If manual intervention is needed, you can:
   - Run the manual update workflow
   - Or update the formula locally and commit

### Version Management

- The formula automatically tracks PyPI releases
- Version updates happen automatically when new releases are published
- The SHA256 checksums are automatically verified and updated

### Troubleshooting

#### Common Issues

1. **Formula fails to build**: Check that all dependencies are correctly specified
2. **SHA256 mismatch**: Usually means PyPI has updated the package - re-run the update workflow
3. **Python version conflicts**: Ensure the formula specifies the correct Python version dependency

#### Manual Formula Regeneration

If you need to completely regenerate the formula:

```bash
# Install homebrew-pypi-poet
pip install homebrew-pypi-poet

# Create virtual environment with the package
python -m venv temp_env
source temp_env/bin/activate
pip install kpf==<version>

# Generate new formula
poet -f kpf > new_formula.rb

# Manually merge the relevant parts into Formula/kpf.rb
```

## Best Practices

1. **Test locally** before pushing updates
2. **Use semantic versioning** to track formula changes
3. **Keep dependencies minimal** - only include what's necessary
4. **Monitor PyPI releases** for upstream changes
5. **Test on multiple macOS versions** when possible

## Support

- For issues with the kpf tool: [Main repository issues](https://github.com/jessegoodier/kpf/issues)
- For Homebrew formula issues: [Tap repository issues](https://github.com/jessegoodier/homebrew-kpf/issues)