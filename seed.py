from datetime import datetime
from random import randint, choice

import faker

from db_session import session
from models import Group, Student, Lecturer, Course, Grade


NUMBER_OF_STUDENTS = 50
NUMBER_OF_LECTURERS = 5
COURSES = [
    "Podstawy programowania",
    "Analiza matematyczna",
    "Bazy danych",
    "Administracja systemem operacyjnym",
    "Technologie sieciowe",
    "Programowanie obiektowe",
    "Metody analizy danych",
    "Inżynieria oprogramowania",
]
GROUPS = [
    ("1A",),
    ("1B",),
    ("1C",),
]
GRADES_SCOPE = [
    2,
    3,
    3.5,
    4,
    4.5,
    5,
]


def generate_fake_data(
    number_of_students, number_of_lecturers, courses, groups, grades_scope
) -> tuple[list, list, list, list]:
    """Function to generate fake data for students, lecturers, courses and grades"""
    for_students = []
    for_lecturers = []
    for_courses = []
    for_grades = []

    fake_data = faker.Faker("pl_PL")

    for _ in range(number_of_students):
        for_students.append(
            (
                fake_data.name(),
                fake_data.ascii_free_email(),
                randint(1, len(groups)),
            )
        )

    for _ in range(number_of_lecturers):
        for_lecturers.append((fake_data.name(), fake_data.ascii_free_email()))

    for course in courses:
        for_courses.append(
            (
                course,
                randint(1, number_of_lecturers),
                randint(1, len(groups)),
            )
        )

    for student_id in range(1, number_of_students + 1):
        for _ in range(randint(15, 20)):
            grade_date = datetime(2024, 1, randint(2, 31)).date()
            for_grades.append(
                (
                    choice(grades_scope),
                    grade_date,
                    randint(1, len(courses)),
                    student_id,
                )
            )
    return for_students, for_lecturers, for_courses, for_grades


def insert_data_to_db(students, lecturers, courses, grades):
    """Function to insert data to database"""
    for lecturer in lecturers:
        lecturer_obj = Lecturer(lecturer_name=lecturer[0], email=lecturer[1])
        session.add(lecturer_obj)
    for group in GROUPS:
        group_obj = Group(group_name=group[0])
        session.add(group_obj)
    for course in courses:
        course_obj = Course(
            course_name=course[0], lecturer_id=course[1], group_id=course[2]
        )
        session.add(course_obj)
    for student in students:
        student_obj = Student(
            student_name=student[0], email=student[1], group_id=student[2]
        )
        session.add(student_obj)
    for grade in grades:
        grade_obj = Grade(
            grade=grade[0], date_of=grade[1], course_id=grade[2], student_id=grade[3]
        )
        session.add(grade_obj)
    session.commit()


if __name__ == "__main__":
    for_students, for_lecturers, for_courses, for_grades = generate_fake_data(
        NUMBER_OF_STUDENTS, NUMBER_OF_LECTURERS, COURSES, GROUPS, GRADES_SCOPE
    )
    insert_data_to_db(for_students, for_lecturers, for_courses, for_grades)
