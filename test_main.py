from fastapi.testclient import TestClient
from fastapi import status
from main import app


# Perform on a clean db.
client = TestClient(app=app)

def test_root_returns_correct():
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome to my user-management API :)"}


def test_create_user():
    body = {"name": "Roy Anglister", "email": "royanglister@gmail.com"}
    response = client.post("/users", json=body)

    assert response.status_code == status.HTTP_201_CREATED


def test_create_another_user():
    body = {"name": "Roni Anglister", "email": "roni.anglister@gmail.com"}
    response = client.post("/users", json=body)

    assert response.status_code == status.HTTP_201_CREATED


def test_get_user():
    id = 2
    body = {"id": id, "name": "Roni Anglister", "email": "roni.anglister@gmail.com"}
    response = client.get(f"/user/{id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == body


def test_get_users():
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK


def test_update_user():
    id = 1
    body = {"id": id, "name": "Test Test", "email": "test.test@gmail.com"}
    response = client.put(f"/user/{id}", json=body)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == body


def test_delete_user():
    response = client.delete("/user/2")
    assert response.status_code == status.HTTP_200_OK
