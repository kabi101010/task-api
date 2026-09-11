import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Write tests"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Write tests"
    assert data["done"] is False


def test_create_task_without_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400


def test_list_tasks(client):
    client.post("/tasks", json={"title": "Task A"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_update_nonexistent_task(client):
    response = client.patch("/tasks/9999", json={"done": True})
    assert response.status_code == 404


def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/9999")
    assert response.status_code == 404
