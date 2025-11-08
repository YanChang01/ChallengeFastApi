from fastapi import HTTPException, status

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, func, or_ 

from data_base.models.models import Departamento
from data_base.schemas.Departamento import ReadDepartamento

#CRUD de Departamento.

#CREATE.
async def create_departamento(departamento_data: dict, db_session: AsyncSession) -> ReadDepartamento:
    #Validar id y nombre. 
    statement = await db_session.execute(select(Departamento).where(or_(Departamento.id_departamento == departamento_data.get("id_departamento"), Departamento.nombre == departamento_data.get("nombre"))))
    db_departamento: Departamento = statement.scalar_one_or_none()

    if isinstance(db_departamento, Departamento):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"Error": "El id o el nombre ya existen"})

    #Crear db_departamento.
    db_departamento: Departamento = Departamento(**departamento_data)

    #Aplicar cambios en la Base de Datos.
    db_session.add(db_departamento)
    await db_session.commit()
    await db_session.refresh(db_departamento)

    #Crear response_departamento.
    return ReadDepartamento.model_validate(db_departamento)

#READ.
async def read_departamento(id_departamento: int, db_session: AsyncSession) -> ReadDepartamento:
    #Consulta con la BD.
    result = await db_session.execute(select(Departamento).where(Departamento.id_departamento == id_departamento).where(Departamento.is_deleted == False))
    departamento: Departamento = result.scalar_one_or_none()
    
    if not isinstance(departamento, Departamento):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "El id del Departamento no existe"})

    #Response_departamento.
    return ReadDepartamento.model_validate(departamento)

async def read_departamentos(limite: int, db_session: AsyncSession) -> List[ReadDepartamento]:
    statement_departamentos = await db_session.execute(select(Departamento).where(Departamento.is_deleted == False).offset(0).limit(limite))
    departamentos: List[Departamento] = statement_departamentos.scalars().all()

    #Response_departamentos.
    return [ReadDepartamento.model_validate(d) for d in departamentos]

async def filtrar_eliminados(limite: int, db_session: AsyncSession) -> List[ReadDepartamento]:
    statement_departamentos = await db_session.execute(select(Departamento).where(Departamento.is_deleted == True).offset(0).limit(limite))
    departamentos: List[Departamento] = statement_departamentos.scalars().all()

    #Response_departamentos.
    return [ReadDepartamento.model_validate(d) for d in departamentos]

#UPDATE.
async def update_departamento(id_departamento: int, update_departamento: dict, db_session: AsyncSession) -> ReadDepartamento:
    statement_departamento = await db_session.execute(select(Departamento).where(Departamento.id_departamento == id_departamento))
    departamento: Departamento = statement_departamento.scalar_one_or_none()

    if departamento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": "El id del Departamento no existe"})
    
    #Actualización.
    actualizacion = update(Departamento).where(Departamento.id_departamento == id_departamento).values(update_departamento)

    #Aplicar cambios en la BD.
    await db_session.execute(actualizacion)
    await db_session.commit()
    await db_session.refresh(departamento)

    #Crear el response_departamento.
    return ReadDepartamento.model_validate(departamento)

#DELETE.
async def delete_departamento(id_departamento: int, db_session: AsyncSession) -> bool:
    statement_departamento = await db_session.execute(select(Departamento).where(Departamento.id_departamento == id_departamento))
    db_departamento = statement_departamento.scalar_one_or_none()

    #Validar si el registro existe y no se ha marcado como eliminado.
    if not db_departamento or db_departamento.is_deleted:
        return False

    #Actualizar las columnas soft-delete.
    statement_update = update(Departamento).where(Departamento.id_departamento == id_departamento).values(is_deleted=True, deleted_at=func.now())

    #Aplicar cambios en la BD.
    await db_session.execute(statement_update)
    await db_session.commit()

    return True
    





