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

    #Aplicar cambios en la Base de Datos.
    db_session.add(db_alumno)
    await db_session.commit()
    await db_session.refresh(db_alumno)

    #Crear response_alumno.
    return ReadAlumno.model_validate(db_alumno)

#READ.
async def read_alumno(id_alumno: int, db_session: AsyncSession) -> ReadAlumno:
    #Buscar alumno por id.
    statement_alumno = await db_session.execute(select(Alumno).where(Alumno.id_alumno == id_alumno).where(Alumno.is_deleted == False))
    alumno: Alumno = statement_alumno.scalar_one_or_none()

    if alumno is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El id del Alumno no existe")

    #Response_alumno.
    return ReadAlumno.model_validate(alumno)

async def read_alumnos(limite: int, db_session: AsyncSession) -> List[ReadAlumno]:
    statement_alumnos = await db_session.execute(select(Alumno).where(Alumno.is_deleted == False).offset(0).limit(limite))
    alumnos: List[Alumno] = statement_alumnos.scalars().all()

    #Response_alumnos.
    return [ReadAlumno.model_validate(a) for a in alumnos]

async def filtrar_eliminados(limite: int, db_session: AsyncSession) -> List[ReadAlumno]:
    statement_alumnos = await db_session.execute(select(Alumno).where(Alumno.is_deleted == True).limit(limite))
    alumnos: List[Alumno] = statement_alumnos.scalars().all()

    #Response_alumnos.
    return [ReadAlumno.model_validate(a) for a in alumnos]

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
    return ReadAlumno.model_validate(alumno)

#DELETE.
async def delete_alumno(id_alumno: int, db_session: AsyncSession) -> bool:
    consulta = select(Alumno).where(Alumno.id_alumno == id_alumno)
    statement_alumno = await db_session.execute(consulta)
    db_alumno = statement_alumno.scalar_one_or_none()

    #Validar si el registro existe y no se ha marcado como eliminado.
    if not db_alumno or db_alumno.is_deleted:
        return False

    #Actualizar las columnas soft-delete.
    statement_update = update(Alumno).where(Alumno.id_alumno == id_alumno).values(is_deleted=True, deleted_at=func.now())

    #Aplicar cambios en la BD.
    await db_session.execute(statement_update)
    await db_session.commit()

    return True


