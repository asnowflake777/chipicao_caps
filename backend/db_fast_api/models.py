from http import HTTPStatus
from fastapi import HTTPException
from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=64, unique=True)


class Series(models.Model):
    name = fields.CharField(max_length=64)
    year = fields.SmallIntField()
    description = fields.TextField(null=True)
    image_uid = fields.CharField(max_length=64, null=True)
    creator = fields.ForeignKeyField('models.User', related_name='series')


class SeriesItem(models.Model):
    name = fields.CharField(max_length=64)
    description = fields.TextField(null=True)
    identify_number = fields.IntField(null=True)
    image_uid = fields.CharField(max_length=64, null=True)
    series = fields.ForeignKeyField('models.Series', related_name='items')


class UserItemLink(models.Model):
    user = fields.ForeignKeyField('models.User', related_name='items')
    item = fields.ForeignKeyField('models.SeriesItem', related_name='users')


UserSerializer = pydantic_model_creator(User, name='User')
SeriesSerializer = pydantic_model_creator(Series, name='Series')
SeriesItemSerializer = pydantic_model_creator(SeriesItem, name='SeriesItem')
UserItemLinkSerializer = pydantic_model_creator(UserItemLink, name='UserItemLink')


MODEL_MAPPER = {
    'user': (User, UserSerializer),
    'series': (Series, SeriesSerializer),
    'series_item': (SeriesItem, SeriesItemSerializer),
    'user_item_link': (UserItemLink, UserItemLinkSerializer),
}


async def get_model_n_serializer(model_name: str):
    items = MODEL_MAPPER.get(model_name)

    if not items:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return items
