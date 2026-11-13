
import pytest
from app import app, medicines, create_token


@pytest.fixture
def client():
    app.config["TESTING"] = True
    medicines.clear()
    medicines.update({
        1: {"id": 1, "name": "Paracetamol", "quantity": 100, "price": 2.50}
    })
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_headers():
    token = create_token("admin")
    return {"Authorization": f"Bearer {token}"}


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_login_success(client):
    response = client.post("/login", json={
        "username": "admin",
        "password": "MediplusAdmin@2026!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_failure(client):
    response = client.post("/login", json={
        "username": "admin",
        "password": "wrong"
    })
    assert response.status_code == 401


def test_inventory_requires_authentication(client):
    response = client.get("/medicines")
    assert response.status_code == 401


def test_get_medicines(client, auth_headers):
    response = client.get("/medicines", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) == 1


def test_add_medicine(client, auth_headers):
    response = client.post("/medicines", headers=auth_headers, json={
        "name": "Vitamin C", "quantity": 50, "price": 5.0
    })
    assert response.status_code == 201


def test_reject_negative_quantity(client, auth_headers):
    response = client.post("/medicines", headers=auth_headers, json={
        "name": "Test", "quantity": -5, "price": 2.0
    })
    assert response.status_code == 400


def test_reject_unexpected_fields(client, auth_headers):
    response = client.post("/medicines", headers=auth_headers, json={
        "name": "Test", "quantity": 5, "price": 2.0, "admin": True
    })
    assert response.status_code == 400


def test_update_medicine(client, auth_headers):
    response = client.put("/medicines/1", headers=auth_headers, json={
        "quantity": 80
    })
    assert response.status_code == 200
    assert response.json["quantity"] == 80


def test_delete_medicine(client, auth_headers):
    response = client.delete("/medicines/1", headers=auth_headers)
    assert response.status_code == 200


def test_missing_medicine(client, auth_headers):
    response = client.delete("/medicines/999", headers=auth_headers)
    assert response.status_code == 404
