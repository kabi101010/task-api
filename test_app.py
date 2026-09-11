import pytest
import app as app_module


@pytest.fixture
def client():
    """Fresh Flask test client with reset in-memory storage for each test."""
    app_module.tasks = []
    app_module.next_id = 1
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


# ---------- /health ----------

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


# ---------- GET /tasks ----------

def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_tasks_after_creation(client):
    client.post("/tasks", json={"title": "Buy milk"})
    response = client.get("/tasks")
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Buy milk"


# ---------- POST /tasks ----------

def test_create_task_success(client):
    response = client.post("/tasks", json={"title": "Write tests"})
    data = response.get_json()
    assert response.status_code == 201
    assert data["title"] == "Write tests"
    assert data["done"] is False
    assert data["id"] == 1
    assert "created_at" in data


def test_create_task_missing_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "title is required"}


def test_create_task_no_body(client):
    # No content-type/body at all -> Flask itself rejects it before
    # the route's own "title is required" check ever runs.
    response = client.post("/tasks")
    assert response.status_code == 415


def test_create_task_ids_increment(client):
    first = client.post("/tasks", json={"title": "First"}).get_json()
    second = client.post("/tasks", json={"title": "Second"}).get_json()
    assert first["id"] == 1
    assert second["id"] == 2


# ---------- PATCH /tasks/<id> ----------

def test_update_task_title(client):
    created = client.post("/tasks", json={"title": "Old title"}).get_json()
    response = client.patch(f"/tasks/{created['id']}", json={"title": "New title"})
    data = response.get_json()
    assert response.status_code == 200
    assert data["title"] == "New title"
    assert data["done"] is False


def test_update_task_done_status(client):
    created = client.post("/tasks", json={"title": "Task"}).get_json()
    response = client.patch(f"/tasks/{created['id']}", json={"done": True})
    data = response.get_json()
    assert response.status_code == 200
    assert data["done"] is True
    assert data["title"] == "Task"  # unchanged


def test_update_task_not_found(client):
    response = client.patch("/tasks/999", json={"title": "Nope"})
    assert response.status_code == 404
    assert response.get_json() == {"error": "task not found"}


# ---------- DELETE /tasks/<id> ----------

def test_delete_task_success(client):
    created = client.post("/tasks", json={"title": "Delete me"}).get_json()
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204

    # Confirm it's actually gone
    remaining = client.get("/tasks").get_json()
    assert remaining == []


def test_delete_task_not_found(client):
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.get_json() == {"error": "task not found"}


def test_delete_only_removes_target_task(client):
    first = client.post("/tasks", json={"title": "Keep me"}).get_json()
    second = client.post("/tasks", json={"title": "Delete me"}).get_json()

    client.delete(f"/tasks/{second['id']}")

    remaining = client.get("/tasks").get_json()
    assert len(remaining) == 1
    assert remaining[0]["id"] == first["id"]
