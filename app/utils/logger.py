import logging
import os
from flask import Flask
from logging.handlers import RotatingFileHandler


def configure_logging(app: Flask) -> None:
    """
    This function sets up logging for the Flask application by configuring both console and file handlers.
    It ensures that log messages are formatted consistently and handles log rotation for file logs.

    Args:
        app (Flask): The Flask application instance for which logging is being configured.

    Raises:
        OSError: If the log directory cannot be created or the file handler cannot be set up.

    Notes:
        - The log level is determined by the "LOG_LEVEL" configuration value, defaulting to "DEBUG".
        - The log directory is determined by the "LOG_DIR" configuration value, defaulting to a "logs" directory within the app's root path.
        - Console logs are set to INFO level by default, but this can be adjusted.
        - File logs are set to DEBUG level and are rotated when they reach 5 MB, with up to 5 backup files kept.
    """
    log_level = app.config.get("LOG_LEVEL", "DEBUG").upper()
    log_dir = app.config.get("LOG_DIR", os.path.join(app.root_path, "logs"))

    app_logger = logging.getLogger(app.name)
    app_logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s() - %(message)s"
    )

    # Remove existing handlers to avoid duplicate logs
    if app_logger.hasHandlers():
        app_logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    app_logger.addHandler(console_handler)

    # File Handler: logs to a file with rotation
    try:
        os.makedirs(log_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, "app.log"),
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        app_logger.addHandler(file_handler)
    except OSError as e:
        app_logger.error(f"Failed to create log directory or file handler: {e}")

    app_logger.info("Logging has been configured via configure_logging.")
