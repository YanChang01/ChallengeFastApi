from fastapi import HTTPException, status, Depends

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func

from data_base.models.models import Departamento
from data_base.schemas.Departamento import CreateDepartamento, ReadDepartamento, UpdateDepartamento

#CRUD de Departamento.

#CREATE.
async def create_departamento(departamento_data: dict, db_session: AsyncSession) -> ReadDepartamento:
    #Validar id.
    statement_id = await db_session.execute(select(Departamento).where(Departamento.id_departamento == departamento_data.get("id_departamento")))
    db_departamento_id = statement_id.scalar_one_or_none()

    if isinstance(db_departamento_id, Departamento):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El id ya existe")

    #Validar nombre.
    statement_nombre = await db_session.execute(select(Departamento).where(Departamento.nombre == departamento_data.get("nombre")))
    db_departamento_nombre = statement_nombre.scalar_one_or_none()

    if isinstance(db_departamento_nombre, Departamento):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre ya existe")

    #Crear db_departamento.
    db_departamento: Departamento = Departamento(**departamento_data)

    #Hashear contraseña.

    #Aplicar cambios en la Base de Datos.
    db_session.add(db_departamento)
    await db_session.commit()
    await db_session.refresh(db_departamento)

    #Crear response_departamento.
    response_departamento: ReadDepartamento = ReadDepartamento(id_departamento=db_departamento.id_departamento, nombre=db_departamento.nombre, descripcion=db_departamento.descripcion)

    return response_departamento

#READ.
async def read_departamento(id_departamento: int, db_session: AsyncSession) -> ReadDepartamento:
    #Buscar departamento por id.
    statement_departamento = await db_session.execute(select(Departamento).where(Departamento.id_departamento == id_departamento))
    departamento: Departamento = statement_departamento.scalar_one_or_none()

    if departamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El id del Departamento no existe")

    #Response_departamento.
    response_departamento: ReadDepartamento = ReadDepartamento(id_departamento=departamento.id_departamento, nombre=departamento.nombre, descripcion=departamento.descripcion)

    return response_departamento

async def read_departamentos(limite: int, db_session: AsyncSession) -> List[Departamento]:
    statement_departamentos = await db_session.execute(select(Departamento).offset(0).limit(limite))
    departamentos: List[Departamento] = statement_departamentos.scalars().all()

    #Response_departamento.
    response_departamento: List[ReadDepartamento] = departamentos
    return response_departamento

#UPDATE.
async def update_departamento(id_departamento: int, update_departamento: dict, db_session: AsyncSession) -> ReadDepartamento:
    statement_departamento = await db_session.execute(select(Departamento).where(Departamento.id_departamento == id_departamento))
    departamento: Departamento = statement_departamento.scalar_one_or_none()

    if departamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El id del Departamento no existe")
    
    #Actualización.
    actualizacion = update(Departamento).where(Departamento.id_departamento == id_departamento).values(update_departamento)

    #Aplicar cambios en la BD.
    await db_session.execute(actualizacion)
    await db_session.commit()
    await db_session.refresh(departamento)

    #Crear el response_departamento.
    response_departamento: ReadDepartamento = ReadDepartamento(id_departamento=departamento.id_departamento, nombre=departamento.nombre, descripcion=departamento.descripcion)

    return response_departamento

#DELETE.







