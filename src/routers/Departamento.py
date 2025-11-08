from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.security import auth_profesor
from crud.Departamento import create_departamento, read_departamento, read_departamentos, update_departamento, delete_departamento, filtrar_eliminados
from data_base.client import get_session
from data_base.schemas.Departamento import CreateDepartamento, ReadDepartamento, UpdateDepartamento

#Routers.
router = APIRouter(prefix="/departamento")

#EndPoints.

#Create.
@router.post("/insertar", status_code=status.HTTP_201_CREATED)
async def crear_departamento(departamento: CreateDepartamento, session: AsyncSession = Depends(get_session)):
    #Json de create_departamento.
    departamento_data: dict = departamento.model_dump() 

    #try:
    #Crear el departamento en la BD.
    departamento_creado: ReadDepartamento = await create_departamento(departamento_data=departamento_data, db_session=session)
    #except:
        #raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "Ha ocurrido un error inesperado durante la inserción del Departamento en la Base de Datos"})

    #Validación.
    if not departamento_creado:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se ha podido insertar el Departamento en la Base de Datos"})

    return {"Mensaje": "Departamento insertado con éxito"}
    
#Read.
@router.get("/obtener/{id_departamento}", response_model=ReadDepartamento)
async def leer_departamento(id_departamento: int, session: AsyncSession = Depends(get_session)):
    try:
        departamento: ReadDepartamento = await read_departamento(id_departamento=id_departamento, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "Ha ocurrido un error inesperado durante la consulta a la Base de Datos"})

    if not departamento:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se ha podido obtener el Departamento de la Base de Datos"})

    return departamento

@router.get("/obtener/departamentos/{limite}", response_model=List[ReadDepartamento])
async def leer_departamentos(limite: int, session: AsyncSession = Depends(get_session)):
    if limite <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Límite inválido")

    try:
        departamentos: List[ReadDepartamento] = await read_departamentos(limite=limite, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "Ha ocurrido un error inesperado durante la consulta a la Base de Datos"})
    
    if not departamentos:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se han podido obtener los Departamentos de la Base de Datos"})

    return departamentos

@router.get("/obtener/eliminados/{limite}", response_model=List[ReadDepartamento])
async def leer_departamentos_eliminados(limite: int, session: AsyncSession = Depends(get_session)):
    try:
        departamentos_eliminados: List[ReadDepartamento] = await filtrar_eliminados(limite=limite, db_session=session)
    except: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "Ha ocurrido un error inesperado durante la consulta a la Base de Datos"})
    
    if not departamentos_eliminados:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se han podido obtener los Departamentos de la Base de Datos"})

    return departamentos_eliminados

#Update.
@router.put("/actualizar/{id_departamento}")
async def actualizar_departamento(id_departamento: int, departamento_actualizado: UpdateDepartamento, session: AsyncSession = Depends(get_session), auth: bool = Depends(auth_profesor)):
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"Error": "Token JWT inválido"})
    
    #Json de update_departamento.
    update_departamento_data: dict = departamento_actualizado.model_dump() 

    try:
        departamento: ReadDepartamento = await update_departamento(id_departamento=id_departamento, update_departamento=update_departamento_data, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Error": "No se ha podido actualizar el Departamento en la Base de Datos"})

    if not departamento:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se ha podido actualizar el Departamento"})

    return {"Mensaje": "Departamento actualizado con éxito"}

#Delete.
@router.delete("/eliminar/{id_departamento}")
async def eliminar_departamento(id_departamento: int, session: AsyncSession = Depends(get_session), auth: bool = Depends(auth_profesor)):
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"Error": "Token JWT inválido"})
    
    try:
        result = await delete_departamento(id_departamento=id_departamento, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "No se ha podido eliminar el Departamento en la Base de Datos"})

    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se ha podido eliminar el Departamento"})
    
    return {"Mensaje": "Departamento eliminado con éxito"}




