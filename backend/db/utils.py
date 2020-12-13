from aiohttp.web_exceptions import HTTPNotFound
from tortoise.contrib.aiohttp import register_tortoise

import models
from settings import DB_URL, MODELS


def connect_to_db(app):
    register_tortoise(
        app=app,
        db_url=DB_URL,
        modules=MODELS,
        generate_schemas=True
    )


MODEL_MAPPER = {
    'user': (models.User, models.UserSerializer),
    'user_token': (models.UserToken, models.UserTokenSerializer),
    'series': (models.Series, models.SeriesSerializer),
    'series_item': (models.Item, models.ItemSerializer),
    'user_item_link': (models.UserItemLink, models.UserItemLinkSerializer),
}


def get_model_n_serializer(model_name: str):
    items = MODEL_MAPPER.get(model_name)

    if not items:
        raise HTTPNotFound

    return items
