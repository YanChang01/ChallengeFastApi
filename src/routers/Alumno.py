from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from crud.Alumno import create_alumno, read_alumno, read_alumnos, update_alumno
from data_base.client import get_session
from data_base.schemas.Alumno import CreateAlumno, ReadAlumno, UpdateAlumno

#Routers.
router = APIRouter()

#EndPoints.

#Create.
@router.post("/insertar/alumno", response_model=ReadAlumno, status_code=status.HTTP_201_CREATED)
async def crear_alumno(alumno: CreateAlumno, session: AsyncSession = Depends(get_session)) -> ReadAlumno:
    alumno_data = alumno.model_dump() #Json de alumno.

    #Crear el alumno en la BD.
    alumno_creado: ReadAlumno = await create_alumno(alumno_data=alumno_data, db_session=session)
    
    return alumno_creado

#Read.
@router.get("/obtener/alumno/{id_alumno}", response_model=ReadAlumno)
async def leer_alumno(id_alumno: int, session: AsyncSession = Depends(get_session)):
    alumno: ReadAlumno = await read_alumno(id_alumno=id_alumno, db_session=session)
    return alumno

@router.get("/obtener/alumnos/{limite}", response_model=List[ReadAlumno])
async def leer_alumnos(limite: int, session: AsyncSession = Depends(get_session)):
    if limite > 0:
        alumnos: List[ReadAlumno] = await read_alumnos(limite=limite, db_session=session)
        return alumnos
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Límite inválido")

#Update.
@router.put("/actualizar/alumno/{id_alumno}", response_model=ReadAlumno)
async def actualizar_alumno(id_alumno: int, alumno_actualizado: UpdateAlumno, session: AsyncSession = Depends(get_session)):
    update_alumno_data: dict = alumno_actualizado.model_dump() #Json de alumno_actualizado.

    alumno: ReadAlumno = await update_alumno(id_alumno=id_alumno, update_alumno=update_alumno_data, db_session=session)

    return alumno




