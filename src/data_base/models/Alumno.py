from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.data_base.models.base import Base

class Alumno(Base):
    #Atributos.
    __tablename__ = "alumnos"

    id_alumno = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    facultad = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, unique=True, nullable=False)

