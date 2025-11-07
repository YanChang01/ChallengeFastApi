from fastapi import FastAPI, HTTPException, status

from routers import Departamento, Profesor, Alumno, Autenticacion
from middlewares.registro_middleware import tiempo_middleware

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
@app.get("/")
async def inicio():
    return "Bienvenido a la API de nuestra universidad"




