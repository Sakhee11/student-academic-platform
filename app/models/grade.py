class Grade:
    """Grade entity."""

    GRADE_POINTS = {
        "A": 10,
        "B": 8,
        "C": 6,
        "D": 5,
        "E": 4,
        "F": 0
    }

    def __init__(self, student_id, course_id, grade):
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade

    @classmethod
    def grade_points(cls, grade):
        return cls.GRADE_POINTS.get(grade.upper(), 0)
