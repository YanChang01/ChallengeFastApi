import os
from dotenv import load_dotenv
from pydantic import BaseModel

#Cargar las variables de entorno.
load_dotenv()

#Seguridad.
SECRET = os.getenv("SECRET")
ALGORITMO = os.getenv("ALGORITMO")
ACCESS_TOKEN_DURATION = int(os.getenv("ACCESS_TOKEN_DURATION"))

#URL de conexión.
DATABASE_URL = os.getenv("DATABASE_URL")

#Clase Settings.
class Settings(BaseModel):
    PROJECT_NAME: str = "FastApi_Challenge"
    PROJECT_VERSION: str = "1.0"
    DATABASE_URL: str = DATABASE_URL
    SECRET: str = SECRET
    ALGORITMO: str = ALGORITMO
    ACCESS_TOKEN_DURATION: int = ACCESS_TOKEN_DURATION

settings = Settings()
