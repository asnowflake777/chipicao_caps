from typing import Optional

from tortoise import fields, models
from pydantic import BaseModel


class User(models.Model):
    username = fields.CharField(max_length=64, unique=True)
    email = fields.CharField(max_length=64, unique=True)
    password = fields.BinaryField()

    async def serialize(self):
        return {
            'id': self.pk,
            'username': self.username,
            'email': self.email,
        }


class Series(models.Model):
    name = fields.CharField(max_length=64)
    year = fields.SmallIntField()
    description = fields.TextField()
    creator = fields.ForeignKeyField('models.User', related_name='series')
    image_uid = fields.CharField(max_length=64)

    async def serialize(self):
        creator = await self.creator.first()
        creator = await creator.serialize()
        return {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
            'creator': creator,
            'image_uid': self.image_uid,
        }


class SeriesItem(models.Model):
    name = fields.CharField(max_length=64)
    description = fields.TextField()
    identify_number = fields.IntField()
    series = fields.ForeignKeyField('models.Series', related_name='items')

    async def serialize(self):
        series = await self.series.first()
        series = await series.serialize()
        return {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
            'identify_number': self.identify_number,
            'series': series,
        }


class UserItemLink(models.Model):
    user = fields.ForeignKeyField('models.User', related_name='items')
    item = fields.ForeignKeyField('models.SeriesItem', related_name='users')

    async def serialize(self):
        user = await self.user.first()
        user = await user.serialize()
        item = await self.item.first()
        item = await item.serialize()
        return {
            'user': user,
            'item': item,
        }


MODEL_MAPPER = {
    'user': User,
    'series': Series,
    'series_item': SeriesItem,
}


class UserValidator(BaseModel):
    username: str
    email: str
    password: str


class SeriesValidator(BaseModel):
    name: str
    year: int
    description: str
    creator: int


class SeriesItemValidator(BaseModel):
    name: str
    description: str
    identify_number: Optional[int]
    series: int


class UserItemLinkValidator(BaseModel):
    user: int
    item: int


MODEL_DATA_VALIDATOR = {
    User: UserValidator,
    Series: SeriesValidator,
    SeriesItem: SeriesItemValidator,
    UserItemLink: UserItemLinkValidator,
}