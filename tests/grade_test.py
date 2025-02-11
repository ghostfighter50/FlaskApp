def test_list_grades_unauthorized(client, student_token):
    headers = {"Authorization": f"Bearer {student_token}"}
    response = client.get("/api/v1/grades/", headers=headers)

    assert response.status_code == 403


def test_list_grades(client, professor_token):
    headers = {"Authorization": f"Bearer {professor_token}"}
    response = client.get("/api/v1/grades/", headers=headers)

    assert response.status_code == 200
    assert "grades" in response.json
    assert isinstance(response.json["grades"], list)


def test_assign_grade_missing_fields(client, professor_token):
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {}

    response = client.post("/api/v1/grades/", json=payload, headers=headers)

    assert response.status_code == 400


def test_assign_grade_invalid_student(client, professor_token, course_id):
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {"course_id": course_id, "student_id": "invalid_student_id", "grade": 85, "grade_name": "DM"}

    response = client.post("/api/v1/grades/", json=payload, headers=headers)

    assert response.status_code == 404


def test_assign_grade_invalid_course(client, professor_token, student_id):
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {"course_id": "invalid_course_id", "student_id": student_id, "grade": 85, "grade_name": "DM"}

    response = client.post("/api/v1/grades/", json=payload, headers=headers)

    assert response.status_code == 404


def test_assign_grade_success(client, professor_token, course_id, student_id):
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {"course_id": course_id, "student_id": student_id, "grade": 90, "grade_name": "DM"}

    response = client.post("/api/v1/grades/", json=payload, headers=headers)

    assert response.status_code == 200

    assert "grade" in response.json


def test_get_grade_unauthorized(client, student_token, grade_id):
    headers = {"Authorization": f"Bearer {student_token}"}
    response = client.get(f"/api/v1/grades/{grade_id}", headers=headers)

    assert response.status_code == 403


def test_get_grade_success(client, professor_token, grade_id):
    headers = {"Authorization": f"Bearer {professor_token}"}
    response = client.get(f"/api/v1/grades/{grade_id}", headers=headers)

    assert response.status_code == 200
    assert "grade" in response.json


def test_update_grade_unauthorized(client, student_token, grade_id):
    headers = {"Authorization": f"Bearer {student_token}"}
    payload = {"grade": 95}

    response = client.put(f"/api/v1/grades/{grade_id}", json=payload, headers=headers)

    assert response.status_code == 403


def test_update_grade_missing_fields(client, professor_token, grade_id):
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {}

    response = client.put(f"/api/v1/grades/{grade_id}", json=payload, headers=headers)

    assert response.status_code == 400


def test_update_grade_success(client, professor_token, grade_id):
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {"grade": 95}

    response = client.put(f"/api/v1/grades/{grade_id}", json=payload, headers=headers)

    assert response.status_code == 200


def test_get_student_grades(client, professor_token, course_id, student_id):
    headers = {"Authorization": f"Bearer {professor_token}"}
    response = client.get(f"/api/v1/grades/courses/{course_id}/students/{student_id}/grades", headers=headers)

    assert response.status_code == 200
    assert "grades" in response.json
    assert isinstance(response.json["grades"], list)


def test_delete_grade_unauthorized(client, professor_token, grade_id):
    headers = {"Authorization": f"Bearer {professor_token}"}
    response = client.delete(f"/api/v1/grades/{grade_id}", headers=headers)

    assert response.status_code == 403


def test_delete_grade_admin(client, admin_token, grade_id):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.delete(f"/api/v1/grades/{grade_id}", headers=headers)

    assert response.status_code == 200
