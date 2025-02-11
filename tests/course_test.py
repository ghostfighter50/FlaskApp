def test_list_courses(client, student_token):
    headers = {"Authorization": f"Bearer {student_token}"}
    response = client.get("/api/v1/courses/", headers=headers)

    assert response.status_code == 200
    assert "courses" in response.json
    assert isinstance(response.json["courses"], list)


def test_get_course(client, student_token, course_id):
    headers = {"Authorization": f"Bearer {student_token}"}
    response = client.get(f"/api/v1/courses/{course_id}", headers=headers)

    assert response.status_code == 200
    assert "course" in response.json
    assert response.json["course"]["id"] == course_id


def test_search_courses(client, student_token):
    headers = {"Authorization": f"Bearer {student_token}"}
    response = client.get("/api/v1/courses/search?name=Test", headers=headers)

    assert response.status_code == 200
    assert "courses" in response.json
    assert any("Test Course" in course["name"] for course in response.json["courses"])


def test_list_students_in_course(client, professor_token, course_id):
    headers = {"Authorization": f"Bearer {professor_token}"}
    response = client.get(f"/api/v1/courses/{course_id}/students", headers=headers)

    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert "students" in response.json


def test_create_course_unauthorized(client, student_token):
    headers = {"Authorization": f"Bearer {student_token}"}
    payload = {"name": "Unauthorized Course"}

    response = client.post("/api/v1/courses/", json=payload, headers=headers)
    assert response.status_code == 403


def test_update_course(client, professor_token, course_id):
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {"name": "Updated Test Course"}

    response = client.put(f"/api/v1/courses/{course_id}", json=payload, headers=headers)
    assert response.status_code == 200


def test_delete_course_unauthorized(client, professor_token, course_id):
    headers = {"Authorization": f"Bearer {professor_token}"}

    response = client.delete(f"/api/v1/courses/{course_id}", headers=headers)
    assert response.status_code == 403


def test_delete_course_admin(client, admin_token, course_id):
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = client.delete(f"/api/v1/courses/{course_id}", headers=headers)
    assert response.status_code == 200
