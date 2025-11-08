from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.security import auth_profesor
from crud.Alumno import create_alumno, read_alumno, read_alumnos, update_alumno, delete_alumno, filtrar_eliminados
from data_base.client import get_session
from data_base.schemas.Alumno import CreateAlumno, ReadAlumno, UpdateAlumno

#Routers.
router = APIRouter(prefix="/alumno")

#EndPoints.

#Create.
@router.post("/insertar", status_code=status.HTTP_201_CREATED)
async def crear_alumno(alumno: CreateAlumno, session: AsyncSession = Depends(get_session), auth: bool = Depends(auth_profesor)):
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"Error": "Token JWT inválido"})
    
    #Json de alumno.
    alumno_data = alumno.model_dump() 

    #Crear el alumno en la BD.
    try:
        alumno_creado: ReadAlumno = await create_alumno(alumno_data=alumno_data, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "No se ha podido insertar el Alumno en la Base de Datos"})

    if not alumno_creado:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se ha podido insertar el Alumno"})
    
    return {"Mensaje": "Alumno insertado con éxito"}

#Read.
@router.get("/obtener/{id_alumno}", response_model=ReadAlumno)
async def leer_alumno(id_alumno: int, session: AsyncSession = Depends(get_session)):
    try:
        alumno: ReadAlumno = await read_alumno(id_alumno=id_alumno, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "Ha ocurrido un error inesperado durante la consulta a la Base de Datos"})

    if not alumno:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se ha podido obtener el Alumno de la Base de Datos"})
    
    return alumno

@router.get("/obtener/alumnos/{limite}", response_model=List[ReadAlumno])
async def leer_alumnos(limite: int, session: AsyncSession = Depends(get_session)):
    if limite <= 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "Límite inválido"})

    try:
        alumnos: List[ReadAlumno] = await read_alumnos(limite=limite, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "Ha ocurrido un error inesperado durante la consulta a la Base de Datos."})
        
    if not alumnos:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se han podido obtener los alumnos de la Base de Datos"})

    return alumnos

@router.get("/obtener/eliminados/{limite}", response_model=List[ReadAlumno])
async def leer_alumnos_eliminados(limite: int, session: AsyncSession = Depends(get_session)):
    try:
        alumnos_eliminados: List[ReadAlumno] = await filtrar_eliminados(limite=limite, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "Ha ocurrido un error inesperado durante la interacción con la Base de Datos"})

    if not alumnos_eliminados:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se han podido obtener los alumnos eliminados de la Base de Datos"})

    return alumnos_eliminados

#Update.
@router.put("/actualizar/{id_alumno}")
async def actualizar_alumno(id_alumno: int, alumno_actualizado: UpdateAlumno, session: AsyncSession = Depends(get_session), auth: bool = Depends(auth_profesor)):
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"Error": "Token JWT inválido"})
    
    update_alumno_data: dict = alumno_actualizado.model_dump() #Json de alumno_actualizado.

    try:
        alumno: ReadAlumno = await update_alumno(id_alumno=id_alumno, update_alumno=update_alumno_data, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "Ha ocurrido un error inesperado durante la interacción con la Base de Datos"})

    if not alumno:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se ha podido actualizar el alumno en la Base de Datos"})

    return {"Mensaje": "Alumno actualizado con éxito"}

#Delete.
@router.delete("/eliminar/{id_alumno}")
async def eliminar_alumno(id_alumno: int, session: AsyncSession = Depends(get_session), auth: bool = Depends(auth_profesor)):
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"Error": "JWT inválido"})
    
    try:
        result = await delete_alumno(id_alumno=id_alumno, db_session=session)
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Exception": "No se ha podido eliminar al Alumno en la Base de Datos"})

    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={"Error": "No se ha podido eliminar al Alumno"})
    
    return {"Mensaje": "Alumno eliminado con éxito"}


