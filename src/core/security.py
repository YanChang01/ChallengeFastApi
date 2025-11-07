from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta

from core.config import settings

#Security

"""
Estructura del JWT.
{
    header: {
        alg: algoritmo,
        type: JWT
    }
    payload: {
        sub: id,
        name: Jane Doe,
        exp: dateTime
    }
    signature: header. + payload. + secret
}
"""

access_token_duration = settings.ACCESS_TOKEN_DURATION
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")
crypt = CryptContext(schemes=["bcrypt"])

#Hashing para contraseñas.
def password_hash(password: str) -> str: #Hash.
    password_bytes = password.encode(encoding="utf-8")[:72]
    password_truncado: str = password_bytes.decode("utf-8", errors="ignore")

    return crypt.hash(password_truncado)

def verificar_password(plain_password: str, hashed_password: str) -> bool: #Verificar hash.
    return crypt.verify(plain_password, hashed_password)

#Autenticación.
def auth_profesor(token: str = Depends(oauth2)) -> bool:
    try:
        validar: str = jwt.decode(token=token, key=settings.SECRET, algorithms=settings.ALGORITMO)
    except (JWTError, ExpiredSignatureError):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Token JWT inválido.")
    
    if not validar:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas")

    return True
