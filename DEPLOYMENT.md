# Homebrew Tap Deployment Guide

This document provides a complete checklist for deploying the homebrew-kpf tap.

## 📋 Deployment Checklist

### 1. Create GitHub Repository

- [ ] Create new GitHub repository: `jessegoodier/homebrew-kpf`
- [ ] Set repository to public
- [ ] Add description: "Homebrew tap for kpf - A better way to port-forward with kubectl"
- [ ] Add topics: `homebrew`, `kubectl`, `kubernetes`, `port-forward`, `cli-tool`

### 2. Upload Repository Content

- [ ] Copy all files from `homebrew-kpf/` directory to the new repository
- [ ] Push initial commit using `init-repo.sh` or manually

### 3. Configure GitHub Secrets

#### In main repository (`jessegoodier/kpf`)

- [ ] Add secret `HOMEBREW_TAP_TOKEN`
  - Go to Settings > Secrets and variables > Actions
  - Create new repository secret
  - Value: Personal Access Token with `repo` scope

#### Generate Personal Access Token

- [ ] Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
- [ ] Click "Generate new token (classic)"
- [ ] Set expiration (recommend 1 year)
- [ ] Select scopes: `repo` (full control of private repositories)
- [ ] Copy the generated token

### 4. Test Workflows

#### Test Manual Update Workflow

- [ ] Go to homebrew-kpf repository
- [ ] Navigate to Actions > Manual Formula Update
- [ ] Click "Run workflow"
- [ ] Enter version: `0.1.10`
- [ ] Verify workflow completes successfully

#### Test Automatic Integration

- [ ] Create a test release in the main kpf repository
- [ ] Verify the `update-homebrew.yml` workflow triggers
- [ ] Check that homebrew-kpf repository receives update

### 5. Local Testing

- [ ] Add the tap locally:

  ```bash
  brew tap jessegoodier/kpf
  ```

- [ ] Install the formula:

  ```bash
  brew install kpf
  ```

- [ ] Test the installation:

  ```bash
  kpf --help
  kpf --version
  ```

- [ ] Uninstall and remove tap (cleanup):

  ```bash
  brew uninstall kpf
  brew untap jessegoodier/kpf
  ```

### 6. Update Documentation

- [ ] Verify main repository README includes Homebrew installation instructions
- [ ] Update any other documentation that mentions installation methods
- [ ] Consider updating the project's setup instructions

### 7. Announcement and Distribution

- [ ] Update GitHub repository description and topics
- [ ] Consider creating a GitHub release announcement
- [ ] Update any external documentation or tutorials
- [ ] Notify users of the new installation method

## 🔧 Maintenance Tasks

### Regular Maintenance

- [ ] Monitor GitHub Actions for failed workflows
- [ ] Check for new kpf releases and verify automatic updates
- [ ] Update dependencies in formula if needed
- [ ] Review and update documentation

### When kpf Updates

1. **Automatic Process** (preferred):
   - New release in main repository triggers update
   - Homebrew formula updates automatically
   - No manual intervention needed

2. **Manual Process** (if needed):
   - Run "Manual Formula Update" workflow
   - Specify version to update to
   - Verify update completes successfully

### Troubleshooting

- Check GitHub Actions logs for errors
- Verify PyPI package availability
- Test formula syntax: `ruby -c Formula/kpf.rb`
- Validate with: `brew formula-check Formula/kpf.rb`

## 📊 Success Metrics

After deployment, you should see:

- [ ] Formula installs successfully via Homebrew
- [ ] Automatic updates work when new versions are released
- [ ] Tests pass in GitHub Actions
- [ ] Users can install and use kpf via `brew install jessegoodier/kpf/kpf`

## 🆘 Rollback Plan

If issues occur:

1. Revert to previous formula version in git history
2. Disable automatic updates by commenting out workflow triggers
3. Fix issues manually and re-enable automation
4. Test thoroughly before announcing fixes

## 📞 Support

- Technical issues: Review SETUP.md
- GitHub Actions issues: Check workflow logs
- Formula issues: Validate syntax and dependencies
- User reports: Direct to appropriate issue tracker
