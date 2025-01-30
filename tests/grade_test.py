import pytest
import json


def test_list_grades_unauthorized(client, student_token):
    """Ensure students cannot list grades."""
    headers = {"Authorization": f"Bearer {student_token}"}
    response = client.get("/api/v1/grades/", headers=headers)
    assert response.status_code == 403
    assert response.json['msg'] == "Unauthorized access."


def test_list_grades(client, professor_token):
    """Test listing all grades (only professors and admins can access)."""
    headers = {"Authorization": f"Bearer {professor_token}"}
    response = client.get("/api/v1/grades/", headers=headers)
    assert response.status_code == 200
    assert "grades" in response.json
    assert isinstance(response.json["grades"], list)


def test_assign_grade_missing_fields(client, professor_token):
    """Test assigning a grade with missing fields."""
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {}  # Missing fields

    response = client.post("/api/v1/grades/", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json['msg'] == "All fields are required."


def test_assign_grade_invalid_student(client, professor_token, course_id):
    """Test assigning a grade to a non-existent student."""
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {"course_id": course_id, "student_id": "invalid_student_id", "grade": 85}

    response = client.post("/api/v1/grades/", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json['msg'] == "Course or student not found."


def test_assign_grade_invalid_course(client, professor_token, student_id):
    """Test assigning a grade to a non-existent course."""
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {"course_id": "invalid_course_id", "student_id": student_id, "grade": 85}

    response = client.post("/api/v1/grades/", json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json['msg'] == "Course or student not found."


def test_assign_grade_success(client, professor_token, course_id, student_id):
    """Test successfully assigning a grade to a student in a course."""
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {"course_id": course_id, "student_id": student_id, "grade": 90}

    response = client.post("/api/v1/grades/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json['msg'] == "Grade assigned successfully."
    assert "grade" in response.json

    # Store grade ID for further tests
    global grade_id
    grade_id = response.json["grade"]["id"]


def test_get_grade_unauthorized(client, student_token, grade_id):
    """Ensure students cannot fetch grades they don't own."""
    headers = {"Authorization": f"Bearer {student_token}"}
    response = client.get(f"/api/v1/grades/{grade_id}", headers=headers)
    assert response.status_code == 403
    assert response.json['msg'] == "Unauthorized access."


def test_get_grade_success(client, professor_token, grade_id):
    """Test retrieving a specific grade."""
    headers = {"Authorization": f"Bearer {professor_token}"}
    response = client.get(f"/api/v1/grades/{grade_id}", headers=headers)

    assert response.status_code == 200
    assert "grade" in response.json
    assert response.json["grade"]["id"] == grade_id


def test_update_grade_unauthorized(client, student_token, grade_id):
    """Ensure students cannot update grades."""
    headers = {"Authorization": f"Bearer {student_token}"}
    payload = {"grade": 95}

    response = client.put(f"/api/v1/grades/{grade_id}", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json['msg'] == "Unauthorized access."


def test_update_grade_missing_fields(client, professor_token, grade_id):
    """Test updating a grade without providing a new grade value."""
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {}  # Missing 'grade'

    response = client.put(f"/api/v1/grades/{grade_id}", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json['msg'] == "Grade value is required."


def test_update_grade_success(client, professor_token, grade_id):
    """Test successfully updating a grade."""
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {"grade": 95}

    response = client.put(f"/api/v1/grades/{grade_id}", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json['msg'] == "Grade updated successfully."
    assert response.json["grade"]["grade"] == 95


def test_get_student_grades(client, professor_token, course_id, student_id):
    """Test retrieving all grades for a student in a specific course."""
    headers = {"Authorization": f"Bearer {professor_token}"}
    response = client.get(f"/api/v1/grades/courses/{course_id}/students/{student_id}/grades", headers=headers)

    assert response.status_code == 200
    assert "grades" in response.json
    assert isinstance(response.json["grades"], list)


def test_delete_grade_unauthorized(client, professor_token, grade_id):
    """Ensure professors cannot delete grades (only admins can)."""
    headers = {"Authorization": f"Bearer {professor_token}"}
    response = client.delete(f"/api/v1/grades/{grade_id}", headers=headers)

    assert response.status_code == 403
    assert response.json['msg'] == "Unauthorized access."


def test_delete_grade_admin(client, admin_token, grade_id):
    """Test successfully deleting a grade as an admin."""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.delete(f"/api/v1/grades/{grade_id}", headers=headers)
    print(response.json)
    assert response.status_code == 200
    assert response.json['msg'] == "Grade deleted successfully."
