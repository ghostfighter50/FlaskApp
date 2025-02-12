# University Management API

The University Management API is a robust RESTful service tailored for university environments. It facilitates user authentication, comprehensive course management, enrollment administration, and grade operations via secure endpoints. Built with Flask and protected by JWT authentication, the API seamlessly integrates with a modern React Vite frontend that leverages Axios for API requests.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
    - [Backend Setup](#backend-setup)
    - [Frontend Setup](#frontend-setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [License](#license)

## Overview

The University Management API offers secure endpoints to manage users, courses, enrollments, and grades. With differentiated access roles (Administrator, Professor, Student) and state-of-the-art security protocols, this API is designed to meet the complex needs of modern academic institutions.

## Features

- **User Authentication:**
    - Secure login using JWT tokens.
    - Administrator-initiated user registration.
    - Password management and change functionality.

- **User Management:**
    - Full CRUD operations for Administrators.
    - Role-based data access tailored for Professors and individual users.

- **Data Security:**
    - AES-256 encryption for sensitive fields.
    - Optimized querying with stored email hashes.

- **Course Management:**
    - Endpoints for course creation, updates, and deletion.
    - Comprehensive course listings accessible to all authenticated users.

- **Enrollment:**
    - Enrollment and course drop features for students.
    - Oversight capabilities for Professors and Administrators on enrollment processes.

- **Grade Management:**
    - Grade assignment, updates, and deletion by Professors and Administrators.
    - Detailed student and course grade reports.

- **Modern Frontend:**
    - A professional React Vite interface.
    - Axios is used on the client to handle API communications, ensuring fast and reliable data exchanges.

## Technology Stack

- **Backend Framework:** Flask
- **Authentication:** Flask-JWT-Extended
- **API Documentation:** OpenAPI 3.0 (Swagger/OpenAPI Specification)
- **Database:** MySQL
- **Logging:** Python logging module
- **Frontend:** React Vite; API requests are handled with Axios

## Installation

### Backend Setup

#### Clone the Repository

```bash
git clone https://github.com/Ghostfighter50/FlaskApp.git
cd FlaskApp/api
```

#### Create a Virtual Environment

```bash
python3 -m venv venv
# On Unix or MacOS
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Set Up the Database

- Update your database connection string in the configuration or environment variables.

### Frontend Setup

#### Clone the Frontend Repository

```bash
git clone https://github.com/Ghostfighter50/FlaskApp.git
cd FlaskApp/client
```

#### Install Frontend Dependencies

```bash
npm install
```

#### Run the Frontend

```bash
npm run dev
```

The React Vite frontend, powered by Axios for API requests, will run on its default port (usually http://localhost:3000) and interact seamlessly with the backend API.

## Configuration

Configure the application using environment variables or a dedicated configuration file. Key settings include:

- `FLASK_ENV`: Set to `development` or `production`
- `DATABASE_URL`: Your database connection URL
- `JWT_SECRET_KEY`: Secure key for JWT tokens
- Additional parameters for logging, debugging, and more.

## Usage

### Running the Backend

Launch the API using the command below:

```bash
python ./run.py
```

The API will be available at:
http://localhost:5000/api/v1

### Authentication

Authenticate by requesting a JWT token from the `/auth/login` endpoint. Include your token in the Authorization header:

```
Authorization: Bearer <your_token_here>
```

## API Documentation

Interactive API documentation is available via Swagger UI or Redoc. The complete OpenAPI specification is maintained in the `openapi.yaml` file at the repository root.

## Testing

### Running Tests

Execute tests with pytest:

```bash
pytest
```

## License

This project is licensed under the MIT License.
