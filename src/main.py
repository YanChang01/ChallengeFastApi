from fastapi import FastAPI, HTTPException, status

from routers import Departamento, Profesor, Alumno

#API.
app = FastAPI()

#Routers.
app.include_router(Departamento.router)
app.include_router(Profesor.router)
app.include_router(Alumno.router)

#EndPoints.
@app.get("/")
async def inicio():
    return "Bienvenido a la API de nuestra universidad"




