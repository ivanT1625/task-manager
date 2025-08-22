import os
from sqlite3 import OperationalError
import time
import pytest

from app.main import app
from app import models, database, crud
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
#TEST_DATABASE_URL = os.getenv(
#    "TEST_DATABASE_URL",
#    "postgresql://taskuser:taskpass@localhost:5432/taskdb_test"
#)

# engine = create_engine(TEST_DATABASE_URL, connect_args={"connect_timeout": 10})
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def wait_for_db():
    for i in range(10):
        try:
            engine.connect()
            return True
        except OperationalError:
            time.sleep(1)
    raise Exception("Не удалось подключиться к PostgreSQL за 10 секунд")

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    wait_for_db()
    # Удаляем и создаём таблицы
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    yield
    # По желанию: можно оставить или удалить
    engine.dispose()

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[database.get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def rollback_db():
    db = TestingSessionLocal()
    yield
    db.rollback()
    db.close()


def test_create_task():
    response = client.post("/tasks/", json={"title": "Test task", "description": "Desc"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "Desc"
    assert data["status"] == "created"
    assert "uuid" in data

def test_get_task():
    create_response = client.post("/tasks/", json={"title": "Get test"})
    uuid = create_response.json()["uuid"]
    response = client.get(f"/tasks/{uuid}")
    assert response.status_code == 200
    assert response.json()["uuid"] == uuid

def test_get_task_not_found():
    response = client.get("/tasks/invalid-uuid")
    assert response.status_code == 404

def test_get_tasks_list():
    client.post("/tasks/", json={"title": "Task 1"})
    client.post("/tasks/", json={"title": "Task 2"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_update_task():
    create_response = client.post("/tasks/", json={"title": "To update"})
    uuid = create_response.json()["uuid"]
    update_response = client.put(f"/tasks/{uuid}", json={"title": "Updated", "status": "in_progress"})
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "Updated"
    assert data["status"] == "in_progress"

def test_update_task_not_found():
    response = client.put("/tasks/invalid-uuid", json={"title": "Nope"})
    assert response.status_code == 404

def test_delete_task():
    create_response = client.post("/tasks/", json={"title": "To delete"})
    uuid = create_response.json()["uuid"]
    delete_response = client.delete(f"/tasks/{uuid}")
    assert delete_response.status_code == 204
    get_response = client.get(f"/tasks/{uuid}")
    assert get_response.status_code == 404

def test_delete_task_not_found():
    response = client.delete("/tasks/invalid-uuid")
    assert response.status_code == 404