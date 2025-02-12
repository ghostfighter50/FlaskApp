from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_cors import CORS
from .config.database import db, initialize_database
from .utils.logger import configure_logging
from .middlewares.auth_middleware import register_auth_middleware
from .middlewares.error_middleware import register_error_handlers


def create_app() -> Flask:
    """
    Initialise et configure l'application Flask.

    Returns:
        Flask: L'instance de l'application Flask configurée.
    """
    app = Flask(__name__)
    app.config.from_object('app.config.config.Config')

    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    configure_logging(app)

    @app.before_request
    def log_request_info():
        from flask import request
        print('Method: %s', request.method)
        print('Headers: %s', request.headers)
        print('Body: %s', request.get_data())

    @app.after_request
    def options(response):
        print('Response: %s', response)
        if response.status_code == 308:
            response.status_code = 200
        return response

    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["2000 per day", "500 per hour"],
        storage_uri="memory://",
    )
    limiter.init_app(app)

    db.init_app(app)

    Talisman(app, force_https=False)

    register_auth_middleware(app)
    register_error_handlers(app)

    with app.app_context():
        if initialize_database():
            app.logger.info("MySQL is connected!")
        else:
            app.logger.error("MySQL connection failed!")

    from .routes.auth_route import auth_bp
    from .routes.course_route import course_bp
    from .routes.user_route import user_bp
    from .routes.grade_route import grade_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(user_bp, url_prefix='/api/v1/users')
    app.register_blueprint(course_bp, url_prefix='/api/v1/courses')
    app.register_blueprint(grade_bp, url_prefix='/api/v1/grades')

    return app
