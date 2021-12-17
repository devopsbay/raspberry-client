from aiohttp import web
import aiohttp_cors

from nfcclient.router import routes


def setup_cors(app):
    resources = [
        'http://localhost:3001',
        'http://localhost:8080'
    ]

    cors = aiohttp_cors.setup(app, defaults={
        resource: aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_methods='*',
            allow_headers='*',
        ) for resource in resources
    })
    for route in app.router.routes():
        cors.add(route)


async def aiohttp_server(app, host: str, port: int):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()


app = web.Application()
for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])

# Configure default CORS settings.
setup_cors(app)
