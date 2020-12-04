from tortoise import fields, models


class ImmutableModel:
    pass


class User(models.Model, ImmutableModel):
    username = fields.CharField(max_length=64, unique=True)
    email = fields.CharField(max_length=64, unique=True)
    password = fields.BinaryField()
    image_uid = fields.CharField(max_length=64, null=True)

    async def serialize(self):
        return {
            'id': self.pk,
            'username': self.username,
        }


class Series(models.Model):
    name = fields.CharField(max_length=64)
    year = fields.SmallIntField()
    description = fields.TextField(null=True)
    image_uid = fields.CharField(max_length=64, null=True)
    creator = fields.ForeignKeyField('models.User', related_name='series')

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
    description = fields.TextField(null=True)
    identify_number = fields.IntField(null=True)
    image_uid = fields.CharField(max_length=64, null=True)
    series = fields.ForeignKeyField('models.Series', related_name='items')

    async def serialize(self):
        series = await self.series.first()
        series = await series.serialize()
        return {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
            'identify_number': self.identify_number,
            'image_uid': self.image_uid,
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
