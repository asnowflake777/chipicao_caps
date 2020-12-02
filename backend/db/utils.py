from tortoise import Tortoise, run_async
from tortoise.contrib.aiohttp import register_tortoise

from settings import DB_URL, MODELS


def connect_to_db(app):
    register_tortoise(
        app=app,
        db_url=DB_URL,
        modules=MODELS,
        generate_schemas=True
    )


async def init_connection():
    return await Tortoise.init(
        db_url=DB_URL,
        modules=MODELS,
    )


async def generate_schemas():
    await init_connection()
    await Tortoise.generate_schemas()


def create_tables():
    run_async(generate_schemas())
