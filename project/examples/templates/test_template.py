"""
Test Template
This template is used to generate test cases for the application.
"""

import pytest
from flask import Flask
from typing import Generator, Any

@pytest.fixture
def app() -> Generator[Flask, Any, None]:
    """Create and configure a test application."""
    from app import app as flask_app
    
    # Configure the app for testing
    flask_app.config.update({
        'TESTING': True,
        'DEBUG': True
    })
    
    yield flask_app

@pytest.fixture
def client(app: Flask) -> Generator[Flask, Any, None]:
    """Create a test client."""
    with app.test_client() as client:
        yield client

def test_health_check(client: Flask) -> None:
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data

def test_metrics(client: Flask) -> None:
    """Test the metrics endpoint."""
    response = client.get('/metrics')
    assert response.status_code == 200
    data = response.get_json()
    assert 'uptime' in data
    assert 'memory_usage' in data
    assert 'cpu_usage' in data

{{additional_tests}} 