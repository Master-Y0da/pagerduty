import pytest
from app.main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_services_hhtp_status(client):
    response = client.get("/api/v1/incidents/")
    assert response.status_code == 200

def test_get_services_structure(client):
    response = client.get("/api/v1/incidents/")
    data = response.get_json()
    assert isinstance(data, list)
    assert all("service" in item and "count" in item for item in data)


def test_get_services_status_hhtp_status(client):
    response = client.get("/api/v1/incidents/by-service-status")
    assert response.status_code == 200

def test_get_services_status_structure(client):
    response = client.get("/api/v1/incidents/by-service-status")
    data = response.get_json()

    structure_to_test = ["incident", "service", "status", "count"]

    assert isinstance(data, list)
    assert all(all(key in item for key in structure_to_test) for item in data)


def test_get_top_incidents_hhtp_status(client):
    response = client.get("/api/v1/incidents/top-incidents")
    assert response.status_code == 200

def test_get_top_incidents_structure(client):
    response = client.get("/api/v1/incidents/top-incidents")
    data = response.get_json()

    structure_to_test = ["service", "total", "incidents_status"]

    assert all(key in data for key in structure_to_test)