import logging
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    """
    Registers global error handlers with the Flask app.
    Provides custom JSON responses for different HTTP error codes
    and ensures that all errors are consistently logged.

    Args:
        app (Flask): The Flask application instance.
    """

    @app.errorhandler(400)
    def bad_request(error: Exception) -> tuple:
        """
        Handles 400 Bad Request errors.
        Returns a JSON response indicating a bad request.

        Args:
            error (Exception): The exception raised.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        logger.error(f"400 Bad Request: {str(error)}")
        response = {
            'msg': 'Bad Request',
            'details': str(error)
        }
        return jsonify(response), 400

    @app.errorhandler(401)
    def unauthorized(error: Exception) -> tuple:
        """
        Handles 401 Unauthorized errors.
        Returns a JSON response indicating unauthorized access.

        Args:
            error (Exception): The exception raised.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        logger.error(f"401 Unauthorized: {str(error)}")
        response = {
            'msg': 'Unauthorized',
            'details': str(error)
        }
        return jsonify(response), 401

    @app.errorhandler(403)
    def forbidden(error: Exception) -> tuple:
        """
        Handles 403 Forbidden errors.
        Returns a JSON response indicating forbidden access.

        Args:
            error (Exception): The exception raised.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        logger.error(f"403 Forbidden: {str(error)}")
        response = {
            'msg': 'Forbidden',
            'details': str(error)
        }
        return jsonify(response), 403

    @app.errorhandler(404)
    def not_found(error: Exception) -> tuple:
        """
        Handles 404 Not Found errors.
        Returns a JSON response indicating that the requested resource was not found.

        Args:
            error (Exception): The exception raised.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        logger.error(f"404 Not Found: {str(error)}")
        response = {
            'msg': 'Not Found',
            'details': str(error)
        }
        return jsonify(response), 404

    @app.errorhandler(405)
    def method_not_allowed(error: Exception) -> tuple:
        """
        Handles 405 Method Not Allowed errors.
        Returns a JSON response indicating that the HTTP method is not allowed.

        Args:
            error (Exception): The exception raised.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        logger.error(f"405 Method Not Allowed: {str(error)}")
        response = {
            'msg': 'Method Not Allowed',
            'details': str(error)
        }
        return jsonify(response), 405

    @app.errorhandler(409)
    def conflict(error: Exception) -> tuple:
        """
        Handles 409 Conflict errors.
        Returns a JSON response indicating a conflict occurred.

        Args:
            error (Exception): The exception raised.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        logger.error(f"409 Conflict: {str(error)}")
        response = {
            'msg': 'Conflict',
            'details': str(error)
        }
        return jsonify(response), 409

    @app.errorhandler(422)
    def unprocessable_entity(error: Exception) -> tuple:
        """
        Handles 422 Unprocessable Entity errors.
        Returns a JSON response indicating that the server understands the content type
        and syntax of the request entity but was unable to process the contained instructions.

        Args:
            error (Exception): The exception raised.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        logger.error(f"422 Unprocessable Entity: {str(error)}")
        response = {
            'msg': 'Unprocessable Entity',
            'details': str(error)
        }
        return jsonify(response), 422

    @app.errorhandler(500)
    def internal_server_error(error: Exception) -> tuple:
        """
        Handles 500 Internal Server Error.
        Returns a JSON response indicating that an unexpected error occurred on the server.

        Args:
            error (Exception): The exception raised.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        logger.error(f"500 Internal Server Error: {str(error)}", exc_info=True)
        response = {
            'msg': 'Internal Server Error',
            'details': 'An unexpected error occurred.'
        }
        return jsonify(response), 500

    @app.errorhandler(Exception)
    def handle_exception(error: Exception) -> tuple:
        """
        Handles all uncaught exceptions.
        Returns a JSON response indicating that an error occurred.

        Args:
            error (Exception): The exception raised.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        if isinstance(error, HTTPException):
            logger.error(f"{error.code} {error.name}: {error.description}")
            response = {
                'msg': error.name,
                'details': error.description
            }
            return jsonify(response), error.code
        else:
            logger.error(f"Unhandled Exception: {str(error)}", exc_info=True)
            response = {
                'msg': 'An error occurred.',
                'details': str(error)
            }
            return jsonify(response), 500
