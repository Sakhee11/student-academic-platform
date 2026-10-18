import pytest

from database.db import db
from app.services.academic_service import AcademicService


@pytest.fixture(autouse=True)
def reset_database():
    db.reset()
    yield
    db.reset()


def test_add_course_success():
    course = AcademicService.add_course(
        "C200",
        "Artificial Intelligence",
        4,
        "F101"
    )

    assert course["course_id"] == "C200"
    assert course["credits"] == 4
    assert course["enrolled"] == 0


def test_duplicate_course_fails():
    with pytest.raises(ValueError, match="already exists"):
        AcademicService.add_course(
            "C101",
            "Duplicate Course",
            4,
            "F101"
        )


def test_invalid_credits_fail():
    with pytest.raises(ValueError, match="greater than zero"):
        AcademicService.add_course(
            "C200",
            "Invalid Course",
            0,
            "F101"
        )
