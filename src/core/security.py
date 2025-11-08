from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError

from core.config import settings

#Security.

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
#Hash.
def password_hash(password: str) -> str: 
    password_bytes = password.encode(encoding="utf-8")[:72] #Validación de longitud de contraseña. (Hasta 72 bytes -> bcrypt)
    password_truncado: str = password_bytes.decode("utf-8", errors="ignore")

    return crypt.hash(password_truncado)

#Verificar hash.
def verificar_password(plain_password: str, hashed_password: str) -> bool: 
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
