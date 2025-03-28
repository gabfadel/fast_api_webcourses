from typing import List, Optional
from pydantic import BaseModel

class DisciplineBase(BaseModel):
    name: str

class DisciplineCreate(DisciplineBase):
    teacher_id: Optional[int] = None

class DisciplineOut(DisciplineBase):
    id: int
    class Config:
        orm_mode = True

class TeacherBase(BaseModel):
    name: str
    phone: Optional[str] = None

class TeacherCreate(TeacherBase):
    password: str
    disciplines: Optional[List[int]] = [] 
    
class TeacherOut(TeacherBase):
    id: int
    disciplines: List[DisciplineOut] = []
    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    name: str
    phone: Optional[str] = None

class StudentCreate(StudentBase):
    password: str
    disciplines: Optional[List[int]] = [] 

class StudentOut(StudentBase):
    id: int
    class Config:
        orm_mode = True