from src.data_base.schemas.base import Base

class CreateDepartamento(Base):
    id : int
    nombre: str
    descripcion: str
    password: str

    class Config:
        orm_mode = True

class ReadDepartamento(Base):
    id: int
    nombre: str
    descripcion: str

    class Config:
        orm_mode = True

class UpdateDepartamento(Base):
    nombre: str
    descripcion: str

    class Config:
        orm_mode = True









