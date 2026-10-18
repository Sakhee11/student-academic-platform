import pytest

from database.db import db
from app.services.academic_service import AcademicService


@pytest.fixture(autouse=True)
def reset_database():
    db.reset()
    yield
    db.reset()


def test_student_enrollment_success():
    enrollment = AcademicService.enroll_student(
        "S101",
        "C101"
    )

    assert enrollment["status"] == "ACTIVE"
    assert enrollment["student_id"] == "S101"
    assert db.students["S101"]["total_credits"] == 4


def test_duplicate_enrollment_fails():
    AcademicService.enroll_student("S101", "C101")

    with pytest.raises(ValueError, match="already enrolled"):
        AcademicService.enroll_student(
            "S101",
            "C101"
        )


def test_credit_limit_enforced():
    AcademicService.add_course(
        "C201",
        "Course 1",
        6,
        "F101"
    )

    AcademicService.add_course(
        "C202",
        "Course 2",
        6,
        "F101"
    )

    AcademicService.add_course(
        "C203",
        "Course 3",
        6,
        "F101"
    )

    AcademicService.add_course(
        "C204",
        "Course 4",
        4,
        "F101"
    )

    AcademicService.enroll_student("S101", "C201")
    AcademicService.enroll_student("S101", "C202")
    AcademicService.enroll_student("S101", "C203")

    assert db.students["S101"]["total_credits"] == 18

    with pytest.raises(ValueError, match="Credit limit exceeded"):
        AcademicService.enroll_student(
            "S101",
            "C204"
        )


def test_gpa_calculation():
    AcademicService.enroll_student("S101", "C101")
    AcademicService.enroll_student("S101", "C102")

    AcademicService.assign_grade(
        "S101",
        "C101",
        "A"
    )

    AcademicService.assign_grade(
        "S101",
        "C102",
        "B"
    )

    gpa = AcademicService.calculate_gpa("S101")

    assert gpa == 9.0
