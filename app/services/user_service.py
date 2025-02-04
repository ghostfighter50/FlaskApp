import logging
from typing import List, Optional
from app.config.models import User
from ..config.database import db

logger = logging.getLogger(__name__)


class UserService:
    """
    Service class for managing user-related operations, including:
    - Retrieving users by ID or email.
    - Searching for users based on a query.
    - Creating, updating, and deleting user records.
    """

    @staticmethod
    def get_all_users() -> List[User]:
        """
        Retrieves all users from the database.

        Returns:
            List[User]: A list of all User objects in the database.
        """
        logger.debug("Fetching all users from the database.")
        users: List[User] = db.session.query(User).all()
        logger.info(f"Fetched {len(users)} users from the database.")
        return users

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[User]:
        """
        Retrieves a user by their unique ID.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            Optional[User]: The User object if found, otherwise None.
        """
        logger.debug(f"Fetching user by ID: {user_id}")
        user: Optional[User] = db.session.get(User, user_id)
        if user:
            logger.debug(f"User found: {user.name} (ID: {user.id})")
        else:
            logger.debug(f"No user found with ID: {user_id}")
        return user

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """
        Retrieves a user by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            Optional[User]: The User object if found, otherwise None.
        """
        logger.debug(f"Fetching user by email: {email}")
        user: Optional[User] = db.session.query(User).filter_by(email=email).first()
        if user:
            logger.debug(f"User found: {user.name} (ID: {user.id})")
        else:
            logger.debug(f"No user found with email: {email}")
        return user

    @staticmethod
    def search_users(query: str) -> List[User]:
        """
        Searches for users whose name or email contains the query string.

        Args:
            query (str): The search query to match against user names and emails.

        Returns:
            List[User]: A list of User objects that match the query.
        """
        logger.debug(f"Searching users with query: {query}")
        users: List[User] = (
            db.session.query(User)
            .filter(
                (User.name.ilike(f"%{query}%")) |
                (User.email.ilike(f"%{query}%"))
            )
            .all()
        )
        logger.info(f"Found {len(users)} users matching query '{query}'.")
        return users

    @staticmethod
    def create_user(name: str, email: str, password: str, role: str) -> User:
        """
        Creates and saves a new user to the database.

        Args:
            name (str): The name of the user.
            email (str): The email address of the user.
            password (str): The user's password in plain text.
            role (str): The role assigned to the user (e.g., "admin", "student").

        Returns:
            User: The newly created User object.
        """
        logger.debug(f"Creating user: {name}, Email: {email}, Role: {role}")
        new_user = User(name=name, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        logger.info(f"User created with ID: {new_user.id}")
        return new_user

    @staticmethod
    def update_user(user: User, name: Optional[str] = None,
                    email: Optional[str] = None,
                    password: Optional[str] = None) -> User:
        """
        Updates an existing user's details.

        Args:
            user (User): The User object to update.
            name (Optional[str]): The new name for the user, if provided.
            email (Optional[str]): The new email for the user, if provided.
            password (Optional[str]): The new password for the user, if provided.

        Returns:
            User: The updated User object.
        """
        logger.debug(
            f"Updating user ID: {user.id} with Name: {name if name else 'unchanged'}, "
            f"Email: {email if email else 'unchanged'}"
        )
        if name:
            user.name = name
        if email:
            user.email = email
        if password:
            user.set_password(password)
        db.session.commit()
        db.session.refresh(user)
        logger.info(f"User ID: {user.id} updated successfully.")
        return user

    @staticmethod
    def delete_user(user: User) -> None:
        """
        Deletes a user from the database.

        Args:
            user (User): The User object to delete.
        """
        logger.debug(f"Deleting user ID: {user.id}")
        db.session.delete(user)
        db.session.commit()
        logger.info(f"User ID: {user.id} deleted successfully.")
