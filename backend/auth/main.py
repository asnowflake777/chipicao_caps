import aiohttp_cors as aiohttp_cors
from aiohttp import web

from settings import HOST, PORT


routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):
    return web.Response(text='Welcome to chipicao caps')


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
