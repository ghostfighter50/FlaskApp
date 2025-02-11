import logging
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from typing import Any, Tuple

from app.utils.serializer import serialize_user
from ..services.user_service import UserService

logger = logging.getLogger(__name__)


class UserController:
    """
    Controller for handling user management operations:
    - Listing users
    - Retrieving user details
    - Searching users
    - Creating, updating, and deleting users
    """

    def __init__(self):
        self.user_service = UserService()

    @jwt_required()
    def list_users(self) -> Tuple[Any, int]:
        """Retrieve a list of all users."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        # Only allow admins to list users
        if current_user is None or current_user.role != 'Administrator':
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        try:
            users = self.user_service.get_all_users()
            users_data = [serialize_user(user) for user in users]
            return jsonify({'users': users_data}), 200
        except Exception as e:
            logger.error(f"Error listing users: {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while listing users.'}), 500

    @jwt_required()
    def get_user(self, user_id: str) -> Tuple[Any, int]:
        """Retrieve details of a specific user by their ID."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        user = self.user_service.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found: ID {user_id}")
            return jsonify({'msg': 'User not found.'}), 404

        if current_user.role not in ['Administrator', 'Professor'] and current_user.id != user_id:
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        user_data = serialize_user(user)
        return jsonify({'user': user_data}), 200

    @jwt_required()
    def search_users(self) -> Tuple[Any, int]:
        """Search for users based on a query string."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        # Only allow admins to search for users
        if current_user is None or current_user.role != 'Administrator':
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        query = request.args.get('query', '').strip()
        try:
            users = self.user_service.search_users(query)
            users_data = [serialize_user(user) for user in users]
            return jsonify({'users': users_data}), 200
        except Exception as e:
            logger.error(f"Error searching users: {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while searching users.'}), 500

    @jwt_required()
    def create_user(self) -> Tuple[Any, int]:
        """Create a new user."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        # Only allow admins to create users
        if current_user is None or current_user.role != 'Administrator':
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        role = data.get('role', '').strip()

        if not all([name, email, password, role]):
            logger.warning("User creation failed: Missing fields.")
            return jsonify({'msg': 'All fields are required.'}), 400

        if role not in ['Student', 'Professor']:
            logger.warning(f"User creation failed: Invalid role '{role}'.")
            return jsonify({'msg': 'Invalid role.'}), 400

        existing_user = self.user_service.get_user_by_email(email)
        if existing_user:
            logger.warning(f"User creation failed: Email '{email}' already exists.")
            return jsonify({'msg': 'User with this email already exists.'}), 409

        try:
            user = self.user_service.create_user(name, email, password, role)
            user_data = serialize_user(user)
            return jsonify({'msg': 'User created successfully.', 'user': user_data}), 200
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while creating the user.'}), 500

    @jwt_required()
    def update_user(self, user_id: str) -> Tuple[Any, int]:
        """Update details of an existing user."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        # Only allow the user themselves or an admin to update
        if current_user is None or (current_user.id != user_id and current_user.role != 'Administrator'):
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        user = self.user_service.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found: ID {user_id}")
            return jsonify({'msg': 'User not found.'}), 404

        data = request.get_json()
        name = data.get('name', '').strip() or None
        email = data.get('email', '').strip().lower() or None
        password = data.get('password', '') or None

        try:
            updated_user = self.user_service.update_user(user, name, email, password)

            updated_user = self.user_service.get_user_by_id(updated_user.id)
            user_data = serialize_user(updated_user)
            return jsonify({'msg': 'User updated successfully.', 'user': user_data}), 200
        except Exception as e:
            logger.error(f"Error updating user ID: {user_id} - {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while updating the user.'}), 500

    @jwt_required()
    def delete_user(self, user_id: str) -> Tuple[Any, int]:
        """Delete an existing user."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        # Only admins can delete users
        if current_user is None or current_user.role != 'Administrator':
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        user = self.user_service.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User not found: ID {user_id}")
            return jsonify({'msg': 'User not found.'}), 404

        try:
            self.user_service.delete_user(user)
            return jsonify({'msg': 'User deleted successfully.'}), 200
        except Exception as e:
            logger.error(f"Error deleting user ID: {user_id} - {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while deleting the user.'}), 500
