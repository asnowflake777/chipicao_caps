import argparse

from aiohttp import web
from aiohttp.abc import Request

from tortoise.exceptions import IntegrityError

from models import ImmutableModel
from utils import connect_to_db, get_model_n_validator
from settings import DEFAULT_HOST, DEFAULT_PORT

app = web.Application()
routes = web.RouteTableDef()


@routes.view(r'/{model:\w+}/{id:\d*}')
class ModelView(web.View):

    def __init__(self, request: Request):
        method = request.method
        model_name = request.match_info.get('model')
        model, validator = get_model_n_validator(model_name)

        if method != 'GET' and issubclass(model, ImmutableModel):
            raise web.HTTPForbidden

        self.model = model
        self.model_instance_data_validator = validator
        self.model_instance_id = request.match_info.get('id')

        super().__init__(request)

    async def get(self,):

        if self.model_instance_id:
            instance = await self.model.filter(pk=self.model_instance_id).first()
            data = await instance.serialize() if instance else {}
        else:
            instances = await self.model.all()
            data = [await instance.serialize() for instance in instances]

        if not data:
            raise web.HTTPNotFound
        return web.json_response(data=data)

    async def post(self):
        try:
            await self.model.create(**self.model_instance_data)
            raise web.HTTPCreated

        except IntegrityError as err:
            raise web.HTTPBadRequest(text=str(err))

    async def patch(self):
        return web.json_response({'hello': 'patch_handler'})

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
