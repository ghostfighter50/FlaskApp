import logging
from typing import List, Optional, Dict, Any
from ..config.models import Grade
from ..config.database import db

logger = logging.getLogger(__name__)

class GradeService:
    """
    Service class for managing grade operations, including retrieving,
    creating, updating, and deleting grades.
    """

    @staticmethod
    def get_all_grades() -> List[Grade]:
        """
        Retrieves all grades from the database.

        Returns:
            List[Grade]: A list of all Grade objects.
        """
        logger.debug("Fetching all grades from the database.")
        grades: List[Grade] = db.session.query(Grade).all()
        logger.info(f"Retrieved {len(grades)} grades from the database.")
        return grades

    @staticmethod
    def get_grade_by_id(grade_id: str) -> Optional[Grade]:
        """
        Retrieves a specific grade by its unique ID.

        Args:
            grade_id (str): The unique identifier of the grade.

        Returns:
            Optional[Grade]: The Grade object if found, otherwise None.
        """
        logger.debug(f"Fetching grade by ID: {grade_id}")
        grade: Optional[Grade] = db.session.get(Grade, grade_id)
        if grade:
            logger.debug(f"Grade found: {grade.id}")
        else:
            logger.debug(f"No grade found with ID: {grade_id}")
        return grade

    @staticmethod
    def assign_grade(course_id: str, student_id: str, grade_value: float) -> Grade:
        """
        Assigns a new grade to a student in a specific course.

        Args:
            course_id (str): The ID of the course.
            student_id (str): The ID of the student.
            grade_value (float): The numeric value of the grade.

        Returns:
            Grade: The newly created Grade object.
        """
        logger.debug(f"Assigning grade {grade_value} to student {student_id} for course {course_id}.")
        new_grade = Grade(
            course_id=course_id,
            student_id=student_id,
            value=grade_value
        )
        db.session.add(new_grade)
        db.session.commit()
        logger.info(f"Grade assigned successfully with ID: {new_grade.id}")
        return new_grade

    @staticmethod
    def update_grade(grade: Grade, grade_value: float) -> Grade:
        """
        Updates the value of an existing grade.

        Args:
            grade (Grade): The Grade object to update.
            grade_value (float): The new numeric value for the grade.

        Returns:
            Grade: The updated Grade object.
        """
        logger.debug(f"Updating grade ID: {grade.id} to new value: {grade_value}")
        grade.value = grade_value
        db.session.commit()
        logger.info(f"Grade ID: {grade.id} updated successfully.")
        return grade

    @staticmethod
    def delete_grade(grade: Grade) -> None:
        """
        Deletes a grade from the database.

        Args:
            grade (Grade): The Grade object to delete.
        """
        logger.debug(f"Deleting grade ID: {grade.id}")
        db.session.delete(grade)
        db.session.commit()
        logger.info(f"Grade ID: {grade.id} deleted successfully.")

    @staticmethod
    def get_grades_by_course_and_student(course_id: str, student_id: str) -> List[Grade]:
        """
        Retrieves all grades for a specific student within a specific course.

        Args:
            course_id (str): The ID of the course.
            student_id (str): The ID of the student.

        Returns:
            List[Grade]: A list of Grade objects.
        """
        logger.debug(f"Fetching grades for student {student_id} in course {course_id}.")
        grades: List[Grade] = (
            db.session.query(Grade)
            .filter_by(course_id=course_id, student_id=student_id)
            .all()
        )
        logger.info(f"Retrieved {len(grades)} grades for student {student_id} in course {course_id}.")
        return grades

    @staticmethod
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
            "id": grade.id,
            "course_id": grade.course_id,
            "student_id": grade.student_id,
            "value": grade.value,
            "created_at": grade.created_at.isoformat() if grade.created_at else None,
            "updated_at": grade.updated_at.isoformat() if grade.updated_at else None
        }
        logger.debug(f"Grade serialized: {grade_data}")
        return grade_data
