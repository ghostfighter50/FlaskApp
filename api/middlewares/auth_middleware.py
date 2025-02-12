import logging
from flask_jwt_extended import JWTManager
from flask import Flask, jsonify
from typing import Any, Dict

logger = logging.getLogger(__name__)

jwt = JWTManager()


def register_auth_middleware(app: Flask) -> None:
    """
    Registers the JWT authentication middleware with the Flask app.
    Sets up custom responses for JWT-related errors to ensure consistent
    error handling and logging across the application.

    Args:
        app (Flask): The Flask application instance.
    """
    jwt.init_app(app)
    logger.debug("JWT Manager initialized and attached to the Flask app.")

    @jwt.unauthorized_loader
    def unauthorized_response(callback: Any) -> tuple:
        """
        Handler for requests missing the Authorization header.
        Returns a JSON response indicating that the Authorization header is missing.

        Args:
            callback (Any): The callback function.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        logger.warning("Unauthorized access attempt: Missing Authorization Header.")
        response = {
            'msg': 'Missing Authorization Header.'
        }
        return jsonify(response), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(callback: Any) -> tuple:
        """
        Handler for requests with invalid JWT tokens.
        Returns a JSON response indicating that the token provided is invalid.

        Args:
            callback (Any): The callback function.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        logger.warning("Invalid JWT token received.")
        response = {
            'msg': 'Invalid token.'
        }
        return jsonify(response), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header: Dict[str, Any], jwt_payload: Dict[str, Any]) -> tuple:
        """
        Handler for requests with expired JWT tokens.
        Returns a JSON response indicating that the token has expired.

        Args:
            jwt_header (Dict[str, Any]): The JWT header.
            jwt_payload (Dict[str, Any]): The JWT payload.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        logger.warning("Expired JWT token received.")
        response = {
            'msg': 'Token has expired.'
        }
        return jsonify(response), 401

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(jwt_header: Dict[str, Any], jwt_payload: Dict[str, Any]) -> tuple:
        """
        Handler for requests requiring a fresh JWT token.
        Returns a JSON response indicating that a fresh token is needed.

        Args:
            jwt_header (Dict[str, Any]): The JWT header.
            jwt_payload (Dict[str, Any]): The JWT payload.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        logger.warning("Fresh JWT token required.")
        response = {
            'msg': 'Fresh token required.'
        }
        return jsonify(response), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header: Dict[str, Any], jwt_payload: Dict[str, Any]) -> tuple:
        """
        Handler for requests with revoked JWT tokens.
        Returns a JSON response indicating that the token has been revoked.

        Args:
            jwt_header (Dict[str, Any]): The JWT header.
            jwt_payload (Dict[str, Any]): The JWT payload.

        Returns:
            tuple: A tuple containing the JSON response and HTTP status code.
        """
        logger.warning("Revoked JWT token received.")
        response = {
            'msg': 'Token has been revoked.'
        }
        return jsonify(response), 401
