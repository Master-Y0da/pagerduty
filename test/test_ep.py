import pytest
from app.main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_ep_count_hhtp_status(client):
    response = client.get("/api/v1/escalation_policies/count")
    assert response.status_code == 200


def test_get_ep_count_structure(client):
    response = client.get("/api/v1/escalation_policies/count")
    data = response.get_json()

    structure_to_test = ["count", "ep"]

    assert isinstance(data, dict)
    assert all(key in data for key in structure_to_test)