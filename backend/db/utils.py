from aiohttp import web
from tortoise import Tortoise, run_async
from tortoise.contrib.aiohttp import register_tortoise

import models
import validators
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


MODEL_DATA_VALIDATOR = {
    models.User: validators.ImmutableModelValidator,
    models.Series: validators.SeriesValidator,
    models.SeriesItem: validators.SeriesItemValidator,
    models.UserItemLink: validators.UserItemLinkValidator,
}


MODEL_MAPPER = {
    'user': models.User,
    'series': models.Series,
    'series_item': models.SeriesItem,
}


def get_model_n_validator(model_alias: str) -> tuple:
    model = MODEL_MAPPER.get(model_alias)
    validator = MODEL_DATA_VALIDATOR.get(model)

    if not all([model, validator]):
        raise web.HTTPNotFound

    return model, validator
