import pytest
import json

def test_register_missing_fields(client):
    """
    Test registration with missing required fields. 
    Expect a 400 status and a JSON error message.
    """
    payload = {
        "name": "TestUser",
        "email": "test@example.com",
        "password": "ValidPass123!"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json.get("error") == "Missing required fields"

def test_register_invalid_email(client):
    """
    Test registration with an invalid email format.
    """
    payload = {
        "name": "Invalid Email User",
        "email": "not-an-email",
        "password": "ValidPass123!",
        "role": "Student"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json.get("error") == "Invalid email format"

def test_register_invalid_password(client):
    """
    Test registration with a password that doesn't meet requirements.
    """
    payload = {
        "name": "Invalid Password User",
        "email": "validemail@example.com",
        "password": "short",
        "role": "Student"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json.get("error") == "Password requirements not met"

def test_register_student_success(client):
    """
    Test successful registration of a student.
    """
    payload = {
        "name": "New Student",
        "email": "newstudent@example.com",
        "password": "ValidPass123!",
        "role": "Student"
    }
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 200
    assert response.json.get("message") == "User created"
    assert "id" in response.json

def test_register_professor_unauthorized(client):
    """
    Test registering a professor without admin privileges.
    Expect 403 status.
    """
    payload = {
        "name": "New Professor",
        "email": "professor@example.com",
        "password": "ValidPass123!",
        "role": "Professor"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 403
    assert response.json.get("msg") == "Unauthorized access."

def test_register_professor_as_admin(client, admin_token):
    """
    Test registering a professor with an admin user token.
    """
    payload = {
        "name": "New Professor Admin",
        "email": "newprofadmin@example.com",
        "password": "ValidPass123!",
        "role": "Professor"
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post("/api/v1/auth/register", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json.get("message") == "User created"
    assert "id" in response.json

def test_register_conflict_email(client, admin_token):
    """
    Test registering a user with an existing email.
    """
    payload = {
        "name": "Conflict User",
        "email": "conflict@example.com",
        "password": "ValidPass123!",
        "role": "Student"
    }
    headers = {"Authorization": f"Bearer {admin_token}"}
    response1 = client.post("/api/v1/auth/register", json=payload, headers=headers)
    assert response1.status_code == 200

    # Attempt to register again with the same email
    response2 = client.post("/api/v1/auth/register", json=payload, headers=headers)
    assert response2.status_code == 409
    assert "error" in response2.json

def test_login_credentials_required(client):
    """
    Test login with no credentials in the payload.
    """
    response = client.post("/api/v1/auth/login", json={})
    assert response.status_code == 400
    assert response.json.get("error") == "Credentials required"

def test_login_invalid_credentials(client):
    """
    Test login with incorrect credentials.
    """
    payload = {
        "email": "doesnotexist@example.com",
        "password": "WrongPassword123"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json.get("error") == "Invalid credentials"

def test_login_success(client):
    """
    Test successful login.
    """
    payload = {
        "email": "student@example.com",
        "password": "ValidPass123!"
    }
    response = client.post("/api/v1/auth/login", json=payload)

    assert response.status_code == 200
    assert "access_token" in response.json
    assert "user" in response.json
  

def test_profile_unauthorized(client):
    """
    Test the profile endpoint without a JWT token.
    """
    response = client.post("/api/v1/auth/profile")
    assert response.status_code == 401
    assert "msg" in response.json
    assert "Missing" in response.json.get("msg", "")

def test_profile_success(client, student_token):
    """
    Test retrieving profile data of a logged-in student.
    """
    headers = {"Authorization": f"Bearer {student_token}"}
    response = client.post("/api/v1/auth/profile", headers=headers)

    assert response.status_code == 200
    assert "user" in response.json

def test_change_password_missing_fields(client, student_token):
        """
        Test changing password with missing required fields.
        """
        headers = {"Authorization": f"Bearer {student_token}"}
        payload = {}
        response = client.post("/api/v1/auth/change-password", json=payload, headers=headers)
        assert response.status_code == 400
        assert response.json.get("error") == "Old and new passwords required"

def test_change_password_incorrect_old_password(client, student_token):
    """
    Test changing password with incorrect old password 
    """
    headers = {"Authorization": f"Bearer {student_token}"}
    payload = {"old_password": "WrongValidPass123!", "new_password": "NewPass123!"}
    response = client.post("/api/v1/auth/change-password", json=payload, headers=headers)
    assert response.status_code == 401
    assert response.json.get("error") == "Old password is incorrect"

def test_change_password_invalid_new_password(client, student_token):
    """
    Test changing password with a new password that doesn't meet requirements.
    """
    headers = {"Authorization": f"Bearer {student_token}"}
    payload = {"old_password": "ValidPass123!", "new_password": "short"}
    response = client.post("/api/v1/auth/change-password", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json.get("error") == "New password requirements not met"

def test_change_password_success(client, student_token):
    """
    Test successful password change.
    """
    headers = {"Authorization": f"Bearer {student_token}"}
    payload = {"old_password": "ValidPass123!", "new_password": "NewPass123!"}
    response = client.post("/api/v1/auth/change-password", json=payload, headers=headers)

    # Log in with the new password to verify the change
    login_payload = {"email": "student@example.com", "password": "NewPass123!"}
    login_response = client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 200
    assert "access_token" in login_response.json

    # Change the password back to the old one
    headers = {"Authorization": f"Bearer {login_response.json['access_token']}"}
    payload = {"old_password": "NewPass123!", "new_password": "ValidPass123!"}
    response = client.post("/api/v1/auth/change-password", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json.get("message") == "Password updated successfully"
    assert response.status_code == 200
    assert response.json.get("message") == "Password updated successfully"

