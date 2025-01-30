from flask import Flask
from .config.database import db, initialize_database
from .utils.logger import configure_logging
from .middlewares.auth_middleware import register_auth_middleware
from .middlewares.error_middleware import register_error_handlers

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('app.config.config.Config')
    
    configure_logging(app)
    
    db.init_app(app)
    
    register_auth_middleware(app)
    register_error_handlers(app)
    
    with app.app_context():
        if initialize_database():
            app.logger.info("MySQL is connected!")
        else:
            app.logger.error("MySQL connection failed!")
    
    # Register blueprints with versioning
    from .routes.auth_route import auth_bp
    from .routes.user_route import user_bp
    from .routes.course_route import course_bp
    from .routes.grade_route import grade_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(user_bp, url_prefix='/api/v1/users')
    app.register_blueprint(course_bp, url_prefix='/api/v1/courses')
    app.register_blueprint(grade_bp, url_prefix='/api/v1/grades')
    
    return app