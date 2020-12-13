from starlette import status
from fastapi import FastAPI

from validators import User
from utils import register_user


app = FastAPI()


@app.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: User):
    token = await register_user(user)
    return token
