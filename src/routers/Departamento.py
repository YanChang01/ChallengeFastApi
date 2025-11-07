from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from crud.Departamento import create_departamento, read_departamento, read_departamentos, update_departamento, delete_departamento, filtrar_eliminados
from data_base.client import get_session
from data_base.schemas.Departamento import CreateDepartamento, ReadDepartamento, UpdateDepartamento

#Routers.
router = APIRouter()

#EndPoints.

#Create.
@router.post("/insertar/departamento", response_model=ReadDepartamento, status_code=status.HTTP_201_CREATED)
async def crear_departamento(departamento: CreateDepartamento, session: AsyncSession = Depends(get_session)) -> ReadDepartamento:
    departamento_data = departamento.model_dump() #Json de departamento.
    #Crear el departamento en la BD.
    departamento_creado: ReadDepartamento = await create_departamento(departamento_data=departamento_data, db_session=session)
    
    return departamento_creado
    
#Read.
@router.get("/obtener/departamento/{id_departamento}", response_model=ReadDepartamento)
async def leer_departamento(id_departamento: int, session: AsyncSession = Depends(get_session)):
    departamento: ReadDepartamento = await read_departamento(id_departamento=id_departamento, db_session=session)
    
    return departamento

@router.get("/obtener/departamentos/{limite}", response_model=List[ReadDepartamento])
async def leer_departamentos(limite: int, session: AsyncSession = Depends(get_session)):
    if limite > 0:
        departamentos: List[ReadDepartamento] = await read_departamentos(limite=limite, db_session=session)
        return departamentos
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Límite inválido")

@router.get("/obtener/departamentos/eliminados/{limite}", response_model=List[ReadDepartamento])
async def leer_departamentos_eliminados(limite: int, session: AsyncSession = Depends(get_session)):
    departamentos_eliminados: List[ReadDepartamento] = await filtrar_eliminados(limite=limite, db_session=session)

    return departamentos_eliminados

#Update.
@router.put("/actualizar/departamento/{id_departamento}", response_model=ReadDepartamento)
async def actualizar_departamento(id_departamento: int, departamento_actualizado: UpdateDepartamento, session: AsyncSession = Depends(get_session)):
    update_departamento_data: dict = departamento_actualizado.model_dump() #Json de update_departamento.

    departamento: ReadDepartamento = await update_departamento(id_departamento=id_departamento, update_departamento=update_departamento_data, db_session=session)

    return departamento

#Delete.
@router.delete("/eliminar/departamento/{id_departamento}")
async def eliminar_departamento(id_departamento: int, session: AsyncSession = Depends(get_session)):
    result = await delete_departamento(id_departamento=id_departamento, db_session=session)

    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No se ha podido eliminar el Departamento")
    
    return "Departamento eliminado con éxito."




