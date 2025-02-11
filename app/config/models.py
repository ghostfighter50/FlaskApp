import uuid
import hashlib
from datetime import datetime, timezone
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import FernetEngine

from app.config import config
from .database import db

SECRET_KEY = config.Config.ENCRYPTION_KEY


def compute_email_hash(email: str) -> str:
    """
    Compute a SHA-256 hash for the given email. This is used for lookups
    and enforcing uniqueness on the email field without needing to decrypt it.
    """
    return hashlib.sha256(email.lower().strip().encode('utf-8')).hexdigest()


class User(db.Model):
    """
    User Model

    This model represents a user in the application. Sensitive fields like name and email
    are stored using encryption. To allow for queries and uniqueness constraints on the email,
    a separate email_hash column is maintained.

    Attributes:
        id (str): Unique identifier for each user, generated using UUID.
        _name (str): Encrypted name of the user, cannot be null.
        _email (str): Encrypted email of the user, cannot be null.
        email_hash (str): SHA-256 hash of the email (used for lookups and uniqueness).
        password_hash (str): Hashed password for security, cannot be null.
        role (Enum): Role of the user, can be 'Student', 'Professor', or 'Administrator'.
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp when the user was last updated.
    """

    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    _name = db.Column(
        "name",
        StringEncryptedType(db.String, SECRET_KEY, engine=FernetEngine, length=512),
        nullable=False
    )
    _email = db.Column(
        "email",
        StringEncryptedType(db.String, SECRET_KEY, engine=FernetEngine, length=512),
        nullable=False
    )
    email_hash = db.Column(db.String(64), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(Enum('Student', 'Professor', 'Administrator', name="user_roles"), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    courses_created = db.relationship('Course', backref='professor', lazy='joined')
    enrollments = db.relationship('Enrollment', backref='student', lazy='joined')
    grades = db.relationship('Grade', backref='student', lazy='joined')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value
        self.email_hash = compute_email_hash(value)

    def set_password(self, password: str) -> None:
        """Hashes the provided password and stores it in the password_hash field."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Checks if the provided password matches the stored password hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Course(db.Model):
    """
    Course Model

    This model represents a course in the application.

    Attributes:
        id (str): Unique identifier for each course, generated using UUID.
        name (str): Name of the course, cannot be null.
        professor_id (str): Unique identifier of the professor assigned to the course, cannot be null.
        created_at (datetime): Timestamp when the course was created.
        updated_at (datetime): Timestamp when the course was last updated.
    """
    __tablename__ = 'courses'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    professor_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    grades = db.relationship('Grade', backref='course', lazy=True)

    def __repr__(self):
        return f"<Course {self.name}>"


class Enrollment(db.Model):
    """
    Enrollment Model

    This model represents an enrollment in a course by a student.

    Attributes:
        id (str): Unique identifier for each enrollment, generated using UUID.
        student_id (str): Unique identifier of the student enrolled in the course, cannot be null.
        course_id (str): Unique identifier of the course the student is enrolled in, cannot be null.
        enrolled_at (datetime): Timestamp when the student was enrolled in the course.
    """
    __tablename__ = 'enrollments'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),)

    def __repr__(self):
        return f"<Enrollment Student ID: {self.student_id}, Course ID: {self.course_id}>"


class Grade(db.Model):
    """
    Grade Model

    This model represents a grade given to a student for a course.

    Attributes:
        id (str): Unique identifier for each grade, generated using UUID.
        name (str): Name of the grade (e.g., "Final Exam", "Midterm"), cannot be null.
        course_id (str): Unique identifier of the course the grade is associated with, cannot be null.
        student_id (str): Unique identifier of the student the grade is assigned to, cannot be null.
        grade (float): The actual grade value, cannot be null.
        created_at (datetime): Timestamp when the grade was created.
        updated_at (datetime): Timestamp when the grade was last updated.
    """
    __tablename__ = 'grades'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Grade Student ID: {self.student_id}, Course ID: {self.course_id}, Grade: {self.grade}>"
