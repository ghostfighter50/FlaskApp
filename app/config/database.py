# app/config/database.py

import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()
logger = logging.getLogger(__name__)

def initialize_database():
    """
    Initializes the database by checking if MySQL is running.
    """
    try:
        with db.engine.connect() as connection:
            # Check Database Connection
            connection.execute(text("SELECT 1"))
            logger.info("Database connection successful!")
        return True

    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False
