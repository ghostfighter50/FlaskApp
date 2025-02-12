import logging
from flask import Blueprint
from ..controllers.grade_controller import GradeController

logger = logging.getLogger(__name__)

grade_bp = Blueprint('grades', __name__, url_prefix='/grades')

grade_controller = GradeController()

grade_bp.route('/', methods=['GET'])(grade_controller.list_grades)
grade_bp.route('/<string:grade_id>', methods=['GET'])(grade_controller.get_grade)
grade_bp.route('/', methods=['POST'])(grade_controller.assign_grade)
grade_bp.route('/<string:grade_id>', methods=['PUT'])(grade_controller.update_grade)
grade_bp.route('/<string:grade_id>', methods=['DELETE'])(grade_controller.delete_grade)
grade_bp.route('/courses/<string:course_id>/students/<string:student_id>/grades', methods=['GET'])(grade_controller.get_student_grades)

logger.debug("Grade routes have been registered.")
