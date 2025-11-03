from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.data_base.models.base import Base, profesor_alumno_tabla

class Profesor(Base):
    #Atributos.
    __tablename__ = "profesores"

    id_profesor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    asignatura = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    

    #Relaciones. 
    #(Profesor - Departamento)
    departamento_id = Column(Integer, ForeignKey("departamentos.id_departamento")) #Relacion de 1:1 (Un profesor solo tiene un departamento)
    departamento = relationship("Departamento", back_populates="profesores") #Relación inversa de 1:n (Un departamento tiene muchos profesores)

    #(Profesor - Alumno)
    #Relacion de m:n (Un alumno tiene muchos profesores y un profesor tiene muchos alumnos)
    #Hay que utilizar la tabla secundaria profesor_alumno_tabla para establecer la relación.
    alumnos = relationship("Alumno", secondary=profesor_alumno_tabla, back_populates="profesores")



