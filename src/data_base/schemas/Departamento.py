from data_base.schemas.base import Base

class CreateDepartamento(Base):
    id_departamento : int
    nombre: str
    descripcion: str
    password: str

class ReadDepartamento(Base):
    id_departamento: int
    nombre: str
    descripcion: str

    class Config:
        orm_mode = True

class UpdateDepartamento(Base):
    nombre: str
    descripcion: str










