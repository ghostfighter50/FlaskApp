def test_register_missing_fields(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "name": "TestUser",
        "email": "test@example.com",
        "password": "ValidPass123!"
    }
    response = client.post("/api/v1/auth/register", json=payload, headers=headers)
    assert response.status_code == 400


def test_register_invalid_email(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "name": "Invalid Email User",
        "email": "not-an-email",
        "password": "ValidPass123!",
        "role": "Student"
    }
    response = client.post("/api/v1/auth/register", json=payload, headers=headers)
    assert response.status_code == 400


def test_register_invalid_password(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "name": "Invalid Password User",
        "email": "validemail@example.com",
        "password": "short",
        "role": "Student"
    }
    response = client.post("/api/v1/auth/register", json=payload, headers=headers)
    assert response.status_code == 400


def test_register_professor_unauthorized(client, professor_token):
    headers = {"Authorization": f"Bearer {professor_token}"}
    payload = {
        "name": "New Professor",
        "email": "professor@example.com",
        "password": "ValidPass123!",
        "role": "Professor"
    }
    response = client.post("/api/v1/auth/register", json=payload, headers=headers)
    assert response.status_code == 403


def test_register_professor_as_admin(client, admin_token):
    payload = {
        "name": "New Professor Admin",
        "email": "newprofadmin@example.com",
        "password": "ValidPass123!",
        "role": "Professor"
    }
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = client.post("/api/v1/auth/register", json=payload, headers=headers)
    assert response.status_code == 200


def test_register_conflict_email(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "name": "Conflict User",
        "email": "conflict@example.com",
        "password": "ValidPass123!",
        "role": "Student"
    }

    response1 = client.post("/api/v1/auth/register", json=payload, headers=headers)
    assert response1.status_code == 200

    response2 = client.post("/api/v1/auth/register", json=payload, headers=headers)
    assert response2.status_code == 409


def test_login_credentials_required(client):
    response = client.post("/api/v1/auth/login", json={})
    assert response.status_code == 400


def test_login_invalid_credentials(client):
    payload = {
        "email": "doesnotexist@example.com",
        "password": "WrongPassword123"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401


def test_login_success(client):
    payload = {
        "email": "student@example.com",
        "password": "ValidPass123!"
    }

    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "user" in response.json


def test_change_password_missing_fields(client):
    payload = {}
    response = client.post("/api/v1/auth/change-password", json=payload)

    assert response.status_code == 400


def test_change_password_incorrect_password(client):
    payload = {
        "email": "student@example.com",
        "password": "WrongValidPass123!",
        "new_password": "NewPass123!"
    }
    response = client.post("/api/v1/auth/change-password", json=payload)
    assert response.status_code == 401


def test_change_password_invalid_new_password(client):
    payload = {
        "email": "student@example.com",
        "password": "ValidPass123!",
        "new_password": "short"
    }
    response = client.post("/api/v1/auth/change-password", json=payload)
    assert response.status_code == 400


def test_change_password_success(client):
    payload = {
        "email": "student@example.com",
        "password": "ValidPass123!",
        "new_password": "NewPass123!"
    }
    response = client.post("/api/v1/auth/change-password", json=payload)
    assert response.status_code == 200

    login_payload = {"email": "student@example.com", "password": "NewPass123!"}
    login_response = client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 200
    assert "access_token" in login_response.json

    revert_payload = {
        "email": "student@example.com",
        "password": "NewPass123!",
        "new_password": "ValidPass123!"
    }
    revert_response = client.post("/api/v1/auth/change-password", json=revert_payload)
    assert revert_response.status_code == 200
