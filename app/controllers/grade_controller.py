# app/controllers/grade_controller.py

import logging
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from typing import Any, Tuple
from ..services.grade_service import GradeService
from ..services.course_service import CourseService
from ..services.user_service import UserService

logger = logging.getLogger(__name__)

class GradeController:
    """
    Controller for handling grade management operations such as
    listing grades, retrieving grade details, assigning, updating,
    and deleting grades.
    """

    def __init__(self):
        self.grade_service = GradeService()
        self.course_service = CourseService()
        self.user_service = UserService()

    @jwt_required()
    def list_grades(self) -> Tuple[Any, int]:
        """Retrieve a list of all grades."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        if current_user.role not in ['Administrator', 'Professor']:
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        try:
            grades = self.grade_service.get_all_grades()
            grades_data = [self.grade_service.serialize_grade(grade) for grade in grades]
            return jsonify({'grades': grades_data}), 200
        except Exception as e:
            logger.error(f"Error listing grades: {str(e)}")
            return jsonify({'msg': 'An error occurred while listing grades.'}), 500

    @jwt_required()
    def get_grade(self, grade_id: str) -> Tuple[Any, int]:
        """Retrieve details of a specific grade by its ID."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        grade = self.grade_service.get_grade_by_id(grade_id)
        if not grade:
            logger.warning(f"Grade not found: ID {grade_id}")
            return jsonify({'msg': 'Grade not found.'}), 404

        if grade.student_id != current_user_id and current_user.role not in ['Administrator', 'Professor']:
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        grade_data = self.grade_service.serialize_grade(grade)
        return jsonify({'grade': grade_data}), 200

    @jwt_required()
    def assign_grade(self) -> Tuple[Any, int]:
        """Assign a grade to a student for a specific course."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        if current_user.role not in ['Administrator', 'Professor']:
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        data = request.get_json()
        course_id = data.get('course_id', '').strip()
        student_id = data.get('student_id', '').strip()
        grade_value = data.get('grade', None)

        if not all([course_id, student_id, grade_value is not None]):
            logger.warning("Grade assignment failed: Missing fields.")
            return jsonify({'msg': 'All fields are required.'}), 400

        course = self.course_service.get_course_by_id(course_id)
        student = self.user_service.get_user_by_id(student_id)

        if not course or not student:
            logger.warning(f"Grade assignment failed: Course ID {course_id} or Student ID {student_id} not found.")
            return jsonify({'msg': 'Course or student not found.'}), 404

        if student.role != 'Student':
            logger.warning(f"Grade assignment failed: User ID {student_id} is not a student.")
            return jsonify({'msg': 'User is not a student.'}), 400

        try:
            grade = self.grade_service.assign_grade(course_id, student_id, grade_value)
            grade_data = self.grade_service.serialize_grade(grade)
            return jsonify({'msg': 'Grade assigned successfully.', 'grade': grade_data}), 200
        except Exception as e:
            logger.error(f"Error assigning grade: {str(e)}")
            return jsonify({'msg': 'An error occurred while assigning the grade.'}), 500

    @jwt_required()
    def update_grade(self, grade_id: str) -> Tuple[Any, int]:
        """Update the value of an existing grade."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        if current_user.role not in ['Administrator', 'Professor']:
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        grade = self.grade_service.get_grade_by_id(grade_id)
        if not grade:
            logger.warning(f"Grade not found: ID {grade_id}")
            return jsonify({'msg': 'Grade not found.'}), 404

        data = request.get_json()
        grade_value = data.get('grade', None)

        if grade_value is None:
            logger.warning("Grade update failed: Missing grade value.")
            return jsonify({'msg': 'Grade value is required.'}), 400

        try:
            updated_grade = self.grade_service.update_grade(grade, grade_value)
            grade_data = self.grade_service.serialize_grade(updated_grade)
            return jsonify({'msg': 'Grade updated successfully.', 'grade': grade_data}), 200
        except Exception as e:
            logger.error(f"Error updating grade ID: {grade_id} - {str(e)}")
            return jsonify({'msg': 'An error occurred while updating the grade.'}), 500

    @jwt_required()
    def delete_grade(self, grade_id: str) -> Tuple[Any, int]:
        """Delete an existing grade."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        if current_user.role != 'Administrator':
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        grade = self.grade_service.get_grade_by_id(grade_id)
        if not grade:
            logger.warning(f"Grade not found: ID {grade_id}")
            return jsonify({'msg': 'Grade not found.'}), 404

        try:
            self.grade_service.delete_grade(grade)
            return jsonify({'msg': 'Grade deleted successfully.'}), 200
        except Exception as e:
            logger.error(f"Error deleting grade ID: {grade_id} - {str(e)}")
            return jsonify({'msg': 'An error occurred while deleting the grade.'}), 500

    @jwt_required()
    def get_student_grades(self, course_id: str, student_id: str) -> Tuple[Any, int]:
        """Retrieve all grades for a specific student within a specific course."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        course = self.course_service.get_course_by_id(course_id)
        student = self.user_service.get_user_by_id(student_id)

        if not course or not student:
            logger.warning(f"Course ID {course_id} or Student ID {student_id} not found.")
            return jsonify({'msg': 'Course or student not found.'}), 404

        if student.role != 'Student':
            logger.warning(f"User ID {student_id} is not a student.")
            return jsonify({'msg': 'User is not a student.'}), 400

        if current_user.role not in ['Administrator', 'Professor'] and current_user.id != student_id:
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        try:
            grades = self.grade_service.get_grades_by_course_and_student(course_id, student_id)
            grades_data = [self.grade_service.serialize_grade(grade) for grade in grades]
            return jsonify({'grades': grades_data}), 200
        except Exception as e:
            logger.error(f"Error retrieving grades: {str(e)}")
            return jsonify({'msg': 'An error occurred while retrieving grades.'}), 500