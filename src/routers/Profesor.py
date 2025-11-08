from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.security import auth_profesor
from crud.Profesor import create_profesor, read_profesor, read_profesores, update_profesor, delete_profesor, filtrar_eliminados
from data_base.client import get_session
from data_base.schemas.Profesor import CreateProfesor, ReadProfesor, UpdateProfesor

#Routers.
router = APIRouter(prefix="/profesor")

#EndPoints.

#Create.
@router.post("/insertar", status_code=status.HTTP_201_CREATED)
async def crear_profesor(profesor: CreateProfesor, session: AsyncSession = Depends(get_session), auth: bool = Depends(auth_profesor)):
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"Error": "Token JWT inválido"})
    
    #Json de profesor.
    profesor_data = profesor.model_dump() 

    #try:
        #Crear el profesor en la BD.
    profesor_creado: ReadProfesor = await create_profesor(profesor_data=profesor_data, db_session=session)
    #except:
        #raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "No se ha podido insertar el Profesor en la Base de Datos"})

    if not profesor_creado:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se ha podido insertar al profesor"})

    return {"Mensaje": "Profesor insertado con éxito"}

#Read.
@router.get("/obtener/{id_profesor}", response_model=ReadProfesor)
async def leer_profesor(id_profesor: int, session: AsyncSession = Depends(get_session)):
    try:
        profesor: ReadProfesor = await read_profesor(id_profesor=id_profesor, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "No se ha podido obtener al Profesor de la Base de Datos"})
    
    if not profesor:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se ha podido obtener al Profesor"})

    return profesor

@router.get("/obtener/profesores/{limite}", response_model=List[ReadProfesor])
async def leer_profesores(limite: int, session: AsyncSession = Depends(get_session)):
    if limite <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Límite inválido")

    try:
        profesores: List[ReadProfesor] = await read_profesores(limite=limite, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "Ha ocurrido un error inesperado durante la consulta a la Base de Datos"})
    
    if not profesores:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se han podido obtener los Profesores de la Base de Datos"})

    return profesores

@router.get("/obtener/eliminados/{limite}", response_model=List[ReadProfesor])
async def leer_profesores_eliminados(limite: int, session: AsyncSession = Depends(get_session)):
    try:
        profesores_eliminados: List[ReadProfesor] = await filtrar_eliminados(limite=limite, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "Ha ocurrido un error inesperado durante la consulta a la Base de Datos"})

    if not profesores_eliminados:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se han podido obtener a los Profesores eliminados"})

    return profesores_eliminados

#Update.
@router.put("/actualizar/{id_profesor}")
async def actualizar_profesor(id_profesor: int, profesor_actualizado: UpdateProfesor, session: AsyncSession = Depends(get_session), auth: bool = Depends(auth_profesor)):
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"Error": "Token JWT inválido"})

    #Json de profesor_actualizado.
    update_profesor_data: dict = profesor_actualizado.model_dump() 

    try:
        profesor: ReadProfesor = await update_profesor(id_profesor=id_profesor, update_profesor=update_profesor_data, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "Ha ocurrido un error inesperado durante la actualización del profesor en la Base de Datos"})

    return {"Mensaje": "Profesor actualizado con éxito"}

#Delete.
@router.delete("/eliminar/{id_profesor}")
async def eliminar_profesor(id_profesor: int, session: AsyncSession = Depends(get_session), auth: bool = Depends(auth_profesor)):
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"Error": "Token JWT inválido"})
    
    try:
        result = await delete_profesor(id_profesor=id_profesor, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "Ha ocurrido un error inesperado durante la eliminación del Profesor de la Base de Datos"})

    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se ha podido eliminar al Profesor"})
    
    return {"Mensaje": "Profesor eliminado con éxito"}


