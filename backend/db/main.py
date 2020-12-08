import argparse
from http import HTTPStatus

from aiohttp import web
from aiohttp.abc import Request

from tortoise.exceptions import IntegrityError, DoesNotExist, FieldError

from utils import connect_to_db, get_model_n_serializer
from settings import DEFAULT_HOST, DEFAULT_PORT

app = web.Application()
routes = web.RouteTableDef()


@routes.view(r'/{model:\w+}/{id:\d*}')
class ModelView(web.View):

    def __init__(self, request: Request):
        model_name = request.match_info.get('model')
        model, serializer = get_model_n_serializer(model_name)

        self.model = model
        self.serializer = serializer
        self.model_instance_id = request.match_info.get('id')

        super().__init__(request)

    async def get(self,):

        if self.model_instance_id:
            queryset = self.model.filter(pk=self.model_instance_id)
        else:
            queryset = self.model.all()

        data = [instance.dict() for instance in await self.serializer.from_queryset(queryset)]
        return web.json_response(data=data, status=HTTPStatus.Ok if data else HTTPStatus.NOT_FOUND)

    async def post(self):
        try:
            data = await self.request.json()
            instance = await self.model.create(**data)
            response = await self.serializer.from_tortoise_orm(instance)
            return web.json_response(response.dict())

        except IntegrityError as err:
            raise web.HTTPBadRequest(text=str(err))

    async def patch(self):
        try:
            await self.model.filter(pk=self.model_instance_id).update(**await self.request.json())
            response = await self.serializer.from_tortoise_orm(await self.model.get(pk=self.model_instance_id))
            return web.json_response(response.dict())

        except (IntegrityError, FieldError) as err:
            raise web.HTTPBadRequest(text=str(err))
        except DoesNotExist:
            raise web.HTTPNotFound

    async def delete(self):
        await self.model.filter(pk=self.model_instance_id).delete()
        raise web.HTTPNoContent


app.add_routes(routes)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Database service')

    parser.add_argument('--host', metavar='', type=str, help='host to start on')
    parser.add_argument('--port', metavar='', type=int, help='port to start with')

    args = parser.parse_args()

    HOST = args.host if args.host else DEFAULT_HOST
    PORT = args.port if args.port else DEFAULT_PORT

    connect_to_db(app)
    web.run_app(app, host=HOST, port=PORT)
