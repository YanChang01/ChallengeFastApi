from pydantic import EmailStr
from src.data_base.schemas.base import Base

class CreateProfesor(Base):
    id: str
    nombre: str
    asignatura: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class ReadProfesor(Base):
    id: str
    nombre: str
    asignatura: str
    email: EmailStr

    class Config:
        orm_mode = True

class UpdateProfesor(Base):
    nombre: str
    asignatura: str
    email: EmailStr

    class Config:
        orm_mode = True






