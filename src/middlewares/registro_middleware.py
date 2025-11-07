from fastapi import Request, Response
from datetime import datetime, timezone, timedelta

#Función para implementar el middleware.
async def tiempo_middleware(request: Request, call_next):
    #Registrar tiempo inicial.
    inicio = datetime.now(timezone.utc)

    #LLamar al middleware o endpoint siguiente y enviar la request.
    response: Response = await call_next(request)

    #Registrar tiempo final.
    fin = datetime.now(timezone.utc)

    #Calcular duración de la request-response.
    duracion: timedelta = fin - inicio

    #Formatear información. (YY/MM/DD/SS/MS)    
    inicio_str = inicio.isoformat()
    fin_str = fin.isoformat()
    duracion_segundos = duracion.total_seconds()

    #Imprimir información en consola.
    print(
        f"Request: {request.method} {request.url.path} | "
        f"Start Time (UTC): {inicio_str} | "
        f"End Time (UTC): {fin_str} | "
        f"Status Code: {response.status_code} | "
        f"Duration: {duracion_segundos: .4f} seconds"
    )

    return response


