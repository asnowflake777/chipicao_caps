import argparse

from aiohttp import web
from http import HTTPStatus

from pydantic import ValidationError
from tortoise.exceptions import IntegrityError

from utils import connect_to_db
from models import MODEL_MAPPER, MODEL_DATA_VALIDATOR
from settings import DEFAULT_HOST, DEFAULT_PORT

app = web.Application()
routes = web.RouteTableDef()


@routes.view(r'/{model:\w+}/{id:\d*}')
class UserView(web.View):

    async def get(self):
        model = self.request.match_info.get('model')
        model = MODEL_MAPPER.get(model)
        instance_id = self.request.match_info.get('id')

        if model:
            if instance_id:
                instance = await model.filter(pk=instance_id).first()
                data = await instance.serialize() if instance else {}
            else:
                instances = await model.all()
                data = [await instance.serialize() for instance in instances]
            return web.json_response(data=data)
        else:
            return web.json_response(data={'msg': 'Model not found'}, status=HTTPStatus.NOT_FOUND)

    async def post(self):
        model = self.request.match_info.get('model')
        model = MODEL_MAPPER.get(model)
        validator = MODEL_DATA_VALIDATOR.get(model)

        if model and validator:
            try:

                data = await self.request.json() if self.request.body_exists else {}
                validator.validate(data)
                instance = await model.create(**data)
                instance_data = await instance.serialize()
                return web.json_response(data=instance_data, status=HTTPStatus.CREATED)

            except (ValidationError, IntegrityError) as err:
                return web.json_response({'msg': str(err)}, status=HTTPStatus.BAD_REQUEST)

    async def put(self):
        model = self.request.match_info.get('model')
        return web.json_response({'hello': 'put_handler'})

    async def patch(self):
        model = self.request.match_info.get('model')
        instance_id = self.request.match_info.get('id')
        return web.json_response({'hello': 'patch_handler'})

    async def delete(self):
        model = self.request.match_info.get('model')
        instance_id = self.request.match_info.get('id')
        return web.json_response({'hello': 'delete_handler'})


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
