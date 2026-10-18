from database.db import db
from app.models.grade import Grade


class AcademicService:
    """Business logic for Student Academic Management Platform."""

    MAX_CREDITS = 18

    @staticmethod
    def add_student(student_id, name, email, semester=1):
        if not student_id or not name or not email:
            raise ValueError(
                "Student ID, name and email are mandatory."
            )

        if student_id in db.students:
            raise ValueError(
                f"Student with ID '{student_id}' already exists."
            )

        student = {
            "student_id": student_id,
            "name": name,
            "email": email,
            "semester": semester,
            "total_credits": 0
        }

        db.students[student_id] = student
        return student

    @staticmethod
    def get_student(student_id):
        return db.students.get(student_id)

    @staticmethod
    def add_course(course_id, name, credits, faculty_id, capacity=30):
        if not course_id or not name or not faculty_id:
            raise ValueError(
                "Course ID, name and faculty ID are mandatory."
            )

        if course_id in db.courses:
            raise ValueError(
                f"Course '{course_id}' already exists."
            )

        if credits <= 0:
            raise ValueError("Course credits must be greater than zero.")

        if faculty_id not in db.faculty:
            raise ValueError(
                f"Faculty '{faculty_id}' does not exist."
            )

        course = {
            "course_id": course_id,
            "name": name,
            "credits": credits,
            "faculty_id": faculty_id,
            "capacity": capacity,
            "enrolled": 0
        }

        db.courses[course_id] = course
        return course

    @staticmethod
    def get_course(course_id):
        return db.courses.get(course_id)

    @staticmethod
    def list_courses():
        return list(db.courses.values())

    @staticmethod
    def enroll_student(student_id, course_id):
        student = db.students.get(student_id)
        course = db.courses.get(course_id)

        if not student:
            raise ValueError(f"Student '{student_id}' not found.")

        if not course:
            raise ValueError(f"Course '{course_id}' not found.")

        # Credit limit: maximum 18 credits per semester
        if student["total_credits"] + course["credits"] > AcademicService.MAX_CREDITS:
            raise ValueError(
                f"Credit limit exceeded. Maximum allowed is "
                f"{AcademicService.MAX_CREDITS} credits."
            )

        # Capacity check
        if course["enrolled"] >= course["capacity"]:
            raise ValueError("Course capacity is full.")

        # Prevent duplicate enrollment
        for enrollment in db.enrollments:
            if (
                enrollment["student_id"] == student_id
                and enrollment["course_id"] == course_id
                and enrollment["status"] == "ACTIVE"
            ):
                raise ValueError(
                    "Student is already enrolled in this course."
                )

        enrollment = {
            "enrollment_id": f"E-{len(db.enrollments) + 1:04d}",
            "student_id": student_id,
            "course_id": course_id,
            "status": "ACTIVE"
        }

        db.enrollments.append(enrollment)
        student["total_credits"] += course["credits"]
        course["enrolled"] += 1

        return enrollment

    @staticmethod
    def assign_grade(student_id, course_id, grade):
        if student_id not in db.students:
            raise ValueError("Student not found.")

        if course_id not in db.courses:
            raise ValueError("Course not found.")

        grade = grade.upper()

        if grade not in Grade.GRADE_POINTS:
            raise ValueError(
                "Invalid grade. Use A, B, C, D, E or F."
            )

        enrolled = any(
            e["student_id"] == student_id
            and e["course_id"] == course_id
            and e["status"] == "ACTIVE"
            for e in db.enrollments
        )

        if not enrolled:
            raise ValueError(
                "Student is not enrolled in this course."
            )

        grade_record = {
            "student_id": student_id,
            "course_id": course_id,
            "grade": grade,
            "grade_points": Grade.grade_points(grade)
        }

        db.grades.append(grade_record)
        return grade_record

    @staticmethod
    def calculate_gpa(student_id):
        if student_id not in db.students:
            raise ValueError("Student not found.")

        student_grades = [
            g for g in db.grades
            if g["student_id"] == student_id
        ]

        if not student_grades:
            return 0.0

        total_points = 0
        total_courses = 0

        for grade in student_grades:
            total_points += grade["grade_points"]
            total_courses += 1

        return round(total_points / total_courses, 2)

    @staticmethod
    def reset():
        db.reset()
