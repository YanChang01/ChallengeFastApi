from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from routers.Autenticacion import auth_profesor
from crud.Profesor import create_profesor, read_profesor, read_profesores, update_profesor, delete_profesor, filtrar_eliminados
from data_base.client import get_session
from data_base.schemas.Profesor import CreateProfesor, ReadProfesor, UpdateProfesor

#Routers.
router = APIRouter()

#EndPoints.

#Create.
@router.post("/insertar/profesor", response_model=ReadProfesor, status_code=status.HTTP_201_CREATED)
async def crear_profesor(profesor: CreateProfesor, session: AsyncSession = Depends(get_session), auth: bool = Depends(auth_profesor)) -> ReadProfesor:
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token JWT inválido")
    
    #Json de profesor.
    profesor_data = profesor.model_dump() 

    #Crear el profesor en la BD.
    profesor_creado: ReadProfesor = await create_profesor(profesor_data=profesor_data, db_session=session)
    
    return profesor_creado

#Read.
@router.get("/obtener/profesor/{id_profesor}", response_model=ReadProfesor)
async def leer_profesor(id_profesor: int, session: AsyncSession = Depends(get_session)):
    profesor: ReadProfesor = await read_profesor(id_profesor=id_profesor, db_session=session)
    return profesor

@router.get("/obtener/profesores/{limite}", response_model=List[ReadProfesor])
async def leer_profesores(limite: int, session: AsyncSession = Depends(get_session)):
    if limite > 0:
        profesores: List[ReadProfesor] = await read_profesores(limite=limite, db_session=session)
        return profesores
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Límite inválido")

@router.get("/obtener/profesores/eliminados/{limite}", response_model=List[ReadProfesor])
async def leer_profesores_eliminados(limite: int, session: AsyncSession = Depends(get_session)):
    profesores_eliminados: List[ReadProfesor] = await filtrar_eliminados(limite=limite, db_session=session)

    return profesores_eliminados

#Update.
@router.put("/actualizar/profesor/{id_profesor}", response_model=ReadProfesor)
async def actualizar_profesor(id_profesor: int, profesor_actualizado: UpdateProfesor, session: AsyncSession = Depends(get_session), auth: bool = Depends(auth_profesor)):
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token JWT inválido")

    #Json de profesor_actualizado.
    update_profesor_data: dict = profesor_actualizado.model_dump() 

    profesor: ReadProfesor = await update_profesor(id_profesor=id_profesor, update_profesor=update_profesor_data, db_session=session)

    return profesor

#Delete.
@router.delete("/eliminar/profesor/{id_profesor}")
async def eliminar_profesor(id_profesor: int, session: AsyncSession = Depends(get_session), auth: bool = Depends(auth_profesor)):
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token JWT inválido")
    
    result = await delete_profesor(id_profesor=id_profesor, db_session=session)

    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No se ha podido eliminar al Profesor")
    
    return "Profesor eliminado con éxito."


