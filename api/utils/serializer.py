from typing import Any, Dict
from api.config.models import Course, Grade
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


logger = logging.getLogger(__name__)


def serialize_user(user):
    """
    Serialize a User object into a dictionary.
    Returns None if the user is None.
    """
    if user is None:
        return None

    serialized = {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at.isoformat() if hasattr(user, "created_at") and user.created_at else None,
        "updated_at": user.updated_at.isoformat() if hasattr(user, "updated_at") and user.updated_at else None,
    }

    if hasattr(user, "courses_enrolled"):
        serialized["courses_enrolled"] = [
            serialize_course(course) for course in user.courses_enrolled
        ]
    elif hasattr(user, "courses_teaching"):
        serialized["courses_teaching"] = [
            serialize_course(course) for course in user.courses_teaching
        ]
    else:
        serialized["courses_enrolled"] = []

    logger.debug(f"User serialized: {serialized}")
    return serialized


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
        'name': grade.name,
        'created_at': grade.created_at.isoformat(),
        'updated_at': grade.updated_at.isoformat()
    }
    logger.debug(f"Grade serialized: {grade_data}")
    return grade_data
