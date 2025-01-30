import logging
from typing import Tuple, Optional, List, Dict, Any
from flask_paginate  import Pagination
from ..config.models import Course, Enrollment
from ..config.database import db

logger = logging.getLogger(__name__)

class CourseService:
    """
    Service class for handling course management operations such as
    retrieving, searching, creating, updating, deleting courses,
    and managing enrollments.
    """

    @staticmethod
    def get_all_courses_paginated(page: int, per_page: int) -> Tuple[List[Course], Pagination]:
        """
        Retrieves a paginated list of all courses.

        Args:
            page (int): The page number to retrieve.
            per_page (int): The number of courses per page.

        Returns:
            Tuple[List[Course], Pagination]: A tuple containing the list of courses
            and a Pagination object with Pagination details.
        """
        logger.debug(f"Fetching courses - Page: {page}, Per Page: {per_page}")
        pagination: Pagination = db.session.query(Course).paginate(page=page, per_page=per_page, error_out=False)
        logger.info(f"Retrieved {len(pagination.items)} courses on page {page}.")
        return pagination.items, pagination

    @staticmethod
    def get_course_by_id(course_id: str) -> Optional[Course]:
        """
        Retrieves a course from the database by its unique ID.

        Args:
            course_id (str): The unique identifier of the course.

        Returns:
            Optional[Course]: The Course object if found, else None.
        """
        logger.debug(f"Fetching course by ID: {course_id}")
        course: Optional[Course] = db.session.get(Course, course_id)  # Using Session.get() for direct retrieval
        if course:
            logger.debug(f"Course found: {course.name} (ID: {course.id})")
        else:
            logger.debug(f"No course found with ID: {course_id}")
        return course

    @staticmethod
    def search_courses_by_name(name_query: str) -> List[Course]:
        """
        Searches for courses whose name contains the given query string.

        Args:
            name_query (str): The query string to search for in course names.

        Returns:
            List[Course]: A list of Course objects matching the search criteria.
        """
        logger.debug(f"Searching courses with name containing: {name_query}")
        courses: List[Course] = (
            db.session.query(Course)
            .filter(Course.name.ilike(f"%{name_query}%"))
            .all()
        )
        logger.info(f"Found {len(courses)} courses matching query '{name_query}'.")
        return courses

    @staticmethod
    def get_students_in_course(course_id: str) -> List[Enrollment]:
        """
        Retrieves all students enrolled in a specific course.

        Args:
            course_id (str): The unique identifier of the course.

        Returns:
            List[Enrollment]: A list of Enrollment objects representing student enrollments.
        """
        logger.debug(f"Fetching students in course ID: {course_id}")
        enrollments: List[Enrollment] = (
            db.session.query(Enrollment)
            .filter_by(course_id=course_id)
            .all()
        )
        logger.info(f"Retrieved {len(enrollments)} students for course ID: {course_id}.")
        return enrollments

    @staticmethod
    def create_course(name: str, professor_id: str) -> Course:
        """
        Creates a new course and saves it to the database.

        Args:
            name (str): The name of the course.
            professor_id (str): The unique identifier of the professor assigned to the course.

        Returns:
            Course: The newly created Course object.
        """
        logger.debug(f"Creating course: {name} by professor ID: {professor_id}")
        course = Course(name=name, professor_id=professor_id)
        db.session.add(course)
        db.session.commit()
        logger.info(f"Course created with ID: {course.id}")
        return course

    @staticmethod
    def update_course(course: Course, name: str) -> Course:
        """
        Updates the name of an existing course.

        Args:
            course (Course): The Course object to be updated.
            name (str): The new name for the course.

        Returns:
            Course: The updated Course object.
        """
        logger.debug(f"Updating course ID: {course.id} with new name: {name}")
        course.name = name
        db.session.commit()
        logger.info(f"Course ID: {course.id} updated successfully.")
        return course

    @staticmethod
    def delete_course(course: Course) -> None:
        """
        Deletes a course from the database.

        Args:
            course (Course): The Course object to be deleted.
        """
        logger.debug(f"Deleting course ID: {course.id}")
        db.session.delete(course)
        db.session.commit()
        logger.info(f"Course ID: {course.id} deleted successfully.")

    @staticmethod
    def join_course(user_id: str, course_id: str) -> Optional[Enrollment]:
        """
        Enrolls a student in a course.

        Args:
            user_id (str): The unique identifier of the student.
            course_id (str): The unique identifier of the course.

        Returns:
            Optional[Enrollment]: The Enrollment object if successful, else None (e.g., if already enrolled).
        """
        logger.debug(f"User ID: {user_id} attempting to join course ID: {course_id}")
        existing_enrollment = (
            db.session.query(Enrollment)
            .filter_by(student_id=user_id, course_id=course_id)
            .first()
        )
        if existing_enrollment:
            logger.warning(f"User ID: {user_id} is already enrolled in course ID: {course_id}")
            return None
        
        enrollment = Enrollment(student_id=user_id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        logger.info(f"User ID: {user_id} joined course ID: {course_id} successfully.")
        return enrollment

    @staticmethod
    def leave_course(user_id: str, course_id: str) -> Optional[Enrollment]:
        """
        Unenrolls a student from a course.

        Args:
            user_id (str): The unique identifier of the student.
            course_id (str): The unique identifier of the course.

        Returns:
            Optional[Enrollment]: The Enrollment object if successful, else None (e.g., if not enrolled).
        """
        logger.debug(f"User ID: {user_id} attempting to leave course ID: {course_id}")
        enrollment = (
            db.session.query(Enrollment)
            .filter_by(student_id=user_id, course_id=course_id)
            .first()
        )
        if not enrollment:
            logger.warning(f"User ID: {user_id} is not enrolled in course ID: {course_id}")
            return None

        db.session.delete(enrollment)
        db.session.commit()
        logger.info(f"User ID: {user_id} left course ID: {course_id} successfully.")
        return enrollment

    @staticmethod
    def get_courses_by_professor(professor_id: str) -> List[Course]:
        """
        Retrieves all courses taught by a specific professor.

        Args:
            professor_id (str): The unique identifier of the professor.

        Returns:
            List[Course]: A list of Course objects taught by the professor.
        """
        logger.debug(f"Fetching courses taught by professor ID: {professor_id}")
        courses: List[Course] = (
            db.session.query(Course)
            .filter_by(professor_id=professor_id)
            .all()
        )
        logger.info(f"Found {len(courses)} courses taught by professor ID: {professor_id}.")
        return courses

    