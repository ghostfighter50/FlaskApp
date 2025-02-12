import logging
from flask import Blueprint
from ..controllers.course_controller import CourseController

logger = logging.getLogger(__name__)

course_bp = Blueprint('courses', __name__, url_prefix='/courses')

course_controller = CourseController()

course_bp.route('/', methods=['GET'])(course_controller.list_courses)
course_bp.route('/<string:course_id>', methods=['GET'])(course_controller.get_course)
course_bp.route('/search', methods=['GET'])(course_controller.search_courses)
course_bp.route('/<string:course_id>/students', methods=['GET'])(course_controller.list_students_in_course)
course_bp.route('/', methods=['POST'])(course_controller.create_course)
course_bp.route('/<string:course_id>', methods=['PUT'])(course_controller.update_course)
course_bp.route('/<string:course_id>', methods=['DELETE'])(course_controller.delete_course)
course_bp.route('/join', methods=['POST'])(course_controller.join_course)
course_bp.route('/leave', methods=['POST'])(course_controller.leave_course)

logger.debug("Course routes have been registered.")
