from http import HTTPStatus
from typing import Union

from fastapi import FastAPI, HTTPException
from tortoise import Model
from tortoise.contrib.pydantic.base import PydanticModel
from tortoise.contrib.fastapi import register_tortoise

from settings import DB_URL, MODULES
from models import get_model_n_serializer, MODELS, SERIALIZERS, UserSerializer

app = FastAPI()


@app.get('/{model_name}/{instance_id}')
async def get_model_instance(model_name: str, instance_id: int):
    model, serializer = await get_model_n_serializer(model_name)
    return await serializer.from_queryset_single(model.get(pk=instance_id))


@app.post('/user', response_model=UserSerializer)
async def get_model_instance(user: UserSerializer):
    # model, serializer = await get_model_n_serializer(model_name)
    print(user, 'instance')
    return {'hello': 'world'}


@app.patch('/{model_name}/{instance_id}')
async def get_model_instance(model_name: str, instance_id: int):
    model, serializer = await get_model_n_serializer(model_name)
    return await serializer.from_queryset_single(model.get(pk=instance_id))


@app.delete('/{model_name}/{instance_id}')
async def get_model_instance(model_name: str, instance_id: int):
    model, serializer = await get_model_n_serializer(model_name)
    deleted_count = await model.filter(pk=instance_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    raise HTTPException(status_code=HTTPStatus.NO_CONTENT)


register_tortoise(
    app,
    db_url=DB_URL,
    modules=MODULES,
    generate_schemas=True,
    add_exception_handlers=True,
)
