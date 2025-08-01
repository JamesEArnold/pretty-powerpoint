# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the Serverless Presentation Generator project.

## Workflow Overview

### 🔄 ci.yml - Continuous Integration
**Triggers**: Push and PR to `develop` or `main` branches
**Purpose**: Ensures code quality and runs tests

**Jobs**:
- **Lint**: Runs pre-commit hooks including Black, Flake8, MyPy, security scans
- **Test**: Runs unit and integration tests with coverage reporting
- **Validate Terraform**: Validates and formats Terraform configurations
- **Build Docker**: Builds Lambda container images using UV-optimized Dockerfile

### 🔒 security.yml - Security Scanning
**Triggers**: Push/PR to main branches, weekly schedule (Mondays), manual dispatch
**Purpose**: Comprehensive security scanning and vulnerability detection

**Jobs**:
- **Dependency Check**: Scans dependencies with Safety and pip-audit
- **Code Scan**: Static analysis with Bandit and Semgrep
- **Terraform Security**: Infrastructure security with tfsec and Checkov
- **Secrets Detection**: Scans for exposed secrets using detect-secrets

### 🚀 Deployment Workflows

#### cd-dev.yml - Development Deployment
**Triggers**: Push to `develop` branch, manual dispatch
**Environment**: `development`
**Purpose**: Automatic deployment to development environment

#### cd-staging.yml - Staging Deployment
**Triggers**: Release creation, manual dispatch
**Environment**: `staging`
**Purpose**: Deployment to staging with integration and performance tests

#### cd-prod.yml - Production Deployment
**Triggers**: Manual dispatch only (with confirmation)
**Environment**: `production`
**Purpose**: Secure production deployment with manual confirmation

## Technology Integration

### UV Package Manager
All workflows use **UV** instead of pip for:
- ⚡ 10-100x faster dependency resolution and installation
- 🔒 Consistent dependency locking with `uv.lock`
- 🧹 Simplified dependency management

**UV Commands Used**:
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --extra dev

# Export for compatibility
uv export --extra dev --format requirements-txt > requirements-temp.txt
```

### Docker Integration
- Uses existing UV-optimized Dockerfile at `infrastructure/docker/lambda/Dockerfile`
- Builds images with GitHub Actions cache for faster builds
- Pushes to Amazon ECR for deployment

### Terraform Integration
- Validates Terraform configurations in CI
- Deploys infrastructure using environment-specific configurations
- Manages state in S3 backend with environment isolation

## Required Configuration

Navigate to **Settings > Secrets and variables > Actions** and add:

### AWS Deployment Secrets
| Secret | Description | Example |
|--------|-------------|---------|
| `AWS_DEPLOY_ROLE_ARN` | IAM role ARN for deployments | `arn:aws:iam::123456789012:role/GitHubActionsRole` |
| `TF_STATE_BUCKET` | S3 bucket for Terraform state | `my-terraform-state-bucket` |

### Security Scanning (Optional)
| Secret | Description | Usage |
|--------|-------------|-------|
| `SAFETY_API_KEY` | Safety vulnerability API key | Enhanced vulnerability data |

## Setting Up Configuration

### Using GitHub CLI
```bash
# Set deployment secrets
gh secret set AWS_DEPLOY_ROLE_ARN --body "arn:aws:iam::123456789012:role/GitHubActionsRole"
gh secret set TF_STATE_BUCKET --body "my-terraform-state-bucket"
```

### Using GitHub Web Interface
1. Navigate to repository **Settings**
2. Go to **Secrets and variables > Actions**
3. Use **Secrets** tab to add deployment secrets

## Environment Configuration

### Dynamic Environment Names
All deployment workflows use **workflow inputs** for environment names:

- **Development**: Default `'development'`, customizable via manual dispatch
- **Staging**: Default `'staging'`, customizable via manual dispatch
- **Production**: User selects from `['prod', 'production']` during manual dispatch

### Manual Deployment
All environments support manual deployment with custom environment names:

1. Go to **Actions** tab in GitHub
2. Select the deployment workflow
3. Click **Run workflow**
4. Choose or enter the environment name
5. Confirm deployment (production requires additional confirmation)

## Environment Protection Rules

### Development
- No protection rules (automatic deployment)
- Used for rapid iteration and testing

### Staging
- Require reviewers: 1 reviewer
- Used for final testing before production

### Production
- Require reviewers: 2 reviewers
- Manual deployment confirmation required
- Input validation: Must type "deploy-to-production"

## Setting Up AWS OIDC

For secure AWS authentication without long-lived credentials:

1. **Create OIDC Identity Provider** in AWS IAM
2. **Create Deployment Role** with necessary permissions
3. **Configure Trust Policy**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:YOUR_ORG/pretty-powerpoint:*"
        }
      }
    }
  ]
}
```

## Monitoring and Troubleshooting

### Common Issues

**UV Installation Fails**:
```bash
# Add PATH explicitly
echo "$HOME/.local/bin" >> $GITHUB_PATH
```

**Terraform Backend Errors**:
- Ensure S3 bucket exists and is accessible
- Check IAM permissions for S3 and DynamoDB (if using locking)

**Pre-commit Hook Failures**:
- Check local pre-commit configuration matches CI
- Ensure all required tools are in `pyproject.toml` dev dependencies

**Docker Build Failures**:
- Verify `uv.lock` file is committed
- Check Dockerfile path in build context

### Workflow Status

Monitor workflow runs in the **Actions** tab:
- ✅ Green: All checks passed
- ❌ Red: Failures need attention
- 🟡 Yellow: In progress or cancelled

### Logs and Artifacts

Access detailed logs and artifacts:
- Click on any workflow run for detailed logs
- Download artifacts like test coverage reports
- Check job summaries for quick status overview

### IDE Validation Warnings

**Issue**: VS Code may show warnings like "Context access might be invalid: DEV_ENVIRONMENT" even when variables exist.

**Cause**: IDE extension cache or sync delays with GitHub's API.

**Resolution**:
1. **Restart VS Code** and reload workspace
2. **Wait 5-10 minutes** for GitHub systems to sync
3. **Verify variables exist** in GitHub web interface
4. **Update GitHub Actions extension** if available

**Note**: These warnings are cosmetic - workflows will execute correctly if variables exist in GitHub settings.

## Local Testing

Test workflows locally before pushing:

```bash
# Install act (GitHub Actions local runner)
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflows locally
act push                    # Test CI workflow
act workflow_dispatch      # Test manual workflows
```

## Future Enhancements

- [ ] Add deployment notifications (Slack, email)
- [ ] Implement blue-green deployments
- [ ] Add performance benchmarking
- [ ] Integrate with monitoring tools (CloudWatch, DataDog)
- [ ] Add automatic rollback on failure
- [ ] Implement canary deployments for production

---

**📝 Note**: This documentation should be updated as workflows evolve and new requirements emerge.
