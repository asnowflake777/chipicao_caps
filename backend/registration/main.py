import aiohttp_cors
from aiohttp import web
from http import HTTPStatus

from settings import HOST, PORT
from utils import get_request_data, email_valid, encrypt_password, password_valid

routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):
    msg = 'username password email are required fields'
    data = await request.json()
    username, password, email = get_request_data(data, ('username', 'password', 'email'))
    try:
        if all([username, password, email]):
            assert email_valid(email), 'email is not valid'
            assert password_valid(password), 'password should has 6 length at least and contains just ascii symbols'
            password = encrypt_password(password)
            print(f'{username=}')
            print(f'{password=}')
            print(f'{email=}')
            return web.Response(status=HTTPStatus.CREATED)

    except AssertionError as err:
        msg = str(err)

    return web.Response(text=msg)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(app, host=HOST, port=PORT)
