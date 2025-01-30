import json
import jwt
import pytest
from flask import Flask
from flask_jwt_extended import create_access_token, get_jwt_identity
from app import create_app, db
from app.config.models import User

@pytest.fixture(scope="session")
def app():
    """
    Create and configure a new app instance for tests.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use an in-memory database for tests
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })
    
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create test users
        student_user = User(name="student", email="student@example.com", role="Student")
        student_user.set_password("ValidPass123!")
        db.session.add(student_user)

        professor_user = User(name="professor", email="professor@example.com", role="Professor")
        professor_user.set_password("ValidPass123!")
        db.session.add(professor_user)

        admin_user = User(name="admin", email="admin@example.com", role="Administrator")
        admin_user.set_password("ValidPass123!")
        db.session.add(admin_user)


        db.session.commit()

        # Store user IDs for reference in other tests
        app.test_student_id = student_user.id
        app.test_professor_id = professor_user.id
        app.test_admin_id = admin_user.id

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_token(app):
    return create_access_token(identity=app.test_admin_id)

@pytest.fixture
def professor_token(app):
    return create_access_token(identity=app.test_professor_id)

@pytest.fixture
def student_token(app):
    return create_access_token(identity=app.test_student_id)

@pytest.fixture()
def course_id(client, professor_token):
    """
    Creates a course before running tests and returns its ID.
    Ensures the same course is used across all test cases.
    """
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {"name": "Test Course"}

    response = client.post("/api/v1/courses/", json=payload, headers=headers)
    assert response.status_code == 200, "Course creation failed"
    
    return response.json["course"]["id"]

@pytest.fixture()
def student_id(client):
    """
    Creates a student before running tests and returns their ID.
    Ensures the same student is used across all test cases.
    """
    payload = {"password": "ValidPass123!", "email": "student@example.com"}
    

    response = client.post("/api/v1/auth/login", json=payload)

    with open("./student_response.json", "w") as f:
        json.dump(response.json, f)

    return response.json["user"]["id"]

@pytest.fixture()
def professor_id(client):
    """
    Creates a professor before running tests and returns their ID.
    Ensures the same professor is used across all test cases.
    """
    payload = {"password": "ValidPass123!", "email": "professor@example.com"}

    response = client.post("/api/v1/auth/login", json=payload)
    
    return response.json["user"]["id"]


@pytest.fixture()
def admin_id(client):
    """
    Creates an admin before running tests and returns their ID.
    Ensures the same admin is used across all test cases.
    """
    payload = {"password": "ValidPass123!", "email": "admin@example.com"}

    response = client.post("/api/v1/auth/login", json=payload)

    return response.json["user"]["id"]


@pytest.fixture()
def grade_id(client, professor_token, course_id, student_id):
    """
    Assigns a grade to a student in a course and returns the grade ID.
    """
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {"course_id": course_id, "student_id": student_id, "grade": 90}
    response = client.post("/api/v1/grades/", json=payload, headers=headers)
    assert response.status_code == 200, "Grade assignment failed"
    
    return response.json["grade"]["id"]