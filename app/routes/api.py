from flask import Blueprint, request, jsonify
from app.services.academic_service import AcademicService

api_bp = Blueprint("api", __name__)


@api_bp.route("/health", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "UP",
        "service": "Enterprise Student Academic Management Platform",
        "version": "1.0.0"
    }), 200


@api_bp.route("/students", methods=["POST"])
def register_student():
    data = request.get_json() or {}

    try:
        student = AcademicService.add_student(
            student_id=data.get("student_id"),
            name=data.get("name"),
            email=data.get("email"),
            semester=int(data.get("semester", 1))
        )

        return jsonify({
            "message": "Student registered successfully",
            "student": student
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/students/<student_id>", methods=["GET"])
def get_student(student_id):
    student = AcademicService.get_student(student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student), 200


@api_bp.route("/courses", methods=["GET"])
def list_courses():
    courses = AcademicService.list_courses()

    return jsonify({
        "count": len(courses),
        "courses": courses
    }), 200


@api_bp.route("/courses", methods=["POST"])
def add_course():
    data = request.get_json() or {}

    try:
        course = AcademicService.add_course(
            course_id=data.get("course_id"),
            name=data.get("name"),
            credits=int(data.get("credits", 0)),
            faculty_id=data.get("faculty_id"),
            capacity=int(data.get("capacity", 30))
        )

        return jsonify({
            "message": "Course added successfully",
            "course": course
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/enroll", methods=["POST"])
def enroll_student():
    data = request.get_json() or {}

    try:
        enrollment = AcademicService.enroll_student(
            student_id=data.get("student_id"),
            course_id=data.get("course_id")
        )

        return jsonify({
            "message": "Student enrolled successfully",
            "enrollment": enrollment
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/grades", methods=["POST"])
def assign_grade():
    data = request.get_json() or {}

    try:
        grade = AcademicService.assign_grade(
            student_id=data.get("student_id"),
            course_id=data.get("course_id"),
            grade=data.get("grade")
        )

        return jsonify({
            "message": "Grade assigned successfully",
            "grade": grade
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/students/<student_id>/gpa", methods=["GET"])
def get_gpa(student_id):
    try:
        gpa = AcademicService.calculate_gpa(student_id)

        return jsonify({
            "student_id": student_id,
            "gpa": gpa
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
