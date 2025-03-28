from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.users.models import User

class Teacher(User, SQLModel, table=True):
    __tablename__ = "teacher"
    disciplines: List["Discipline"] = Relationship(
        back_populates="teacher",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class Discipline(SQLModel, table=True):
    __tablename__ = "discipline"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    teacher_id: Optional[int] = Field(default=None, foreign_key="teacher.id")
    teacher: Optional[Teacher] = Relationship(
        back_populates="disciplines",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    students: List["DisciplineStudentLink"] = Relationship(
        back_populates="discipline",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class DisciplineStudentLink(SQLModel, table=True):
    __tablename__ = "discipline_student_link"
    discipline_id: Optional[int] = Field(default=None, foreign_key="discipline.id", primary_key=True)
    student_id: Optional[int] = Field(default=None, foreign_key="student.id", primary_key=True)
    discipline: "Discipline" = Relationship(
        back_populates="students",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    student: "Student" = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class Student(User, SQLModel, table=True):
    __tablename__ = "student"
    disciplines: List["DisciplineStudentLink"] = Relationship(
        back_populates="student",
        sa_relationship_kwargs={"lazy": "selectin"}
    )