import pytest

from database.db import db
from app.services.academic_service import AcademicService


@pytest.fixture(autouse=True)
def reset_database():
    db.reset()
    yield
    db.reset()


def test_add_student_success():
    student = AcademicService.add_student(
        "S200",
        "Grace Hopper",
        "grace@university.edu",
        2
    )

    assert student["student_id"] == "S200"
    assert student["name"] == "Grace Hopper"
    assert student["total_credits"] == 0


def test_duplicate_student_fails():
    with pytest.raises(ValueError, match="already exists"):
        AcademicService.add_student(
            "S101",
            "Duplicate Alice",
            "duplicate@university.edu"
        )


def test_missing_student_fields_fail():
    with pytest.raises(
        ValueError,
        match="mandatory"
    ):
        AcademicService.add_student(
            "",
            "Test User",
            "test@university.edu"
        )
