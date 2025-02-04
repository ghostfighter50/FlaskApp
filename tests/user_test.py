def test_list_users_admin(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/v1/users/", headers=headers)
    data = response.get_json()
    assert response.status_code == 200
    assert "users" in data
    assert isinstance(data["users"], list)


def test_list_users_non_admin(client, professor_token):
    headers = {"Authorization": f"Bearer {professor_token}"}
    response = client.get("/api/v1/users/", headers=headers)
    response.get_json()
    # Only an administrator should be allowed to list users.
    assert response.status_code == 403


def test_get_user_admin(client, admin_token, student_id):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get(f"/api/v1/users/{student_id}", headers=headers)
    data = response.get_json()
    assert response.status_code == 200
    assert "user" in data
    assert data["user"]["id"] == student_id


def test_get_user_self(client, professor_token, professor_id):
    headers = {"Authorization": f"Bearer {professor_token}"}
    response = client.get(f"/api/v1/users/{professor_id}", headers=headers)
    data = response.get_json()
    assert response.status_code == 200
    assert "user" in data
    assert data["user"]["id"] == professor_id


def test_get_user_not_found(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/v1/users/nonexistent-user-id", headers=headers)
    assert response.status_code == 404


def test_search_users_admin(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/v1/users/search?query=student", headers=headers)
    data = response.get_json()
    assert response.status_code == 200
    assert "users" in data
    assert isinstance(data["users"], list)


def test_search_users_non_admin(client, professor_token):
    headers = {"Authorization": f"Bearer {professor_token}"}
    response = client.get("/api/v1/users/search?query=student", headers=headers)
    assert response.status_code == 403


def test_create_user_missing_fields(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {}  # Missing required fields
    response = client.post("/api/v1/users/", json=payload, headers=headers)
    response.get_json()
    assert response.status_code == 400


def test_create_user_invalid_role(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "TestPass123!",
        "role": "Administrator"  # Only "Student" or "Professor" allowed
    }
    response = client.post("/api/v1/users/", json=payload, headers=headers)
    response.get_json()
    assert response.status_code == 400


def test_create_user_success(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "name": "New Student",
        "email": "newstudent@example.com",
        "password": "TestPass123!",
        "role": "Student"
    }
    response = client.post("/api/v1/users/", json=payload, headers=headers)
    data = response.get_json()
    assert response.status_code == 200
    assert "msg" in data
    assert "user" in data
    new_user_id = data["user"]["id"]

    get_response = client.get(f"/api/v1/users/{new_user_id}", headers=headers)
    get_data = get_response.get_json()
    assert get_response.status_code == 200
    assert get_data["user"]["id"] == new_user_id


def test_update_user_unauthorized(client, professor_token, student_id):
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {"name": "Updated Student Name"}
    response = client.put(f"/api/v1/users/{student_id}", json=payload, headers=headers)
    response.get_json()
    assert response.status_code == 403


def test_update_user_self(client, professor_token, professor_id):
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {"name": "Updated Professor Name"}
    response = client.put(f"/api/v1/users/{professor_id}", json=payload, headers=headers)
    data = response.get_json()
    assert response.status_code == 200
    assert data["user"]["name"] == "Updated Professor Name"


def test_delete_user_admin(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "name": "Temp Student",
        "email": "tempstudent@example.com",
        "password": "TempPass123!",
        "role": "Student"
    }
    create_response = client.post("/api/v1/users/", json=payload, headers=headers)
    create_data = create_response.get_json()
    assert create_response.status_code == 200
    temp_user_id = create_data["user"]["id"]

    delete_response = client.delete(f"/api/v1/users/{temp_user_id}", headers=headers)
    assert delete_response.status_code == 200

    get_response = client.get(f"/api/v1/users/{temp_user_id}", headers=headers)
    assert get_response.status_code == 404
