from typing import Optional, List, Set, Union

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, Response, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Integer, select, asc, update
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column


def set_attrs(obj, data: dict):
    if data:
        for key, value in data.items():
            setattr(obj, key, value)


class Base(DeclarativeBase):
    pass


engine = create_engine('mysql+mysqldb://root:test@localhost/testdb', echo=True)


# Define database models
class StudentEntity(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
app = FastAPI()


# Define API models
class StudentBase(BaseModel):
    name: str
    gender: str


class StudentCreate(StudentBase):
    ...


class StudentUpdate(StudentBase):
    ...


class StudentOut(StudentBase):
    id: int


def get_db_session():
    db_session = Session()

    try:
        yield db_session
    finally:
        db_session.close()


@app.get('/students', response_model=List[StudentOut])
async def get_students(db_session: Session = Depends(get_db_session)):
    query = select(StudentEntity).order_by(asc(StudentEntity.name))
    return db_session.execute(query).scalars().all()


@app.post('/students', response_model=StudentOut)
async def create_student(student: StudentCreate, db_session: Session = Depends(get_db_session)):
    query = select(StudentEntity).where(StudentEntity.name == student.name)
    records = db_session.execute(query).scalars().all()
    if records:
        raise HTTPException(status_code=400, detail=f'Student {student.name} already exists')
    
    student_entity = StudentEntity(name=student.name, gender=student.gender)
    db_session.add(student_entity)
    db_session.commit()

    return student_entity


def check_student_exist(student_id: int, db_session: Session):
    query = select(StudentEntity).where(StudentEntity.id == student_id)
    exist_student = db_session.execute(query).scalar()
    if not exist_student:
        raise HTTPException(status_code=404, detail=f'Student id({student_id}) not found')

    return exist_student


@app.put('/students/{student_id}', response_model=StudentOut)
async def update_student(*, student_id: int = Path(...), student: StudentUpdate,
                         db_session: Session = Depends(get_db_session)):
    exist_student = check_student_exist(student_id, db_session)

    # update_query = update(StudentEntity).values(student.model_dump()).where(StudentEntity.id == student_id)
    # db_session.execute(update_query)

    # exist_student.name = student.name
    # exist_student.gender = student.gender

    set_attrs(exist_student, student.model_dump())

    db_session.commit()

    return exist_student


@app.delete('/students/{student_id}', response_model=StudentOut)
async def delete_student(student_id: int = Path(...), db_session: Session = Depends(get_db_session)):
    exist_student = check_student_exist(student_id, db_session)

    db_session.delete(exist_student)

    return exist_student


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
