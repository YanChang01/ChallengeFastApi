from pydantic import EmailStr
from data_base.schemas.base import Base

class CreateAlumno(Base):
    id_alumno: int
    nombre: str
    facultad: str
    email: EmailStr
    password: str

class ReadAlumno(Base):
    id_alumno: int
    nombre: str
    facultad: str
    email: EmailStr

    class Config:
        orm_mode = True

class UpdateAlumno(Base):
    nombre: str
    facultad: str
    email: EmailStr






