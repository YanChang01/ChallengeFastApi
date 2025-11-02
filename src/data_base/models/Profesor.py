from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import EmailStr


class Profesor(table=True):
    #Atributos.
    __tablename__ = "profesores"

    id_profesor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    asignatura = Column(String, nullable=False)
    email = Column(EmailStr, unique=True, index=True, nullable=False)
    password = Column(String, unique=True, nullable=False)





