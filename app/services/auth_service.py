import logging
from typing import Optional

from werkzeug.security import generate_password_hash, check_password_hash

from .user_service import UserService
from ..config.models import User
from ..config.database import db

logger = logging.getLogger(__name__)


class AuthService:
    """
    Service layer for authentication operations.
    """

    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by verifying the provided email and password.

        Args:
            email (str): The user's email (plain text).
            password (str): The user's password (plain text).

        Returns:
            Optional[User]: The authenticated User object if credentials are valid,
            otherwise None.
        """
        logger.debug("Authenticating user with email: %s", email)

        # -- IMPORTANT --
        # Instead of a direct encrypted-email lookup, this function relies on
        # the updated get_user_by_email in UserService (which uses email_hash).
        user = UserService.get_user_by_email(email)

        if user:
            if user.check_password(password):
                logger.info("User (ID: %s) authenticated successfully.", user.id)
                return user
            else:
                logger.warning("Password mismatch for user with email: %s", email)
        else:
            logger.warning("No user found with email: %s", email)

        return None

    @staticmethod
    def update_user_password(user: Optional[User], current_pw: str, new_pw: str) -> bool:
        """
        Update a user's password if the current password is correct.

        Args:
            user (Optional[User]): The user object to update. If None, the operation fails.
            current_pw (str): The user's current password in plain text.
            new_pw (str): The new password in plain text.

        Returns:
            bool: True if the password was updated successfully, False otherwise.
        """
        if user is None:
            logger.warning("User not provided or not found. Cannot update password.")
            return False

        logger.debug("Attempting to update password for user ID: %s", user.id)

        # Verify the current password using a secure hash check
        if check_password_hash(user.password_hash, current_pw):
            try:
                # Generate a new hash for the new password and update the user's record
                user.password_hash = generate_password_hash(new_pw)
                db.session.commit()
                logger.info("Password updated successfully for user ID: %s", user.id)
                return True
            except Exception as e:
                logger.error("Error updating password for user ID: %s, Error: %s", user.id, e)
                db.session.rollback()
                return False
        else:
            logger.warning("Incorrect current password for user ID: %s.", user.id)
            return False
