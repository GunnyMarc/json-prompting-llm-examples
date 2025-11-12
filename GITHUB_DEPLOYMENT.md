# GitHub Deployment Guide

This guide walks you through deploying the JSON Prompting LLM Examples repository to GitHub.

## Prerequisites

Before deploying, ensure you have:

- [x] Git installed on your local machine
- [x] GitHub account created
- [x] GitHub CLI (`gh`) installed (optional but recommended)
- [x] SSH key configured with GitHub (or HTTPS credentials)

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface

1. Go to https://github.com/new
2. Fill in repository details:
   - **Repository name**: `json-prompting-llm`
   - **Description**: "Comprehensive examples and research on JSON prompting techniques for LLMs"
   - **Visibility**: Public (recommended for open source)
   - **Initialize**: Do NOT check any initialization options (README, .gitignore, license)

3. Click "Create repository"

### Option B: Using GitHub CLI

```bash
gh repo create json-prompting-llm \
  --public \
  --description "Comprehensive examples and research on JSON prompting techniques for LLMs" \
  --source=. \
  --remote=origin
```

## Step 2: Connect Local Repository to GitHub

If you created the repo via web interface, connect it:

```bash
# Add remote origin
git remote add origin https://github.com/GunnyMarc/json-prompting-llm.git

# Or with SSH
git remote add origin git@github.com:GunnyMarc/json-prompting-llm.git

# Verify remote
git remote -v
```

## Step 3: Push to GitHub

```bash
# Push main branch
git push -u origin main

# If your default branch is different
git branch -M main  # Rename current branch to main
git push -u origin main
```

## Step 4: Verify Deployment

1. Visit your repository: `https://github.com/GunnyMarc/json-prompting-llm`
2. Check that all files are present
3. Verify README.md is displayed on the main page
4. Confirm GitHub Actions workflow is running (check Actions tab)

## Step 5: Configure Repository Settings

### Enable Issue Templates

Issue templates are automatically detected from `.github/ISSUE_TEMPLATE/`:
- Bug reports
- Feature requests

### Set Up Branch Protection (Recommended)

1. Go to Settings → Branches
2. Add rule for `main` branch:
   - ✓ Require a pull request before merging
   - ✓ Require status checks to pass before merging
   - ✓ Require branches to be up to date before merging
   - ✓ Include administrators

### Configure GitHub Actions

GitHub Actions will automatically run on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

No additional configuration needed!

### Add Repository Topics

Add relevant topics to help others discover your repository:

1. Go to your repository main page
2. Click the gear icon next to "About"
3. Add topics:
   - `json`
   - `llm`
   - `prompting`
   - `openai`
   - `gpt-4`
   - `claude`
   - `anthropic`
   - `assemblyai`
   - `ai`
   - `machine-learning`
   - `python`

## Step 6: Add Secrets for CI/CD

For testing that requires API keys, add repository secrets:

1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add the following secrets (optional, for enhanced testing):
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `ASSEMBLYAI_API_KEY`: Your AssemblyAI API key

**Note**: These are optional. Tests are designed to work without real API keys using mocks.

## Step 7: Create Initial Release

Create your first release to mark the v1.0.0:

```bash
# Using GitHub CLI
gh release create v1.0.0 \
  --title "Version 1.0.0 - Initial Release" \
  --notes "First stable release with comprehensive JSON prompting examples"

# Or via web interface:
# Go to Releases → Draft a new release
# Tag: v1.0.0
# Title: Version 1.0.0 - Initial Release
# Description: Copy from CHANGELOG.md
```

## Step 8: Set Up GitHub Pages (Optional)

To host documentation:

1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main`, folder: `/docs`
4. Click Save

Documentation will be available at: `https://GunnyMarc.github.io/json-prompting-llm/`

## Post-Deployment Tasks

### 1. Add Social Preview Image

1. Go to Settings
2. Scroll to "Social preview"
3. Upload an image (1280x640 pixels recommended)

### 2. Add Repository Description

Ensure your repository has a clear description and website URL:
- Description: "Comprehensive examples and research on JSON prompting techniques for LLMs"
- Website: Documentation URL or project page

### 3. Create Welcome Issues

Create a few "good first issue" items to welcome contributors:

```bash
gh issue create \
  --title "Add example: JSON prompting for code generation" \
  --body "We could use an example showing JSON-structured code generation..." \
  --label "good first issue,enhancement"
```

### 4. Set Up Discussions

Enable GitHub Discussions for community engagement:

1. Go to Settings → Features
2. Check "Discussions"
3. Create categories:
   - 💡 Ideas
   - 🙏 Q&A
   - 📣 Announcements
   - 🗣️ General

### 5. Add Contributors

If you have collaborators:

1. Go to Settings → Collaborators
2. Add team members with appropriate permissions

## Continuous Integration Status

After deployment, your CI/CD pipeline will:

1. ✓ Run tests on Python 3.9, 3.10, 3.11, 3.12
2. ✓ Check code formatting with black
3. ✓ Lint with flake8
4. ✓ Type check with mypy
5. ✓ Run security scans
6. ✓ Generate coverage reports

View status at: `https://github.com/GunnyMarc/json-prompting-llm/actions`

## Troubleshooting

### Push Rejected

If your push is rejected:

```bash
# Pull latest changes first
git pull origin main --rebase

# Then push
git push origin main
```

### Authentication Failed

If authentication fails:

```bash
# For HTTPS, use personal access token
# Generate at: https://github.com/settings/tokens

# For SSH, ensure key is added
ssh-add ~/.ssh/id_rsa
ssh -T git@github.com
```

### Actions Failing

If GitHub Actions fail:

1. Check the Actions tab for error details
2. Common issues:
   - Missing dependencies in requirements.txt
   - Python version compatibility
   - Test failures

Fix locally and push again:

```bash
# Run tests locally first
pytest tests/ -v

# Fix issues, commit, and push
git add .
git commit -m "Fix: Resolve test failures"
git push origin main
```

## Updating After Deployment

To push updates:

```bash
# Make changes
git add .
git commit -m "Description of changes"
git push origin main
```

For major updates, use feature branches:

```bash
# Create feature branch
git checkout -b feature/new-example

# Make changes and commit
git add .
git commit -m "Add new example"

# Push feature branch
git push origin feature/new-example

# Create pull request via GitHub web interface or CLI
gh pr create --title "Add new example" --body "Description"
```

## Maintenance

### Regular Updates

Keep your repository healthy:

1. **Weekly**: Review and respond to issues
2. **Monthly**: Update dependencies
3. **Quarterly**: Review and update documentation
4. **Annually**: Major version updates

### Dependency Updates

```bash
# Update requirements.txt
pip install --upgrade openai anthropic assemblyai

# Test updates
pytest tests/ -v

# Commit if tests pass
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

## Resources

- [GitHub Docs](https://docs.github.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [GitHub CLI](https://cli.github.com/)
- [Semantic Versioning](https://semver.org/)

## Success Checklist

After deployment, verify:

- [x] Repository is accessible
- [x] README displays correctly
- [x] All files and directories present
- [x] GitHub Actions passing
- [x] Issue templates working
- [x] Branch protection enabled (if applicable)
- [x] Repository topics added
- [x] Initial release created
- [x] Documentation accessible

---

**Congratulations!** Your repository is now successfully deployed on GitHub! 🎉

For questions or issues, refer to the [CONTRIBUTING.md](CONTRIBUTING.md) guide.
