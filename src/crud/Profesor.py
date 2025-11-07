from fastapi import HTTPException, status, Depends

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func

from data_base.models.models import Profesor, Departamento
from data_base.schemas.Profesor import CreateProfesor, ReadProfesor, UpdateProfesor

#CREATE.
async def create_profesor(profesor_data: dict, db_session: AsyncSession) -> ReadProfesor:
    #Validar id.
    statement_id = await db_session.execute(select(Profesor).where(Profesor.id_profesor == profesor_data.get("id_profesor")))
    db_profesor_id = statement_id.scalar_one_or_none()

    if isinstance(db_profesor_id, Profesor):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El id ya existe")

    #Validar email.
    statement_email = await db_session.execute(select(Profesor).where(Profesor.email == profesor_data.get("email")))
    db_profesor_email = statement_email.scalar_one_or_none()

    if isinstance(db_profesor_email, Profesor):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya existe")

    #Validar departamento_id.
    statement_departamento_id = await db_session.execute(select(Departamento).where(Departamento.id_departamento == profesor_data.get("departamento_id")))
    db_departamento_id = statement_departamento_id.scalar_one_or_none()

    if db_departamento_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un departamento con ese id")

    #Crear db_profesor.
    db_profesor: Profesor = Profesor(**profesor_data)

    #Hashear contraseña.


    #Aplicar cambios en la Base de Datos.
    db_session.add(db_profesor)
    await db_session.commit()
    await db_session.refresh(db_profesor)

    #Crear response_profesor.
    return ReadProfesor.model_validate(db_profesor)

#READ.
async def read_profesor(id_profesor: int, db_session: AsyncSession) -> ReadProfesor:
    #Buscar profesor por id.
    statement_profesor = await db_session.execute(select(Profesor).where(Profesor.id_profesor == id_profesor).where(Profesor.is_deleted == False))
    profesor: Profesor = statement_profesor.scalar_one_or_none()

    if profesor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El id del Profesor no existe")

    #Response_profesor.
    return ReadProfesor.model_validate(profesor)

async def read_profesores(limite: int, db_session: AsyncSession) -> List[ReadProfesor]:
    statement_profesores = await db_session.execute(select(Profesor).where(Profesor.is_deleted == False).limit(limite))
    profesores: List[Profesor] = statement_profesores.scalars().all()

    #Response_profesores.
    return [ReadProfesor.model_validate(p) for p in profesores]

async def filtrar_eliminados(limite: int, db_session: AsyncSession) -> List[ReadProfesor]:
    statement_profesores = await db_session.execute(select(Profesor).where(Profesor.is_deleted == True))
    profesores: List[Profesor] = statement_profesores.scalars().all()

    #Response_profesores.
    return [ReadProfesor.model_validate(p) for p in profesores]

#UPDATE.
async def update_profesor(id_profesor: int, update_profesor: dict, db_session: AsyncSession) -> ReadProfesor:
    statement_profesor = await db_session.execute(select(Profesor).where(Profesor.id_profesor == id_profesor))
    profesor: Profesor = statement_profesor.scalar_one_or_none()

    #Validar id_profesor.
    if profesor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El id no existe")
    
    #Validar email.
    statement_email = await db_session.execute(select(Profesor).where(Profesor.email == update_profesor.get("email")))
    profesor_email: Profesor = statement_email.scalar_one_or_none()

    if isinstance(profesor_email, Profesor):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya existe")

    #Validar departamento_id.
    statement_departamento_id = await db_session.execute(select(Departamento).where(Departamento.id_departamento == update_profesor.get("departamento_id")))
    departamento_id: Departamento = statement_departamento_id.scalar_one_or_none()

    if departamento_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El departamento_id no existe")

    #Actualización.
    actualizacion = update(Profesor).where(Profesor.id_profesor == id_profesor).values(update_profesor)

    #Aplicar cambios en la BD.
    await db_session.execute(actualizacion)
    await db_session.commit()
    await db_session.refresh(profesor)

    #Crear el response_profesor.
    return ReadProfesor.model_validate(profesor)

#DELETE.
async def delete_profesor(id_profesor: int, db_session: AsyncSession) -> bool:
    consulta = select(Profesor).where(Profesor.id_profesor == id_profesor)
    statement_profesor = await db_session.execute(consulta)
    db_profesor = statement_profesor.scalar_one_or_none()

    #Validar si el registro existe y no se ha marcado como eliminado.
    if not db_profesor or db_profesor.is_deleted:
        return False

    #Actualizar las columnas soft-delete.
    statement_update = update(Profesor).where(Profesor.id_profesor == id_profesor).values(is_deleted=True, deleted_at=func.now())

    #Aplicar cambios en la BD.
    await db_session.execute(statement_update)
    await db_session.commit()

    return True





