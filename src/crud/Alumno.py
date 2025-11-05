from fastapi import HTTPException, status, Depends

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func

from data_base.models.models import Alumno
from data_base.schemas.Alumno import CreateAlumno, ReadAlumno, UpdateAlumno

#CRUD de Departamento.


#CREATE.
async def create_alumno(alumno_data: dict, db_session: AsyncSession) -> ReadAlumno:
    #Validar id.
    statement_id = await db_session.execute(select(Alumno).where(Alumno.id_alumno == alumno_data.get("id_alumno")))
    db_alumno_id = statement_id.scalar_one_or_none()

    if isinstance(db_alumno_id, Alumno):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El id ya existe")

    #Validar email.
    statement_email = await db_session.execute(select(Alumno).where(Alumno.email == alumno_data.get("email")))
    db_alumno_email = statement_email.scalar_one_or_none()

    if isinstance(db_alumno_email, Alumno):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya existe")

    #Crear db_alumno.
    db_alumno: Alumno = Alumno(**alumno_data)

    #Hashear contraseña.


    #Aplicar cambios en la Base de Datos.
    db_session.add(db_alumno)
    await db_session.commit()
    await db_session.refresh(db_alumno)

    #Crear response_alumno.
    response_alumno: ReadAlumno = ReadAlumno(id_alumno=db_alumno.id_alumno, nombre=db_alumno.nombre, facultad=db_alumno.facultad, email=db_alumno.email)

    return response_alumno

#READ.
async def read_alumno(id_alumno: int, db_session: AsyncSession) -> ReadAlumno:
    #Buscar alumno por id.
    statement_alumno = await db_session.execute(select(Alumno).where(Alumno.id_alumno == id_alumno))
    alumno: Alumno = statement_alumno.scalar_one_or_none()

    if alumno is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El id del Alumno no existe")

    #Response_alumno.
    response_alumno: ReadAlumno = ReadAlumno(id_alumno=alumno.id_alumno, nombre=alumno.nombre, facultad=alumno.facultad, email=alumno.email)

    return response_alumno

async def read_alumnos(limite: int, db_session: AsyncSession) -> List[Alumno]:
    statement_alumno = await db_session.execute(select(Alumno).offset(0).limit(limite))
    alumnos: List[Alumno] = statement_alumno.scalars().all()

    #Response_alumnos.
    response_alumnos: List[ReadAlumno] = alumnos
    
    return response_alumnos

#UPDATE.
async def update_alumno(id_alumno: int, update_alumno: dict, db_session: AsyncSession) -> ReadAlumno:
    statement_alumno= await db_session.execute(select(Alumno).where(Alumno.id_alumno == id_alumno))
    alumno: Alumno = statement_alumno.scalar_one_or_none()

    #Validar id_alumno.
    if alumno is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El id del Alumno no existe")
    
    #Validar email.
    statement_email = await db_session.execute(select(Alumno).where(Alumno.email == update_alumno.get("email")))
    alumno_email: Alumno = statement_email.scalar_one_or_none()

    if isinstance(alumno_email, Alumno):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya existe")

    #Actualización.
    actualizacion = update(Alumno).where(Alumno.id_alumno == id_alumno).values(update_alumno)

    #Aplicar cambios en la BD.
    await db_session.execute(actualizacion)
    await db_session.commit()
    await db_session.refresh(alumno)

    #Crear el response_alumno.
    response_alumno: ReadAlumno = ReadAlumno(id_alumno=alumno.id_alumno, nombre=alumno.nombre, facultad=alumno.facultad, email=alumno.email)

    return response_alumno




