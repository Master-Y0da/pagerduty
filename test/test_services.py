import pytest
from app.main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_services_hhtp_status(client):
    response = client.get("/api/v1/services/")
    assert response.status_code == 200

def test_get_services_structure(client):
    response = client.get("/api/v1/services/")
    data = response.get_json()

    structure_to_test = ["id", "id_service", "name", "status", "description", "team"]

    assert isinstance(data, list)
    assert all(all(key in item for key in structure_to_test) for item in data)


def test_get_services_count_hhtp_status(client):
    response = client.get("/api/v1/services/count")
    assert response.status_code == 200


def test_get_services_count_structure(client):
    response = client.get("/api/v1/services/count")
    data = response.get_json()

    assert isinstance(data, dict)
    assert "number_of_services" in data


def test_get_services_incident_count_hhtp_status(client):
    response = client.get("/api/v1/services/incident-count")
    assert response.status_code == 200


def test_get_services_incident_count_structure(client):
    response = client.get("/api/v1/services/incident-count")
    data = response.get_json()

    structure_to_test = ["name", "count"]

    assert isinstance(data, list)
    assert all(all(key in item for key in structure_to_test) for item in data)