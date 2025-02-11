import logging
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.serializer import serialize_grade
from ..services.grade_service import GradeService
from ..services.user_service import UserService
from ..services.course_service import CourseService

logger = logging.getLogger(__name__)


class GradeController:
    """
    Controller for handling grade-related operations:
    - List grades
    - Get a specific grade
    - Assign/update/delete a grade
    - Get all grades for a specific student in a course
    """

    def __init__(self):
        self.grade_service = GradeService()
        self.user_service = UserService()
        self.course_service = CourseService()

    @jwt_required()
    def list_grades(self):
        """List all grades (only professors/admins)."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        # Only allow professors or admins to list grades
        if current_user.role not in ["Professor", "Administrator"]:
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({"msg": "Unauthorized access."}), 403

        try:
            all_grades = self.grade_service.list_grades()
            serialized = [serialize_grade(g) for g in all_grades]
            return jsonify({"grades": serialized}), 200
        except Exception as e:
            logger.error(f"Error listing grades: {str(e)}", exc_info=True)
            return jsonify({"msg": "An error occurred while listing grades."}), 500

    @jwt_required()
    def get_grade(self, grade_id):
        """Retrieve a specific grade by ID."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        grade = self.grade_service.get_grade_by_id(grade_id)
        if not grade:
            logger.warning(f"Grade not found: ID {grade_id}")
            return jsonify({"msg": "Grade not found."}), 404

        # Students cannot fetch grades
        if current_user.role == "Student":
            logger.warning(f"Unauthorized grade access attempt by user ID: {current_user_id}")
            return jsonify({"msg": "Unauthorized access."}), 403

        grade_data = serialize_grade(grade)
        return jsonify({"grade": grade_data}), 200

    @jwt_required()
    def assign_grade(self):
        """Assign a grade to a student for a particular course."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        # Only professors or admins can assign a grade
        if current_user.role not in ["Professor", "Administrator"]:
            logger.warning(f"Unauthorized grade assignment attempt by user ID: {current_user_id}")
            return jsonify({"msg": "Unauthorized access."}), 403

        data = request.get_json() or {}
        if not all(k in data for k in ("course_id", "student_id", "grade", "grade_name")):
            logger.warning(f"Missing required fields in grade assignment: {data}")
            return jsonify({"msg": "All fields are required."}), 400

        course_id = data["course_id"]
        student_id = data["student_id"]
        grade_value = data["grade"]
        grade_name = data["grade_name"]

        try:
            course = self.course_service.get_course_by_id(course_id)
            student = self.user_service.get_user_by_id(student_id)
            if not course or not student:
                logger.warning(f"Course or student not found for grade assignment: course_id={course_id}, student_id={student_id}")
                return jsonify({"msg": "Course or student not found."}), 404

            new_grade = self.grade_service.assign_grade(student_id, course_id, grade_value, grade_name)
            grade_data = serialize_grade(new_grade)
            return jsonify({"msg": "Grade assigned successfully.", "grade": grade_data}), 200
        except Exception as e:
            logger.error(f"Error assigning grade: {str(e)}", exc_info=True)
            return jsonify({"msg": "An error occurred while assigning the grade."}), 500

    @jwt_required()
    def update_grade(self, grade_id):
        """Update an existing grade."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        # Only professors or admins can update a grade
        if current_user.role not in ["Professor", "Administrator"]:
            logger.warning(f"Unauthorized grade update attempt by user ID: {current_user_id}")
            return jsonify({"msg": "Unauthorized access."}), 403

        grade_obj = self.grade_service.get_grade_by_id(grade_id)
        if not grade_obj:
            logger.warning(f"Grade not found: ID {grade_id}")
            return jsonify({"msg": "Grade not found."}), 404

        data = request.get_json() or {}
        if "grade" not in data:
            logger.warning(f"Missing grade value for update: {data}")
            return jsonify({"msg": "Grade value is required."}), 400

        new_grade_value = data["grade"]

        try:
            updated = self.grade_service.update_grade(grade_obj, new_grade_value)
            grade_data = serialize_grade(updated)
            return jsonify({"msg": "Grade updated successfully.", "grade": grade_data}), 200
        except Exception as e:
            logger.error(f"Error updating grade ID {grade_id}: {str(e)}", exc_info=True)
            return jsonify({"msg": "An error occurred while updating the grade."}), 500

    @jwt_required()
    def delete_grade(self, grade_id):
        """Delete a grade (only admins)."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        if current_user.role != "Administrator":
            logger.warning(f"Unauthorized grade deletion attempt by user ID: {current_user_id}")
            return jsonify({"msg": "Unauthorized access."}), 403

        grade_obj = self.grade_service.get_grade_by_id(grade_id)
        if not grade_obj:
            logger.warning(f"Grade not found: ID {grade_id}")
            return jsonify({"msg": "Grade not found."}), 404

        try:
            self.grade_service.delete_grade(grade_obj)
            return jsonify({"msg": "Grade deleted successfully."}), 200
        except Exception as e:
            logger.error(f"Error deleting grade ID {grade_id}: {str(e)}", exc_info=True)
            return jsonify({"msg": "An error occurred while deleting the grade."}), 500

    @jwt_required()
    def get_student_grades(self, course_id, student_id):
        """Retrieve all grades for a student in a specific course."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        if current_user.role not in ["Professor", "Administrator"]:
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({"msg": "Unauthorized access."}), 403

        try:
            course = self.course_service.get_course_by_id(course_id)
            student = self.user_service.get_user_by_id(student_id)
            if not course or not student:
                logger.warning(f"Course or student not found: course_id={course_id}, student_id={student_id}")
                return jsonify({"msg": "Course or student not found."}), 404

            grades = self.grade_service.get_student_grades(course_id, student_id)
            serialized = [serialize_grade(g) for g in grades]
            return jsonify({"grades": serialized}), 200
        except Exception as e:
            logger.error(f"Error retrieving student grades: {str(e)}", exc_info=True)
            return jsonify({"msg": "An error occurred while retrieving grades."}), 500
