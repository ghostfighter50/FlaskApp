
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from typing import Tuple, Dict

from app.utils.serizializer import serialize_user
from ..services.auth_service import AuthService
from ..services.user_service import UserService
from ..utils.validators import validate_email, validate_password
import logging

logger = logging.getLogger(__name__)

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()
        self.user_service = UserService()
        self.required_fields = ['name', 'email', 'password', 'role']

    @jwt_required(optional=True)
    def register(self) -> Tuple[Dict, int]:
        try:
            data = request.get_json()
            
            if not all(field in data for field in self.required_fields):
                return {"error": "Missing required fields"}, 400

            if not validate_email(data['email']):
                return {"error": "Invalid email format"}, 400

            if not validate_password(data['password']):
                return {"error": "Password requirements not met"}, 400
            
            current_user_id = get_jwt_identity()
            current_user = None
            if current_user_id:
                current_user = self.user_service.get_user_by_id(current_user_id)


            if not current_user:
                # Anonymous user => only allow creating a "Student"
                if data["role"] != "Student":
                    return jsonify({"msg": "Unauthorized access."}), 403
            else:
                # Authenticated user => must be Admin to create non-Student
                if current_user.role != "Administrator" and data["role"] != "Student":
                    logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
                    return jsonify({"msg": "Unauthorized access."}), 403

            # Check if email already exists
            existing_user = self.user_service.get_user_by_email(data["email"])
            if existing_user:
                return {"error": "Email already in use"}, 409

            user = self.user_service.create_user(
                data["name"],
                data["email"],
                data["password"],
                data["role"]
            )
            return {"message": "User created", "id": str(user.id)}, 200

        except ValueError as e:
            logger.error(f"Registration error: {str(e)}")
            return {"error": str(e)}, 409
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {"error": "Server error"}, 500


    def login(self) -> Tuple[Dict, int]:
        try:
            data = request.get_json()
            if not data or 'email' not in data or 'password' not in data:
                return {"error": "Credentials required"}, 400

            user = self.auth_service.authenticate_user(data['email'], data['password'])
            if not user:
                return {"error": "Invalid credentials"}, 401

            access_token = create_access_token(identity=str(user.id))
            return {
                "access_token": access_token,
                "user": serialize_user(user)
            }, 200

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return {"error": "Authentication failed"}, 500

    @jwt_required()
    def profile(self) -> Tuple[Dict, int]:
        try:
            user = self.user_service.get_user_by_id(get_jwt_identity())
            return {"user": serialize_user(user)}, 200
        except Exception as e:
            logger.error(f"Profile error: {str(e)}")
            return {"error": "Unable to fetch profile"}, 500
        
    jwt_required()
    def change_password(self) -> Tuple[Dict, int]:
        try:
            data = request.get_json()
            if not data or 'old_password' not in data or 'new_password' not in data:
                return {"error": "Old and new passwords required"}, 400

            user_id = get_jwt_identity()
            user = self.user_service.get_user_by_id(user_id)
            if not user:
                return {"error": "User not found"}, 404

            logger.debug(data['old_password'])
            logger.debug(data['new_password'])
            logger.debug(user.check_password(data['old_password']))
            if not user.check_password(data['old_password']):
                return {"error": "Old password is incorrect"}, 401

            if not validate_password(data['new_password']):
                return {"error": "New password requirements not met"}, 400

            self.auth_service.update_user_password(user, data['old_password'], data['new_password'])
            return {"message": "Password updated successfully"}, 200

        except Exception as e:
            logger.error(f"Change password error: {str(e)}")
            return {"error": "Unable to change password"}, 500       
        
