import pytest
from pathlib import Path
import tempfile
import shutil
import docker

@pytest.fixture(scope="session")
def temp_dir():
    """Create temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture(scope="session")
def docker_client():
    """Create Docker client for tests."""
    return docker.from_env()

@pytest.fixture(scope="function")
def mock_code_package():
    """Create mock code package for testing."""
    return {
        'code': 'print("Hello, World!")',
        'framework': 'flask',
        'type': 'web_app',
        'dependencies': {
            'requirements': ['flask', 'requests']
        }
    } 