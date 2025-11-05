from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

#Crear la engine asíncrona.
engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

#Crear la sessión asíncrona de Base de Datos.
Session_Async = sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit=False
)

#Función asíncrona para obtener la Session_Async.
async def get_session():
    async with Session_Async() as session:
        yield session



