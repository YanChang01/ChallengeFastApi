from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.data_base.models.base import Base

class Profesor(Base):
    #Atributos.
    __tablename__ = "profesores"

    id_profesor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    asignatura = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, unique=True, nullable=False)





