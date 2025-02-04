import logging
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from typing import Any, Tuple, Optional, Dict

from app.utils.serializer import serialize_course, serialize_user
from ..services.course_service import CourseService
from ..services.user_service import UserService

logger = logging.getLogger(__name__)


class CourseController:
    """
    Controller for managing course operations such as listing, searching,
    creating, updating, deleting courses and handling student enrollments.
    """

    def __init__(self) -> None:
        """
        Initialize CourseController with required services.
        """
        self.course_service: CourseService = CourseService()
        self.user_service: UserService = UserService()

    @jwt_required()
    def list_courses(self) -> Tuple[Any, int]:
        """
        Retrieve a paginated list of courses.

        Query parameters:
          - page (int): Current page number (default is 1)
          - per_page (int): Number of courses per page (default is 10)

        Returns:
            Tuple[Dict[str, Any], int]: A tuple with a JSON response containing course data and pagination info.
        """
        page: int = request.args.get('page', 1, type=int)
        per_page: int = request.args.get('per_page', 10, type=int)
        logger.info(f"Listing courses - Page: {page}, Per Page: {per_page}")

        try:
            courses, pagination = self.course_service.get_all_courses_paginated(page, per_page)
            courses_data = [serialize_course(course) for course in courses]
            response: Dict[str, Any] = {
                'courses': courses_data,
                'pagination': {
                    'page': pagination.page,
                    'per_page': pagination.per_page,
                    'total_pages': pagination.pages,
                    'total_items': pagination.total
                }
            }
            return jsonify(response), 200

        except Exception as e:
            logger.error(f"Error listing courses: {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while listing courses.'}), 500

    @jwt_required()
    def get_course(self, course_id: str) -> Tuple[Any, int]:
        """
        Retrieve details of a specific course by its ID.

        Args:
            course_id (str): The unique identifier of the course.

        Returns:
            Tuple[Dict[str, Any], int]: Course details or an error message.
        """
        logger.info(f"Retrieving course with ID: {course_id}")
        try:
            course = self.course_service.get_course_by_id(course_id)
            if not course:
                logger.warning(f"Course not found: ID {course_id}")
                return jsonify({'msg': 'Course not found.'}), 404

            return jsonify({'course': serialize_course(course)}), 200

        except Exception as e:
            logger.error(f"Error retrieving course: {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while retrieving the course.'}), 500

    @jwt_required()
    def search_courses(self) -> Tuple[Any, int]:
        """
        Search for courses based on a partial name query.

        Query parameters:
          - name (str): The search string to match course names.

        Returns:
            Tuple[Dict[str, Any], int]: A list of matching courses.
        """
        name_query: str = request.args.get('name', '').strip()
        logger.info(f"Searching courses with query: '{name_query}'")

        try:
            courses = self.course_service.search_courses_by_name(name_query)
            courses_data = [serialize_course(course) for course in courses]
            return jsonify({'courses': courses_data}), 200

        except Exception as e:
            logger.error(f"Error searching courses: {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while searching courses.'}), 500

    @jwt_required()
    def list_students_in_course(self, course_id: str) -> Tuple[Any, int]:
        """
        List all students enrolled in a specific course.

        Accessible only by Administrators or Professors.

        Args:
            course_id (str): The unique identifier of the course.

        Returns:
            Tuple[Dict[str, Any], int]: A list of students or an error message.
        """
        current_user_id: Optional[str] = get_jwt_identity()
        if not current_user_id:
            logger.warning("JWT identity not found.")
            return jsonify({'msg': 'Unauthorized, token missing or invalid.'}), 401

        current_user = self.user_service.get_user_by_id(current_user_id)
        if not current_user:
            logger.warning(f"User not found for ID: {current_user_id}")
            return jsonify({'msg': 'User not found.'}), 404

        if current_user.role not in ['Administrator', 'Professor']:
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        try:
            course = self.course_service.get_course_by_id(course_id)
            if not course:
                logger.warning(f"Course not found: ID {course_id}")
                return jsonify({'msg': 'Course not found.'}), 404

            students = self.course_service.get_students_in_course(course_id)
            students_data = [serialize_user(enrollment.student) for enrollment in students]
            return jsonify({'students': students_data}), 200

        except Exception as e:
            logger.error(f"Error listing students for course {course_id}: {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while listing students.'}), 500

    @jwt_required()
    def create_course(self) -> Tuple[Any, int]:
        """
        Create a new course.

        Only Administrators or Professors are allowed to create courses.

        Expected JSON payload:
          { "name": "<course_name>" }

        Returns:
            Tuple[Dict[str, Any], int]: The created course information or an error message.
        """
        current_user_id: Optional[str] = get_jwt_identity()
        if not current_user_id:
            logger.warning("JWT identity not found.")
            return jsonify({'msg': 'Unauthorized, token missing or invalid.'}), 401

        current_user = self.user_service.get_user_by_id(current_user_id)
        if not current_user:
            logger.warning(f"User not found for ID: {current_user_id}")
            return jsonify({'msg': 'User not found.'}), 404

        if current_user.role not in ['Administrator', 'Professor']:
            logger.warning(f"Unauthorized course creation attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        data: Optional[Dict[str, Any]] = request.get_json()
        name: str = data.get('name', '').strip() if data else ''
        if not name:
            logger.warning("Course creation failed: Missing course name.")
            return jsonify({'msg': 'Course name is required.'}), 400

        try:
            course = self.course_service.create_course(name, current_user.id)
            logger.info(f"Course created successfully with ID: {course.id}")
            return jsonify({
                'msg': 'Course created successfully.',
                'course': serialize_course(course)
            }), 200

        except Exception as e:
            logger.error(f"Error creating course: {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while creating the course.'}), 500

    @jwt_required()
    def update_course(self, course_id: str) -> Tuple[Any, int]:
        """
        Update an existing course's name.

        Only Administrators or the assigned Professor can update a course.

        Expected JSON payload:
          { "name": "<new_course_name>" }

        Args:
            course_id (str): The unique identifier of the course.

        Returns:
            Tuple[Dict[str, Any], int]: The updated course data or an error message.
        """
        current_user_id: Optional[str] = get_jwt_identity()
        if not current_user_id:
            logger.warning("JWT identity not found.")
            return jsonify({'msg': 'Unauthorized, token missing or invalid.'}), 401

        current_user = self.user_service.get_user_by_id(current_user_id)
        if not current_user:
            logger.warning(f"User not found for ID: {current_user_id}")
            return jsonify({'msg': 'User not found.'}), 404

        try:
            course = self.course_service.get_course_by_id(course_id)
            if not course:
                logger.warning(f"Course not found: ID {course_id}")
                return jsonify({'msg': 'Course not found.'}), 404

            # Only Administrators or the assigned Professor can update the course.
            if current_user.role not in ['Administrator', 'Professor'] and course.professor_id != current_user.id:
                logger.warning(f"Unauthorized course update attempt by user ID: {current_user_id}")
                return jsonify({'msg': 'Unauthorized access.'}), 403

            data: Optional[Dict[str, Any]] = request.get_json()
            name: str = data.get('name', '').strip() if data else ''
            if not name:
                logger.warning("Course update failed: Missing course name.")
                return jsonify({'msg': 'Course name is required.'}), 400

            updated_course = self.course_service.update_course(course, name)
            logger.info(f"Course updated successfully with ID: {course_id}")
            return jsonify({
                'msg': 'Course updated successfully.',
                'course': serialize_course(updated_course)
            }), 200

        except Exception as e:
            logger.error(f"Error updating course {course_id}: {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while updating the course.'}), 500

    @jwt_required()
    def delete_course(self, course_id: str) -> Tuple[Any, int]:
        """
        Delete an existing course.

        Only Administrators can delete courses.

        Args:
            course_id (str): The unique identifier of the course.

        Returns:
            Tuple[Dict[str, Any], int]: A success message or an error message.
        """
        current_user_id: Optional[str] = get_jwt_identity()
        if not current_user_id:
            logger.warning("JWT identity not found.")
            return jsonify({'msg': 'Unauthorized, token missing or invalid.'}), 401

        current_user = self.user_service.get_user_by_id(current_user_id)
        if not current_user:
            logger.warning(f"User not found for ID: {current_user_id}")
            return jsonify({'msg': 'User not found.'}), 404

        if current_user.role != 'Administrator':
            logger.warning(f"Unauthorized course deletion attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        try:
            course = self.course_service.get_course_by_id(course_id)
            if not course:
                logger.warning(f"Course not found: ID {course_id}")
                return jsonify({'msg': 'Course not found.'}), 404

            self.course_service.delete_course(course)
            logger.info(f"Course deleted successfully with ID: {course_id}")
            return jsonify({'msg': 'Course deleted successfully.'}), 200

        except Exception as e:
            logger.error(f"Error deleting course {course_id}: {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while deleting the course.'}), 500

    @jwt_required()
    def join_course(self) -> Tuple[Any, int]:
        """
        Enroll a student into a course.

        Only students can enroll in courses.

        Expected JSON payload:
          { "course_id": "<course_id>" }

        Returns:
            Tuple[Dict[str, Any], int]: A success message or an error message.
        """
        current_user_id: Optional[str] = get_jwt_identity()
        if not current_user_id:
            logger.warning("JWT identity not found.")
            return jsonify({'msg': 'Unauthorized, token missing or invalid.'}), 401

        current_user = self.user_service.get_user_by_id(current_user_id)
        if not current_user:
            logger.warning(f"User not found for ID: {current_user_id}")
            return jsonify({'msg': 'User not found.'}), 404

        if current_user.role != 'Student':
            logger.warning(f"Non-student user ID: {current_user_id} attempted to join a course.")
            return jsonify({'msg': 'Only students can join courses.'}), 403

        data: Optional[Dict[str, Any]] = request.get_json()
        course_id: str = data.get('course_id', '').strip() if data else ''
        if not course_id:
            logger.warning("Join course failed: Missing course ID.")
            return jsonify({'msg': 'Course ID is required.'}), 400

        try:
            course = self.course_service.get_course_by_id(course_id)
            if not course:
                logger.warning(f"Join course failed: Course not found with ID {course_id}")
                return jsonify({'msg': 'Course not found.'}), 404

            enrollment = self.course_service.join_course(current_user.id, course_id)
            if not enrollment:
                logger.warning(f"User ID: {current_user_id} already enrolled in course ID: {course_id}")
                return jsonify({'msg': 'Already enrolled in this course.'}), 409

            logger.info(f"User ID: {current_user_id} enrolled in course ID: {course_id}")
            return jsonify({'msg': 'Joined course successfully.'}), 200

        except Exception as e:
            logger.error(f"Error joining course {course_id} by user {current_user_id}: {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while joining the course.'}), 500

    @jwt_required()
    def leave_course(self) -> Tuple[Any, int]:
        """
        Unenroll a student from a course.

        Only students can unenroll.

        Expected JSON payload:
          { "course_id": "<course_id>" }

        Returns:
            Tuple[Dict[str, Any], int]: A success message or an error message.
        """
        current_user_id: Optional[str] = get_jwt_identity()
        if not current_user_id:
            logger.warning("JWT identity not found.")
            return jsonify({'msg': 'Unauthorized, token missing or invalid.'}), 401

        current_user = self.user_service.get_user_by_id(current_user_id)
        if not current_user:
            logger.warning(f"User not found for ID: {current_user_id}")
            return jsonify({'msg': 'User not found.'}), 404

        if current_user.role != 'Student':
            logger.warning(f"Non-student user ID: {current_user_id} attempted to leave a course.")
            return jsonify({'msg': 'Only students can leave courses.'}), 403

        data: Optional[Dict[str, Any]] = request.get_json()
        course_id: str = data.get('course_id', '').strip() if data else ''
        if not course_id:
            logger.warning("Leave course failed: Missing course ID.")
            return jsonify({'msg': 'Course ID is required.'}), 400

        try:
            enrollment = self.course_service.leave_course(current_user.id, course_id)
            if not enrollment:
                logger.warning(f"User ID: {current_user_id} is not enrolled in course ID: {course_id}")
                return jsonify({'msg': 'Not enrolled in this course.'}), 404

            logger.info(f"User ID: {current_user_id} left course ID: {course_id}")
            return jsonify({'msg': 'Left course successfully.'}), 200

        except Exception as e:
            logger.error(f"Error leaving course {course_id} by user {current_user_id}: {str(e)}", exc_info=True)
            return jsonify({'msg': 'An error occurred while leaving the course.'}), 500
