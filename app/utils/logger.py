import logging
import os
from flask import Flask
from logging.handlers import RotatingFileHandler

def configure_logging(app: Flask) -> None:
    """
    Configures logging for the Flask app.
    Sets up console and file handlers with appropriate log levels and formats.
    """
    log_level = app.config.get("LOG_LEVEL", "DEBUG").upper()

    # Create a logger for this app
    app_logger = logging.getLogger(app.name)
    app_logger.setLevel(log_level)

    # Define a formatter
    formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s() - %(msg)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Or log_level
    console_handler.setFormatter(formatter)
    app_logger.addHandler(console_handler)

    # File Handler
    log_dir = os.path.join(app.root_path, "logs")
    os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "app.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    app_logger.addHandler(file_handler)

    app_logger.info("Logging has been configured via configure_logging.")

# Optional: also define get_logger if you want module-specific loggers
def get_logger(module_name: str) -> logging.Logger:
    return logging.getLogger(module_name)
