from tortoise import fields, models


class User(models.Model):
    name = fields.CharField(max_length=64)
    password = fields.BinaryField()
    email = fields.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class TokenAuth(models.Model):
    user = fields.ForeignKeyField('User', 'token_auth')
    token = fields.BinaryField()