from http import HTTPStatus
from fastapi import HTTPException
from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    name = fields.CharField(max_length=64, unique=True)
    email = fields.CharField(max_length=64, unique=True)
    password = fields.CharField(max_length=128)


class UserToken(models.Model):
    user = fields.ForeignKeyField('models.User', related_name='tokens')
    token = fields.CharField(max_length=128)


class Series(models.Model):
    name = fields.CharField(max_length=64)
    year = fields.SmallIntField()
    description = fields.TextField(null=True)
    image_uid = fields.CharField(max_length=64, null=True)
    creator = fields.ForeignKeyField('models.User', related_name='series')


class Item(models.Model):
    name = fields.CharField(max_length=64)
    description = fields.TextField(null=True)
    identify_number = fields.IntField(null=True)
    image_uid = fields.CharField(max_length=64, null=True)
    series = fields.ForeignKeyField('models.Series', related_name='items')


class UserItemLink(models.Model):
    user = fields.ForeignKeyField('models.User', related_name='items')
    item = fields.ForeignKeyField('models.Item', related_name='users')


UserSerializer = pydantic_model_creator(User, name='User')
UserTokenSerializer = pydantic_model_creator(UserToken, name='UserToken')
SeriesSerializer = pydantic_model_creator(Series, name='Series')
ItemSerializer = pydantic_model_creator(Item, name='Item')
UserItemLinkSerializer = pydantic_model_creator(UserItemLink, name='UserItemLink')


MODEL_MAPPER = {
    'user': (User, UserSerializer),
    'series': (Series, SeriesSerializer),
    'series_item': (Item, ItemSerializer),
    'user_item_link': (UserItemLink, UserItemLinkSerializer),
}


MODELS = [User, UserToken, Series, Item, UserItemLink]
SERIALIZERS = [UserSerializer, UserTokenSerializer, SeriesSerializer, ItemSerializer, UserItemLinkSerializer]


async def get_model_n_serializer(model_name: str):
    items = MODEL_MAPPER.get(model_name)

    if not items:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return items
