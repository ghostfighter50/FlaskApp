from typing import Any, Dict
from app.config.models import Course, Grade, User
import logging

logger = logging.getLogger(__name__)

def serialize_course(course: Course) -> Dict[str, Any]:
        """
        Serializes a Course object into a dictionary for API responses.

        Args:
            course (Course): The Course object to serialize.

        Returns:
            Dict[str, Any]: A dictionary representation of the course.
        """
        logger.debug(f"Serializing course ID: {course.id}")
        course_data = {
            'id': course.id,
            'name': course.name,
            'professor_id': course.professor_id,
            'created_at': course.created_at.isoformat(),
            'updated_at': course.updated_at.isoformat()
        }
        logger.debug(f"Course serialized: {course_data}")
        return course_data


def serialize_user(user: User) -> Dict[str, Any]:
        """
        Serializes a User object into a dictionary for API responses.

        Args:
            user (User): The User object to serialize.

        Returns:
            Dict[str, Any]: A dictionary representation of the user.
        """
        logger.debug(f"Serializing user ID: {user.id}")
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        }

        # If role is 'Professor', include courses taught
        if user.role == 'Professor':
            user_data["courses_teaching"] = [
                serialize_course(course)
                for course in user.courses_created
            ]

        # If role is 'Student', include courses the student is enrolled in
        if user.role == 'Student':
            user_data["courses_enrolled"] = [
                enrollment.course_id for enrollment in user.enrollments
            ]

        logger.debug(f"User serialized: {user_data}")
def serialize_grade(grade: Grade) -> Dict[str, Any]:
    """
    Serializes a Grade object into a dictionary for API responses.
    Args:
        grade (Grade): The Grade object to serialize.

    Returns:
        Dict[str, Any]: A dictionary representation of the grade.
            """
    logger.debug(f"Serializing grade ID: {grade.id}")
    grade_data = {
        'id': grade.id,
        'course_id': grade.course_id,
        'student_id': grade.student_id,
        'grade': grade.grade,
        'created_at': grade.created_at.isoformat(),
        'updated_at': grade.updated_at.isoformat()
    }
    logger.debug(f"Grade serialized: {grade_data}")
    return grade_data       