import os
from dotenv import load_dotenv
from pydantic import BaseModel

#Cargar las variables de entorno.
load_dotenv()

#Seguridad.
SECRET = os.getenv("SECRET")
ALGORITMO = os.getenv("ALGORITMO")

#URL de conexión.
DATABASE_URL = os.getenv("DATABASE_URL")

#Clase Settings.
class Settings(BaseModel):
    PROJECT_NAME: str = "FastApi_Challenge"
    PROJECT_VERSION: str = "0.0.1"
    DATABASE_URL: str = DATABASE_URL
    SECRET: str = SECRET
    ALGORITMO: str = ALGORITMO

settings = Settings()
