"""Tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_extract_without_file(client):
    """Test extract endpoint without file."""
    response = client.post("/api/extract")
    assert response.status_code == 422  # Validation error
