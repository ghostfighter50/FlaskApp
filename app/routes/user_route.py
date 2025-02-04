import logging
from flask import Blueprint
from ..controllers.user_controller import UserController

logger = logging.getLogger(__name__)

user_bp = Blueprint('users', __name__, url_prefix='/users')

user_controller = UserController()

user_bp.route('/', methods=['GET'])(user_controller.list_users)
user_bp.route('/<string:user_id>', methods=['GET'])(user_controller.get_user)
user_bp.route('/search', methods=['GET'])(user_controller.search_users)
user_bp.route('/', methods=['POST'])(user_controller.create_user)
user_bp.route('/<string:user_id>', methods=['PUT'])(user_controller.update_user)
user_bp.route('/<string:user_id>', methods=['DELETE'])(user_controller.delete_user)

logger.debug("User routes have been registered.")