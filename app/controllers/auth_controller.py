import logging
from typing import Any, Dict, Tuple, Optional, List

from flask import request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from app.utils.serializer import serialize_user
from app.utils.validators import validate_email, validate_password
from app.services.auth_service import AuthService
from app.services.user_service import UserService

logger = logging.getLogger(__name__)


class AuthController:
    """
    Controller for handling user authentication, including registration, login,
    and password changes.
    """

    def __init__(self) -> None:
        """
        Initialize AuthController with its dependent services.
        """
        self.auth_service: AuthService = AuthService()
        self.user_service: UserService = UserService()
        self.required_fields: List[str] = ['name', 'email', 'password', 'role']

    @jwt_required()
    def register(self) -> Tuple[Dict[str, Any], int]:
        """
        Register a new user.

        - Only authenticated users can register new users. Administrators can
          create users with any role, while non-admin users can only create 'Student' users.

        Returns:
            Tuple[Dict[str, Any], int]: Response dictionary with HTTP status code.
        """
        try:
            data: Optional[Dict[str, Any]] = request.get_json()
            if not data:
                logger.warning("No JSON payload provided in registration request.")
                return {"error": "Request payload is missing"}, 400

            missing_fields = [field for field in self.required_fields if field not in data]
            if missing_fields:
                logger.warning(f"Missing fields: {missing_fields}")
                return {"error": f"Missing required fields: {', '.join(missing_fields)}"}, 400

            # Validate email and password formats.
            if not validate_email(data['email']):
                logger.warning("Invalid email format during registration.")
                return {"error": "Invalid email format"}, 400

            if not validate_password(data['password']):
                logger.warning("Password requirements not met during registration.")
                return {"error": "Password requirements not met"}, 400

            current_user_id: Optional[str] = get_jwt_identity()
            current_user: Optional[Any] = (
                self.user_service.get_user_by_id(current_user_id) if current_user_id else None
            )

            # Disallow anonymous registration by requiring an authenticated user.
            if not current_user:
                logger.warning("Registration attempted by anonymous user.")
                return {"error": "Unauthorized access"}, 403

            # Authorization: Only an admin can create users.
            if current_user.role != "Administrator":
                logger.warning(f"Unauthorized registration attempt by user ID: {current_user_id}")
                return {"error": "Unauthorized access"}, 403

            # Check if the email is already in use.
            if self.user_service.get_user_by_email(data["email"]):
                logger.warning("Email already in use during registration.")
                return {"error": "Email already in use"}, 409

            user = self.user_service.create_user(
                name=data["name"],
                email=data["email"],
                password=data["password"],
                role=data["role"]
            )
            logger.info(f"User registered successfully with ID: {user.id}")
            return {"message": "User created", "id": str(user.id)}, 200

        except ValueError as ve:
            logger.error(f"ValueError during registration: {str(ve)}", exc_info=True)
            return {"error": str(ve)}, 409
        except Exception as e:
            logger.error(f"Unexpected registration error: {str(e)}", exc_info=True)
            return {"error": "Server error"}, 500

    def login(self) -> Tuple[Dict[str, Any], int]:
        """
        Authenticate a user and generate a JWT access token.

        Returns:
            Tuple[Dict[str, Any], int]: Access token and user information or error message.
        """
        try:
            data: Optional[Dict[str, Any]] = request.get_json()
            if not data or 'email' not in data or 'password' not in data:
                logger.warning("Login failed: Missing credentials.")
                return {"error": "Credentials required"}, 400

            user = self.auth_service.authenticate_user(email=data['email'], password=data['password'])
            if not user:
                logger.warning("Invalid credentials during login.")
                return {"error": "Invalid credentials"}, 401

            access_token: str = create_access_token(identity=str(user.id))
            logger.info(f"User logged in successfully with ID: {user.id}")
            return {
                "access_token": access_token,
                "user": serialize_user(user)
            }, 200

        except Exception as e:
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return {"error": "Authentication failed"}, 500

    def change_password(self) -> Tuple[Dict[str, Any], int]:
        """
        Change the password for an existing user.

        Expected JSON payload:
            {
                "email": "<user_email>",
                "password": "<current_password>",
                "new_password": "<new_password>"
            }

        Returns:
            Tuple[Dict[str, Any], int]: Success or error message.
        """
        try:
            data: Optional[Dict[str, Any]] = request.get_json()
            if not data or not all(field in data for field in ['email', 'password', 'new_password']):
                logger.warning("Change password failed: Missing required fields.")
                return {"error": "Email, password, and new password required"}, 400

            user = self.user_service.get_user_by_email(data["email"])
            if not user:
                logger.warning("User not found for password change.")
                return {"error": "User not found"}, 404

            if not user.check_password(data['password']):
                logger.warning("Incorrect current password during password change.")
                return {"error": "Incorrect current password"}, 401

            if not validate_password(data['new_password']):
                logger.warning("New password requirements not met.")
                return {"error": "New password requirements not met"}, 400

            self.auth_service.update_user_password(user, data['password'], data['new_password'])
            logger.info(f"Password updated successfully for user ID: {user.id}")
            return {"message": "Password updated successfully"}, 200

        except Exception as e:
            logger.error(f"Change password error: {str(e)}", exc_info=True)
            return {"error": "Unable to change password"}, 500
