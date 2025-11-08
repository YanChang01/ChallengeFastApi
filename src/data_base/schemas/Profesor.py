from pydantic import EmailStr
from data_base.schemas.base import Base

class CreateProfesor(Base):
    id_profesor: int
    nombre: str
    asignatura: str
    email: EmailStr
    password: str
    departamento_id: int

class ReadProfesor(Base):
    id_profesor: int
    nombre: str
    asignatura: str
    email: EmailStr
    departamento_id: int

    model_config = {
        "from_attributes": True
    }

class UpdateProfesor(Base):
    nombre: str
    asignatura: str
    email: EmailStr
    departamento_id: int







