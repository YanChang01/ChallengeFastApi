from data_base.schemas.base import Base

class CreateDepartamento(Base):
    id_departamento : int
    nombre: str
    descripcion: str

class ReadDepartamento(Base):
    id_departamento: int
    nombre: str
    descripcion: str

    model_config = {
        "from_attributes": True
    }

class UpdateDepartamento(Base):
    nombre: str
    descripcion: str










