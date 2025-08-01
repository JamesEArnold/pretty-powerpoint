# Pre-commit Hooks Guide

## Overview
This project uses pre-commit hooks to maintain code quality and prevent common issues from entering the codebase.

## Setup
1. Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh` (or `pip install uv`)
2. Install dev dependencies: `uv pip install -r requirements-dev.txt`
3. Install hooks: `pre-commit install`

## Running Manually
- All files: `pre-commit run --all-files`
- Specific hook: `pre-commit run black --all-files`

## Bypassing Hooks
In emergencies only: `git commit --no-verify`

## Configured Hooks

### Python Code Quality
- **Black**: Python code formatter with 100-character line length
- **Flake8**: Python linting with additional plugins for docstrings and bug detection
- **MyPy**: Static type checking for Python code

### Terraform
- **terraform_fmt**: Automatically formats Terraform files
- **terraform_validate**: Validates Terraform configuration
- **terraform_docs**: Generates documentation for Terraform modules

### General File Checks
- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Ensures files end with a newline
- **check-yaml**: Validates YAML file syntax
- **check-json**: Validates JSON file syntax
- **check-added-large-files**: Prevents committing large files (>1MB)
- **check-case-conflict**: Prevents case-sensitive filename conflicts
- **check-merge-conflict**: Detects merge conflict markers
- **detect-private-key**: Prevents committing private keys

### Security
- **detect-secrets**: Scans for secrets and credentials using a baseline file

## Troubleshooting

### Hook Installation Issues
If hooks fail to install, try:
```bash
pre-commit clean
pre-commit install
```

### Python Version Issues
Ensure you're using Python 3.8+ as configured in the hooks.

### Virtual Environment Issues
With UV, you can create and manage virtual environments more efficiently:
```bash
# Create virtual environment with UV
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows

# Install dependencies and run pre-commit
uv pip install -r requirements-dev.txt
pre-commit run --all-files
```

Alternatively, run commands directly with UV without activating the environment:
```bash
uv run pre-commit run --all-files
```

### Secrets Detection False Positives
If detect-secrets flags legitimate strings as secrets:
1. Review the flagged content
2. If it's a false positive, update `.secrets.baseline`:
   ```bash
   detect-secrets scan --baseline .secrets.baseline --update
   ```
