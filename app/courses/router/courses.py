from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import async_session
from app.courses import models
from app.courses.schemas import (
    TeacherCreate, TeacherOut,
    StudentCreate, StudentOut,
    DisciplineCreate, DisciplineOut
)
from app.users.utils import hash_password

router = APIRouter(prefix="/courses", tags=["courses"])

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# GET all teachers
@router.get("/teachers", response_model=list[TeacherOut])
async def get_teachers(db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(models.Teacher))
    return results.scalars().all()

# GET teacher by id
@router.get("/teacher/{id}", response_model=TeacherOut)
async def get_teacher(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Teacher).where(models.Teacher.id == id))
    teacher = result.scalar_one_or_none()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

# POST create teacher
@router.post("/teacher", response_model=TeacherOut)
async def create_teacher(data: TeacherCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Teacher).where(models.Teacher.name == data.name))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Teacher with this name already exists"
        )
    teacher = models.Teacher(
        name=data.name,
        phone=data.phone,
        password_hash=hash_password(data.password)
    )
    db.add(teacher)
    await db.commit()
    await db.refresh(teacher)

    if data.disciplines:
        for disc_id in data.disciplines:
            disc_result = await db.execute(select(models.Discipline).where(models.Discipline.id == disc_id))
            discipline = disc_result.scalar_one_or_none()
            if not discipline:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Discipline with id {disc_id} not found"
                )
            discipline.teacher_id = teacher.id
            db.add(discipline)
        await db.commit()
        await db.refresh(teacher)
        
    return teacher


# GET all students
@router.get("/students", response_model=list[StudentOut])
async def get_students(db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(models.Student))
    return results.scalars().all()

# GET student by id
@router.get("/student/{id}", response_model=StudentOut)
async def get_student(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).where(models.Student.id == id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# POST create student
@router.post("/student", response_model=StudentOut)
async def create_student(data: StudentCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).where(models.Student.name == data.name))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student with this name already exists"
        )
    student = models.Student(
        name=data.name,
        phone=data.phone,
        password_hash=hash_password(data.password)
    )
    db.add(student)
    await db.commit()
    await db.refresh(student)

    if data.disciplines:
        for disc_id in data.disciplines:
            disc_result = await db.execute(select(models.Discipline).where(models.Discipline.id == disc_id))
            discipline = disc_result.scalar_one_or_none()
            if not discipline:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Discipline with id {disc_id} not found"
                )
            link = models.DisciplineStudentLink(discipline_id=disc_id, student_id=student.id)
            db.add(link)
        await db.commit()
        await db.refresh(student)
    return student

# GET all disciplines
@router.get("/disciplines", response_model=list[DisciplineOut])
async def get_disciplines(db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(models.Discipline))
    return results.scalars().all()

# GET discipline by id
@router.get("/discipline/{id}", response_model=DisciplineOut)
async def get_discipline(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Discipline).where(models.Discipline.id == id))
    discipline = result.scalar_one_or_none()
    if not discipline:
        raise HTTPException(status_code=404, detail="Discipline not found")
    return discipline

# POST create discipline com verificação de duplicidade (usando o name)
@router.post("/discipline", response_model=DisciplineOut)
async def create_discipline(data: DisciplineCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Discipline).where(models.Discipline.name == data.name))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Discipline with this name already exists"
        )
    discipline = models.Discipline(
        name=data.name,
        teacher_id=data.teacher_id
    )
    db.add(discipline)
    await db.commit()
    await db.refresh(discipline)
    return discipline