from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.data_base.models.base import Base

class Departamento(Base):
    #Atributos.
    __tablename__ = "departamentos"

    id_departamento = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String, nullable=False)
    password = Column(String, unique=True, nullable=False)

    #Relaciones. (Un Departamento tiene muchos Profesores)
    profesores = relationship("Profesor", back_populates="departamento")




