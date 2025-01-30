import logging
from typing import List, Optional, Dict, Any

from app.utils.serizializer import serialize_course
from ..config.models import User
from ..config.database import db
from ..services.course_service import CourseService

logger = logging.getLogger(__name__)

class UserService:
    """
    Service class for handling user management operations such as
    retrieving, searching, creating, updating, and deleting users.
    """

    @staticmethod
    def get_all_users() -> List[User]:
        """
        Retrieves all users from the database.

        Returns:
            List[User]: A list of all User objects.
        """
        logger.debug("Fetching all users from the database.")
        users: List[User] = db.session.query(User).all()
        logger.info(f"Fetched {len(users)} users from the database.")
        return users

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[User]:
        """
        Retrieves a user from the database by their unique ID.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            Optional[User]: The User object if found, else None.
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
        Retrieves a user from the database by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            Optional[User]: The User object if found, else None.
        """
        logger.debug(f"Fetching user by email: {email}")
        user: Optional[User] = (
            db.session.query(User)
            .filter_by(email=email)
            .first()
        )
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
            query (str): The search query string.

        Returns:
            List[User]: A list of User objects matching the search criteria.
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
        Creates a new user and saves them to the database.

        Args:
            name (str): The full name of the user.
            email (str): The email address of the user.
            password (str): The plaintext password for the user.
            role (str): The role assigned to the user.

        Returns:
            User: The newly created User object.
        """
        logger.debug(f"Creating user: {name}, Email: {email}, Role: {role}")
        new_user = User(name=name, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        logger.info(f"User created with ID: {new_user.id}")
        return new_user

    @staticmethod
    def update_user(
        user: User,
        name: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None
    ) -> User:
        """
        Updates an existing user's details.

        Args:
            user (User): The User object to be updated.
            name (Optional[str]): The new name for the user.
            email (Optional[str]): The new email for the user.
            password (Optional[str]): The new password for the user.

        Returns:
            User: The updated User object.
        """
        logger.debug(
            f"Updating user ID: {user.id} "
            f"with Name: {name if name else 'unchanged'}, "
            f"Email: {email if email else 'unchanged'}"
        )
        if name:
            user.name = name
        if email:
            user.email = email
        if password:
            user.set_password(password)
        db.session.commit()
        logger.info(f"User ID: {user.id} updated successfully.")
        return user

    @staticmethod
    def delete_user(user: User) -> None:
        """
        Deletes a user from the database.

        Args:
            user (User): The User object to be deleted.
        """
        logger.debug(f"Deleting user ID: {user.id}")
        db.session.delete(user)
        db.session.commit()
        logger.info(f"User ID: {user.id} deleted successfully.")