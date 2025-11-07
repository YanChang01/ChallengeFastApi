from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func

from core.config import settings
from core.security import auth_profesor, verificar_password
from crud.Profesor import create_profesor
from data_base.client import get_session
from data_base.models.models import Profesor
from data_base.schemas.Profesor import CreateProfesor, ReadProfesor, UpdateProfesor

#Routers.
router = APIRouter()

#EndPoints.
@router.post("/registrarse", status_code=status.HTTP_201_CREATED, response_model=ReadProfesor)
async def registro(profesor: CreateProfesor, session: AsyncSession = Depends(get_session)) -> ReadProfesor:
    #Validación de longitud de contraseña.
    if len(profesor.password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="La contraseña no puede exceder los 72 bytes.")

    profesor_data: dict = profesor.model_dump()
    profesor_registrado: ReadProfesor = await create_profesor(profesor_data=profesor_data, db_session=session)

    if not profesor_registrado:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Error: Registro inválido")

    return profesor_registrado

@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(form: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    statement_profesores = await session.execute(select(Profesor).where(Profesor.is_deleted == False).where(Profesor.nombre == form.username))
    db_profesores = statement_profesores.scalars().all()

    #Verificar contraseña correcta.
    db_profesor: Profesor = None
    for p in db_profesores:
        if verificar_password(form.password, p.password):
            db_profesor = p
            break

    if not db_profesor:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credenciales de autenticación inválidas")

    #Construir el access_token.
    access_token = {
        "sub": str(db_profesor.id_profesor),
        "name": db_profesor.nombre,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_DURATION)
    }

    #Retornar jwt.
    return {
        "access_token": jwt.encode(claims=access_token, key=settings.SECRET, algorithm=settings.ALGORITMO),
        "token_type": "bearer"
    }