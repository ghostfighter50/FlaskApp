import logging
from typing import List, Optional

from app.config.models import User, compute_email_hash
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
        logger.info("Fetched %d users from the database.", len(users))
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
        logger.debug("Fetching user by ID: %s", user_id)
        user: Optional[User] = db.session.get(User, user_id)
        if user:
            logger.debug("User found: %s (ID: %s)", user.name, user.id)
        else:
            logger.debug("No user found with ID: %s", user_id)
        return user

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """
        Retrieves a user by their email address (uses email_hash for lookup).

        Args:
            email (str): The email address (plain text).

        Returns:
            Optional[User]: The User object if found, otherwise None.
        """
        logger.debug("Fetching user by email: %s", email)

        email_hash = compute_email_hash(email)
        user: Optional[User] = db.session.query(User).filter_by(email_hash=email_hash).first()

        if user:
            logger.debug("User found: %s (ID: %s)", user.name, user.id)
        else:
            logger.debug("No user found with email: %s", email)
        return user

    @staticmethod
    def search_users(query: str) -> List[User]:
        """
        Searches for users whose name or email contains the query string.
        Because name/email may be encrypted, we cannot directly do partial
        matching in the SQL query. As a workaround, we:
          1. Fetch all users (caution: large DB impact).
          2. Decrypt name and email in Python.
          3. Perform a case-insensitive substring check.

        Args:
            query (str): The search query to match against user name/email.

        Returns:
            List[User]: A list of User objects that match the query.
        """
        logger.debug("Searching users with query: %s", query)
        query_lower = query.lower()

        all_users: List[User] = db.session.query(User).all()

        matched = []
        for user in all_users:
            if (user.name and query_lower in user.name.lower()) or \
               (user.email and query_lower in user.email.lower()):
                matched.append(user)

        logger.info("Found %d users matching query '%s'.", len(matched), query)
        return matched

    @staticmethod
    def create_user(name: str, email: str, password: str, role: str) -> User:
        """
        Creates and saves a new user to the database.

        Args:
            name (str): The name of the user.
            email (str): The email address of the user.
            password (str): The user's password in plain text.
            role (str): The role assigned to the user (e.g., "Administrator", "Student", etc.).

        Returns:
            User: The newly created User object.
        """
        logger.debug("Creating user: %s, Email: %s, Role: %s", name, email, role)
        new_user = User(name=name, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        logger.info("User created with ID: %s", new_user.id)
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
            user (User): The User object to update.
            name (Optional[str]): The new name for the user, if provided.
            email (Optional[str]): The new email for the user, if provided.
            password (Optional[str]): The new password for the user, if provided.

        Returns:
            User: The updated User object.
        """
        logger.debug(
            "Updating user ID: %s with Name: %s, Email: %s",
            user.id,
            name,
            email,
        )
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if password is not None:
            user.set_password(password)

        db.session.commit()
        db.session.refresh(user)
        logger.info("User ID: %s updated successfully.", user.id)
        return user

    @staticmethod
    def delete_user(user: User) -> None:
        """
        Deletes a user from the database.

        Args:
            user (User): The User object to delete.
        """
        logger.debug("Deleting user ID: %s", user.id)
        db.session.delete(user)
        db.session.commit()
        logger.info("User ID: %s deleted successfully.", user.id)
