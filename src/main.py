from fastapi import FastAPI, status

from routers import Departamento, Profesor, Alumno, Autenticacion
from middlewares.registro_middleware import tiempo_middleware
from core.config import settings

#API.
app = FastAPI()

#Routers.
app.include_router(Departamento.router)
app.include_router(Profesor.router)
app.include_router(Alumno.router)
app.include_router(Autenticacion.router)

#Middlewares.
app.middleware("http")(tiempo_middleware)

#EndPoints.
@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return f"Bienvenido a la APP {settings.PROJECT_NAME} versión {settings.PROJECT_VERSION}"




