from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Departamento(table=True):
    #Atributos.
    __tablename__ = "departamentos"

    id_departamento = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String, nullable=False)
    password = Column(String, unique=True, nullable=False)




