import pytest,httpx
from app.main import app
from unittest.mock import AsyncMock

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_teams_by_service_status_hhtp_status(client):
    response = client.get("/api/v1/teams/by-service-status")
    assert response.status_code == 200


def test_get_teams_by_service_status_structure(client):
    response = client.get("/api/v1/teams/by-service-status")
    data = response.get_json()

    structure_to_test = ["number_of_teams", "teams"]

    assert isinstance(data, dict)
    assert all(key in data for key in structure_to_test)