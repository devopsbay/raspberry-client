from aiohttp import web

from nfcclient.router import routes


async def aiohttp_server(app, host: str, port: int):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()


app = web.Application()
for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])