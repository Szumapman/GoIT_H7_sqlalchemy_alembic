from sqlalchemy import select, desc, func

from models import Group, Student, Lecturer, Course, Grade
from db_session import session


def select_1():
    stmt = (
        select(
            Student.id,
            Student.student_name,
            func.avg(Grade.grade).label("avg_grade"),
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )
    return session.execute(stmt)


def select_2(course_id_number):
    subquery = (
        select(
            Grade.course_id, Grade.student_id, func.avg(Grade.grade).label("avg_grade")
        )
        .where(Grade.course_id == course_id_number)
        .group_by(Grade.student_id, Grade.course_id)
        .subquery()
    )
    stmt = (
        select(subquery.c.avg_grade, Student.student_name, Course.course_name)
        .join(Student, Student.id == subquery.c.student_id)
        .join(Course, Course.id == subquery.c.course_id)
        .where(
            subquery.c.avg_grade
            == select(func.max(subquery.c.avg_grade)).scalar_subquery()
        )
    )
    return session.execute(stmt)


def select_3(course_id_number):
    stmt = (
        select(
            Course.course_name.label("przedmiot"),
            Group.group_name.label("klasa"),
            func.avg(Grade.grade).label("avg_grade"),
        )
        .join(Student, Grade.student_id == Student.id)
        .join(Course, Grade.course_id == Course.id)
        .join(Group, Student.group_id == Group.id)
        .where(Course.id == course_id_number)
        .group_by(Course.course_name, Group.group_name)
    )
    return session.execute(stmt)


def select_4():
    stmt = (
        select(
            Group.group_name.label("klasa"),
            func.avg(Grade.grade).label("srednia_ocen_klasy"),
        )
        .join(Student, Grade.student_id == Student.id)
        .join(Course, Grade.course_id == Course.id)
        .join(Group, Student.group_id == Group.id)
        .group_by(Group.group_name)
        .order_by(desc("srednia_ocen_klasy"))
    )
    return session.execute(stmt)


def select_5(lecturer_id_number):
    stmt = (
        select(Course.course_name, Lecturer.lecturer_name.label("wykladowca"))
        .join(Lecturer, Course.lecturer_id == Lecturer.id)
        .where(Lecturer.id == lecturer_id_number)
    )
    return session.execute(stmt)


def select_6(group_id_number):
    stmt = (
        select(Student.student_name, Group.group_name)
        .join(Group, Student.group_id == Group.id)
        .where(Group.id == group_id_number)
    )
    return session.execute(stmt)


def select_7(group_id_number, course_id_number):
    stmt = (
        select(Student.student_name, Grade.grade, Course.course_name, Group.group_name)
        .join(Grade, Student.id == Grade.student_id)
        .join(Course, Grade.course_id == Course.id)
        .join(Group, Student.group_id == Group.id)
        .where(Course.id == course_id_number, Group.id == group_id_number)
        .order_by(Student.student_name)
    )
    return session.execute(stmt)


# treść zapytania w pracy domowej 7 jest logicznie różna od tej w zadaniu 6,
# dlatego odpowiedzi są inne :)
def select_8(lecturer_id_number):
    stmt = (
        select(
            Course.course_name.label("przedmiot"),
            Lecturer.lecturer_name.label("wykladowca"),
            func.avg(Grade.grade).label("srednia_ocen"),
        )
        .join(Course, Grade.course_id == Course.id)
        .join(Lecturer, Course.lecturer_id == Lecturer.id)
        .where(Lecturer.id == lecturer_id_number)
        .group_by(Course.id, Lecturer.lecturer_name)
    )
    return session.execute(stmt)


# treść zapytania w pracy domowej 7 jest nie do odgadnięcia ;),
# dlatego zapytanie odpowiada na pytanie 9 z zadania domowego nr 6
def select_9(student_id_number):
    stmt = (
        select(
            Student.student_name.label("student"), Course.course_name.label("przedmiot")
        )
        .join(Student, Course.group_id == Student.group_id)
        .where(Student.id == student_id_number)
    )
    return session.execute(stmt)


def select_10(lecturer_id_number, student_id_number):
    stmt = (
        select(
            Course.course_name.label("przedmiot"),
            Lecturer.lecturer_name.label("wykladowca"),
            Student.student_name.label("student"),
        )
        .join(Lecturer, Course.lecturer_id == Lecturer.id)
        .join(Student, Student.group_id == Course.group_id)
        .where(Lecturer.id == lecturer_id_number, Student.id == student_id_number)
    )
    return session.execute(stmt)


def select_11(lecturer_id_number, student_id_number):
    stmt = (
        select(
            Lecturer.lecturer_name.label("wykladowca"),
            Student.student_name.label("student"),
            func.avg(Grade.grade).label("srednia_ocen"),
        )
        .join(Course, Grade.course_id == Course.id)
        .join(Student, Grade.student_id == Student.id)
        .join(Lecturer, Course.lecturer_id == Lecturer.id)
        .where(Lecturer.id == lecturer_id_number, Student.id == student_id_number)
        .group_by(Lecturer.lecturer_name, Student.student_name)
    )
    return session.execute(stmt)


def select_12(group_id_number, course_id_number):
    stmt = (
        select(
            Grade.date_of.label("data"),
            Course.course_name.label("przedmiot"),
            Student.student_name,
            Grade.grade.label("ocena"),
        )
        .join(Grade, Student.id == Grade.student_id)
        .join(Course, Grade.course_id == Course.id)
        .where(
            Course.id == course_id_number,
            Student.group_id == group_id_number,
            Grade.date_of == (select(func.max(Grade.date_of)).scalar_subquery()),
        )
    )
    return session.execute(stmt)


SELECTS = {
    "Znajdź 5 studentów z najwyższą średnią ocen ze wszystkich przedmiotów.": select_1,
    "Znajdź studenta (studentów) z najwyższą średnią ocen z określonego przedmiotu.": lambda: select_2(
        1
    ),
    "Znajdź średni wynik w grupach dla określonego przedmiotu.": lambda: select_3(1),
    "Znajdź średni wynik w grupie (w całej tabeli ocen).": select_4,
    "Znajdź przedmioty, których uczy określony wykładowca.": lambda: select_5(1),
    "Znajdź listę studentów w określonej grupie.": lambda: select_6(3),
    "Znajdź oceny studentów w określonej grupie z danego przedmiotu.": lambda: select_7(
        3, 1
    ),
    "Znajdź średnią ocenę wystawioną przez określonego wykładowcę z jego przedmiotów.": lambda: select_8(
        3
    ),
    "Lista kursów, na które uczęszcza uczeń - z zad. 6/nPyt z zad 7: Znajdź listę przedmiotów zaliczonych ...": lambda: select_9(
        11
    ),
    "Znajdź listę kursów prowadzonych przez określonego wykładowcę dla określonego studenta.": lambda: select_10(
        2, 7
    ),
    # Zadania dodatkowe
    "Średnia ocena, jaką określony wykładowca wystawił pewnemu studentowi.": lambda: select_11(
        2, 7
    ),
    "Oceny studentów w określonej grupie z określonego przedmiotu na ostatnich zajęciach.": lambda: select_12(
        1, 3
    ),
}


if __name__ == "__main__":
    i = 1
    for question, answer_select in SELECTS.items():
        print(f"Zadanie {i}: {question}:")
        print(*answer_select())
        i += 1
