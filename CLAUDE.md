# CLAUDE.md - Project Context & Guidelines

This file provides essential context for AI agents working on the **Serverless Presentation Generator** project.

## Project Overview

**Name**: Serverless Presentation Generator
**Purpose**: Generate PowerPoint presentations using AI and serverless architecture
**Architecture**: Clean Architecture with AWS Lambda deployment
**Status**: Early development phase - project structure and tooling established

## Technology Stack

### Core Technologies
- **Python**: 3.8+ (currently using 3.8.5 locally)
- **Package Manager**: UV (migrated from pip for 10-100x faster builds)
- **Configuration**: Pydantic with environment-based settings
- **Infrastructure**: AWS Lambda, Terraform, Docker
- **Local Development**: LocalStack for AWS simulation

### Development Tools
- **Code Formatting**: Black (100-character line length)
- **Linting**: Flake8 with docstring and bugbear plugins
- **Type Checking**: MyPy with strict type annotations
- **Testing**: Pytest with coverage reporting
- **Security**: detect-secrets for credential scanning
- **Pre-commit**: Comprehensive quality gate automation

## Architecture Principles

This project follows **Clean Architecture** with strict layer separation:

```
┌─────── Presentation Layer ───────┐
│  src/presentation/api/           │ ← Controllers, serializers
├─────── Application Layer ────────┤
│  src/application/handlers/       │ ← Lambda handlers, services, DTOs
│  src/application/services/       │
│  src/application/dto/            │
├─────── Infrastructure Layer ─────┤
│  src/infrastructure/aws/         │ ← AWS services, external APIs
│  src/infrastructure/external_services/
│  src/infrastructure/persistence/ │
└─────── Core Layer ───────────────┘
   src/core/entities/              ← Business entities (pure domain logic)
   src/core/use_cases/             ← Business rules and orchestration
   src/core/interfaces/            ← Abstract contracts
```

### Key Principles
- **Dependency Inversion**: Dependencies point inward toward core business logic
- **Repository Pattern**: Data access abstracted through interfaces
- **Single Responsibility**: Each layer has clear boundaries and purposes
- **No Framework Dependencies**: Core layer is framework-agnostic

## Development Environment Setup

### Quick Start Commands
```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup project (from project root)
uv sync --extra dev                    # Install all dependencies
uv run pre-commit install             # Setup quality gates
uv run pre-commit run --all-files     # Verify setup
```

### Alternative Setup (Traditional)
```bash
uv venv                               # Create virtual environment
source .venv/bin/activate            # Activate (Linux/macOS)
uv pip install -r pyproject.toml     # Install dependencies
pre-commit install                   # Setup hooks
```

## Project Structure

```
├── src/                             # Application source code
│   ├── core/                        # Business logic (framework-independent)
│   │   ├── entities/               # Domain models
│   │   ├── use_cases/              # Business rules
│   │   └── interfaces/             # Abstract contracts
│   ├── application/                # Application coordination layer
│   │   ├── handlers/               # Lambda/API entry points
│   │   ├── services/               # Application services
│   │   └── dto/                    # Data transfer objects
│   ├── infrastructure/             # External dependencies
│   │   ├── aws/                    # AWS service integrations
│   │   ├── external_services/      # Third-party APIs
│   │   └── persistence/            # Repository implementations
│   └── presentation/               # User interface layer
│       └── api/                    # REST API controllers
├── tests/                          # Test hierarchy
│   ├── unit/                       # Isolated component tests
│   ├── integration/                # Multi-component tests
│   └── e2e/                        # End-to-end workflow tests
├── infrastructure/                 # Infrastructure as Code
│   ├── terraform/                  # AWS resource definitions
│   │   ├── modules/               # Reusable Terraform modules
│   │   └── environments/          # Environment-specific configs
│   └── docker/                     # Container configurations
│       └── lambda/                 # Lambda deployment container
├── docs/                          # Documentation
│   ├── architecture/              # System design docs
│   ├── api/                       # API documentation & OpenAPI spec
│   ├── development/               # Developer guides
│   └── operations/                # Deployment & monitoring
├── config/                        # Configuration management
└── .github/                       # GitHub workflows & templates
```

## Code Quality Standards

### Mandatory Quality Gates
All code must pass these checks before commit:

1. **Black**: Code formatting (100-char lines, Python 3.8 target)
2. **Flake8**: Linting with docstring requirements
3. **MyPy**: Static type checking with strict settings
4. **Security**: detect-secrets scanning
5. **General**: Trailing whitespace, file endings, YAML/JSON validation

### Pre-commit Integration
- **Automatic**: Runs on every `git commit`
- **Manual**: `uv run pre-commit run --all-files`
- **Bypass**: `git commit --no-verify` (emergencies only)

### Docstring Requirements
```python
"""Module summary ending with period.

Detailed description after blank line.
Follows PEP 257 conventions.
"""
```

## Common Commands

### UV Workflows
```bash
# Development
uv sync --extra dev                   # Install dev dependencies
uv run pytest                        # Run tests
uv run black .                        # Format code
uv run mypy src/                      # Type check
uv run pre-commit run --all-files     # Run all quality checks

# Production
uv sync --frozen --no-dev             # Production install (Docker)
```

### Testing
```bash
uv run pytest tests/unit/            # Unit tests only
uv run pytest tests/integration/     # Integration tests
uv run pytest --cov=src              # With coverage
```

### Docker Development
```bash
# LocalStack development environment
cd infrastructure/docker/
docker-compose up -d localstack       # Start local AWS

# Build Lambda container (UV-powered)
docker build -f infrastructure/docker/lambda/Dockerfile .
```

## Git Workflow

### Branch Strategy
- **`master`**: Protected main branch
- **`develop`**: Integration branch
- **`feature/*`**: Feature development branches

### Branch Protection Rules (master)
- Require pull request reviews (minimum 1)
- Dismiss stale PR approvals
- Require status checks to pass
- Include administrators in restrictions

### Commit Standards
- Use conventional commits: `feat:`, `fix:`, `refactor:`, etc.
- All commits trigger pre-commit hooks
- Quality gates must pass before merge

## Key Architecture Decisions

### 1. UV Migration (Completed)
**Decision**: Migrated from pip to UV for dependency management
**Rationale**: 10-100x faster builds, better dependency resolution
**Impact**: Faster local development and Docker builds

### 2. Clean Architecture (Implemented)
**Decision**: Strict layer separation with dependency inversion
**Rationale**: Maintainability, testability, framework independence
**Impact**: More structured but potentially more complex codebase

### 3. Comprehensive Quality Gates (Active)
**Decision**: Mandatory pre-commit hooks with multiple tools
**Rationale**: Code quality, security, consistency
**Impact**: Slower commit process but higher code quality

### 4. Docker + UV Integration (Implemented)
**Decision**: Use UV in Dockerfile instead of pip + requirements.txt
**Rationale**: Consistency with local development, faster builds
**Impact**: Faster Docker builds, eliminated requirements.txt

## Configuration Management

### Environment-Based Settings
```python
# config/settings.py - Pydantic-based configuration
class Settings(BaseSettings):
    environment: Literal["local", "dev", "staging", "prod"] = "local"
    aws_region: str = "us-east-1"
    openai_api_key: str = ""
    # ... other settings
```

### Usage
```python
from config import settings
print(settings.environment)  # Reads from .env or environment variables
```

## Infrastructure

### Local Development
- **LocalStack**: Simulates AWS services locally
- **Docker Compose**: Orchestrates local environment
- **Terraform**: Infrastructure as Code (disabled in pre-commit until installed)

### AWS Deployment
- **Lambda**: Serverless compute with UV-optimized containers
- **API Gateway**: HTTP endpoints
- **S3**: File storage
- **DynamoDB**: NoSQL database

## Troubleshooting

### Common Issues

**Pre-commit hooks failing:**
```bash
pre-commit clean                      # Clear cached environments
pre-commit install                    # Reinstall hooks
```

**UV command not found:**
```bash
source ~/.local/bin/env               # Add UV to PATH
# or restart shell after UV installation
```

**Docker build failures:**
```bash
# Ensure pyproject.toml and uv.lock are in build context
# Dockerfile expects these files at project root
```

**Type checking errors:**
```bash
uv run mypy src/ --show-error-codes   # See specific error codes
# All functions must have type annotations (disallow_untyped_defs = true)
```

### Quality Gate Bypasses
**NEVER disable quality gates permanently**. If needed temporarily:
```bash
git commit --no-verify                # Bypass pre-commit (emergency only)
```

## Development Guidelines

### Before Starting Work
1. Pull latest changes: `git pull origin develop`
2. Create feature branch: `git checkout -b feature/your-feature`
3. Install dependencies: `uv sync --extra dev`
4. Verify setup: `uv run pre-commit run --all-files`

### During Development
1. Follow clean architecture layer boundaries
2. Add type annotations to all functions
3. Write docstrings for all modules and classes
4. Add tests for new functionality
5. Run quality checks frequently: `uv run pre-commit run --all-files`

### Before Committing
1. Ensure all tests pass: `uv run pytest`
2. Verify code formatting: `uv run black --check .`
3. Check types: `uv run mypy src/`
4. Test hooks: `uv run pre-commit run --all-files`

### Commit Authorship Guidelines
- **Never reference AI assistance in commit messages or authorship**
- Focus commit messages on the changes made, not who made them
- Use conventional commit format: `type: description`
- Commits should appear as standard development work

### When Creating PRs
1. Target `develop` branch (not `master`)
2. Include clear description of changes
3. Ensure all CI checks pass
4. Request review from team members

## Future Considerations

### Planned Enhancements
- GitHub Actions CI/CD pipelines
- Terraform infrastructure deployment
- API documentation generation
- Performance monitoring integration

### Technology Decisions Pending
- Web framework choice (FastAPI likely)
- Database layer implementation
- Authentication/authorization strategy
- External API integrations (OpenAI, etc.)

---

**Last Updated**: Project setup phase completion
**Next Phase**: Core business logic implementation

This document should be updated as the project evolves and new architectural decisions are made.
