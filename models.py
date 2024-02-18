from datetime import datetime
from sqlalchemy import (
    Integer,
    Float,
    String,
    Date,
    ForeignKey,
)

from sqlalchemy.orm import (
    declarative_base,
    Mapped,
    mapped_column,
    relationship,
)
from db_session import engine


Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    group_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("groups.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=False,
    )
    group: Mapped[Group] = relationship("Group", backref="students")


class Lecturer(Base):
    __tablename__ = "lecturers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lecturer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_name: Mapped[str] = mapped_column(String(255), nullable=False)
    lecturer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("lecturers.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    lecturer: Mapped[Lecturer] = relationship("Lecturer", backref="courses")
    group_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("groups.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    group: Mapped[Group] = relationship("Group", backref="courses")


class Grade(Base):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    grade: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        info={"check_constraint": "grade IN (2, 3, 3.5, 4, 4.5, 5)"},
    )
    date_of: Mapped[datetime] = mapped_column(Date, nullable=False)
    course_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("courses.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    course: Mapped[Course] = relationship("Course", backref="grades")
    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    student: Mapped[Student] = relationship("Student", backref="grades")


Base.metadata.create_all(engine)
