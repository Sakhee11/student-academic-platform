import pytest

from app import create_app
from database.db import db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        db.reset()
        yield client
        db.reset()


def test_healthcheck(client):
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "UP"
    assert "Student Academic" in data["service"]


def test_list_courses(client):
    response = client.get("/api/courses")

    assert response.status_code == 200

    data = response.get_json()

    assert data["count"] >= 2


def test_register_student(client):
    response = client.post(
        "/api/students",
        json={
            "student_id": "S300",
            "name": "John Doe",
            "email": "john@university.edu",
            "semester": 2
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["student"]["student_id"] == "S300"


def test_enroll_student(client):
    response = client.post(
        "/api/enroll",
        json={
            "student_id": "S101",
            "course_id": "C101"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Student enrolled successfully"
