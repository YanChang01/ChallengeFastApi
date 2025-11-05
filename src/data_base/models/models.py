from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

from data_base.models.base import Base, profesor_alumno_tabla


class Departamento(Base):
    #Atributos.
    __tablename__ = 'departamentos'

    id_departamento: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    descripcion: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    #Relaciones. (Un Departamento tiene muchos Profesores)
    profesores: Mapped[List["Profesor"]] = relationship("Profesor", back_populates="departamentos")


class Profesor(Base):
    #Atributos.
    __tablename__ = 'profesores'

    id_profesor: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    asignatura: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    departamento_id: Mapped[int] = mapped_column(Integer, ForeignKey("departamentos.id_departamento")) #Relacion de 1:1 (Un profesor solo tiene un departamento)

    #Relaciones. 
    #(Profesor - Departamento)
    departamentos: Mapped["Departamento"] = relationship("Departamento", back_populates="profesores") #Relación inversa de 1:n (Un departamento tiene muchos profesores)

    #(Profesor - Alumno)
    #Relacion de m:n (Un alumno tiene muchos profesores y un profesor tiene muchos alumnos)
    #Hay que utilizar la tabla intermedia profesor_alumno_tabla para establecer la relación.
    alumnos: Mapped[List["Alumno"]] = relationship(secondary=profesor_alumno_tabla, back_populates="profesores")


class Alumno(Base):
    #Atributos.
    __tablename__ = 'alumnos'

    id_alumno: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    facultad: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    #Relación Alumnmo - Profesor.
    profesores: Mapped[List["Profesor"]] = relationship(secondary=profesor_alumno_tabla, back_populates="alumnos")




