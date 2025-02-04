import logging
from typing import Tuple, Optional, List
from flask_paginate import Pagination
from ..config.models import Course, Enrollment, Grade
from ..config.database import db

logger = logging.getLogger(__name__)


class CourseService:
    """
    Service class for managing course-related operations, including:
    - Retrieving courses with pagination.
    - Searching courses by name.
    - Enrolling and unenrolling students.
    - Creating, updating, and deleting courses.
    """

    @staticmethod
    def get_all_courses_paginated(page: int, per_page: int) -> Tuple[List[Course], Pagination]:
        """
        Retrieves a paginated list of all courses.

        Args:
            page (int): The page number to retrieve.
            per_page (int): The number of courses per page.

        Returns:
            Tuple[List[Course], Pagination]: A tuple containing a list of courses
            and a Pagination object with pagination details.
        """
        logger.debug("Fetching courses - Page: %d, Per Page: %d", page, per_page)
        pagination: Pagination = db.session.query(Course).paginate(page=page, per_page=per_page, error_out=False)
        logger.info("Retrieved %d courses on page %d.", len(pagination.items), page)
        return pagination.items, pagination

    @staticmethod
    def get_course_by_id(course_id: str) -> Optional[Course]:
        """
        Retrieves a course by its unique ID.

        Args:
            course_id (str): The unique identifier of the course.

        Returns:
            Optional[Course]: The Course object if found, otherwise None.
        """
        logger.debug("Fetching course by ID: %s", course_id)
        course: Optional[Course] = db.session.get(Course, course_id)
        if course:
            logger.debug("Course found: %s (ID: %s)", course.name, course.id)
        else:
            logger.debug("No course found with ID: %s", course_id)
        return course

    @staticmethod
    def search_courses_by_name(name_query: str) -> List[Course]:
        """
        Searches for courses by name.

        Args:
            name_query (str): The query string to search for in course names.

        Returns:
            List[Course]: A list of Course objects matching the query.
        """
        logger.debug("Searching courses with name containing: %s", name_query)
        courses: List[Course] = (
            db.session.query(Course)
            .filter(Course.name.ilike(f"%{name_query}%"))
            .all()
        )
        logger.info("Found %d courses matching query '%s'.", len(courses), name_query)
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
        logger.debug("Fetching students in course ID: %s", course_id)
        enrollments: List[Enrollment] = (
            db.session.query(Enrollment)
            .filter_by(course_id=course_id)
            .all()
        )
        logger.info("Retrieved %d students for course ID: %s.", len(enrollments), course_id)
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
        logger.debug("Creating course: %s by professor ID: %s", name, professor_id)
        course = Course(name=name, professor_id=professor_id)
        db.session.add(course)
        db.session.commit()
        logger.info("Course created with ID: %s", course.id)
        return course

    @staticmethod
    def update_course(course: Course, name: str) -> Course:
        """
        Updates an existing course's name.

        Args:
            course (Course): The Course object to be updated.
            name (str): The new name for the course.

        Returns:
            Course: The updated Course object.
        """
        logger.debug("Updating course ID: %s with new name: %s", course.id, name)
        course.name = name
        db.session.commit()
        logger.info("Course ID: %s updated successfully.", course.id)
        return course

    @staticmethod
    def delete_course(course: Course) -> None:
        """
        Deletes a course from the database.

        Args:
            course (Course): The Course object to be deleted.
        """
        logger.debug("Deleting course ID: %s", course.id)

        # Ensure all related records (enrollments, grades) are removed first
        db.session.query(Enrollment).filter_by(course_id=course.id).delete()
        db.session.query(Grade).filter_by(course_id=course.id).delete()

        # Delete the course record
        db.session.delete(course)
        db.session.commit()
        logger.info("Course ID: %s deleted successfully.", course.id)

    @staticmethod
    def join_course(user_id: str, course_id: str) -> Optional[Enrollment]:
        """
        Enrolls a student in a course.

        Args:
            user_id (str): The unique identifier of the student.
            course_id (str): The unique identifier of the course.

        Returns:
            Optional[Enrollment]: The Enrollment object if successful, or None if already enrolled.
        """
        logger.debug("User ID: %s attempting to join course ID: %s", user_id, course_id)
        existing_enrollment = (
            db.session.query(Enrollment)
            .filter_by(student_id=user_id, course_id=course_id)
            .first()
        )
        if existing_enrollment:
            logger.warning("User ID: %s is already enrolled in course ID: %s", user_id, course_id)
            return None

        enrollment = Enrollment(student_id=user_id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        logger.info("User ID: %s joined course ID: %s successfully.", user_id, course_id)
        return enrollment

    @staticmethod
    def leave_course(user_id: str, course_id: str) -> Optional[Enrollment]:
        """
        Unenrolls a student from a course.

        Args:
            user_id (str): The unique identifier of the student.
            course_id (str): The unique identifier of the course.

        Returns:
            Optional[Enrollment]: The Enrollment object if successful, or None if not enrolled.
        """
        logger.debug("User ID: %s attempting to leave course ID: %s", user_id, course_id)
        enrollment = (
            db.session.query(Enrollment)
            .filter_by(student_id=user_id, course_id=course_id)
            .first()
        )
        if not enrollment:
            logger.warning("User ID: %s is not enrolled in course ID: %s", user_id, course_id)
            return None

        db.session.delete(enrollment)
        db.session.commit()
        logger.info("User ID: %s left course ID: %s successfully.", user_id, course_id)
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
        logger.debug("Fetching courses taught by professor ID: %s", professor_id)
        courses: List[Course] = (
            db.session.query(Course)
            .filter_by(professor_id=professor_id)
            .all()
        )
        logger.info("Found %d courses taught by professor ID: %s.", len(courses), professor_id)
        return courses
