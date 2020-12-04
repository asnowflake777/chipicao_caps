from fastapi import FastAPI

from tortoise.contrib.fastapi import register_tortoise

from settings import DB_URL, MODULES
from models import get_model_n_serializer


app = FastAPI()


@app.get('/{model_name}/{instance_id}')
async def get_model_instance(model_name: str, instance_id: int):
    model, serializer = await get_model_n_serializer(model_name)
    return await serializer.from_queryset_single(model.get(pk=instance_id))


@app.post('/{model_name}/{instance_id}')
async def get_model_instance(model_name: str, instance_id: int):
    model, serializer = await get_model_n_serializer(model_name)
    return await serializer.from_queryset_single(model.get(pk=instance_id))


@app.patch('/{model_name}/{instance_id}')
async def get_model_instance(model_name: str, instance_id: int):
    model, serializer = await get_model_n_serializer(model_name)
    return await serializer.from_queryset_single(model.get(pk=instance_id))


@app.delete('/{model_name}/{instance_id}')
async def get_model_instance(model_name: str, instance_id: int):
    model, serializer = await get_model_n_serializer(model_name)
    return await serializer.from_queryset_single(model.get(pk=instance_id))


register_tortoise(
    app,
    db_url=DB_URL,
    modules=MODULES,
    generate_schemas=True,
    add_exception_handlers=True,
)
