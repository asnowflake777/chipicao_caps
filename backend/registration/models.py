from tortoise import fields, models


class User(models.Model):
    name = fields.CharField(max_length=64)
    password = fields.BinaryField()
    email = fields.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
