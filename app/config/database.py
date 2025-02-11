import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()
logger = logging.getLogger(__name__)


def initialize_database() -> bool:
    """
    Initializes the database by checking if MySQL is running and can be connected to.

    This function attempts to establish a connection to the database and logs the result.

    Returns:
        bool: True if the connection was successful, False if an error occurred.
    """
    try:
        # Attempt to connect to the database
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Database connection successful!")
        return True

    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy error: {str(e)}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return False
