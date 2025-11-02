from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import EmailStr

class Alumno(table=True):
    #Atributos.
    __tablename__ = "alumnos"

    id_alumno = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    facultad = Column(String, nullable=False)
    email = Column(EmailStr, unique=True, index=True, nullable=False)
    password = Column(String, unique=True, nullable=False)

