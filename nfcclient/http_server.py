from aiohttp import web
import aiohttp_cors

from nfcclient.router import routes


async def aiohttp_server(app, host: str, port: int):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()


app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
        # Allow all to read all CORS-enabled resources from
        "http://localhost:3001": aiohttp_cors.ResourceOptions(),
    })

for route in routes:
    #app.router.add_route(route[0], route[1], route[2], name=route[3])
    resource = cors.add(app.router.add_resource(route[1]))
    route = cors.add(resource.add_route(route[0], route[2]))