class Course:
    """Course entity."""

    def __init__(self, course_id, name, credits, faculty_id, capacity=30):
        self.course_id = course_id
        self.name = name
        self.credits = credits
        self.faculty_id = faculty_id
        self.capacity = capacity
