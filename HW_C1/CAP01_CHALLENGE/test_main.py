import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def register_and_login(username="testuser", password="testpass"):
    # Register user
    response = client.post("/register", json={"username": username, "password": password})
    # Ignore if already exists
    # Login user
    response = client.post(
        "/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return token

@pytest.fixture(scope="module")
def auth_token():
    return register_and_login()

def test_bubble_sort_success(auth_token):
    payload = {"numbers": [5, 2, 9, 1, 7]}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/bubble_sort", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"sorted_numbers": [1, 2, 5, 7, 9]}

def test_bubble_sort_empty_list(auth_token):
    payload = {"numbers": []}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/bubble_sort", json=payload, headers=headers)
    assert response.status_code == 400
    assert "La lista de números no puede estar vacía" in response.text

def test_bubble_sort_single_element(auth_token):
    payload = {"numbers": [42]}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/bubble_sort", json=payload, headers=headers)
    assert response.status_code == 400
    assert "La lista de números debe tener al menos dos elementos" in response.text

def test_bubble_sort_duplicates(auth_token):
    payload = {"numbers": [1, 2, 2, 3]}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/bubble_sort", json=payload, headers=headers)
    assert response.status_code == 400
    assert "no puede contener duplicados" in response.text

def test_bubble_sort_large_list(auth_token):
    payload = {"numbers": list(range(1001))}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/bubble_sort", json=payload, headers=headers)
    assert response.status_code == 400
    assert "no puede tener más de 1000 elementos" in response.text

def test_bubble_sort_out_of_range(auth_token):
    payload = {"numbers": [1, 2, 1001]}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/bubble_sort", json=payload, headers=headers)
    assert response.status_code == 400
    assert "deben estar entre -1000 y 1000" in response.text

def test_bubble_sort_invalid_token():
    payload = {"numbers": [1, 2, 3]}
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.post("/bubble_sort", json=payload, headers=headers)
    assert response.status_code == 401
    assert "Token inválido" in response.text

def test_bubble_sort_missing_token():
    payload = {"numbers": [1, 2, 3]}
    response = client.post("/bubble_sort", json=payload)
    assert response.status_code == 401