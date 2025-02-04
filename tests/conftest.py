import pytest
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.config.models import Course, Grade, User


@pytest.fixture()
def app():
    """
    Create and configure a new app instance for tests.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use an in-memory database for tests
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        student_user = User(name="student", email="student@example.com", role="Student")
        student_user.set_password("ValidPass123!")
        db.session.add(student_user)

        professor_user = User(name="professor", email="professor@example.com", role="Professor")
        professor_user.set_password("ValidPass123!")
        db.session.add(professor_user)

        admin_user = User(name="admin", email="admin@example.com", role="Administrator")
        admin_user.set_password("ValidPass123!")
        db.session.add(admin_user)

        db.session.commit()

        course = Course(name="Test Course", professor_id=professor_user.id)
        db.session.add(course)

        db.session.commit()

        grade = Grade(name="DM", grade=90, course_id=course.id, student_id=student_user.id)
        db.session.add(grade)

        db.session.commit()

        app.student_id = student_user.id
        app.professor_id = professor_user.id
        app.admin_id = admin_user.id
        app.course_id = course.id
        app.grade_id = grade.id

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_token(app):
    return create_access_token(identity=app.admin_id)


@pytest.fixture
def professor_token(app):
    return create_access_token(identity=app.professor_id)


@pytest.fixture
def student_token(app):
    return create_access_token(identity=app.student_id)


@pytest.fixture()
def course_id(app):
    print(f"course_id: {app.course_id}")
    return app.course_id


@pytest.fixture()
def student_id(app):
    return app.student_id


@pytest.fixture()
def professor_id(app):
    return app.professor_id


@pytest.fixture()
def admin_id(app):
    return app.admin_id


@pytest.fixture()
def grade_id(app):
    return app.grade_id
