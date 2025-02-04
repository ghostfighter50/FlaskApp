from .database import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from sqlalchemy import Enum


class User(db.Model):
    """
    User Model
    This model represents a user in the application. It includes fields for user identification,
    authentication, and role-based access control. The model also establishes relationships with
    other models such as Course, Enrollment, and Grade.

    Attributes:
        id (str): Unique identifier for each user, generated using UUID.
        name (str): Name of the user, cannot be null.
        email (str): Email of the user, must be unique and cannot be null.
        password_hash (str): Hashed password for security, cannot be null.
        role (Enum): Role of the user, can be 'Student', 'Professor', or 'Administrator'.
        created_at (datetime): Timestamp when the user was created, defaults to current UTC time.
        updated_at (datetime): Timestamp when the user was last updated, defaults to current UTC time and updates on modification.

    Relationships:
        courses_created (list[Course]): Courses created by the professor.
        enrollments (list[Enrollment]): Courses the student is enrolled in.
        grades (list[Grade]): Grades the student has received.

    Methods:
        set_password(password):
            Hashes the provided password and stores it in the password_hash field.
        check_password(password):
            Checks if the provided password matches the stored password hash.
        __repr__():
            Returns a string representation of the user, showing the user's email.
    """
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(Enum('Student', 'Professor', 'Administrator', name="user_roles", create_type=False), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    courses_created = db.relationship('Course', backref='professor', lazy='joined')
    enrollments = db.relationship('Enrollment', backref='student', lazy='joined')
    grades = db.relationship('Grade', backref='student', lazy='joined')

    def set_password(self, password):
        """Hashes the provided password and stores it in the password_hash field."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored password hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Course(db.Model):
    """
    Course Model
    This model represents a course in the application. It includes fields for course identification
    and relationships with other models such as Enrollment and Grade.

    Attributes:
        id (str): Unique identifier for each course, generated using UUID.
        name (str): Name of the course, cannot be null.
        professor_id (str): ID of the professor teaching the course, cannot be null.
        created_at (datetime): Timestamp when the course was created, defaults to current UTC time.
        updated_at (datetime): Timestamp when the course was last updated, defaults to current UTC time and updates on modification.

    Relationships:
        enrollments (list[Enrollment]): Enrollments in the course.
        grades (list[Grade]): Grades given in the course.

    Methods:
        __repr__():
            Returns a string representation of the course, showing the course's name.
    """
    __tablename__ = 'courses'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    professor_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    grades = db.relationship('Grade', backref='course', lazy=True)

    def __repr__(self):
        return f"<Course {self.name}>"


class Enrollment(db.Model):
    """
    Enrollment Model
    This model represents an enrollment in a course by a student. It includes fields for enrollment
    identification and relationships with other models such as User and Course.

    Attributes:
        id (str): Unique identifier for each enrollment, generated using UUID.
        student_id (str): ID of the student enrolled in the course, cannot be null.
        course_id (str): ID of the course the student is enrolled in, cannot be null.
        enrolled_at (datetime): Timestamp when the enrollment was created, defaults to current UTC time.

    Constraints:
        __table_args__ (tuple): Ensures a student can only enroll in a course once.

    Methods:
        __repr__():
            Returns a string representation of the enrollment, showing the student and course IDs.
    """
    __tablename__ = 'enrollments'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),)

    def __repr__(self):
        return f"<Enrollment Student ID: {self.student_id}, Course ID: {self.course_id}>"


class Grade(db.Model):
    """
    Grade Model
    This model represents a grade given to a student for a course. It includes fields for grade
    identification and relationships with other models such as User and Course.

    Attributes:
        id (str): Unique identifier for each grade, generated using UUID.
        name (str): Name of the grade (e.g., "Midterm", "Final"), cannot be null.
        course_id (str): ID of the course the grade is for, cannot be null.
        student_id (str): ID of the student receiving the grade, cannot be null.
        grade (float): The grade value, cannot be null.
        created_at (datetime): Timestamp when the grade was created, defaults to current UTC time.
        updated_at (datetime): Timestamp when the grade was last updated, defaults to current UTC time and updates on modification.

    Methods:
        __repr__():
            Returns a string representation of the grade, showing the student and course IDs and the grade value.
    """
    __tablename__ = 'grades'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Grade Student ID: {self.student_id}, Course ID: {self.course_id}, Grade: {self.grade}>"
