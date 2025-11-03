from pydantic import EmailStr
from src.data_base.schemas.base import Base

class CreateAlumno(Base):
    id: int
    nombre: str
    facultad: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class ReadAlumno(Base):
    id: int
    nombre: str
    facultad: str
    email: EmailStr

    class Config:
        orm_mode = True

class UpdateAlumno(Base):
    nombre: str
    facultad: str
    email: EmailStr

    class Config:
        orm_mode = True





