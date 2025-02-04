from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config.database import db, initialize_database
from .utils.logger import configure_logging
from .middlewares.auth_middleware import register_auth_middleware
from .middlewares.error_middleware import register_error_handlers
from flask_talisman import Talisman


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('app.config.config.Config')

    configure_logging(app)

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
