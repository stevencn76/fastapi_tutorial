from typing import Optional, List, Set, Union

import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, Response, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Integer, select, asc
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column


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


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
