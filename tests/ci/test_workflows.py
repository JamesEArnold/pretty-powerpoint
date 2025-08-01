"""Tests for CI/CD workflows."""
import yaml  # type: ignore
import pytest
from pathlib import Path

WORKFLOW_DIR = Path(".github/workflows")


def test_workflow_directory_exists() -> None:
    """Ensure workflow directory exists."""
    assert WORKFLOW_DIR.exists(), "Workflow directory not found"
    assert WORKFLOW_DIR.is_dir(), "Workflow path is not a directory"


def test_all_workflows_valid_yaml() -> None:
    """Ensure all workflow files are valid YAML."""
    workflow_files = list(WORKFLOW_DIR.glob("*.yml"))
    assert len(workflow_files) > 0, "No workflow files found"

    for workflow_file in workflow_files:
        with open(workflow_file, "r") as f:
            try:
                content = yaml.safe_load(f)
                assert content is not None, f"Empty YAML content in {workflow_file}"
                assert isinstance(content, dict), f"Invalid YAML structure in {workflow_file}"
            except yaml.YAMLError as e:
                pytest.fail(f"Invalid YAML in {workflow_file}: {e}")


def test_required_workflows_exist() -> None:
    """Ensure all required workflows exist."""
    required_workflows = ["ci.yml", "security.yml", "cd-dev.yml", "cd-staging.yml", "cd-prod.yml"]

    for workflow in required_workflows:
        workflow_path = WORKFLOW_DIR / workflow
        assert workflow_path.exists(), f"Required workflow {workflow} not found"


def test_ci_workflow_structure() -> None:
    """Test CI workflow has required structure."""
    ci_path = WORKFLOW_DIR / "ci.yml"
    with open(ci_path, "r") as f:
        ci_config = yaml.safe_load(f)

    # Test triggers (YAML parser converts 'on' to True)
    triggers = ci_config.get("on") or ci_config.get(True)
    assert triggers is not None, "CI workflow missing 'on' triggers"
    assert "push" in triggers, "CI workflow missing push trigger"
    assert "pull_request" in triggers, "CI workflow missing PR trigger"

    # Test required jobs
    required_jobs = ["lint", "test", "validate-terraform", "build-docker"]
    assert "jobs" in ci_config, "CI workflow missing jobs"

    for job in required_jobs:
        assert job in ci_config["jobs"], f"CI workflow missing required job: {job}"


def test_security_workflow_structure() -> None:
    """Test security workflow has required structure."""
    security_path = WORKFLOW_DIR / "security.yml"
    with open(security_path, "r") as f:
        security_config = yaml.safe_load(f)

    # Test triggers include schedule (YAML parser converts 'on' to True)
    triggers = security_config.get("on") or security_config.get(True)
    assert triggers is not None, "Security workflow missing triggers"
    assert "schedule" in triggers, "Security workflow missing schedule trigger"

    # Test required security jobs
    required_jobs = ["dependency-check", "code-scan", "terraform-security", "secrets-scan"]
    assert "jobs" in security_config, "Security workflow missing jobs"

    for job in required_jobs:
        assert job in security_config["jobs"], f"Security workflow missing job: {job}"


def test_deployment_workflows_structure() -> None:
    """Test deployment workflows have correct structure."""
    deployment_workflows = ["cd-dev.yml", "cd-staging.yml", "cd-prod.yml"]

    for workflow_name in deployment_workflows:
        workflow_path = WORKFLOW_DIR / workflow_name
        with open(workflow_path, "r") as f:
            config = yaml.safe_load(f)

        # Test environment variables
        assert "env" in config, f"{workflow_name} missing environment variables"
        assert "AWS_REGION" in config["env"], f"{workflow_name} missing AWS_REGION"
        assert "ENVIRONMENT" in config["env"], f"{workflow_name} missing ENVIRONMENT"

        # Test deploy job exists
        assert "jobs" in config, f"{workflow_name} missing jobs"
        assert "deploy" in config["jobs"], f"{workflow_name} missing deploy job"


def test_production_workflow_safety() -> None:
    """Test production workflow has manual confirmation."""
    prod_path = WORKFLOW_DIR / "cd-prod.yml"
    with open(prod_path, "r") as f:
        prod_config = yaml.safe_load(f)

    # Test manual dispatch only (YAML parser converts 'on' to True)
    triggers = prod_config.get("on") or prod_config.get(True)
    assert triggers is not None, "Production workflow missing triggers"
    assert "workflow_dispatch" in triggers, "Production workflow missing manual dispatch"

    # Test confirmation input
    dispatch_config = triggers["workflow_dispatch"]
    assert "inputs" in dispatch_config, "Production workflow missing inputs"
    assert (
        "confirm_deployment" in dispatch_config["inputs"]
    ), "Production workflow missing confirmation"
    assert (
        "environment" in dispatch_config["inputs"]
    ), "Production workflow missing environment input"

    # Test validation job
    assert "validate-input" in prod_config["jobs"], "Production workflow missing input validation"


def test_workflows_use_uv() -> None:
    """Test that workflows use UV instead of pip."""
    workflow_files = ["ci.yml", "security.yml", "cd-dev.yml", "cd-staging.yml", "cd-prod.yml"]

    for workflow_name in workflow_files:
        workflow_path = WORKFLOW_DIR / workflow_name
        with open(workflow_path, "r") as f:
            content = f.read()

        # Check for UV installation and usage
        assert "Install UV" in content, f"{workflow_name} missing UV installation"
        assert "uv sync" in content, f"{workflow_name} not using UV sync"
        assert (
            "curl -LsSf https://astral.sh/uv/install.sh" in content
        ), f"{workflow_name} using wrong UV install method"


def test_workflows_have_python_version() -> None:
    """Test that workflows specify Python version."""
    workflow_files = ["ci.yml", "security.yml", "cd-dev.yml", "cd-staging.yml", "cd-prod.yml"]

    for workflow_name in workflow_files:
        workflow_path = WORKFLOW_DIR / workflow_name
        with open(workflow_path, "r") as f:
            content = f.read()

        # Check Python version is specified
        assert "python-version:" in content, f"{workflow_name} missing Python version specification"
        # Ensure it's using Python 3.8+ (compatible with project requirements)
        assert "'3.8'" in content, f"{workflow_name} not using correct Python version"


def test_terraform_workflows_have_version() -> None:
    """Test that workflows using Terraform specify version."""
    terraform_workflows = ["ci.yml", "cd-dev.yml", "cd-staging.yml", "cd-prod.yml"]

    for workflow_name in terraform_workflows:
        workflow_path = WORKFLOW_DIR / workflow_name
        with open(workflow_path, "r") as f:
            content = f.read()

        if "terraform" in content.lower():
            assert (
                "terraform_version:" in content or "terraform-version:" in content
            ), f"{workflow_name} using Terraform but missing version specification"


def test_docker_workflows_use_correct_dockerfile() -> None:
    """Test that Docker builds use the correct Dockerfile path."""
    docker_workflows = ["ci.yml", "cd-dev.yml", "cd-staging.yml", "cd-prod.yml"]

    for workflow_name in docker_workflows:
        workflow_path = WORKFLOW_DIR / workflow_name
        with open(workflow_path, "r") as f:
            content = f.read()

        if "docker build" in content or "docker/build-push-action" in content:
            assert (
                "infrastructure/docker/lambda/Dockerfile" in content
            ), f"{workflow_name} not using correct Dockerfile path"


def test_cache_configurations() -> None:
    """Test that workflows properly configure caching."""
    cached_workflows = ["ci.yml", "security.yml"]

    for workflow_name in cached_workflows:
        workflow_path = WORKFLOW_DIR / workflow_name
        with open(workflow_path, "r") as f:
            content = f.read()

        # Check for UV cache configuration
        if "uv sync" in content:
            assert "~/.cache/uv" in content, f"{workflow_name} missing UV cache configuration"
            assert "uv.lock" in content, f"{workflow_name} cache not keyed on uv.lock"


def test_environment_configurations() -> None:
    """Test deployment workflows have proper environment configurations."""
    expected_patterns = {
        "cd-dev.yml": ["inputs.environment", "development"],
        "cd-staging.yml": ["inputs.environment", "staging"],
        "cd-prod.yml": ["inputs.environment"],
    }

    for workflow_name, expected_patterns_list in expected_patterns.items():
        workflow_path = WORKFLOW_DIR / workflow_name
        with open(workflow_path, "r") as f:
            config = yaml.safe_load(f)

        # Check environment is set in deploy job
        deploy_job = config["jobs"]["deploy"]
        assert "environment" in deploy_job, f"{workflow_name} missing environment configuration"

        # Environment should be an object with 'name' field containing expression
        env_config = deploy_job["environment"]
        assert isinstance(env_config, dict), f"{workflow_name} environment should be an object"
        assert "name" in env_config, f"{workflow_name} environment object missing 'name' field"

        env_expression = env_config["name"]

        # Check that the environment uses inputs.environment
        assert (
            "inputs.environment" in env_expression
        ), f"{workflow_name} environment should use inputs.environment, got: {env_expression}"

        # Check for appropriate fallback values (except prod which has no fallback)
        if workflow_name != "cd-prod.yml":
            fallback_value = expected_patterns_list[1]  # second item is the fallback
            assert (
                fallback_value in env_expression
            ), f"{workflow_name} should have '{fallback_value}' fallback, got: {env_expression}"


def test_deployment_workflows_have_inputs() -> None:
    """Test that all deployment workflows have environment inputs defined."""
    deployment_workflows = ["cd-dev.yml", "cd-staging.yml", "cd-prod.yml"]

    for workflow_name in deployment_workflows:
        workflow_path = WORKFLOW_DIR / workflow_name
        with open(workflow_path, "r") as f:
            config = yaml.safe_load(f)

        # Get triggers (handling YAML parser converting 'on' to True)
        triggers = config.get("on") or config.get(True)
        assert triggers is not None, f"{workflow_name} missing triggers"
        assert "workflow_dispatch" in triggers, f"{workflow_name} missing workflow_dispatch trigger"

        # Check workflow_dispatch has inputs
        dispatch_config = triggers["workflow_dispatch"]
        assert "inputs" in dispatch_config, f"{workflow_name} missing workflow inputs"
        assert (
            "environment" in dispatch_config["inputs"]
        ), f"{workflow_name} missing environment input"

        # Verify environment input configuration
        env_input = dispatch_config["inputs"]["environment"]
        assert "description" in env_input, f"{workflow_name} environment input missing description"
        assert "required" in env_input, f"{workflow_name} environment input missing required field"
