class Student:
    """Student entity."""

    def __init__(self, student_id, name, email, semester=1):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.semester = semester
