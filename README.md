# University Management API

The University Management API is a robust RESTful service that facilitates user authentication, course management, enrollment, and grade operations. It supports role-based access control (Administrator, Professor, Student) using JWT authentication and is fully documented with an OpenAPI 3.0 specification.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [License](#license)

## Overview

This API is designed for university environments, offering secure endpoints to manage users, courses, enrollments, and grades. Its modular design and clear separation between roles make it both powerful and scalable.

## Features

- **User Authentication:**
    - Login using JWT tokens
    - User registration (initiated by administrators)
    - Password change functionality

- **User Management:**
    - Administrators can list, search, create, update, and delete users.
    - Professors and individual users have tailored access to user information.

- **Course Management:**
    - Create, update, and delete courses (for Administrators and Professors).
    - All authenticated users can search and view course listings.

- **Enrollment:**
    - Students can join or leave courses.
    - Professors and administrators can review all students enrolled in a course.

- **Grade Management:**
    - Professors and Administrators can assign, update, list, and delete student grades.
    - Retrieve grade reports per student for a specific course.

## Technology Stack

- **Backend Framework:** Flask
- **Authentication:** Flask-JWT-Extended
- **API Documentation:** OpenAPI 3.0 (Swagger/OpenAPI Specification)
- **Database:** SQLAlchemy (assumed based on implementation)
- **Logging:** Python logging module

## Installation

### Clone the Repository

```bash
git clone https://github.com/Ghostfighter50/FlaskApp.git
cd FlaskApp
```

### Create a Virtual Environment

```bash
python3 -m venv venv
# On Unix or MacOS
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up the Database

- Update your database connection string in the configuration.
- Run migration commands if applicable to set up the schema.

## Configuration

The application can be configured through environment variables or a dedicated configuration file. Common settings include:

- `FLASK_ENV`: Set to `development` or `production`
- `DATABASE_URL`: Provide your database connection URL
- `JWT_SECRET_KEY`: Define a secure secret key for JWT tokens

Additional settings control logging, debugging, and other application parameters.

## Usage

### Running the Application

Start the API with the following command:

```bash
python ./run.py
```

The API will run at:
http://localhost:5000/api/v1

### Authentication

Obtain a JWT token by calling the `/auth/login` endpoint. Include your token in the Authorization header:

```
Authorization: Bearer <your_token_here>
```

## API Documentation

Interactive API documentation is available through Swagger UI or Redoc. The full OpenAPI specification can be found in the `openapi.yaml` file located at the repository root.

## Testing

### Tests

Run tests with pytest:

```bash
pytest
```

## License

This project is licensed under the MIT License.
