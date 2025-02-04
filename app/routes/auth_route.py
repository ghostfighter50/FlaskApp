import logging
from flask import Blueprint
from ..controllers.auth_controller import AuthController

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_controller = AuthController()

auth_bp.route('/register', methods=['POST'])(auth_controller.register)
auth_bp.route('/login', methods=['POST'])(auth_controller.login)
auth_bp.route('/change-password', methods=['POST'])(auth_controller.change_password)

logger.debug("Authentication routes have been registered.")
