from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

from core.config import settings

#Security
access_token_duration = settings.ACCESS_TOKEN_DURATION
oauth2 = OAuth2PasswordBearer(tokenUrl="/registro")
crypt = CryptContext(schemes=["bcrypt"])






