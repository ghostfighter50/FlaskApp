import logging
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from .user_service import UserService
from ..config.models import User
from ..config.database import db

logger = logging.getLogger(__name__)

class AuthService:
    """
    Service layer for authentication operations
    """
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by verifying the provided email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password in plain text.

        Returns:
            Optional[User]: The authenticated User object or None if authentication fails.
        """
        logger.debug(f"Authenticating user with email: {email}")
        user = UserService.get_user_by_email(email)
        
        if user and user.check_password(password):
            logger.info(f"User (ID: {user.id}) authenticated successfully.")
            return user
        logger.warning("Invalid email/password combination. Authentication failed.")
        return None

    @staticmethod
    def update_user_password(user: User, current_pw: str, new_pw: str) -> bool:
        """
        Update a user's password if the current password is correct.

        Args:
            user (int): The user object to update.
            current_pw (str): The user's current password in plain text.
            new_pw (str): The new password in plain text.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        logger.debug(f"Attempting to update password for user ID: {user.id}")
      
        if not user:
            logger.warning(f"User ID: {user_id} not found. Cannot update password.")
            return False

        if check_password_hash(user.password_hash, current_pw):
            user.password_hash = generate_password_hash(new_pw)
            db.session.commit()
            logger.info(f"Password updated successfully for user ID: {user.id}")
            return True
        else:
            logger.warning(f"Incorrect current password for user ID: {user.id}.")
            return False
