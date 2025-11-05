from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

import asyncio
from asyncio import get_running_loop

from alembic import context

import os
from dotenv import load_dotenv

from src.data_base.models.base import Base, profesor_alumno_tabla
from src.data_base.models.models import Departamento, Profesor, Alumno


#Cargar Variables de Entorno.
load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no configurada")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

#Enlazando la configuración con la DATABASE_URL.
config.set_main_option(name="sqlalchemy.url", value=DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
#target_metadata = None

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

#Migraciones.
def run_migrations_sync(connection: AsyncConnection, target_metadata: any):
    #Run migraciones en contexto asíncrono.
    context.configure(connection=connection, target_metadata=target_metadata)

    #Transacción asíncrona.
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online(): #Modo online.
    #Crear engine asíncrona.
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass = pool.AsyncAdaptedQueuePool
    )

    async with connectable.connect() as connection:
        await connection.run_sync(run_migrations_sync, target_metadata)


def run_migrations_offline() -> None: #Modo offline.
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

#Lógica de ejecución.
if context.is_offline_mode():
    run_migrations_offline()
else:
    try:
        loop = get_running_loop() #Obtener el loop que está corriendo.
    except RuntimeError:
        loop = asyncio.new_event_loop() #Crear un nuevo loop.
        asyncio.set_event_loop(loop)

    loop.run_until_complete(run_migrations_online()) #Correr el nuevo loop.
