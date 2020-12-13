import scrypt
from base64 import b64encode

import requests
from requests.exceptions import ConnectionError
from fastapi.exceptions import HTTPException

from starlette import status

from settings import SALT, DB_URL
from validators import User, CreatedUser, UserToken, CreatedUserToken


def password_valid(password: str, min_length: int = 6) -> bool:
    return password.isascii() and len(password) >= min_length


def encrypt_password(password: str) -> str:
    _password = password + SALT
    encrypted_password = scrypt.hash(_password, SALT)
    return b64encode(encrypted_password).decode()


async def make_post_request(url: str, data: dict) -> dict:
    try:
        response = requests.post(url, json=data)
        if response.status_code != status.HTTP_201_CREATED:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except ConnectionError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


async def create_user_token(user_token: UserToken) -> str:
    response_data = await make_post_request(DB_URL + '/user_token/', data=user_token.dict())
    created_user_token = CreatedUserToken(**response_data)
    return created_user_token.token


async def register_user(user: User) -> str:
    user.password = encrypt_password(user.password)
    response_data = await make_post_request(DB_URL + '/user/', data=user.dict())
    created_user = CreatedUser(**response_data)
    token_data = UserToken(user_id=created_user.id, token=created_user.password)
    token = await create_user_token(token_data)
    return token
