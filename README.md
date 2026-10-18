# Enterprise Student Record & Academic Management Platform

A Flask-based academic management platform demonstrating
automated testing, CI/CD, Docker containerization and
Kubernetes orchestration.

## Technology Stack

- Python 3.11
- Flask 3.0
- Pytest
- Flake8
- Jenkins
- Docker
- Kubernetes / Minikube

## Business Rules

- Maximum 18 credits per semester
- Students cannot enroll in the same course twice
- Course capacity is enforced
- GPA is calculated from assigned grades

## Health Endpoint

GET /api/health

## Main APIs

POST /api/students
GET /api/students/<student_id>
GET /api/courses
POST /api/courses
POST /api/enroll
POST /api/grades
GET /api/students/<student_id>/gpa
