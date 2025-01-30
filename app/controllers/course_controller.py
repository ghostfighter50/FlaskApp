import logging
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from typing import Any,  Tuple

from app.utils.serizializer import serialize_course
from ..services.course_service import CourseService
from ..services.user_service import UserService

logger = logging.getLogger(__name__)

class CourseController:
    """
    Controller for handling course management operations such as
    listing courses, retrieving course details, searching courses,
    managing enrollments, creating, updating, and deleting courses.
    """

    def __init__(self):
        self.course_service = CourseService()
        self.user_service = UserService()

    @jwt_required()
    def list_courses(self) -> Tuple[Any, int]:
        """Retrieve a paginated list of all courses."""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        logger.info(f"Listing courses - Page: {page}, Per Page: {per_page}")

        try:
            courses, pagination = self.course_service.get_all_courses_paginated(page, per_page)
            courses_data = [serialize_course(course) for course in courses]
            return jsonify({
                'courses': courses_data,
                'pagination': {
                    'page': pagination.page,
                    'per_page': pagination.per_page,
                    'total_pages': pagination.pages,
                    'total_items': pagination.total
                }
            }), 200
        except Exception as e:
            logger.error(f"Error listing courses: {str(e)}")
            return jsonify({'msg': 'An error occurred while listing courses.'}), 500

    @jwt_required()
    def get_course(self, course_id: str) -> Tuple[Any, int]:
        """Retrieve details of a specific course by its ID."""
        logger.info(f"Retrieving course ID: {course_id}")
        course = self.course_service.get_course_by_id(course_id)

        if not course:
            logger.warning(f"Course not found: ID {course_id}")
            return jsonify({'msg': 'Course not found.'}), 404

        course_data = serialize_course(course)
        return jsonify({'course': course_data}), 200

    @jwt_required()
    def search_courses(self) -> Tuple[Any, int]:
        """Search for courses based on a name query string."""
        name_query = request.args.get('name', '').strip()
        logger.info(f"Searching courses with name containing: '{name_query}'")

        try:
            courses = self.course_service.search_courses_by_name(name_query)
            courses_data = [serialize_course(course) for course in courses]
            return jsonify({'courses': courses_data}), 200
        except Exception as e:
            logger.error(f"Error searching courses: {str(e)}")
            return jsonify({'msg': 'An error occurred while searching courses.'}), 500

    @jwt_required()
    def list_students_in_course(self, course_id: str) -> Tuple[Any, int]:
        """List all students enrolled in a specific course."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        if current_user.role not in ['Administrator', 'Professor']:
            logger.warning(f"Unauthorized access attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        course = self.course_service.get_course_by_id(course_id)
        if not course:
            logger.warning(f"Course not found: ID {course_id}")
            return jsonify({'msg': 'Course not found.'}), 404

        try:
            students = self.course_service.get_students_in_course(course_id)
            students_data = [self.user_service.serialize_user(enrollment.student) for enrollment in students]
            return jsonify({'students': students_data}), 200
        except Exception as e:
            logger.error(f"Error listing students in course ID: {course_id} - {str(e)}")
            return jsonify({'msg': 'An error occurred while listing students.'}), 500

    @jwt_required()
    def create_course(self) -> Tuple[Any, int]:
        """Create a new course."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        if current_user.role not in ['Administrator', 'Professor']:
            logger.warning(f"Unauthorized course creation attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        data = request.get_json()
        name = data.get('name', '').strip()

        if not name:
            logger.warning("Course creation failed: Missing course name.")
            return jsonify({'msg': 'Course name is required.'}), 400

        try:
            course = self.course_service.create_course(name, current_user.id)
            course_data = serialize_course(course)
            return jsonify({'msg': 'Course created successfully.', 'course': course_data}), 200
        except Exception as e:
            logger.error(f"Error creating course: {str(e)}")
            return jsonify({'msg': 'An error occurred while creating the course.'}), 500

    @jwt_required()
    def update_course(self, course_id: str) -> Tuple[Any, int]:
        """Update the name of an existing course."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        course = self.course_service.get_course_by_id(course_id)
        if not course:
            logger.warning(f"Course not found: ID {course_id}")
            return jsonify({'msg': 'Course not found.'}), 404

        if current_user.role not in ['Administrator', 'Professor'] and course.professor_id != current_user.id:
            logger.warning(f"Unauthorized course update attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        data = request.get_json()
        name = data.get('name', '').strip()

        if not name:
            logger.warning("Course update failed: Missing course name.")
            return jsonify({'msg': 'Course name is required.'}), 400

        try:
            updated_course = self.course_service.update_course(course, name)
            course_data = serialize_course(updated_course)
            return jsonify({'msg': 'Course updated successfully.', 'course': course_data}), 200
        except Exception as e:
            logger.error(f"Error updating course ID: {course_id} - {str(e)}")
            return jsonify({'msg': 'An error occurred while updating the course.'}), 500

    @jwt_required()
    def delete_course(self, course_id: str) -> Tuple[Any, int]:
        """Delete an existing course."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        if current_user.role != 'Administrator':
            logger.warning(f"Unauthorized course deletion attempt by user ID: {current_user_id}")
            return jsonify({'msg': 'Unauthorized access.'}), 403

        course = self.course_service.get_course_by_id(course_id)
        if not course:
            logger.warning(f"Course not found: ID {course_id}")
            return jsonify({'msg': 'Course not found.'}), 404

        try:
            self.course_service.delete_course(course)
            return jsonify({'msg': 'Course deleted successfully.'}), 200
        except Exception as e:
            logger.error(f"Error deleting course ID: {course_id} - {str(e)}")
            return jsonify({'msg': 'An error occurred while deleting the course.'}), 500

    @jwt_required()
    def join_course(self) -> Tuple[Any, int]:
        """Allow a student to enroll in a course."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        if current_user.role != 'Student':
            logger.warning(f"Non-student user ID: {current_user_id} attempted to join a course.")
            return jsonify({'msg': 'Only students can join courses.'}), 403

        data = request.get_json()
        course_id = data.get('course_id', '').strip()

        if not course_id:
            logger.warning("Join course failed: Missing course ID.")
            return jsonify({'msg': 'Course ID is required.'}), 400

        course = self.course_service.get_course_by_id(course_id)
        if not course:
            logger.warning(f"Join course failed: Course not found with ID {course_id}")
            return jsonify({'msg': 'Course not found.'}), 404

        try:
            enrollment = self.course_service.join_course(current_user.id, course_id)
            if not enrollment:
                logger.warning(f"User ID: {current_user_id} already enrolled in course ID: {course_id}")
                return jsonify({'msg': 'Already enrolled in this course.'}), 409

            return jsonify({'msg': 'Joined course successfully.'}), 200
        except Exception as e:
            logger.error(f"Error joining course ID: {course_id} by user ID: {current_user_id} - {str(e)}")
            return jsonify({'msg': 'An error occurred while joining the course.'}), 500

    @jwt_required()
    def leave_course(self) -> Tuple[Any, int]:
        """Allow a student to unenroll from a course."""
        current_user_id = get_jwt_identity()
        current_user = self.user_service.get_user_by_id(current_user_id)

        if current_user.role != 'Student':
            logger.warning(f"Non-student user ID: {current_user_id} attempted to leave a course.")
            return jsonify({'msg': 'Only students can leave courses.'}), 403

        data = request.get_json()
        course_id = data.get('course_id', '').strip()

        if not course_id:
            logger.warning("Leave course failed: Missing course ID.")
            return jsonify({'msg': 'Course ID is required.'}), 400

        try:
            enrollment = self.course_service.leave_course(current_user.id, course_id)
            if not enrollment:
                logger.warning(f"User ID: {current_user_id} is not enrolled in course ID: {course_id}")
                return jsonify({'msg': 'Not enrolled in this course.'}), 404

            return jsonify({'msg': 'Left course successfully.'}), 200
        except Exception as e:
            logger.error(f"Error leaving course ID: {course_id} by user ID: {current_user_id} - {str(e)}")
            return jsonify({'msg': 'An error occurred while leaving the course.'}), 500