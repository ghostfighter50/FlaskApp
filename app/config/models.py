from .database import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from sqlalchemy import Enum


class User(db.Model):
    __tablename__ = 'users'
    
    # Columns for the User table
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(Enum('Student', 'Professor', 'Administrator', name="user_roles", create_type=False), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
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
    __tablename__ = 'courses'
    
    # Columns for the Course table
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    professor_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    grades = db.relationship('Grade', backref='course', lazy=True)

    def __repr__(self):
        return f"<Course {self.name}>"

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    # Columns for the Enrollment table
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Unique constraint to ensure a student can enroll in a course only once
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),)

    def __repr__(self):
        return f"<Enrollment Student ID: {self.student_id}, Course ID: {self.course_id}>"

class Grade(db.Model):
    __tablename__ = 'grades'
    
    # Columns for the Grade table
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Unique constraint to ensure a student can have only one grade per course
    __table_args__ = (db.UniqueConstraint('course_id', 'student_id', name='unique_grade'),)

    def __repr__(self):
        return f"<Grade Student ID: {self.student_id}, Course ID: {self.course_id}, Grade: {self.grade}>"