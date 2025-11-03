from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table

#La clase Base se va a usar para cargar las metadata y para definir atributos comúnes a todos los modelos.
class Base(DeclarativeBase):
    #Atributos comunes para todos los modelos.

    pass

#Tabla para resolver la relación de m:n de Profesor-Alumno.
profesor_alumno_tabla = Table(
    "profesor-alumno",
    Base.metadata,
    Column("profesor_id", Integer, ForeignKey("profesores.id_profesor"), primary_key=True),
    Column("alumno_id", Integer, ForeignKey("alumnos.id_alumno"), primary_key=True)
)

