# Serverless Presentation Generator

## Overview
[Brief project description]

## Architecture
[High-level architecture diagram placeholder]

## Prerequisites
- Python 3.8+
- UV (Python package manager)
- Terraform 1.5+
- Docker & Docker Compose
- AWS CLI configured
- LocalStack (for local development)

## Quick Start

### 1. Install UV
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### 2. Set up development environment
```bash
# Clone the repository
git clone <repository-url>
cd pretty-powerpoint

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows

# Install development dependencies
uv pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### 3. Alternative: Use UV directly (no activation needed)
```bash
# Install dependencies (including dev dependencies)
uv sync --extra dev

# Run commands with UV (no venv activation required)
uv run pytest
uv run pre-commit run --all-files
uv run black .
uv run mypy src/
```

## Project Structure
[Directory structure placeholder]

## Development
[Local development guide placeholder]

## Testing
[Testing guide placeholder]

## Deployment
[Deployment guide placeholder]

## Contributing
[Contributing guidelines placeholder]

## License
MIT License
