from http import HTTPStatus
from fastapi import FastAPI

from validators import User
from settings import HOST, PORT
from utils import encrypt_password, password_valid


app = FastAPI()


@app.post('/')
async def hello(user: User):
    user.password = encrypt_password(user.password)
    print(user.dict())
    print(type(user))
    return {'hello': 'world'}
