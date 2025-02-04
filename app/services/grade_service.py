import logging
from typing import List, Optional
from app import db
from app.config.models import Grade

logger = logging.getLogger(__name__)

class GradeService:
    """
    Service class encapsulating database operations related to the Grade model.
    Provides functionality for creating, retrieving, updating, and deleting grades,
    as well as querying grades for specific students and courses.
    """

    def list_grades(self) -> List[Grade]:
        """
        Retrieves all grades from the database.

        Returns:
            List[Grade]: A list of all Grade objects in the database.
        """
        logger.debug("Retrieving all grades from the database.")
        grades = db.session.query(Grade).all()
        logger.info(f"Retrieved {len(grades)} grades.")
        return grades

    def get_grade_by_id(self, grade_id: str) -> Optional[Grade]:
        """
        Retrieves a grade by its unique ID.

        Args:
            grade_id (str): The unique identifier of the grade.

        Returns:
            Optional[Grade]: The Grade object if found, else None.
        """
        logger.debug(f"Fetching grade with ID: {grade_id}")
        grade = db.session.get(Grade, grade_id)
        if grade:
            logger.debug(f"Grade found: {grade.id}, Grade Value: {grade.grade}")
        else:
            logger.debug(f"No grade found with ID: {grade_id}")
        return grade

    def assign_grade(self, student_id: str, course_id: str, grade_value: float, grade_name: str) -> Grade:
        """
        Assigns a grade to a student for a specific course.

        Args:
            student_id (str): The unique identifier of the student.
            course_id (str): The unique identifier of the course.
            grade_value (float): The grade value to be assigned.
            grade_name (str): The name of the grade (e.g., "Final Exam", "Midterm").

        Returns:
            Grade: The newly created Grade object.
        """
        logger.debug(f"Assigning grade {grade_value} to student {student_id} for course {course_id}.")
        new_grade = Grade(
            student_id=student_id,
            course_id=course_id,
            grade=grade_value,
            name=grade_name
        )
        db.session.add(new_grade)
        db.session.commit()
        logger.info(f"Grade assigned: {new_grade.id}, Value: {new_grade.grade}")
        return new_grade

    def update_grade(self, grade_obj: Grade, new_grade_value: float) -> Grade:
        """
        Updates an existing grade's value.

        Args:
            grade_obj (Grade): The Grade object to update.
            new_grade_value (float): The new grade value.

        Returns:
            Grade: The updated Grade object.
        """
        logger.debug(f"Updating grade ID: {grade_obj.id} to new value: {new_grade_value}.")
        grade_obj.grade = new_grade_value
        db.session.commit()
        logger.info(f"Grade ID: {grade_obj.id} updated to value: {new_grade_value}.")
        return grade_obj

    def delete_grade(self, grade_obj: Grade) -> None:
        """
        Deletes a grade record from the database.

        Args:
            grade_obj (Grade): The Grade object to be deleted.
        """
        logger.debug(f"Deleting grade ID: {grade_obj.id}.")
        db.session.delete(grade_obj)
        db.session.commit()
        logger.info(f"Grade ID: {grade_obj.id} deleted successfully.")

    def get_student_grades(self, course_id: str, student_id: str) -> List[Grade]:
        """
        Retrieves all grades for a specific student within a given course.

        Args:
            course_id (str): The unique identifier of the course.
            student_id (str): The unique identifier of the student.

        Returns:
            List[Grade]: A list of Grade objects for the specified student and course.
        """
        logger.debug(f"Fetching grades for student ID: {student_id} in course ID: {course_id}.")
        grades = db.session.query(Grade).filter_by(course_id=course_id, student_id=student_id).all()
        logger.info(f"Retrieved {len(grades)} grades for student ID: {student_id} in course ID: {course_id}.")
        return grades
